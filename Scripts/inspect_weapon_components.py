import unreal


ASSETS = [
    "/Game/Variant_Shooter/Blueprints/Pickups/Weapons/BP_ShooterWeapon_Pistol",
    "/Game/Variant_Shooter/Blueprints/Pickups/Weapons/BP_ShooterWeapon_Rifle",
]

TOKENS = ("mesh", "skeletal", "static", "anim", "montage", "sound", "audio")


def log(message):
    unreal.log("[FPS_WEAPON_COMPONENTS] {}".format(message))


def dump_properties(obj, indent):
    for name in sorted(n for n in dir(obj) if not n.startswith("_")):
        if not any(token in name.lower() for token in TOKENS):
            continue
        try:
            value = obj.get_editor_property(name)
            log("{}{} = {}".format(indent, name, value))
        except Exception:
            pass


for asset_path in ASSETS:
    bp = unreal.EditorAssetLibrary.load_asset(asset_path)
    log("ASSET {} -> {}".format(asset_path, bp))
    if not bp:
        continue

    generated_class = bp.generated_class()
    cdo = unreal.get_default_object(generated_class)
    dump_properties(cdo, "  ")

    scs = bp.get_editor_property("simple_construction_script")
    nodes = scs.get_all_nodes()
    log("  SCS_NODES {}".format(len(nodes)))
    for node in nodes:
        template = None
        try:
            template = node.get_actual_component_template(generated_class)
        except Exception:
            try:
                template = node.component_template
            except Exception:
                template = None
        log("  NODE {} class={} template={}".format(node.get_variable_name(), node.component_class, template))
        if template:
            dump_properties(template, "    ")
