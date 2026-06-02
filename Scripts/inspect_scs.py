import unreal


ASSET_PATH = "/Game/Variant_Shooter/Blueprints/Pickups/Projectiles/BP_ShooterProjectile_Bullet"
TOKENS = ["projectile", "speed", "velocity", "gravity", "collision", "mesh", "sphere", "bounce"]


def log(message):
    unreal.log("[FPS_SCS_INSPECT] {}".format(message))


def dump(obj, indent="  "):
    for name in sorted(set(n for n in dir(obj) if not n.startswith("_"))):
        lower = name.lower()
        if not any(token in lower for token in TOKENS):
            continue
        try:
            value = obj.get_editor_property(name)
            log("{}{} = {}".format(indent, name, value))
        except Exception:
            pass


bp = unreal.EditorAssetLibrary.load_asset(ASSET_PATH)
log("BP = {}".format(bp))
for attr in ("simple_construction_script", "component_templates", "new_variables", "inheritable_component_handler"):
    try:
        value = bp.get_editor_property(attr)
        log("{} = {}".format(attr, value))
    except Exception as exc:
        log("{} unreadable: {}".format(attr, exc))

try:
    scs = bp.get_editor_property("simple_construction_script")
    nodes = scs.get_all_nodes()
    log("node_count = {}".format(len(nodes)))
    for node in nodes:
        log("NODE {} component_class={} template={}".format(node.get_variable_name(), node.component_class, node.get_actual_component_template(bp.generated_class())))
        try:
            template = node.get_actual_component_template(bp.generated_class())
            dump(template, indent="    ")
        except Exception as exc:
            log("    template dump failed: {}".format(exc))
except Exception as exc:
    log("SCS failed: {}".format(exc))
