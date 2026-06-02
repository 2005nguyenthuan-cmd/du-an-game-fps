import unreal


ASSET_PATHS = [
    "/Game/Variant_Shooter/Blueprints/Pickups/Weapons/BP_ShooterWeapon_Pistol",
    "/Game/Variant_Shooter/Blueprints/Pickups/Weapons/BP_ShooterWeapon_Rifle",
    "/Game/Variant_Shooter/Blueprints/Pickups/Weapons/BP_ShooterWeapon_GrenadeLauncher",
    "/Game/Variant_Shooter/Blueprints/Pickups/Projectiles/BP_ShooterProjectile_Bullet",
]

TOKENS = [
    "spawn",
    "projectile",
    "trace",
    "line",
    "damage",
    "impact",
    "fire",
    "shoot",
    "audio",
    "sound",
]


def log(message):
    unreal.log("[FPS_GRAPH_INSPECT] {}".format(message))


for asset_path in ASSET_PATHS:
    bp = unreal.EditorAssetLibrary.load_asset(asset_path)
    log("ASSET {} -> {}".format(asset_path, bp))
    if bp is None:
        continue

    graphs = []
    for attr in ("ubergraph_pages", "function_graphs", "macro_graphs", "delegate_signature_graphs"):
        try:
            value = bp.get_editor_property(attr)
            if value:
                graphs.extend(list(value))
        except Exception:
            pass

    for graph in graphs:
        try:
            graph_name = graph.get_name()
        except Exception:
            graph_name = "<graph>"
        log("  GRAPH {}".format(graph_name))
        try:
            nodes = graph.get_nodes()
        except Exception as exc:
            log("    get_nodes failed: {}".format(exc))
            continue

        for node in nodes:
            try:
                node_title = node.get_node_title(unreal.NodeTitleType.LIST_VIEW)
            except Exception:
                node_title = node.get_name()
            text = "{} {}".format(node.get_class().get_name(), node_title).lower()
            if any(token in text for token in TOKENS):
                log("    NODE {} | {} | {}".format(node.get_name(), node.get_class().get_name(), node_title))
