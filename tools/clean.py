import os
import shutil

SNAPSHOT_DIR = "snapshots/ci_net/s1/configs"
CLEAN_SNAPSHOT_DIR = "snapshots/ci_net/s1/snapshot_cleaned"

# Очистка старой
if os.path.exists(CLEAN_SNAPSHOT_DIR):
    shutil.rmtree(CLEAN_SNAPSHOT_DIR)
os.makedirs(CLEAN_SNAPSHOT_DIR, exist_ok=True)

# Копируем только нужные cfg (manual + generated)
for cfg_dir in ["manual", "generated"]:
    src_dir = os.path.join(SNAPSHOT_DIR, cfg_dir)
    if not os.path.exists(src_dir):
        continue
    for f in os.listdir(src_dir):
        if f.endswith(".cfg"):
            shutil.copy(os.path.join(src_dir, f), CLEAN_SNAPSHOT_DIR)

print("Snapshot cleaned, ready for Batfish")
