import json
import os

# Function to calculate average if both values are valid
def calculate_combined(val1, val2):
    if isinstance(val1, (int, float)) and isinstance(val2, (int, float)):
        return round((val1 + val2) / 2, 4)
    try:
        val1 = float(val1)
        val2 = float(val2)
        return round((val1 + val2) / 2, 4)
    except:
        return "N/A"

# Desired key order
desired_order = [
    "albumTitle",
    "circleName",
    "albumPhoto",
    "dateCompleted",
    "subjectiveJordan",
    "subjectiveNick",
    "objectiveJordan",
    "objectiveNick",
    "subjectiveCombined",
    "objectiveCombined",
    "songAmount",
    "ratings"
]

# Function to reorder dictionary keys
def reorder_json_keys(data):
    return {key: data.get(key) for key in desired_order if key in data or key in ["subjectiveCombined", "objectiveCombined"]}

# Process all JSON files in the current directory
for filename in os.listdir():
    if filename.endswith(".json") and not filename.startswith("all_albums"):
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Calculate combined values
        subjectiveCombined = calculate_combined(data.get("subjectiveJordan"), data.get("subjectiveNick"))
        objectiveCombined = calculate_combined(data.get("objectiveJordan"), data.get("objectiveNick"))

        # Add to data
        data["subjectiveCombined"] = subjectiveCombined
        data["objectiveCombined"] = objectiveCombined

        # Reorder keys
        reordered_data = reorder_json_keys(data)

        # Overwrite the original file
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(reordered_data, f, indent=4)

print("All applicable JSON files have been updated with combined scores and reordered keys.")

# Function to convert string to float if possible
def convert_to_float(value):
    try:
        return float(value)
    except (ValueError, TypeError):
        return value  # Leave unchanged if not convertible

# Process all JSON files in the current directory
for filename in os.listdir():
    if filename.endswith(".json") and not filename.startswith("all_albums"):
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Convert objective ratings to float if they are strings
        if "objectiveJordan" in data:
            data["objectiveJordan"] = convert_to_float(data["objectiveJordan"])
        if "objectiveNick" in data:
            data["objectiveNick"] = convert_to_float(data["objectiveNick"])

        # Overwrite the original file with updated content
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

print("Objective ratings have been converted to floats in all applicable JSON files.")
