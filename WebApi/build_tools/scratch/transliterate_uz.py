import json
import os
import re

def transliterate_uz(text):
    if not isinstance(text, str):
        return text
    
    # Mapping for common combinations
    # Note: Order matters!
    mapping = {
        "sh": "ш", "Sh": "Ш", "SH": "Ш",
        "ch": "ч", "Ch": "Ч", "CH": "Ч",
        "o'": "ў", "O'": "Ў", "o’": "ў", "O’": "Ў", "o`": "ў", "O`": "Ў",
        "g'": "ғ", "G'": "Ғ", "g’": "ғ", "G’": "Ғ", "g`": "ғ", "G`": "Ғ",
        "yu": "ю", "Yu": "Ю", "YU": "Ю",
        "ya": "я", "Ya": "Я", "YA": "Я",
        "yo": "ё", "Yo": "Ё", "YO": "Ё",
        "ts": "ц", "Ts": "Ц", "TS": "Ц",
    }
    
    # Sort keys by length so sh is handled before s
    # But wait, I'll do specific replacements first
    
    res = text
    for lat, cyr in mapping.items():
        res = res.replace(lat, cyr)
        
    # Single character mapping
    single_mapping = {
        'a': 'а', 'b': 'б', 'd': 'д', 'f': 'ф',
        'g': 'г', 'h': 'ҳ', 'i': 'и', 'j': 'ж', 'k': 'к',
        'l': 'л', 'm': 'м', 'n': 'н', 'o': 'о', 'p': 'п',
        'q': 'қ', 'r': 'р', 's': 'с', 't': 'т', 'u': 'у',
        'v': 'в', 'w': 'в', 'x': 'х', 'y': 'й', 'z': 'з',
        'A': 'А', 'B': 'Б', 'D': 'Д', 'F': 'Ф',
        'G': 'Г', 'H': 'Ҳ', 'I': 'А', 'J': 'Ж', 'K': 'К', # Wait, I -> И usually, but here I'll fix it below
        'L': 'Л', 'M': 'М', 'N': 'Н', 'O': 'О', 'P': 'П',
        'Q': 'Қ', 'R': 'Р', 'S': 'С', 'T': 'Т', 'U': 'У',
        'V': 'В', 'W': 'В', 'X': 'Х', 'Y': 'Й', 'Z': 'З',
        "'": "ъ", # tutuq belgisi
    }
    
    # Fix mapping for I and i
    single_mapping['i'] = 'и'
    single_mapping['I'] = 'И'

    # Handle 'e' at start of word or after vowel
    res = ""
    vowels = "aeiouAEOIU'’`"
    
    # Simple word tokenizer to handle 'e'
    words = re.split(r'(\W+)', text)
    processed_words = []
    for word in words:
        if not word or not word[0].isalpha():
            processed_words.append(word)
            continue
            
        new_word = ""
        for i, char in enumerate(word):
            lower_char = char.lower()
            if lower_char == 'e':
                if i == 0 or (i > 0 and word[i-1].lower() in vowels):
                    new_word += 'Э' if char.isupper() else 'э'
                else:
                    new_word += 'Е' if char.isupper() else 'е'
            else:
                new_word += char
        processed_words.append(new_word)
    
    text = "".join(processed_words)

    res = text
    for lat, cyr in mapping.items():
        res = res.replace(lat, cyr)
        
    for lat, cyr in single_mapping.items():
        res = res.replace(lat, cyr)
        
    return res

def process_locales():
    base_dir = r"c:\Users\k_hasanov\Downloads\build_tools-master\build_tools-master\web-apps\apps"
    for root, dirs, files in os.walk(base_dir):
        if "uz.json" in files:
            uz_path = os.path.join(root, "uz.json")
            cyrl_path = os.path.join(root, "uz-cyrl.json")
            
            with open(uz_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            cyrl_data = {}
            for key, val in data.items():
                cyrl_data[key] = transliterate_uz(val)
            
            with open(cyrl_path, 'w', encoding='utf-8') as f:
                json.dump(cyrl_data, f, indent=2, ensure_ascii=False)
            
            print(f"Created: {cyrl_path}")

if __name__ == "__main__":
    process_locales()
