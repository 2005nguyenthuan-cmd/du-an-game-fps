import unreal


BP_PATH = "/Game/Variant_Shooter/Blueprints/Pickups/Projectiles/BP_ShooterProjectile_Bullet"


def log(message):
    unreal.log("[FPS_CS_BULLET] {}".format(message))


def save_dirty():
    unreal.EditorAssetLibrary.save_asset(BP_PATH, only_if_is_dirty=False)
    unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)


bp = unreal.EditorAssetLibrary.load_asset(BP_PATH)
if bp is None:
    raise RuntimeError("Could not load {}".format(BP_PATH))

subsystem = unreal.get_engine_subsystem(unreal.SubobjectDataSubsystem)
handles = subsystem.k2_gather_subobject_data_for_blueprint(bp)
log("handles = {}".format(len(handles)))

for handle in handles:
    data = subsystem.k2_find_subobject_data_from_handle(handle)
    obj = unreal.SubobjectDataBlueprintFunctionLibrary.get_object(data)
    class_name = obj.get_class().get_name()
    log("editing {} ({})".format(obj.get_name(), class_name))

    if class_name == "ProjectileMovementComponent":
        obj.set_editor_property("initial_speed", 60000.0)
        obj.set_editor_property("max_speed", 60000.0)
        obj.set_editor_property("projectile_gravity_scale", 0.0)
        obj.set_editor_property("should_bounce", False)
        obj.set_editor_property("bounce_velocity_stop_simulating_threshold", 0.0)
        obj.set_editor_property("rotation_follows_velocity", True)
        obj.set_editor_property("velocity", unreal.Vector(60000.0, 0.0, 0.0))
        log("  projectile movement tuned")

    elif class_name == "SphereComponent":
        obj.set_editor_property("sphere_radius", 2.0)
        log("  sphere radius set to 2.0")

    elif class_name == "StaticMeshComponent":
        try:
            obj.set_editor_property("hidden_in_game", True)
        except Exception:
            pass
        try:
            obj.set_editor_property("visible", False)
        except Exception:
            pass
        try:
            obj.set_editor_property("cast_shadow", False)
        except Exception:
            pass
        log("  projectile mesh hidden")

cdo = unreal.get_default_object(unreal.load_class(None, BP_PATH + ".BP_ShooterProjectile_Bullet_C"))
cdo.set_editor_property("initial_life_span", 0.35)
log("life span set to 0.35s")

bp.modify()
save_dirty()
log("Counter-Strike-like projectile tuning saved.")
