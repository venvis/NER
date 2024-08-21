import os
import json
import csv
import subprocess


repo_url = 'https://github.com/lawfulcomputing/GDPRxiv.git'
clone_dir = 'GDPRxiv'
script_name = 'process_files.py'


def clone_repository(repo_url, target_dir):
    if not os.path.exists(target_dir):
        subprocess.run(['git', 'clone', repo_url, target_dir], check=True)
    else:
        print(f"Repository already exists at {target_dir}, skipping clone.")


def get_dir():
    current = os.getcwd()
    countries = f"{current}/documents"
    get_c = os.listdir(countries)
    result_dict = {}
    for counts in get_c:
        country_path = f"{countries}/{counts}"
        if any("decisions" in folder.lower() for folder in os.listdir(country_path)):
            result_dict[counts] = os.listdir(country_path)
    return result_dict

def get_metadata():
    fields = {}
    dic = get_dir()
    for country, dirs in dic.items():
        country_data = {}
        for dir in dirs:
            if "decisions" in dir.lower():
                decision_path = f"documents/{country}/{dir}"
                for file in os.listdir(decision_path):
                    file_path = os.path.join(decision_path, file)
                    if os.path.isdir(file_path):
                        en_txt_path = os.path.join(file_path, "en.txt")
                        metadata_json_path = os.path.join(file_path, "metadata.json")
                        
                        if os.path.exists(en_txt_path) and os.path.exists(metadata_json_path):
                            with open(en_txt_path, 'r', encoding='utf-8') as en_file:
                                en_text = en_file.read()
                            
                            with open(metadata_json_path, 'r', encoding='utf-8') as json_file:
                                metadata = json.load(json_file)
                            
                            country_data[file] = {
                                'en_text': en_text,
                                'metadata': metadata
                            }
        
        if country_data:
            fields[country] = country_data
    
    return fields

def write_to_csv(data):
    with open('output.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Country', 'Decision', 'Text', 'Metadata']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for country, decisions in data.items():
            for decision, content in decisions.items():
                writer.writerow({
                    'Country': country,
                    'Decision': decision,
                    'Text': content['en_text'],
                    'Metadata': json.dumps(content['metadata']) 
                })


def main():
    
    clone_repository(repo_url, clone_dir)

 
    os.chdir(clone_dir)
    
   
    data = get_metadata()
    write_to_csv(data)


if __name__ == "__main__":
    main()
