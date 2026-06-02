import unreal


BP_PATH = "/Game/Variant_Shooter/Blueprints/Pickups/Projectiles/BP_ShooterProjectile_Bullet"
TOKENS = ["projectile", "speed", "velocity", "gravity", "collision", "mesh", "sphere", "bounce", "life"]


def log(message):
    unreal.log("[FPS_BULLET_SUBOBJECTS] {}".format(message))


def dump_props(obj, indent="  "):
    for name in sorted(set(n for n in dir(obj) if not n.startswith("_"))):
        lower = name.lower()
        if not any(token in lower for token in TOKENS):
            continue
        try:
            value = obj.get_editor_property(name)
            log("{}{} = {}".format(indent, name, value))
        except Exception:
            pass


bp = unreal.EditorAssetLibrary.load_asset(BP_PATH)
subsystem = unreal.get_engine_subsystem(unreal.SubobjectDataSubsystem)
handles = subsystem.k2_gather_subobject_data_for_blueprint(bp)
log("handle_count = {}".format(len(handles)))
for handle in handles:
    try:
        data = subsystem.k2_find_subobject_data_from_handle(handle)
    except Exception as exc:
        log("find failed: {}".format(exc))
        continue
    log("HANDLE data = {}".format(data))
    try:
        obj = unreal.SubobjectDataBlueprintFunctionLibrary.get_object(data)
    except Exception as exc:
        log("  get_object failed: {}".format(exc))
        continue
    log("  OBJECT {} ({})".format(obj.get_name(), obj.get_class().get_path_name()))
    dump_props(obj, indent="    ")
