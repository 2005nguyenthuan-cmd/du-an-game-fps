import unreal


ASSETS = [
    "/Game/Variant_Shooter/Blueprints/BP_ShooterCharacter",
    "/Game/Variant_Shooter/Blueprints/AI/BP_ShooterNPC",
    "/Game/Variant_Shooter/Blueprints/Pickups/BP_ShooterPickup",
    "/Game/Variant_Shooter/Blueprints/Pickups/Weapons/BP_ShooterWeapon_Pistol",
    "/Game/Variant_Shooter/Blueprints/Pickups/Weapons/BP_ShooterWeapon_Rifle",
    "/Game/Variant_Shooter/Blueprints/Pickups/Weapons/BP_ShooterWeapon_GrenadeLauncher",
]

TOKENS = [
    "mesh",
    "skeletal",
    "static",
    "sound",
    "audio",
    "weapon",
    "projectile",
    "muzzle",
    "impact",
]


def log(message):
    unreal.log("[FPS_BP_INSPECT] {}".format(message))


def dump_properties(obj, indent="  "):
    for name in sorted(set(n for n in dir(obj) if not n.startswith("_"))):
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

    dump_properties(bp)

    try:
        handler = bp.get_editor_property("inheritable_component_handler")
        log("  inheritable_component_handler = {}".format(handler))
    except Exception:
        pass

    try:
        scs = bp.get_editor_property("simple_construction_script")
        nodes = scs.get_all_nodes()
        log("  scs_nodes = {}".format(len(nodes)))
        for node in nodes:
            try:
                template = node.get_actual_component_template(bp.generated_class())
            except Exception:
                template = None
            log(
                "  NODE {} class={} template={}".format(
                    node.get_variable_name(),
                    node.component_class,
                    template,
                )
            )
            if template:
                dump_properties(template, indent="    ")
    except Exception as exc:
        log("  scs unreadable: {}".format(exc))

    try:
        generated_class = bp.generated_class()
        cdo = unreal.get_default_object(generated_class)
        log("  cdo = {}".format(cdo))
        dump_properties(cdo, indent="    ")
        for comp in cdo.get_components_by_class(unreal.ActorComponent):
            log("  CDO component {} ({})".format(comp.get_name(), comp.get_class().get_path_name()))
            dump_properties(comp, indent="    ")
    except Exception as exc:
        log("  cdo unreadable: {}".format(exc))
