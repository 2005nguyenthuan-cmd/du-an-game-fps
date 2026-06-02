import unreal


def log(message):
    unreal.log("[FPS_SUBOBJECT_API] {}".format(message))


try:
    subsystem = unreal.get_engine_subsystem(unreal.SubobjectDataSubsystem)
    log("subsystem = {}".format(subsystem))
    methods = [name for name in dir(subsystem) if not name.startswith("_")]
    log("methods = {}".format(", ".join(sorted(methods))))
except Exception as exc:
    log("failed = {}".format(exc))
