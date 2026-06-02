import unreal


def log(message):
    unreal.log("[FPS_BP_API] {}".format(message))


target = unreal.BlueprintEditorLibrary
log("TARGET {}".format(target.__name__))
for name in sorted(n for n in dir(target) if not n.startswith("_")):
    if any(token in name.lower() for token in ("graph", "node", "function", "pin", "blueprint", "spawn", "call", "compile")):
        log("  {}".format(name))
