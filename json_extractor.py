import json
import sys
from collections import defaultdict
import logging

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

def extract_relational_data(data):
    tables = defaultdict(list)

    def process_object(obj, table_name, parent_table=None, parent_id=None):
        if not isinstance(obj, dict):
            logger.warning(f"Skipping non-object data in {table_name}")
            return None

        if 'id' not in obj:
            logger.warning(f"ID not found for an object in {table_name}. Skipping this object.")
            return None

        row = {"id": obj['id']}
        if parent_table and parent_id:
            row[f"{parent_table}_id"] = parent_id

        for key, value in obj.items():
            if key == 'id':
                continue
            if isinstance(value, (str, int, float, bool)) or value is None:
                row[key] = value
            elif isinstance(value, dict):
                subtable_name = key
                sub_id = process_object(value, subtable_name, table_name, obj['id'])
                if sub_id:
                    row[f"{subtable_name}_id"] = sub_id
            elif isinstance(value, list):
                subtable_name = key
                for item in value:
                    if isinstance(item, dict):
                        process_object(item, subtable_name, table_name, obj['id'])
                    else:
                        # Handle primitive lists
                        list_table_name = f"{table_name}_{key}"
                        list_row = {
                            f"{table_name}_id": obj['id'],
                            "value": item
                        }
                        if isinstance(item, dict) and 'id' in item:
                            list_row['id'] = item['id']
                        tables[list_table_name].append(list_row)

        tables[table_name].append(row)
        return obj['id']

    # Handle the root object
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, dict):
                process_object(value, key)
            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, dict):
                        process_object(item, key)
    elif isinstance(data, list):
        for item in data:
            if isinstance(item, dict):
                process_object(item, "main")

    return tables

def main():
    # if len(sys.argv) != 2:
    #     print("Usage: python script.py <input_json_file>")
    #     sys.exit(1)

    # input_file = sys.argv[1]
    input_file = "sample_data.json"
    try:
        with open(input_file, 'r') as file:
            input_data = json.load(file)
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in file '{input_file}'.")
        sys.exit(1)

    # Extract relational data
    relational_data = extract_relational_data(input_data)

    # Print the resulting JSON structures
    for table_name, table_data in relational_data.items():
        print(f"\n{table_name.upper()}:")
        print(json.dumps(table_data, indent=2))

if __name__ == "__main__":
    main()