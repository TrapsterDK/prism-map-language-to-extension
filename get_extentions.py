#simple python tool to map extensions to language codes

import json
import requests
import sys

components_url = "https://prismjs.com/components.js"
extensions_url = "https://gist.githubusercontent.com/ppisarczyk/43962d06686722d26d176fad46879d41/raw/211547723b4621a622fc56978d74aa416cbd1729/Programming_Languages_Extensions.json"

def main():
    if len(sys.argv) <= 1: 
        print("Missing output")
        return

    r_components = requests.get(components_url)

    components_json_str = ""
    for line in r_components.iter_lines():
        components_json_str = line.decode("utf-8")[:-1].split('=', 1)[1]
        break

    r_extensions = requests.get(extensions_url)

    components_json = json.loads(components_json_str)
    extensions_json = json.loads(r_extensions.content)

    language_map = {}

    for language_code in components_json['languages']:
        if(language_code == 'meta'): continue
        title_lower = components_json['languages'][language_code]['title'].lower()

        for extension_dict in extensions_json:
            if extension_dict['name'].lower() == title_lower:
                language_map[language_code] = [ext[1:] for ext in extension_dict['extensions']]
                break
    
    with open(sys.argv[1], "w", encoding="utf-8") as file:
        json.dump(language_map, file, indent=4, sort_keys=True, ensure_ascii=False)


if __name__ == "__main__":
    main()