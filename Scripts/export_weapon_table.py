import unreal


def log(message):
    unreal.log("[FPS_DT_EXPORT] {}".format(message))


asset = unreal.EditorAssetLibrary.load_asset("/Game/Variant_Shooter/Blueprints/Pickups/DT_WeaponList")
log("asset = {}".format(asset))
log("row_struct = {}".format(asset.get_editor_property("row_struct")))

json_text = unreal.DataTableFunctionLibrary.export_data_table_to_json_string(asset)
log("json = {}".format(json_text))
