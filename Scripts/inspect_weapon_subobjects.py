import unreal


ASSETS = [
    "/Game/Variant_Shooter/Blueprints/Pickups/Weapons/BP_ShooterWeapon_Pistol",
    "/Game/Variant_Shooter/Blueprints/Pickups/Weapons/BP_ShooterWeapon_Rifle",
]


def log(message):
    unreal.log("[FPS_SUBOBJECTS] {}".format(message))


subsystem = unreal.get_engine_subsystem(unreal.SubobjectDataSubsystem)
lib = unreal.SubobjectDataBlueprintFunctionLibrary

for asset_path in ASSETS:
    bp = unreal.EditorAssetLibrary.load_asset(asset_path)
    log("ASSET {} -> {}".format(asset_path, bp))
    if not bp:
        continue

    handles = subsystem.k2_gather_subobject_data_for_blueprint(bp)
    log("  handles = {}".format(len(handles)))
    for handle in handles:
        valid = lib.is_handle_valid(handle)
        data = subsystem.k2_find_subobject_data_from_handle(handle) if valid else None
        assoc = lib.get_associated_object(data) if data else None
        parent = lib.get_parent_handle(data) if data else None
        log(
            "  handle valid={} data={} associated={} is_component={} is_scene={} is_root={} parent_valid={}".format(
                valid,
                data,
                assoc,
                lib.is_component(data) if data else None,
                lib.is_scene_component(data) if data else None,
                lib.is_root_component(data) if data else None,
                lib.is_handle_valid(parent) if parent else None,
            )
        )
        target = assoc
        if target:
            for prop_name in ("static_mesh", "skeletal_mesh", "anim_class", "animation_mode"):
                try:
                    value = target.get_editor_property(prop_name)
                    log("    {} = {}".format(prop_name, value))
                except Exception:
                    pass
