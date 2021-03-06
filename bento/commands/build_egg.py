import os
import warnings

from bento.private.bytecode import \
        bcompile, PyCompileError
from bento.core.utils import \
        pprint, ensure_dir
from bento.core import \
        PackageMetadata
from bento.installed_package_description import \
        InstalledPkgDescription, iter_files
from bento._config \
    import \
        IPKG_PATH

from bento.commands.errors \
    import \
        UsageException
from bento.commands.core import \
        Command
from bento.commands.egg_utils import \
        EggInfo, egg_filename

import bento.compat.api as compat

class BuildEggCommand(Command):
    long_descr = """\
Purpose: build egg
Usage:   bentomaker build_egg [OPTIONS]"""
    short_descr = "build egg."

    def run(self, ctx):
        argv = ctx.get_command_arguments()
        p = ctx.options_context.parser
        o, a = p.parse_args(argv)
        if o.help:
            p.print_help()
            return

        n = ctx.build_node.make_node(IPKG_PATH)
        ipkg = InstalledPkgDescription.from_file(n.abspath())
        build_egg(ipkg, ctx, ctx.build_node.abspath())

def build_egg(ipkg, ctx, source_root, path=None):
    meta = PackageMetadata.from_ipkg(ipkg)
    egg_info = EggInfo.from_ipkg(ipkg)

    # FIXME: fix egg name
    if path is None:
        egg = egg_filename(os.path.join("dist", meta.fullname))
    else:
        egg = egg_filename(os.path.join(path, meta.fullname))
    ensure_dir(egg)

    egg_info = EggInfo.from_ipkg(ipkg)

    zid = compat.ZipFile(egg, "w", compat.ZIP_DEFLATED)
    try:
        ipkg.update_paths({"prefix": ".", "eprefix": ".", "sitedir": "."})
        for filename, cnt in egg_info.iter_meta(ctx.build_node):
            zid.writestr(os.path.join("EGG-INFO", filename), cnt)

        file_sections = ipkg.resolve_paths(source_root)
        for kind, source, target in iter_files(file_sections):
            if not kind in ["executables"]:
                zid.write(source, target)

        pprint("PINK", "Byte-compiling ...")
        for kind, source, target in iter_files(file_sections):
            if kind in ["pythonfiles"]:
                try:
                    bytecode = bcompile(source)
                except PyCompileError, e:
                    warnings.warn("Error byte-compiling %r" % source)
                else:
                    zid.writestr("%sc" % target, bcompile(source))
    finally:
        zid.close()

    return
