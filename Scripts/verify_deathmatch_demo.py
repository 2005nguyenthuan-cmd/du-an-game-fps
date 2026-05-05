import unreal


MAP_PATH = "/Game/Variant_Shooter/Lvl_ArenaShooter"
SPAWNER_CLASS_PATH = "/Game/Variant_Shooter/Blueprints/AI/BP_ShooterNPCSpawner.BP_ShooterNPCSpawner_C"
PICKUP_CLASS_PATH = "/Game/Variant_Shooter/Blueprints/Pickups/BP_ShooterPickup.BP_ShooterPickup_C"


def log(message):
    unreal.log("[FPS_DEMO_VERIFY] " + str(message))


def row_name_for_pickup(actor):
    row_handle = actor.get_editor_property("Weapon Type")
    return str(row_handle.get_editor_property("row_name"))


unreal.EditorLoadingAndSavingUtils.load_map(MAP_PATH)
spawner_class = unreal.load_class(None, SPAWNER_CLASS_PATH)
pickup_class = unreal.load_class(None, PICKUP_CLASS_PATH)

pickup_counts = {}
spawner_summaries = []
dm_labels = []

for actor in unreal.EditorLevelLibrary.get_all_level_actors():
    class_path = actor.get_class().get_path_name()
    label = actor.get_actor_label()
    if label.startswith("DM_"):
        dm_labels.append(label)
    if pickup_class and class_path == pickup_class.get_path_name():
        row_name = row_name_for_pickup(actor)
        pickup_counts[row_name] = pickup_counts.get(row_name, 0) + 1
    if spawner_class and class_path == spawner_class.get_path_name():
        spawner_summaries.append(
            "{} count={} initial_delay={} respawn_delay={}".format(
                label,
                actor.get_editor_property("Spawn Count"),
                actor.get_editor_property("Initial Spawn Delay"),
                actor.get_editor_property("Respawn Delay"),
            )
        )

log("DM labels: {}".format(", ".join(sorted(dm_labels))))
for row_name, count in sorted(pickup_counts.items()):
    log("Pickup {} count: {}".format(row_name, count))
log("Spawner count: {}".format(len(spawner_summaries)))
for summary in sorted(spawner_summaries):
    log(summary)

