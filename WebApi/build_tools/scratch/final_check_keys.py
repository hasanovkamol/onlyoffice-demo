import json
import os

apps_dir = r"c:\Users\k_hasanov\Downloads\build_tools-master\build_tools-master\web-apps\apps"
editors = ["documenteditor", "spreadsheeteditor", "presentationeditor", "pdfeditor"]

for editor in editors:
    locale_dir = os.path.join(apps_dir, editor, "main", "locale")
    en_path = os.path.join(locale_dir, "en.json")
    uz_path = os.path.join(locale_dir, "uz.json")
    
    if os.path.exists(en_path) and os.path.exists(uz_path):
        with open(en_path, 'r', encoding='utf-8') as f:
            en_keys = set(json.load(f).keys())
        with open(uz_path, 'r', encoding='utf-8') as f:
            uz_keys = set(json.load(f).keys())
        
        missing = en_keys - uz_keys
        if missing:
            print(f"Editor {editor} is MISSING {len(missing)} keys!")
        else:
            print(f"Editor {editor} has all keys.")
