import json

def save_to_file(data, filename):
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)
