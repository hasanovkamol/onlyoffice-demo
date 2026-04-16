import json
import os

locale_dir = r"c:\Users\k_hasanov\Downloads\build_tools-master\build_tools-master\web-apps\apps\documenteditor\main\locale"
en_path = os.path.join(locale_dir, "en.json")
uz_path = os.path.join(locale_dir, "uz.json")

with open(en_path, 'r', encoding='utf-8') as f:
    en_keys = set(json.load(f).keys())

with open(uz_path, 'r', encoding='utf-8') as f:
    uz_keys = set(json.load(f).keys())

missing = en_keys - uz_keys
extra = uz_keys - en_keys

print(f"Missing from uz.json: {len(missing)}")
if missing:
    print(f"Sample missing: {list(missing)[:10]}")

print(f"Extra in uz.json: {len(extra)}")
if extra:
    print(f"Sample extra: {list(extra)[:10]}")
