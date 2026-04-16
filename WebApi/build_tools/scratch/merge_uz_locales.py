import json
import os
import glob

def merge_common_keys(src_uz_data, dest_en_path, output_uz_path):
    try:
        with open(dest_en_path, 'r', encoding='utf-8') as f:
            dest_en_data = json.load(f)
        
        output_data = {}
        for key, val in dest_en_data.items():
            if key in src_uz_data:
                output_data[key] = src_uz_data[key]
            else:
                output_data[key] = val # Fallback to English for now

        with open(output_uz_path, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Error processing {dest_en_path}: {e}")
        return False

base_dir = r'c:\Users\k_hasanov\Downloads\build_tools-master\build_tools-master\web-apps\apps'
src_uz_path = os.path.join(base_dir, 'documenteditor', 'main', 'locale', 'uz.json')

with open(src_uz_path, 'r', encoding='utf-8') as f:
    src_uz_data = json.load(f)

# Find all en.json files in web-apps/apps
en_files = glob.glob(os.path.join(base_dir, '**', 'en.json'), recursive=True)

for en_file in en_files:
    dir_name = os.path.dirname(en_file)
    uz_file = os.path.join(dir_name, 'uz.json')
    if merge_common_keys(src_uz_data, en_file, uz_file):
        print(f"Created/Updated: {uz_file}")

print("All uz.json files created/updated.")
