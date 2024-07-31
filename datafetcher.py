import os
import json
import csv

def process_directory(root_dir):
    for country in os.listdir(root_dir):
        country_path = os.path.join(root_dir, country)
        if os.path.isdir(country_path):
            decisions_path = os.path.join(country_path, 'decisions')
            if os.path.exists(decisions_path):
                process_country(country, decisions_path)

def process_country(country, decisions_path):
    csv_filename = f"{country}_decisions.csv"
    
    with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile)
        
        # Write header
        header = ['Decision', 'Content']
        metadata_keys = get_metadata_keys(decisions_path)
        header.extend(metadata_keys)
        csvwriter.writerow(header)
        
        for decision in os.listdir(decisions_path):
            decision_path = os.path.join(decisions_path, decision)
            if os.path.isdir(decision_path):
                content = read_file(os.path.join(decision_path, 'en.txt'))
                metadata = read_json(os.path.join(decision_path, 'metadata.json'))
                
                row = [decision, content]
                row.extend([get_metadata_value(metadata, key) for key in metadata_keys])
                csvwriter.writerow(row)

def get_metadata_keys(decisions_path):
    keys = set()
    for decision in os.listdir(decisions_path):
        decision_path = os.path.join(decisions_path, decision)
        if os.path.isdir(decision_path):
            metadata = read_json(os.path.join(decision_path, 'metadata.json'))
            if isinstance(metadata, list):
                for item in metadata:
                    if isinstance(item, dict):
                        keys.update(item.keys())
            elif isinstance(metadata, dict):
                keys.update(metadata.keys())
    return sorted(keys)

def get_metadata_value(metadata, key):
    if isinstance(metadata, list):
        for item in metadata:
            if isinstance(item, dict) and key in item:
                return item[key]
    elif isinstance(metadata, dict) and key in metadata:
        return metadata[key]
    return ''

def read_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read().strip()
    except FileNotFoundError:
        return ''

def read_json(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}


root_directory = ' ' # Replace the directory with respective directory of the cloned repo
process_directory(root_directory)
