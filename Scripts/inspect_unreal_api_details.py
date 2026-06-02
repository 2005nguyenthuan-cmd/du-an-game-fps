import inspect
import unreal


def log(message):
    unreal.log("[FPS_API_DETAILS] {}".format(message))


def dump_doc(target, names):
    log("TARGET {}".format(target.__name__))
    for name in names:
        attr = getattr(target, name, None)
        if attr is None:
            log("  {} = <missing>".format(name))
            continue
        doc = getattr(attr, "__doc__", None)
        if doc:
            doc = " ".join(line.strip() for line in doc.strip().splitlines())
        else:
            doc = "<no doc>"
        log("  {} :: {}".format(name, doc))


dump_doc(
    unreal.MetaHumanCharacterEditorSubsystem,
    [
        "request_auto_rigging",
        "can_build_meta_human",
        "build_meta_human",
        "assemble_for_preview",
        "import_from_template",
        "import_from_face_dna",
    ],
)

dump_doc(
    unreal.AnimNotify_PlaySound,
    [
        "get_editor_property",
        "set_editor_property",
    ],
)

for candidate_name, names in [
    (
        "AnimNotifyLibrary",
        [
            "get_current_animation_notify_state_time",
            "get_current_animation_notify_state_weight",
            "notify_state_reached_end",
        ],
    ),
    (
        "UAnimNotifyLibrary",
        [
            "get_current_animation_notify_state_time",
            "get_current_animation_notify_state_weight",
            "notify_state_reached_end",
        ],
    ),
]:
    target = getattr(unreal, candidate_name, None)
    if target:
        dump_doc(target, names)
