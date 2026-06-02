import unreal


CHARACTER_PATH = "/Game/Characters/MetaHumans/DemoMetaHuman.DemoMetaHuman"


def log(message):
    unreal.log("[FPS_MH_BUILD] {}".format(message))


character = unreal.load_asset(CHARACTER_PATH)
if not character:
    raise RuntimeError("Missing MetaHuman asset {}".format(CHARACTER_PATH))

subsystem = unreal.get_editor_subsystem(unreal.MetaHumanCharacterEditorSubsystem)
if not subsystem.try_add_object_to_edit(character):
    raise RuntimeError("Unable to edit MetaHuman asset")

try:
    params = unreal.MetaHumanCharacterEditorBuildParameters()
    params.pipeline_type = unreal.MetaHumanDefaultPipelineType.OPTIMIZED
    params.pipeline_quality = unreal.MetaHumanQualityLevel.MEDIUM
    params.absolute_build_path = "/Game/GeneratedMetaHumans/DemoMetaHuman"
    params.common_folder_path = "/Game/GeneratedMetaHumans/Common"
    params.enable_wardrobe_item_validation = False
    log("starting build")
    subsystem.build_meta_human(character=character, params=params)
    log("build finished")
finally:
    if subsystem.is_object_added_for_editing(character):
        subsystem.remove_object_to_edit(character)
        log("edit session closed")
