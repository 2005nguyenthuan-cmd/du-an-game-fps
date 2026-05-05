import unreal


def log(message):
    unreal.log("[FPS_DEMO_SAVE_API] " + str(message))


for obj_name, obj in (
    ("EditorLevelLibrary", unreal.EditorLevelLibrary),
    ("EditorLoadingAndSavingUtils", unreal.EditorLoadingAndSavingUtils),
):
    names = [name for name in dir(obj) if "save" in name.lower() or "dirty" in name.lower()]
    log("{}: {}".format(obj_name, ", ".join(sorted(names))))
    for name in sorted(names):
        func = getattr(obj, name)
        log("{} doc: {}".format(name, getattr(func, "__doc__", "(no doc)")))

