"""
Generic parsing tools, for parsing when you know a file name or file type.
"""

import asyncio
import logging
import pathlib
import sys
from typing import Dict, Optional, Union

from .access_security import AccessSecurityConfig
from .common import AnyPath, FileFormat, IocMetadata
from .db import Database
from .dbtemplate import TemplateSubstitution
from .gateway import PVList as GatewayPVList
from .macro import MacroContext, PassthroughMacroContext
from .makefile import Makefile
from .shell import LoadedIoc
from .snl import SequencerProgram
from .streamdevice import StreamProtocol

logger = logging.getLogger(__name__)


ParseResult = Union[
    AccessSecurityConfig,
    Database,
    GatewayPVList,
    LoadedIoc,
    SequencerProgram,
    StreamProtocol,
    TemplateSubstitution,
    Makefile,
]


def parse(
    filename: AnyPath,
    dbd: Optional[str] = None,
    standin_directories: Optional[Dict[str, str]] = None,
    macros: Optional[str] = None,
    disable_macros: bool = False,
    use_gdb: bool = False,
    format: Optional[FileFormat] = None,
    expand: bool = False,
    v3: bool = False,
) -> ParseResult:
    """
    Generically parse either a startup script or a database file.

    Hopefully does the right thing based on file extension.  If not, use
    the ``format`` kwarg to specify it directly.

    Parameters
    ----------
    filename : str or pathlib.Path
        The filename to parse.

    dbd : str or pathlib.Path, optional
        The associated database definition file, if parsing a database or
        substitutions file.

    standin_directories : dict, optional
        Rewrite hard-coded directory prefixes by setting::

            standin_directories = {"/replace_this/": "/with/this"}

    macros : str, optional
        Macro string to use when parsing the file.

    disable_macros : bool, optional
        Disable macro handling, leaving unexpanded macros in the output.

    expand : bool, optional
        Expand a substitutions file.

    v3 : bool, optional
        Use V3 database grammar where applicable.
    """
    standin_directories = standin_directories or {}

    if str(filename) == "-":
        if format is None:
            options = [fmt.name for fmt in list(FileFormat)]
            raise ValueError(
                f"Format must be specified when piping data from standard "
                f"input.  Choose one of: {options}"
            )
        if format == FileFormat.iocsh:
            raise ValueError(
                "IOC shell script parsing not supported through standard input"
            )

        contents = sys.stdin.read()
        filename = pathlib.Path(sys.stdin.name)
    else:
        with open(filename, "rt") as fp:
            contents = fp.read()
        filename = pathlib.Path(filename)

    # The shared macro context - used in different ways below:
    if disable_macros:
        macro_context = PassthroughMacroContext()
    else:
        macro_context = MacroContext(macro_string=macros or "")

    if format is None:
        format = FileFormat.from_filename(filename)

    if format in (FileFormat.database, FileFormat.database_definition):
        if format == FileFormat.database_definition or not dbd:
            return Database.from_string(
                contents,
                filename=filename,
                macro_context=macro_context,
                version=3 if v3 else 4
            )
        return Database.from_string(
            contents,
            filename=filename,
            dbd=Database.from_file(dbd, version=3 if v3 else 4),
            macro_context=macro_context
        )

    if format == FileFormat.iocsh:
        md = IocMetadata.from_filename(
            filename,
            standin_directories=standin_directories,
            macros=dict(macro_context),
        )
        if use_gdb:
            try:
                asyncio.run(md.get_binary_information())
            except KeyboardInterrupt:
                logger.info("Skipping gdb information...")

        return LoadedIoc.from_metadata(md)

    if format == FileFormat.substitution:
        template = TemplateSubstitution.from_string(contents, filename=filename)
        if not expand:
            return template

        database_text = template.expand_files()
        # It's technically possible that this *isn't* a database file; so
        # perhaps a `whatrecord msi` could be implemented in the future.
        return Database.from_string(
            database_text,
            macro_context=macro_context,
            dbd=Database.from_file(dbd) if dbd is not None else None,
            filename=filename,
            version=3 if v3 else 4,
        )

    if format == FileFormat.state_notation:
        return SequencerProgram.from_string(contents, filename=filename)

    if macros:
        contents = macro_context.expand_file(contents)

    if format == FileFormat.gateway_pvlist:
        return GatewayPVList.from_string(contents, filename=filename)

    if format == FileFormat.access_security:
        return AccessSecurityConfig.from_string(contents, filename=filename)

    if format == FileFormat.stream_protocol:
        return StreamProtocol.from_string(contents, filename=filename)

    if format == FileFormat.makefile:
        return Makefile.from_string(contents, filename=filename)

    raise RuntimeError(
        f"Sorry, whatrecord doesn't support the {format!r} format just yet in the "
        f"CLI parsing tool.  Please open an issue."
    )
