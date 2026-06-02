import unreal


CLASSES = [
    "/Game/Variant_Shooter/Blueprints/BP_ShooterCharacter.BP_ShooterCharacter_C",
    "/Game/Variant_Shooter/Blueprints/AI/BP_ShooterNPC.BP_ShooterNPC_C",
    "/Game/Variant_Shooter/Blueprints/Pickups/BP_ShooterWeapon.BP_ShooterWeapon_C",
    "/Game/Variant_Shooter/Blueprints/Pickups/Weapons/BP_ShooterWeapon_Pistol.BP_ShooterWeapon_Pistol_C",
    "/Game/Variant_Shooter/Blueprints/Pickups/Weapons/BP_ShooterWeapon_Rifle.BP_ShooterWeapon_Rifle_C",
    "/Game/Variant_Shooter/Blueprints/Pickups/Weapons/BP_ShooterWeapon_GrenadeLauncher.BP_ShooterWeapon_GrenadeLauncher_C",
    "/Game/Variant_Shooter/Blueprints/Pickups/Projectiles/BP_ShooterProjectile.BP_ShooterProjectile_C",
]

TOKENS = [
    "weapon",
    "projectile",
    "damage",
    "range",
    "speed",
    "spread",
    "fire",
    "shot",
    "ammo",
    "sound",
    "audio",
    "mesh",
    "skeletal",
    "static",
]


def log(message):
    unreal.log("[FPS_WEAPON_INSPECT] {}".format(message))


def matching_properties(obj):
    matches = []
    for name in dir(obj):
        if name.startswith("_"):
            continue
        lower = name.lower()
        if any(token in lower for token in TOKENS):
            matches.append(name)
    return sorted(set(matches))


def dump_properties(obj, indent=""):
    for name in matching_properties(obj):
        try:
            value = obj.get_editor_property(name)
            log("{}{} = {}".format(indent, name, value))
        except Exception as exc:
            log("{}{} = <unreadable {}>".format(indent, name, exc))


def dump_components(cdo):
    try:
        components = cdo.get_components_by_class(unreal.ActorComponent)
    except Exception as exc:
        log("  get_components_by_class failed: {}".format(exc))
        return

    for comp in components:
        try:
            comp_name = comp.get_name()
        except Exception:
            comp_name = "<unnamed>"
        log("  component: {} ({})".format(comp_name, comp.get_class().get_path_name()))
        dump_properties(comp, indent="    ")


for class_path in CLASSES:
    cls = unreal.load_class(None, class_path)
    log("CLASS {} -> {}".format(class_path, cls))
    if not cls:
        continue
    cdo = unreal.get_default_object(cls)
    dump_properties(cdo, indent="  ")
    dump_components(cdo)
