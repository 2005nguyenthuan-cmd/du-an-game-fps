import unreal


def log(message):
    unreal.log("[FPS_DEMO_DUP_API] " + str(message))


subsystem = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
for name in ("duplicate_actor", "duplicate_actors", "spawn_actor_from_class"):
    func = getattr(subsystem, name)
    log("{} doc: {}".format(name, getattr(func, "__doc__", "(no doc)")))

