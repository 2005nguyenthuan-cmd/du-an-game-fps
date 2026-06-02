import unreal


ASSET_PATHS = [
    "/Game/Variant_Shooter/Blueprints/Pickups/DT_WeaponList",
    "/Game/Variant_Shooter/Blueprints/Pickups/BP_ShooterPickup",
    "/Game/Variant_Shooter/Blueprints/Pickups/Weapons/BP_ShooterWeapon_Pistol",
    "/Game/Variant_Shooter/Blueprints/Pickups/Weapons/BP_ShooterWeapon_Rifle",
    "/Game/Variant_Shooter/Blueprints/Pickups/Weapons/BP_ShooterWeapon_GrenadeLauncher",
    "/Game/Variant_Shooter/Blueprints/Pickups/Projectiles/BP_ShooterProjectileBase",
    "/Game/Variant_Shooter/Blueprints/Pickups/Projectiles/BP_ShooterProjectile_Bullet",
    "/Game/Variant_Shooter/Blueprints/Pickups/Projectiles/BP_ShooterProjectile_Grenade",
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
    "impact",
    "fx",
]


def log(message):
    unreal.log("[FPS_ASSET_INSPECT] {}".format(message))


def dump_matching_properties(obj, indent="  "):
    for name in sorted(set(n for n in dir(obj) if not n.startswith("_"))):
        lower = name.lower()
        if not any(token in lower for token in TOKENS):
            continue
        try:
            value = obj.get_editor_property(name)
            log("{}{} = {}".format(indent, name, value))
        except Exception:
            pass


for asset_path in ASSET_PATHS:
    asset = unreal.EditorAssetLibrary.load_asset(asset_path)
    log("ASSET {} -> {}".format(asset_path, asset))
    if asset is None:
        continue

    if isinstance(asset, unreal.DataTable):
        row_names = unreal.DataTableFunctionLibrary.get_data_table_row_names(asset)
        log("  rows = {}".format([str(name) for name in row_names]))
        for row_name in row_names:
            try:
                row = unreal.DataTableFunctionLibrary.get_data_table_row_from_name(asset, row_name)
                log("  row {} -> {}".format(row_name, row))
            except Exception as exc:
                log("  row {} unreadable: {}".format(row_name, exc))
        continue

    generated_class = None
    try:
        generated_class = asset.generated_class()
    except Exception:
        try:
            generated_class = unreal.load_class(None, asset_path + "." + asset.get_name() + "_C")
        except Exception:
            generated_class = None

    log("  generated_class = {}".format(generated_class))
    if generated_class:
        cdo = unreal.get_default_object(generated_class)
        dump_matching_properties(cdo)
