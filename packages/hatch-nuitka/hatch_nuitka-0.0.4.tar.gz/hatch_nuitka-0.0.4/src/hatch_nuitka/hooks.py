from hatchling.plugin import hookimpl
from hatch_nuitka.plugin import NuitkaBuildHook

@hookimpl
def hatch_register_build_hook():
    return NuitkaBuildHook