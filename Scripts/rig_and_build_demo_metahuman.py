import unreal


CHARACTER_PATH = "/Game/Characters/MetaHumans/DemoMetaHuman.DemoMetaHuman"


def log(message):
    unreal.log("[FPS_MH_RIG] {}".format(message))


character = unreal.load_asset(CHARACTER_PATH)
if not character:
    raise RuntimeError("Missing MetaHuman asset {}".format(CHARACTER_PATH))

subsystem = unreal.get_editor_subsystem(unreal.MetaHumanCharacterEditorSubsystem)
if not subsystem.try_add_object_to_edit(character):
    raise RuntimeError("Unable to edit MetaHuman asset")

try:
    log("initial can_build = {}".format(subsystem.can_build_meta_human(character=character, log_error=True)))

    autorig_params = unreal.MetaHumanCharacterAutoRiggingRequestParams()
    autorig_params.blocking = True
    autorig_params.report_progress = False
    autorig_params.rig_type = unreal.MetaHumanRigType.JOINTS_ONLY
    log("requesting auto rigging")
    subsystem.request_auto_rigging(character=character, params=autorig_params)

    log("after autorig can_build = {}".format(subsystem.can_build_meta_human(character=character, log_error=True)))

    texture_params = unreal.MetaHumanCharacterTextureRequestParams()
    texture_params.blocking = True
    texture_params.report_progress = False
    log("requesting texture sources")
    subsystem.request_texture_sources(character=character, params=texture_params)
    log("has_high_resolution_textures = {}".format(character.get_editor_property("has_high_resolution_textures")))

    can_build = subsystem.can_build_meta_human(character=character, log_error=True)
    log("final can_build = {}".format(can_build))

    if can_build:
        build_params = unreal.MetaHumanCharacterEditorBuildParameters()
        build_params.pipeline_type = unreal.MetaHumanDefaultPipelineType.OPTIMIZED
        build_params.pipeline_quality = unreal.MetaHumanQualityLevel.MEDIUM
        build_params.absolute_build_path = "/Game/GeneratedMetaHumans/DemoMetaHuman"
        build_params.common_folder_path = "/Game/GeneratedMetaHumans/Common"
        build_params.enable_wardrobe_item_validation = False
        log("building optimized metahuman")
        subsystem.build_meta_human(character=character, params=build_params)
        log("build finished")

    unreal.EditorAssetLibrary.save_loaded_asset(character, only_if_is_dirty=False)
    unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
finally:
    if subsystem.is_object_added_for_editing(character):
        subsystem.remove_object_to_edit(character)
        log("edit session closed")
