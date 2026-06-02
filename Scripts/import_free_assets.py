import os
import unreal


PROJECT_ROOT = r"C:\UnrealProjects\MyProject2_Local"

IMPORTS = [
    {
        "filename": os.path.join(PROJECT_ROOT, "ExternalAssets", "Pistol_Free", "pirate_low_poly_pistol.fbx"),
        "destination": "/Game/Imported/Weapons/Pistol_Free",
        "options": "fbx_static_mesh",
    },
    {
        "filename": os.path.join(PROJECT_ROOT, "ExternalAssets", "Downloads", "highpoly_ak47.obj"),
        "destination": "/Game/Imported/Weapons/Rifle_Free",
        "options": "obj_static_mesh",
    },
    {
        "filename": os.path.join(PROJECT_ROOT, "ExternalAssets", "Gunshot_Sounds", "sounds", "cz.wav"),
        "destination": "/Game/Imported/Audio/Gunshots",
        "options": None,
    },
    {
        "filename": os.path.join(PROJECT_ROOT, "ExternalAssets", "Gunshot_Sounds", "sounds", "mosin.wav"),
        "destination": "/Game/Imported/Audio/Gunshots",
        "options": None,
    },
    {
        "filename": os.path.join(PROJECT_ROOT, "ExternalAssets", "Gunshot_Sounds", "sounds", "shotty.wav"),
        "destination": "/Game/Imported/Audio/Gunshots",
        "options": None,
    },
    {
        "filename": os.path.join(PROJECT_ROOT, "ExternalAssets", "Gunshot_Sounds", "sounds", "sks.wav"),
        "destination": "/Game/Imported/Audio/Gunshots",
        "options": None,
    },
]


def log(message):
    unreal.log("[FPS_IMPORT] {}".format(message))


def build_fbx_options():
    ui = unreal.FbxImportUI()
    ui.set_editor_property("import_mesh", True)
    ui.set_editor_property("import_textures", True)
    ui.set_editor_property("import_materials", True)
    ui.set_editor_property("import_as_skeletal", False)
    ui.set_editor_property("create_physics_asset", False)
    ui.set_editor_property("automated_import_should_detect_type", False)
    ui.set_editor_property("mesh_type_to_import", unreal.FBXImportType.FBXIT_STATIC_MESH)

    static_mesh_data = ui.static_mesh_import_data
    static_mesh_data.set_editor_property("combine_meshes", True)
    static_mesh_data.set_editor_property("generate_lightmap_u_vs", True)
    static_mesh_data.set_editor_property("auto_generate_collision", True)
    return ui


def build_obj_options():
    data = unreal.FbxStaticMeshImportData()
    data.set_editor_property("combine_meshes", True)
    data.set_editor_property("generate_lightmap_u_vs", True)
    data.set_editor_property("auto_generate_collision", True)
    return data


def build_task(spec):
    task = unreal.AssetImportTask()
    task.set_editor_property("filename", spec["filename"])
    task.set_editor_property("destination_path", spec["destination"])
    task.set_editor_property("automated", True)
    task.set_editor_property("replace_existing", True)
    task.set_editor_property("save", True)

    option_kind = spec["options"]
    if option_kind == "fbx_static_mesh":
        task.set_editor_property("options", build_fbx_options())
    elif option_kind == "obj_static_mesh":
        task.set_editor_property("options", build_obj_options())
    return task


asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
tasks = []
for spec in IMPORTS:
    if not os.path.exists(spec["filename"]):
        raise RuntimeError("Missing import source: {}".format(spec["filename"]))
    log("queue {} -> {}".format(spec["filename"], spec["destination"]))
    tasks.append(build_task(spec))

asset_tools.import_asset_tasks(tasks)

for task in tasks:
    imported = task.get_editor_property("imported_object_paths")
    log("imported {} -> {}".format(task.get_editor_property("filename"), imported))

unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
log("save complete")
