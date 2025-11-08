import os
import yaml
from render_config import render_config

DEVICE_DIR = "snapshots/ci_net/s1/device-yaml"
OUTPUT_DIR = "snapshots/ci_net/s1/configs/generated"

os.makedirs(OUTPUT_DIR, exist_ok=True)

for file in os.listdir(DEVICE_DIR):
    if not file.endswith(".yaml"):
        continue

    path = os.path.join(DEVICE_DIR, file)
    with open(path) as f:
        data = yaml.safe_load(f)

    # Если YAML содержит список устройств
    if isinstance(data, list):
        devices = data
    else:
        devices = [data]

    for device in devices:
        cfg = render_config(device)
        hostname = device["hostname"]

        out_path = os.path.join(OUTPUT_DIR, f"{hostname}_gen.cfg")
        with open(out_path, "w") as out:
            out.write(cfg)

        print(f"Rendered: {hostname}_gen.cfg")
