import unreal


MAP_PATH = "/Game/Variant_Shooter/Lvl_ArenaShooter"
SPAWNER_CLASS_PATH = "/Game/Variant_Shooter/Blueprints/AI/BP_ShooterNPCSpawner.BP_ShooterNPCSpawner_C"
PICKUP_CLASS_PATH = "/Game/Variant_Shooter/Blueprints/Pickups/BP_ShooterPickup.BP_ShooterPickup_C"


def log(message):
    unreal.log("[FPS_DEMO_DUP] " + str(message))


def mark_actor_dirty(actor):
    try:
        actor.modify()
    except Exception as exc:
        log("modify failed for {}: {}".format(actor.get_actor_label(), exc))
    try:
        actor.mark_package_dirty()
    except Exception as exc:
        log("mark_package_dirty failed for {}: {}".format(actor.get_actor_label(), exc))


def save_everything():
    dirty_maps = unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()
    dirty_content = unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()
    log("Dirty map packages before save: {}".format(len(dirty_maps)))
    log("Dirty content packages before save: {}".format(len(dirty_content)))
    unreal.EditorLoadingAndSavingUtils.save_current_level()
    unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
    packages = list(dirty_maps) + list(dirty_content)
    if packages:
        unreal.EditorLoadingAndSavingUtils.save_packages(packages, False)


def all_actors():
    return unreal.EditorLevelLibrary.get_all_level_actors()


def actor_by_label(label):
    for actor in all_actors():
        if actor.get_actor_label() == label:
            return actor
    return None


def row_name_for_pickup(actor):
    row_handle = actor.get_editor_property("Weapon Type")
    return str(row_handle.get_editor_property("row_name"))


def configure_spawner(actor, spawn_count=100, respawn_delay=3.0, initial_delay=1.0):
    mark_actor_dirty(actor)
    actor.set_editor_property("Should Spawn Enemies Immediately", True)
    actor.set_editor_property("Initial Spawn Delay", initial_delay)
    actor.set_editor_property("Spawn Count", spawn_count)
    actor.set_editor_property("Respawn Delay", respawn_delay)
    mark_actor_dirty(actor)


def duplicate_or_update(label, template, location, rotation=None):
    actor = actor_by_label(label)
    if actor is None:
        log("Duplicating {} into {}".format(template.get_actor_label(), label))
        actor = ACTOR_SUBSYSTEM.duplicate_actor(template, None, unreal.Vector(0.0, 0.0, 0.0))
        if actor is None:
            raise RuntimeError("Failed to duplicate {}".format(template.get_actor_label()))
        actor.set_actor_label(label)
    else:
        log("Updating {}".format(label))

    mark_actor_dirty(actor)
    actor.set_actor_location(location, False, False)
    if rotation is not None:
        actor.set_actor_rotation(rotation, False)
    mark_actor_dirty(actor)
    return actor


unreal.EditorLoadingAndSavingUtils.load_map(MAP_PATH)
ACTOR_SUBSYSTEM = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
spawner_class = unreal.load_class(None, SPAWNER_CLASS_PATH)
pickup_class = unreal.load_class(None, PICKUP_CLASS_PATH)

pickup_templates = {}
spawner_template = None
existing_spawners = []

for actor in all_actors():
    class_path = actor.get_class().get_path_name()
    if pickup_class and class_path == pickup_class.get_path_name():
        row_name = row_name_for_pickup(actor)
        pickup_templates.setdefault(row_name, actor)
    if spawner_class and class_path == spawner_class.get_path_name() and spawner_template is None:
        spawner_template = actor
    if spawner_class and class_path == spawner_class.get_path_name():
        existing_spawners.append(actor)

log("Pickup templates: {}".format(", ".join(sorted(pickup_templates.keys()))))
if spawner_template:
    log("Spawner template: {}".format(spawner_template.get_actor_label()))

for index, spawner in enumerate(existing_spawners):
    mark_actor_dirty(spawner)
    if not spawner.get_actor_label().startswith("DM_BotSpawner"):
        spawner.set_actor_label("DM_BotSpawner_Existing_{}".format(index + 1))
    configure_spawner(spawner, initial_delay=1.0 + index * 0.5)
    log("{} tuned with respawn delay 3.0".format(spawner.get_actor_label()))

pickup_specs = [
    ("DM_Pickup_Pistol_North", "Pistol", unreal.Vector(-315.0, 1235.0, 92.0)),
    ("DM_Pickup_Pistol_West", "Pistol", unreal.Vector(-1185.0, -260.0, 92.0)),
    ("DM_Pickup_Rifle_CenterLow", "Rifle", unreal.Vector(150.0, -690.0, 92.0)),
    ("DM_Pickup_Rifle_East", "Rifle", unreal.Vector(1180.0, 260.0, 92.0)),
    ("DM_Pickup_GrenadeLauncher_CenterHigh", "GrenadeLauncher", unreal.Vector(0.0, 0.0, 495.0)),
    ("DM_Pickup_GrenadeLauncher_South", "GrenadeLauncher", unreal.Vector(700.0, -1325.0, 92.0)),
]

for label, row_name, location in pickup_specs:
    template = pickup_templates.get(row_name)
    if template is None:
        log("No template for weapon row {}; skipped {}".format(row_name, label))
        continue
    pickup = duplicate_or_update(label, template, location)
    mark_actor_dirty(pickup)
    pickup.set_editor_property("Spawn Time", 2.0)
    mark_actor_dirty(pickup)
    log("{} ready as {}".format(label, row_name))

if spawner_template:
    spawner_specs = [
        ("DM_BotSpawner_North", unreal.Vector(-535.0, 1320.0, 92.0), unreal.Rotator(0.0, -90.0, 0.0)),
        ("DM_BotSpawner_South", unreal.Vector(1095.0, -1340.0, 92.0), unreal.Rotator(0.0, 135.0, 0.0)),
        ("DM_BotSpawner_West", unreal.Vector(-1190.0, -620.0, 92.0), unreal.Rotator(0.0, 15.0, 0.0)),
    ]

    for index, (label, location, rotation) in enumerate(spawner_specs):
        spawner = duplicate_or_update(label, spawner_template, location, rotation)
        configure_spawner(spawner, initial_delay=1.5 + index * 0.5)
        log("{} ready with respawn delay 3.0".format(label))

save_everything()
log("Duplicated deathmatch actors saved.")
