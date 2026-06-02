import unreal


def log(message):
    unreal.log("[FPS_API_SURFACE] {}".format(message))


def dump_methods(target, tokens):
    log("TARGET {}".format(target.__name__))
    for name in sorted(n for n in dir(target) if not n.startswith("_")):
        lower = name.lower()
        if any(token in lower for token in tokens):
            log("  {}".format(name))


def dump_matching_classes(tokens):
    for name in sorted(n for n in dir(unreal) if not n.startswith("_")):
        lower = name.lower()
        if any(token in lower for token in tokens):
            attr = getattr(unreal, name)
            if isinstance(attr, type):
                log("CLASS {}".format(name))


dump_methods(
    unreal.MetaHumanCharacterEditorSubsystem,
    ("build", "rig", "import", "edit", "character", "pipeline", "assemble", "texture"),
)
dump_methods(
    unreal.BlueprintEditorLibrary,
    ("graph", "node", "pin", "function", "compile", "event"),
)
dump_matching_classes(("anim", "notify", "montage", "metahuman"))
