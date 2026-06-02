import unreal


CLASS_PATHS = [
    "/Game/Variant_Shooter/Blueprints/Pickups/Projectiles/BP_ShooterProjectileBase.BP_ShooterProjectileBase_C",
    "/Game/Variant_Shooter/Blueprints/Pickups/Projectiles/BP_ShooterProjectile_Bullet.BP_ShooterProjectile_Bullet_C",
    "/Game/Variant_Shooter/Blueprints/Pickups/Projectiles/BP_ShooterProjectile_Grenade.BP_ShooterProjectile_Grenade_C",
]

TOKENS = [
    "projectile",
    "velocity",
    "speed",
    "gravity",
    "damage",
    "collision",
    "sphere",
    "mesh",
    "life",
    "homing",
    "bounce",
]


def log(message):
    unreal.log("[FPS_PROJECTILE_INSPECT] {}".format(message))


def dump(obj, indent="  "):
    for name in sorted(set(n for n in dir(obj) if not n.startswith("_"))):
        lower = name.lower()
        if not any(token in lower for token in TOKENS):
            continue
        try:
            value = obj.get_editor_property(name)
            log("{}{} = {}".format(indent, name, value))
        except Exception:
            pass


for class_path in CLASS_PATHS:
    cls = unreal.load_class(None, class_path)
    log("CLASS {} -> {}".format(class_path, cls))
    if not cls:
        continue
    cdo = unreal.get_default_object(cls)
    dump(cdo)
    try:
        components = cdo.get_components_by_class(unreal.ActorComponent)
    except Exception as exc:
        log("  components failed: {}".format(exc))
        continue
    for comp in components:
        log("  COMPONENT {} ({})".format(comp.get_name(), comp.get_class().get_path_name()))
        dump(comp, indent="    ")
