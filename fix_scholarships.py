import json

def convert_gpa_cgpa(value):
    try:
        # Attempt to convert to float
        return float(value)
    except (ValueError, TypeError):
        # If conversion fails, return a default or handle as needed
        # For now, let's return None or a specific default if it's not a number
        return None # Or a sensible default like 0.0 or 1.0

def fix_scholarships_json(file_path):
    with open(file_path, 'r') as f:
        scholarships = json.load(f)

    for scholarship in scholarships:
        if 'gpa_requirement' in scholarship and isinstance(scholarship['gpa_requirement'], str):
            scholarship['gpa_requirement'] = convert_gpa_cgpa(scholarship['gpa_requirement'])
        if 'cgpa_requirement' in scholarship and isinstance(scholarship['cgpa_requirement'], str):
            scholarship['cgpa_requirement'] = convert_gpa_cgpa(scholarship['cgpa_requirement'])

    with open(file_path, 'w') as f:
        json.dump(scholarships, f, indent=2)

if __name__ == "__main__":
    json_file_path = "/Users/rdxhimadri/Desktop/AI SF/scholarships.json"
    fix_scholarships_json(json_file_path)
    print(f"Processed {json_file_path} to convert GPA/CGPA requirements.")