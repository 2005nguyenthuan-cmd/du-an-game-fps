import unreal


MAP_PATH = "/Game/Variant_Shooter/Lvl_ArenaShooter"
PICKUP_CLASS_PATH = "/Game/Variant_Shooter/Blueprints/Pickups/BP_ShooterPickup.BP_ShooterPickup_C"
SPAWNER_CLASS_PATH = "/Game/Variant_Shooter/Blueprints/AI/BP_ShooterNPCSpawner.BP_ShooterNPCSpawner_C"
WEAPON_TABLE_PATH = "/Game/Variant_Shooter/Blueprints/Pickups/DT_WeaponList"


def log(message):
    unreal.log("[FPS_DEMO_SETUP] " + str(message))


def load_required_class(path):
    cls = unreal.load_class(None, path)
    if not cls:
        raise RuntimeError("Could not load class: {}".format(path))
    return cls


def get_actor_by_label(label):
    for actor in unreal.EditorLevelLibrary.get_all_level_actors():
        if actor.get_actor_label() == label:
            return actor
    return None


def spawn_or_move(label, cls, location, rotation=None):
    actor = get_actor_by_label(label)
    if rotation is None:
        rotation = unreal.Rotator(0.0, 0.0, 0.0)

    if actor is None:
        actor = unreal.EditorLevelLibrary.spawn_actor_from_class(cls, location, rotation)
        actor.set_actor_label(label)
        log("Spawned {}".format(label))
    else:
        actor.set_actor_location(location, False, False)
        actor.set_actor_rotation(rotation, False)
        log("Updated {}".format(label))

    return actor


def make_weapon_row(row_name):
    handle = unreal.DataTableRowHandle()
    handle.set_editor_property("data_table", WEAPON_TABLE)
    handle.set_editor_property("row_name", unreal.Name(row_name))
    return handle


def configure_pickup(actor, row_name):
    actor.set_editor_property("Weapon Type", make_weapon_row(row_name))
    actor.set_editor_property("Spawn Time", 2.0)


def configure_spawner(actor, spawn_count=100, respawn_delay=3.0, initial_delay=1.0):
    actor.set_editor_property("Should Spawn Enemies Immediately", True)
    actor.set_editor_property("Initial Spawn Delay", initial_delay)
    actor.set_editor_property("Spawn Count", spawn_count)
    actor.set_editor_property("Respawn Delay", respawn_delay)


unreal.EditorLoadingAndSavingUtils.load_map(MAP_PATH)

PICKUP_CLASS = load_required_class(PICKUP_CLASS_PATH)
SPAWNER_CLASS = load_required_class(SPAWNER_CLASS_PATH)
WEAPON_TABLE = unreal.EditorAssetLibrary.load_asset(WEAPON_TABLE_PATH)
if not WEAPON_TABLE:
    raise RuntimeError("Could not load weapon table: {}".format(WEAPON_TABLE_PATH))

pickup_specs = [
    ("DM_Pickup_Pistol_North", "Pistol", unreal.Vector(-315.0, 1235.0, 92.0)),
    ("DM_Pickup_Pistol_West", "Pistol", unreal.Vector(-1185.0, -260.0, 92.0)),
    ("DM_Pickup_Rifle_CenterLow", "Rifle", unreal.Vector(150.0, -690.0, 92.0)),
    ("DM_Pickup_Rifle_East", "Rifle", unreal.Vector(1180.0, 260.0, 92.0)),
    ("DM_Pickup_GrenadeLauncher_CenterHigh", "GrenadeLauncher", unreal.Vector(0.0, 0.0, 495.0)),
    ("DM_Pickup_GrenadeLauncher_South", "GrenadeLauncher", unreal.Vector(700.0, -1325.0, 92.0)),
]

for label, row_name, location in pickup_specs:
    pickup = spawn_or_move(label, PICKUP_CLASS, location)
    configure_pickup(pickup, row_name)
    log("{} uses {}".format(label, row_name))

existing_spawners = []
for actor in unreal.EditorLevelLibrary.get_all_level_actors():
    if actor.get_class().get_path_name() == SPAWNER_CLASS.get_path_name():
        existing_spawners.append(actor)

for index, spawner in enumerate(existing_spawners):
    configure_spawner(spawner, spawn_count=100, respawn_delay=3.0, initial_delay=1.0 + index * 0.5)
    if not spawner.get_actor_label().startswith("DM_BotSpawner"):
        spawner.set_actor_label("DM_BotSpawner_Existing_{}".format(index + 1))
    log("Configured {}".format(spawner.get_actor_label()))

spawner_specs = [
    ("DM_BotSpawner_North", unreal.Vector(-535.0, 1320.0, 92.0), unreal.Rotator(0.0, -90.0, 0.0)),
    ("DM_BotSpawner_South", unreal.Vector(1095.0, -1340.0, 92.0), unreal.Rotator(0.0, 135.0, 0.0)),
    ("DM_BotSpawner_West", unreal.Vector(-1190.0, -620.0, 92.0), unreal.Rotator(0.0, 15.0, 0.0)),
]

for index, (label, location, rotation) in enumerate(spawner_specs):
    spawner = spawn_or_move(label, SPAWNER_CLASS, location, rotation)
    configure_spawner(spawner, spawn_count=100, respawn_delay=3.0, initial_delay=1.5 + index * 0.5)

unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
log("Deathmatch demo setup complete.")

