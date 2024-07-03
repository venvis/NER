# import os

# def get_dir():
#     current=os.getcwd()
#     countries=f"{current}/documents"
#     get_c=os.listdir(countries)
#     dict={}
#     for counts in get_c:
#         if "Decisions" or "Decisions 2" in os.listdir(f"{countries}/{counts}"):
#             dict[counts]=os.listdir(f"{countries}/{counts}")
            

#     return dict
# # print(get_dir())
# def get_metadata():
#     fields = {}
#     dic = get_dir()
#     for country, dirs in dic.items():
#         for dir in dirs:
#             if dir.lower() in ["decisions", "decisions 2"]:
#                 decision_path = f"documents/{country}/{dir}"
#                 fields[country] = os.listdir(decision_path)
#     return fields

# a=get_metadata()
# print(a)
    


import os
import json
import csv

def get_dir():
    current = os.getcwd()
    countries = f"{current}/documents"
    get_c = os.listdir(countries)
    dict = {}
    for counts in get_c:
        country_path = f"{countries}/{counts}"
        if any("decisions" in folder.lower() for folder in os.listdir(country_path)):
            dict[counts] = os.listdir(country_path)
    return dict

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
                    'Metadata': json.dumps(content['metadata'])  # Convert metadata back to JSON string
                })

# Get the metadata
a = get_metadata()

# Write the data to CSV
write_to_csv(a)

print("Data has been written to output.csv")