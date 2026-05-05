import unreal


def log(message):
    unreal.log("[FPS_DEMO_API] " + str(message))


for obj_name, obj in (
    ("EditorLevelLibrary", unreal.EditorLevelLibrary),
    ("EditorActorSubsystem", unreal.get_editor_subsystem(unreal.EditorActorSubsystem)),
):
    names = [name for name in dir(obj) if "actor" in name.lower() or "duplicate" in name.lower() or "spawn" in name.lower()]
    log("{}: {}".format(obj_name, ", ".join(sorted(names))))

