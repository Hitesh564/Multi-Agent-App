import importlib, sys
pkgs=["transformers","diffusers","langchain","langchain_community","sentence_transformers"]
print(sys.executable)
for p in pkgs:
    try:
        m=importlib.import_module(p)
        print(p, getattr(m, "__version__", "unknown"))
    except Exception as e:
        print(p, "not installed")
