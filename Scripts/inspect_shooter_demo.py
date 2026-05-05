import unreal


def log(message):
    unreal.log("[FPS_DEMO_INSPECT] " + str(message))


def property_names(obj):
    names = set()
    for name in dir(obj):
        if not name.startswith("_"):
            names.add(name)
    return sorted(names)


def dump_matching_properties(obj, tokens):
    names = property_names(obj)
    lower_tokens = [token.lower() for token in tokens]
    matches = [name for name in names if any(token in name.lower() for token in lower_tokens)]
    log("  matching properties: {}".format(", ".join(matches) if matches else "(none)"))
    for name in matches:
        try:
            value = obj.get_editor_property(name)
            log("    {} = {}".format(name, value))
        except Exception as exc:
            log("    {} = <unreadable: {}>".format(name, exc))


try:
    MAP_PATH = "/Game/Variant_Shooter/Lvl_ArenaShooter"

    unreal.EditorLoadingAndSavingUtils.load_map(MAP_PATH)
    actors = unreal.EditorLevelLibrary.get_all_level_actors()

    log("Loaded map: {}".format(MAP_PATH))
    log("Actor count: {}".format(len(actors)))

    interesting_tokens = ("Spawner", "Pickup", "Weapon", "NPC", "PlayerStart")
    property_tokens = (
        "spawn",
        "respawn",
        "delay",
        "time",
        "npc",
        "bot",
        "weapon",
        "projectile",
        "damage",
        "ammo",
        "clip",
        "rate",
        "round",
        "score",
    )
    exact_property_names = (
        "Should Spawn Enemies Immediately",
        "Initial Spawn Delay",
        "NPC Class",
        "Spawn Count",
        "Respawn Delay",
        "Spawn Time",
        "Target Class",
        "Weapon Class",
        "Weapon Type",
        "Projectile Offset",
    )

    for actor in actors:
        name = actor.get_actor_label()
        cls = actor.get_class().get_path_name()
        if any(token.lower() in name.lower() or token.lower() in cls.lower() for token in interesting_tokens):
            log("{} | {} | location={}".format(name, cls, actor.get_actor_location()))
            for prop_name in exact_property_names:
                try:
                    value = actor.get_editor_property(prop_name)
                    log("  exact {} = {}".format(prop_name, value))
                except Exception:
                    pass
            dump_matching_properties(actor, property_tokens)

    class_paths = [
        "/Game/Variant_Shooter/Blueprints/AI/BP_ShooterNPCSpawner.BP_ShooterNPCSpawner_C",
        "/Game/Variant_Shooter/Blueprints/AI/BP_ShooterNPC.BP_ShooterNPC_C",
        "/Game/Variant_Shooter/Blueprints/BP_ShooterGameMode.BP_ShooterGameMode_C",
        "/Game/Variant_Shooter/Blueprints/Pickups/BP_ShooterPickup.BP_ShooterPickup_C",
        "/Game/Variant_Shooter/Blueprints/Pickups/Weapons/BP_ShooterWeapon_Pistol.BP_ShooterWeapon_Pistol_C",
        "/Game/Variant_Shooter/Blueprints/Pickups/Weapons/BP_ShooterWeapon_Rifle.BP_ShooterWeapon_Rifle_C",
        "/Game/Variant_Shooter/Blueprints/Pickups/Weapons/BP_ShooterWeapon_GrenadeLauncher.BP_ShooterWeapon_GrenadeLauncher_C",
    ]

    for path in class_paths:
        cls = unreal.load_class(None, path)
        log("Class {} -> {}".format(path, cls))
        if cls:
            cdo = unreal.get_default_object(cls)
            for prop_name in exact_property_names:
                try:
                    value = cdo.get_editor_property(prop_name)
                    log("  exact default {} = {}".format(prop_name, value))
                except Exception:
                    pass
            dump_matching_properties(cdo, property_tokens)

except Exception as exc:
    log("SCRIPT_FAILED: {}".format(exc))
    raise
