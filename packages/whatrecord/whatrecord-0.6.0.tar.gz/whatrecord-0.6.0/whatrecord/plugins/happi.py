"""
happi whatrecord plugin

Match your happi devices to IOCs and records.
"""
from __future__ import annotations

import argparse
import collections
import fnmatch
import json
import logging
import typing
from dataclasses import dataclass
from typing import Dict, Generator, List, Tuple, Type, TypeVar, Union

import apischema

from ..server.common import PluginResults
from ..util import get_file_sha256
from .util import suppress_output_decorator

try:
    import happi
    import happi.backends
    import happi.backends.json_db
    import ophyd
    from ophyd.ophydobj import OphydObject
    from ophyd.signal import EpicsSignalBase
except ImportError as ex:
    raise ImportError(f"Dependency required for happi plugin unavailable: {ex}")


logger = logging.getLogger(__name__)

# Stash the description for later usage by the CLI interface.
DESCRIPTION = __doc__.strip()
CriteriaDict = Dict[str, Union[float, str]]
T = TypeVar("T")


HappiItem = Dict[str, Union[str, List[str], Dict[str, str]]]  # kinda...

# TODO: this can be improved
SIGNAL_CLASSES = (
    EpicsSignalBase,
    ophyd.EpicsMotor,
    ophyd.EpicsScaler,
)


@dataclass
class HappiPluginResults(PluginResults):
    # Could potentially further specify metadata_by_key or metadata
    ...


@dataclass
class HappiRecordInfo:
    name: str
    kind: str
    signal: str


def get_all_devices(
    client: happi.Client = None,
) -> Generator[ophyd.Device, None, None]:
    """
    Get all devices from a given happi client.

    Parameters
    ----------
    client : happi.Client, optional
        The happi client to use.  Defaults to using one from the environment
        configuration.

    Yields
    ------
    ophyd.Device
    """
    if client is None:
        client = happi.Client.from_config()

    if hasattr(client.backend, "_load_or_initialize"):
        # HACK: TODO: avoid re-re-re-reading the JSON database; happi needs
        # some work.
        loaded_database = client.backend._load_or_initialize()
        client.backend._load_or_initialize = lambda: loaded_database

    for dev in client:
        try:
            obj = client[dev].get()
        except Exception:
            logger.exception("Failed to instantiate device: %s", dev)
        else:
            yield obj


def get_devices_by_criteria(
    search_criteria: CriteriaDict,
    *,
    client: happi.Client = None,
    regex: bool = True,
) -> Generator[ophyd.Device, None, None]:
    """
    Get all devices from a given happi client.

    Parameters
    ----------
    search_criteria : dict
        Dictionary of ``{'happi_key': 'search_value'}``.

    client : happi.Client, optional
        The happi client to use.  Defaults to using one from the environment
        configuration.

    Yields
    ------
    ophyd.Device
    """
    if client is None:
        client = happi.Client.from_config()

    search_method = client.search_regex if regex else client.search
    for item in search_method(**search_criteria):
        try:
            obj = item.get()
        except Exception:
            logger.exception("Failed to instantiate device: %s", obj)
        else:
            yield obj


def get_components_matching(
    obj: ophyd.Device,
    predicate: callable,
) -> Generator[OphydObject, None, None]:
    """
    Find signals of a specific type from a given ophyd Device.

    Parameters
    ----------
    obj : ophyd.Device
        The ophyd Device.

    predicate : callable
        Callable that should return True on a match.

    Yields
    ------
    obj : OphydObject
    """
    for name, dev in obj.walk_subdevices(include_lazy=True):
        try:
            included = predicate(dev)
        except Exception:
            logger.exception("Failed to check predicate against %s %s", name, dev)
        else:
            if included:
                yield dev

    for walk in obj.walk_signals(include_lazy=True):
        try:
            included = predicate(walk.item)
        except Exception:
            logger.exception("Failed to check predicate against %s", walk)
        else:
            if included:
                yield walk.item


def patch_and_use_dummy_shim():
    """
    Hack ophyd and its dummy shim.  We don't want _any_ control-layer
    connections being made while we're looking for signals.

    Warning
    -------
    Under no circumstances should this be used in a production environment
    where you intend to actually _use_ ophyd for its intended purpose.
    """
    ophyd.Device.lazy_wait_for_connection = False

    def _no_op(*args, **kwargs):
        ...

    class _PVStandIn:
        _reference_count = 0

        def __init__(self, pvname, *args, **kwargs):
            self.pvname = pvname
            self.connected = True

        add_callback = _no_op
        remove_callback = _no_op
        clear_callbacks = _no_op
        get = _no_op
        put = _no_op
        get_with_metadata = _no_op
        wait_for_connection = _no_op

    def get_pv(pvname, *args, **kwargs):
        return _PVStandIn(pvname)

    from ophyd import _dummy_shim

    _dummy_shim.get_pv = get_pv
    _dummy_shim.release_pvs = _no_op
    ophyd.set_cl("dummy")


def find_signals(
    criteria: CriteriaDict,
    signal_class: Type[T],
) -> Generator[Tuple[OphydObject, T], None, None]:
    """
    Find all signal metadata that match the given criteria.

    Yields
    ------
    root : OphydObject
        The root OphydObject - may be the same as signal.  This is guaranteed
        to have happi metadata on it as the ``md`` attribute.

    sig : signal_class
        Signals of type `signal_class`.
    """

    patch_and_use_dummy_shim()

    def is_of_class(obj):
        return isinstance(obj, signal_class)

    if not criteria:
        devices = get_all_devices()
    else:
        devices = get_devices_by_criteria(criteria)

    for dev in devices:
        if not hasattr(dev, "md"):
            # This should be a guarantee, but check just in case.
            continue

        for sig in get_components_matching(dev, predicate=is_of_class):
            yield dev, sig
        # Top-level devices are OK too
        if isinstance(dev, signal_class):
            yield dev, dev


def find_signal_metadata_pairs(
    criteria: CriteriaDict,
) -> Generator[Tuple[OphydObject, str, EpicsSignalBase], None, None]:
    """
    Find all signal metadata that match the given criteria.

    Yields
    ------
    root : OphydObject
        The root OphydObject - may be the same as signal.  This is guaranteed
        to have happi metadata on it as the ``md`` attribute.

    pvname : str
        The PV name.

    signal : EpicsSignal, EpicsSignalRO, ...
        The signal instance, one of ``SIGNAL_CLASSES``.
    """

    attributes = [
        "pvname",
        "setpoint_pvname",
    ]

    for root, sig in find_signals(criteria, signal_class=SIGNAL_CLASSES):
        found_pvs = set()
        for attr in attributes:
            pvname = getattr(sig, attr, None)
            if pvname is not None and isinstance(pvname, str):
                found_pvs.add(pvname)

        if found_pvs:
            for pvname in sorted(found_pvs):
                yield root, pvname, sig
        else:
            # Then it's the prefix - possibly
            pvname = getattr(sig, "prefix", None)
            if pvname is not None:
                yield root, pvname, sig


def _parse_criteria(criteria_string: str) -> CriteriaDict:
    """
    Parse search criteria into a dictionary of ``{key: value}``.

    Converts floating point values to float.
    """
    search_args = {}
    for user_arg in criteria_string:
        if "=" in user_arg:
            criteria, value = user_arg.split("=", 1)
        else:
            criteria = "name"
            value = user_arg

        if criteria in search_args:
            logger.warning(
                "Received duplicate search criteria %s=%r (was %r)",
                criteria,
                value,
                search_args[criteria],
            )
            continue

        try:
            value = float(value)
        except ValueError:
            value = fnmatch.translate(value)

        search_args[criteria] = value

    return search_args


def _get_argparser(parser: typing.Optional[argparse.ArgumentParser] = None):
    if parser is None:
        parser = argparse.ArgumentParser(description=DESCRIPTION)

    parser.add_argument(
        "search_criteria", nargs="*", help="Search criteria: field=value"
    )
    parser.add_argument(
        "-p", "--pretty", action="store_true", help="Pretty JSON output"
    )
    return parser


def get_all_happi_items(client: happi.Client) -> Generator[happi.SearchResult, None, None]:
    """
    Get all happi search results from the given client.

    Parameters
    ----------
    client : happi.Client
        The happi client instance.

    Yields
    ------
    SearchResult
        The happi item wrapped in a SearchResult.
    """
    for name in client:
        try:
            yield client[name]
        except Exception:
            logger.debug("Failed to get happi item: %s", name, exc_info=True)


@suppress_output_decorator
def main(search_criteria: str, pretty: bool = False):
    client = happi.Client.from_config()

    files_to_monitor = {}

    if isinstance(client.backend, happi.backends.json_db.JSONBackend):
        files_to_monitor[client.backend.path] = get_file_sha256(
            client.backend.path
        )

    results = HappiPluginResults(
        files_to_monitor=files_to_monitor,
        record_to_metadata_keys=collections.defaultdict(list),
        metadata_by_key={
            result.item["name"]: dict(result.item)
            for result in get_all_happi_items(client)
        },
        execution_info={},
    )

    criteria = _parse_criteria(search_criteria)
    for root, record, sig in find_signal_metadata_pairs(criteria):
        if "." in record:
            record, *_ = record.split(".")

        happi_md = root.md

        if happi_md.name not in results.record_to_metadata_keys[record]:
            results.record_to_metadata_keys[record].append(happi_md.name)
            try:
                md = results.metadata_by_key[happi_md.name]
            except KeyError:
                # Mismatched _id and name
                continue

            if "_whatrecord" not in md:
                md["_whatrecord"] = {"records": []}
            if sig.root is not root:
                # TODO: this would not work for nested GroupDevice components.
                dotted_name = ".".join((sig.root.attr_name, sig.dotted_name))
            else:
                dotted_name = sig.dotted_name
            md["_whatrecord"]["records"].append(
                HappiRecordInfo(
                    name=record,
                    kind=str(sig.kind),
                    signal=dotted_name,
                )
            )

    return results


def _cli_main():
    parser = _get_argparser()
    args = parser.parse_args()
    results = main(**vars(args))
    json_results = apischema.serialize(results)
    dump_args = {"indent": 4} if args.pretty else {}
    print(json.dumps(json_results, sort_keys=True, **dump_args))


if __name__ == "__main__":
    _cli_main()
