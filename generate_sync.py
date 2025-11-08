import json
import os
import sys

# ==============================
# Parámetros generales
# ==============================

GITHUB_USER = "MrE3gman"
REPO_NAME = "Torrecraft"
BRANCH = "main"

# Rutas internas del repo
MODS_PATH = "Mods/Client/mods"
CONFIGS_ZIP_PATH = "Configs/Client/client-configs.zip"

CONFIGS_ENTRY_NAME = "Client_Configs"
CONFIGS_TARGET_DIR = "config"

# ==============================
# Parámetros dinámicos (CLI)
# ==============================
# Uso:
#   python generate_sync.py <version_mods> <version_configs>
#
# Ejemplo:
#   python generate_sync.py 1.2.0 1.0.3

if len(sys.argv) >= 2:
    MODS_VERSION = sys.argv[1]
else:
    MODS_VERSION = "1.0.0"

if len(sys.argv) >= 3:
    CONFIGS_VERSION = sys.argv[2]
else:
    CONFIGS_VERSION = "1.0.0"

print(f"Versión global de mods: {MODS_VERSION}")
print(f"Versión del paquete de configs: {CONFIGS_VERSION}")

# ==============================
# Generación de URLs base
# ==============================
mods_base_url = (
    f"https://raw.githubusercontent.com/{GITHUB_USER}/"
    f"{REPO_NAME}/{BRANCH}/{MODS_PATH}"
)

configs_url = (
    f"https://raw.githubusercontent.com/{GITHUB_USER}/"
    f"{REPO_NAME}/{BRANCH}/{CONFIGS_ZIP_PATH}"
)

sync_entries = []

# --- 1) Procesar los mods ---
for filename in os.listdir(MODS_PATH):
    if not filename.lower().endswith(".jar"):
        continue

    url = f"{mods_base_url}/{filename}"
    name = os.path.splitext(filename)[0]

    entry = {
        "url": url,
        "name": name,
        "version": MODS_VERSION,
        "type": "mod"
    }
    sync_entries.append(entry)

# --- 2) Añadir las configs empaquetadas ---
if os.path.exists(CONFIGS_ZIP_PATH):
    configs_entry = {
        "url": configs_url,
        "name": CONFIGS_ENTRY_NAME,
        "version": CONFIGS_VERSION,
        "type": "packed",
        "directory": CONFIGS_TARGET_DIR
    }
    sync_entries.append(configs_entry)
    print(f"Añadida entrada de configs empaquetadas: {CONFIGS_ZIP_PATH}")
else:
    print(f"AVISO: No se encontró el ZIP de configs en {CONFIGS_ZIP_PATH}")

# --- 3) Bloque modify para eliminar config/fml.toml ---
modify_entries = [
    {
        "type": "remove",
        "pattern": "^fml\\.toml$",
        "path": "config"
    }
]

# --- 4) Crear estructura final del JSON ---
sync_json = {
    "sync_version": 3,
    "modify": modify_entries,
    "sync": sync_entries
}

# --- 5) Escribir sync.json ---
with open("sync.json", "w", encoding="utf-8") as f:
    json.dump(sync_json, f, indent=2, ensure_ascii=False)

print(f"sync.json generado con {len(sync_entries)} entradas y bloque 'modify'.")
