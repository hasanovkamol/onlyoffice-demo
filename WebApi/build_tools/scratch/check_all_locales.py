import json
import os

apps_dir = r"c:\Users\k_hasanov\Downloads\build_tools-master\build_tools-master\web-apps\apps"
editors = ["documenteditor", "spreadsheeteditor", "presentationeditor", "pdfeditor"]

for editor in editors:
    locale_dir = os.path.join(apps_dir, editor, "main", "locale")
    en_path = os.path.join(locale_dir, "en.json")
    uz_path = os.path.join(locale_dir, "uz.json")
    
    if not os.path.exists(en_path) or not os.path.exists(uz_path):
        print(f"Skipping {editor} - files not found")
        continue
        
    with open(en_path, 'r', encoding='utf-8') as f:
        en_data = json.load(f)

    with open(uz_path, 'r', encoding='utf-8') as f:
        uz_data = json.load(f)

    en_keys = set(en_data.keys())
    uz_keys = set(uz_data.keys())

    missing_keys = en_keys - uz_keys
    print(f"Editor: {editor}")
    print(f"  Total keys in en.json: {len(en_keys)}")
    print(f"  Total keys in uz.json: {len(uz_keys)}")
    print(f"  Missing keys in uz.json: {len(missing_keys)}")
    if missing_keys:
        print(f"  First 5 missing: {list(missing_keys)[:5]}")
