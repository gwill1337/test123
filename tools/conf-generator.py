#!/usr/bin/env python3
import os
import shutil
import yaml
from render_config import render_config

# Папки
DEVICE_DIR = "snapshots/ci_net/s1/device-yaml"
GENERATED_DIR = "snapshots/ci_net/s1/configs/generated"
MANUAL_DIR = "snapshots/ci_net/s1/configs/manual"
SNAPSHOT_ROOT = "snapshots/ci_net/s1"

# Создать папку для generated и очистить
os.makedirs(GENERATED_DIR, exist_ok=True)
for f in os.listdir(GENERATED_DIR):
    if f.endswith(".cfg"):
        os.remove(os.path.join(GENERATED_DIR, f))

# Генерация конфигов из YAML
for file in os.listdir(DEVICE_DIR):
    if not file.endswith(".yaml"):
        continue
    path = os.path.join(DEVICE_DIR, file)
    with open(path) as f:
        data = yaml.safe_load(f)

    cfg = render_config(data)
    hostname = data["hostname"]
    out_path = os.path.join(GENERATED_DIR, f"{hostname}_gen.cfg")
    with open(out_path, "w") as out:
        out.write(cfg)
    print(f"Rendered: {hostname}_gen.cfg")

# Очистка старых cfg в корне snapshot
for f in os.listdir(SNAPSHOT_ROOT):
    if f.endswith(".cfg"):
        os.remove(os.path.join(SNAPSHOT_ROOT, f))

# Копирование всех cfg из manual и generated в корень snapshot
for src_dir in [MANUAL_DIR, GENERATED_DIR]:
    if os.path.exists(src_dir):
        for f in os.listdir(src_dir):
            if f.endswith(".cfg"):
                shutil.copy(os.path.join(src_dir, f), SNAPSHOT_ROOT)
                print(f"Copied {f} to snapshot root")


# import os
# import shutil
# import yaml
# from render_config import render_config  # твоя функция с Jinja2

# # Папки
# DEVICE_DIR = "snapshots/ci_net/s1/device-yaml"
# GENERATED_DIR = "snapshots/ci_net/s1/configs/generated"

# # Очистка и создание папки generated
# if os.path.exists(GENERATED_DIR):
#     shutil.rmtree(GENERATED_DIR)
# os.makedirs(GENERATED_DIR, exist_ok=True)

# # Перебор всех YAML файлов
# for file in os.listdir(DEVICE_DIR):
#     if not file.endswith(".yaml"):
#         continue

#     path = os.path.join(DEVICE_DIR, file)
#     with open(path) as f:
#         data = yaml.safe_load(f)

#     # Если YAML содержит список устройств, обрабатываем каждый
#     devices = data if isinstance(data, list) else [data]

#     for device in devices:
#         # Рендеринг конфигурации через Jinja2
#         cfg = render_config(device)

#         hostname = device.get("hostname", "unnamed").replace(" ", "_")
#         out_path = os.path.join(GENERATED_DIR, f"{hostname}_gen.cfg")

#         with open(out_path, "w") as out:
#             out.write(cfg)

#         print(f"Rendered: {hostname}_gen.cfg")


# import os
# import yaml
# from render_config import render_config

# DEVICE_DIR = "snapshots/ci_net/s1/device-yaml"
# OUTPUT_DIR = "snapshots/ci_net/s1/configs/generated"

# os.makedirs(OUTPUT_DIR, exist_ok=True)

# for file in os.listdir(DEVICE_DIR):
#     if not file.endswith(".yaml"):
#         continue

#     path = os.path.join(DEVICE_DIR, file)
#     with open(path) as f:
#         data = yaml.safe_load(f)

#     # Если YAML содержит список устройств
#     if isinstance(data, list):
#         devices = data
#     else:
#         devices = [data]

#     for device in devices:
#         cfg = render_config(device)
#         hostname = device["hostname"]

#         out_path = os.path.join(OUTPUT_DIR, f"{hostname}_gen.cfg")
#         with open(out_path, "w") as out:
#             out.write(cfg)

#         print(f"Rendered: {hostname}_gen.cfg")
