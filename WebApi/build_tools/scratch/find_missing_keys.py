import json
import os

locale_dir = r"c:\Users\k_hasanov\Downloads\build_tools-master\build_tools-master\web-apps\apps\documenteditor\main\locale"
en_path = os.path.join(locale_dir, "en.json")
uz_path = os.path.join(locale_dir, "uz.json")

with open(en_path, 'r', encoding='utf-8') as f:
    en_data = json.load(f)

with open(uz_path, 'r', encoding='utf-8') as f:
    uz_data = json.load(f)

en_keys = set(en_data.keys())
uz_keys = set(uz_data.keys())

missing_keys = en_keys - uz_keys

print(f"Total keys in en.json: {len(en_keys)}")
print(f"Total keys in uz.json: {len(uz_keys)}")
print(f"Missing keys in uz.json: {len(missing_keys)}")

missing_data = {k: en_data[k] for k in missing_keys}
with open("missing_keys.json", "w", encoding="utf-8") as f:
    json.dump(missing_data, f, indent=4, ensure_ascii=False)
