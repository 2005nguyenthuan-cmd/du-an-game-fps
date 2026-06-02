import json
import unreal


WEAPON_TABLE_PATH = "/Game/Variant_Shooter/Blueprints/Pickups/DT_WeaponList"

MESH_OVERRIDES = {
    "Pistol": "/Game/Imported/Weapons/Pistol_Free/pirate_low_poly_pistol.pirate_low_poly_pistol",
    "Rifle": "/Game/Imported/Weapons/Rifle_Free/highpoly_ak47.highpoly_ak47",
}

SOUND_CUES = [
    {
        "asset_name": "SC_Pistol_Fire_Free",
        "package_path": "/Game/Imported/Audio/Gunshots/Cues",
        "sound_wave": "/Game/Imported/Audio/Gunshots/shotty.shotty",
    },
    {
        "asset_name": "SC_Rifle_Fire_Free",
        "package_path": "/Game/Imported/Audio/Gunshots/Cues",
        "sound_wave": "/Game/Imported/Audio/Gunshots/sks.sks",
    },
]


def log(message):
    unreal.log("[FPS_FREE_UPGRADE] {}".format(message))


def update_weapon_table():
    table = unreal.EditorAssetLibrary.load_asset(WEAPON_TABLE_PATH)
    if not table:
        raise RuntimeError("Could not load weapon table")

    rows = json.loads(unreal.DataTableFunctionLibrary.export_data_table_to_json_string(table))
    changed = False
    for row in rows:
        name = row.get("Name")
        if name in MESH_OVERRIDES:
            new_mesh = MESH_OVERRIDES[name]
            if row.get("Static Mesh") != new_mesh:
                row["Static Mesh"] = new_mesh
                changed = True
                log("row {} mesh -> {}".format(name, new_mesh))

    if changed:
        ok = unreal.DataTableFunctionLibrary.fill_data_table_from_json_string(table, json.dumps(rows, indent=2))
        if not ok:
            raise RuntimeError("Failed to write DT_WeaponList from JSON")
        unreal.EditorAssetLibrary.save_loaded_asset(table, only_if_is_dirty=False)
        log("weapon table saved")
    else:
        log("weapon table already up to date")


def create_sound_cues():
    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
    factory = unreal.SoundCueFactoryNew()
    sound_cue_cls = unreal.SoundCue

    for spec in SOUND_CUES:
        package_name = "{}/{}".format(spec["package_path"], spec["asset_name"])
        if unreal.EditorAssetLibrary.does_asset_exist(package_name):
            cue = unreal.EditorAssetLibrary.load_asset(package_name)
            log("reuse cue {}".format(package_name))
        else:
            cue = asset_tools.create_asset(
                asset_name=spec["asset_name"],
                package_path=spec["package_path"],
                asset_class=sound_cue_cls,
                factory=factory,
            )
            log("created cue {}".format(package_name))

        wave = unreal.EditorAssetLibrary.load_asset(spec["sound_wave"])
        if not wave:
            raise RuntimeError("Missing sound wave {}".format(spec["sound_wave"]))

        try:
            cue.set_editor_property("first_node", wave)
        except Exception as exc:
            log("first_node bind skipped for {}: {}".format(package_name, exc))

        try:
            graph = cue.get_editor_property("sound_graph")
            nodes = graph.get_nodes()
            for node in nodes:
                try:
                    if node.get_class().get_name() == "SoundCueGraphNode_Root":
                        node.set_editor_property("sound_class", None)
                except Exception:
                    pass
        except Exception:
            pass

        unreal.EditorAssetLibrary.save_loaded_asset(cue, only_if_is_dirty=False)


update_weapon_table()
create_sound_cues()
unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
log("done")
