
import os
import json
from datetime import datetime
import re

# Set the correct path to your album folder
album_folder = os.path.expanduser("~/Downloads/Album Ranking Database")
output_file = os.path.join(album_folder, "all_albums.json")
all_albums = []

# Helper function to clean up all text fields recursively
def clean_text_fields(obj):
    if isinstance(obj, dict):
        return {k: clean_text_fields(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [clean_text_fields(item) for item in obj]
    elif isinstance(obj, str):
        # Replace common misencoded apostrophes and quotes
        obj = obj.replace('\u00e2\u20ac\u2122', "'")
        obj = re.sub(r'[\u2018\u2019]', "'", obj)  # left/right single quotes
        obj = re.sub(r'[\u201c\u201d]', '"', obj)  # left/right double quotes
        return obj
    else:
        return obj

# Helper function to extract 'dateCompleted' from each file
def get_date_completed(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if isinstance(data, list):
                date_str = data[0].get("dateCompleted", "1900-01-01T00:00")
            else:
                date_str = data.get("dateCompleted", "1900-01-01T00:00")
            return datetime.strptime(date_str, "%Y-%m-%dT%H:%M")
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return datetime.min

# Get list of JSON files excluding the output file
json_files = [f for f in os.listdir(album_folder) if f.endswith(".json") and f != "all_albums.json"]
json_files.sort(key=lambda f: get_date_completed(os.path.join(album_folder, f)))

# Loop through all JSON files in the specified folder
for filename in json_files:
    try:
        with open(os.path.join(album_folder, filename), 'r', encoding='utf-8') as f:
            data = json.load(f)
            cleaned_data = clean_text_fields(data)
            if isinstance(cleaned_data, list):
                all_albums.extend(cleaned_data)
            else:
                all_albums.append(cleaned_data)
    except Exception as e:
        print(f"Error reading {filename}: {e}")

# Write the merged album data to the output file
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(all_albums, f, indent=2, ensure_ascii=False)

print(f"Merged {len(all_albums)} album entries into '{output_file}'.")
