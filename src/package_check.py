def check_required_packages(packages):
    import importlib
    for pkg in packages:
        try:
            importlib.import_module(pkg)
            print(f'✅ {pkg} geïnstalleerd')
        except ImportError:
            print(f'⚠️ {pkg} NIET geïnstalleerd')
