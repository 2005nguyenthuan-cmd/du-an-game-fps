import unreal


MONTAGES = [
    "/Game/Variant_Shooter/Anims/FP_Rifle_Shoot_Montage",
    "/Game/Characters/Mannequins/Anims/Pistol/MM_Pistol_Fire_Montage",
]

TOKENS = ("notify", "sound", "montage", "time", "slot", "track")


def log(message):
    unreal.log("[FPS_MONTAGE_INSPECT] {}".format(message))


def dump_props(obj, indent="  "):
    for name in sorted(n for n in dir(obj) if not n.startswith("_")):
        if not any(token in name.lower() for token in TOKENS):
            continue
        try:
            value = obj.get_editor_property(name)
            log("{}{} = {}".format(indent, name, value))
        except Exception:
            pass


for asset_path in MONTAGES:
    montage = unreal.EditorAssetLibrary.load_asset(asset_path)
    log("ASSET {} -> {}".format(asset_path, montage))
    if not montage:
        continue
    dump_props(montage)
    try:
        notifies = montage.get_editor_property("notifies")
        log("  notifies_count = {}".format(len(notifies)))
        for idx, notify in enumerate(notifies):
            log("  notify[{}] = {}".format(idx, notify))
            try:
                payload = notify.get_editor_property("notify")
                log("    notify_object = {}".format(payload))
                if payload:
                    dump_props(payload, "      ")
            except Exception as exc:
                log("    notify inspect failed: {}".format(exc))
    except Exception as exc:
        log("  notifies unreadable: {}".format(exc))


for cls in (unreal.AnimNotifyEvent, unreal.AnimNotify_PlaySound):
    log("CLASS {}".format(cls.__name__))
    for name in sorted(n for n in dir(cls) if not n.startswith("_")):
        lower = name.lower()
        if any(token in lower for token in TOKENS):
            log("  METHOD {}".format(name))
