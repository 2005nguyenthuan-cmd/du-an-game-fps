import unreal


def log(message):
    unreal.log("[FPS_MH_PARAMS] {}".format(message))


for cls_name in [
    "MetaHumanCharacterAutoRiggingRequestParams",
    "MetaHumanCharacterEditorBuildParameters",
    "MetaHumanRigType",
]:
    cls = getattr(unreal, cls_name, None)
    log("CLASS {} -> {}".format(cls_name, cls))
    if not cls:
        continue
    if isinstance(cls, type):
        try:
            obj = cls()
            log("  instance = {}".format(obj))
            for name in sorted(n for n in dir(obj) if not n.startswith("_")):
                try:
                    value = obj.get_editor_property(name)
                    log("  {} = {}".format(name, value))
                except Exception:
                    pass
        except Exception as exc:
            log("  instance failed: {}".format(exc))
    else:
        for name in dir(cls):
            if name.startswith("_"):
                continue
            log("  member = {}".format(name))


for cls_name in [
    "SubobjectDataSubsystem",
    "SubobjectDataBlueprintFunctionLibrary",
]:
    cls = getattr(unreal, cls_name, None)
    log("CLASS {} -> {}".format(cls_name, cls))
    if not cls:
        continue
    for name in sorted(n for n in dir(cls) if not n.startswith("_")):
        lower = name.lower()
        if any(token in lower for token in ("subobject", "component", "blueprint", "object", "handle")):
            log("  method = {}".format(name))
