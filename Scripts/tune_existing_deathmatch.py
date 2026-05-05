import unreal


MAP_PATH = "/Game/Variant_Shooter/Lvl_ArenaShooter"
SPAWNER_CLASS_PATH = "/Game/Variant_Shooter/Blueprints/AI/BP_ShooterNPCSpawner.BP_ShooterNPCSpawner_C"
PICKUP_CLASS_PATH = "/Game/Variant_Shooter/Blueprints/Pickups/BP_ShooterPickup.BP_ShooterPickup_C"


def log(message):
    unreal.log("[FPS_DEMO_TUNE] " + str(message))


def row_name_for_pickup(actor):
    try:
        row_handle = actor.get_editor_property("Weapon Type")
        return str(row_handle.get_editor_property("row_name"))
    except Exception:
        return ""


def configure_spawner(actor, index):
    actor.set_editor_property("Should Spawn Enemies Immediately", True)
    actor.set_editor_property("Initial Spawn Delay", 1.0 + index * 0.5)
    actor.set_editor_property("Spawn Count", 100)
    actor.set_editor_property("Respawn Delay", 3.0)
    if not actor.get_actor_label().startswith("DM_BotSpawner"):
        actor.set_actor_label("DM_BotSpawner_{}".format(index + 1))


unreal.EditorLoadingAndSavingUtils.load_map(MAP_PATH)
spawner_class = unreal.load_class(None, SPAWNER_CLASS_PATH)
pickup_class = unreal.load_class(None, PICKUP_CLASS_PATH)

spawner_count = 0
pickup_counts = {}
for actor in unreal.EditorLevelLibrary.get_all_level_actors():
    actor_class_path = actor.get_class().get_path_name()
    if spawner_class and actor_class_path == spawner_class.get_path_name():
        configure_spawner(actor, spawner_count)
        spawner_count += 1
        log("Configured {}: Spawn Count=100, Respawn Delay=3.0".format(actor.get_actor_label()))
    if pickup_class and actor_class_path == pickup_class.get_path_name():
        row_name = row_name_for_pickup(actor)
        pickup_counts[row_name] = pickup_counts.get(row_name, 0) + 1

log("Spawner count: {}".format(spawner_count))
for row_name, count in sorted(pickup_counts.items()):
    log("Pickup {} count: {}".format(row_name if row_name else "(unset)", count))

unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
log("Existing deathmatch tuning saved.")

