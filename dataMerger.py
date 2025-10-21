import os
import json

# Set the correct path to your album folder
album_folder = os.path.expanduser("~/Downloads/Album Ranking Database")
output_file = os.path.join(album_folder, "all_albums.json")
all_albums = []


# Get list of JSON files sorted by creation time (oldest to newest)
json_files = [f for f in os.listdir(album_folder) if f.endswith(".json") and f != "all_albums.json"]
json_files.sort(key=lambda f: os.path.getctime(os.path.join(album_folder, f)))

# Loop through all JSON files in the specified folder
for filename in json_files:
    if filename.endswith(".json") and filename != "all_albums.json":
        try:
            with open(os.path.join(album_folder, filename), 'r') as f:
                data = json.load(f)
                if isinstance(data, list):
                    all_albums.extend(data)
                else:
                    all_albums.append(data)
        except Exception as e:
            print(f"Error reading {filename}: {e}")

# Write the merged album data to the output file
with open(output_file, 'w') as f:
    json.dump(all_albums, f, indent=2)

print(f"Merged {len(all_albums)} album entries into '{output_file}'.")
