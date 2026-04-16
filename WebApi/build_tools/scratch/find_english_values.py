import json
import os

locale_dir = r"c:\Users\k_hasanov\Downloads\build_tools-master\build_tools-master\web-apps\apps\documenteditor\main\locale"
en_path = os.path.join(locale_dir, "en.json")
uz_path = os.path.join(locale_dir, "uz.json")

with open(en_path, 'r', encoding='utf-8') as f:
    en_data = json.load(f)

with open(uz_path, 'r', encoding='utf-8') as f:
    uz_data = json.load(f)

english_values = []
for key, val in uz_data.items():
    if key in en_data and val == en_data[key]:
        # Filter out very short things or things that might be same in both (like "OK", "Alt", ",")
        if len(val) > 3 or (val.isalpha() and val != "OK"):
             english_values.append((key, val))

print(f"Total keys: {len(uz_data)}")
print(f"Likely English values: {len(english_values)}")

with open("english_values_to_translate.json", "w", encoding="utf-8") as f:
    json.dump(english_values[:100], f, indent=4, ensure_ascii=False) # Only first 100 for inspection
