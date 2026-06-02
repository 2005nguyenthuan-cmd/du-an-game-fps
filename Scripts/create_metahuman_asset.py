import unreal


def log(message):
    unreal.log("[FPS_MH_CREATE] {}".format(message))


asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
package_path = "/Game/Characters/MetaHumans"
asset_name = "DemoMetaHuman"

unreal.EditorAssetLibrary.make_directory(package_path)

existing = unreal.EditorAssetLibrary.does_asset_exist("{}/{}".format(package_path, asset_name))
if existing:
    log("Asset already exists at {}/{}".format(package_path, asset_name))
else:
    asset = asset_tools.create_asset(
        asset_name=asset_name,
        package_path=package_path,
        asset_class=unreal.MetaHumanCharacter,
        factory=unreal.new_object(type=unreal.MetaHumanCharacterFactoryNew),
    )
    log("created = {}".format(asset))

asset = unreal.EditorAssetLibrary.load_asset("{}/{}".format(package_path, asset_name))
log("loaded = {}".format(asset))

try:
    subsystem = unreal.get_editor_subsystem(unreal.MetaHumanCharacterEditorSubsystem)
    log("editor subsystem = {}".format(subsystem))
    if subsystem.try_add_object_to_edit(character=asset):
        log("added asset to MetaHuman editor subsystem")
        subsystem.remove_object_to_edit(character=asset)
    else:
        log("could not add asset to MetaHuman editor subsystem")
except Exception as exc:
    log("subsystem failed: {}".format(exc))

unreal.EditorAssetLibrary.save_asset("{}/{}".format(package_path, asset_name), only_if_is_dirty=False)
log("saved asset")
