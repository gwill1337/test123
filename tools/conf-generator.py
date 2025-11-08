#!/usr/bin/env python3
import os
import shutil
import yaml
from render_config import render_config  # оставляем импорт

# --- Папки ---
DEVICE_DIR = "snapshots/ci_net/s1/device-yaml"
GENERATED_DIR = "snapshots/ci_net/s1/configs/generated"

# --- Очищаем папку generated ---
if os.path.exists(GENERATED_DIR):
    shutil.rmtree(GENERATED_DIR)
os.makedirs(GENERATED_DIR, exist_ok=True)

# --- Основной цикл по YAML ---
yaml_files = [f for f in os.listdir(DEVICE_DIR) if f.endswith(".yaml")]

if not yaml_files:
    print("No YAML files found in", DEVICE_DIR)

for file in yaml_files:
    path = os.path.join(DEVICE_DIR, file)
    with open(path) as f:
        content = yaml.safe_load(f)

    # Поддержка как списка, так и словаря
    devices = content if isinstance(content, list) else [content]

    for data in devices:
        if not isinstance(data, dict) or "hostname" not in data:
            print(f"Skipping invalid entry in {file}")
            continue

        try:
            cfg = render_config(data)  # используем render_config из render_config.py
        except Exception as e:
            print(f"Error rendering {data.get('hostname')}: {e}")
            continue

        hostname = data["hostname"]
        out_path = os.path.join(GENERATED_DIR, f"{hostname}_gen.cfg")

        with open(out_path, "w") as out:
            out.write(cfg)

        print(f"Rendered: {hostname}_gen.cfg")



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
