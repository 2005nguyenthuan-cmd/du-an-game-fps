import unreal


CLASS_PATH = "/Game/Variant_Shooter/Blueprints/Pickups/Projectiles/BP_ShooterProjectile_Bullet.BP_ShooterProjectile_Bullet_C"
TOKENS = ["projectile", "speed", "velocity", "gravity", "collision", "mesh", "sphere", "bounce", "life"]


def log(message):
    unreal.log("[FPS_SUBOBJECT_INSPECT] {}".format(message))


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


cls = unreal.load_class(None, CLASS_PATH)
log("CLASS -> {}".format(cls))
cdo = unreal.get_default_object(cls)
dump(cdo)

try:
    subs = cdo.get_default_subobjects()
    log("subobject_count = {}".format(len(subs)))
    for sub in subs:
        log("SUBOBJECT {} ({})".format(sub.get_name(), sub.get_class().get_path_name()))
        dump(sub, indent="    ")
except Exception as exc:
    log("get_default_subobjects failed: {}".format(exc))
