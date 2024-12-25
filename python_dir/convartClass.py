import json
import yaml



def convert(format_type: str, data: str)-> str:
    try:
        if format_type.lower() == "json":
            # Convert JSON string to YAML
            json_data = json.loads(data)
            yaml_data = yaml.dump(json_data, allow_unicode=True, default_flow_style=False)
            return yaml_data

        elif format_type.lower() == "yaml":
            # Convert YAML string to JSON
            yaml_data = yaml.safe_load(data)
            json_data = json.dumps(yaml_data, ensure_ascii=False, indent=4)
            return json_data

        else:
            raise ValueError("Invalid format type. Use 'json' or 'yaml'.")

    except Exception as e:
        return f"Error during conversion: {e}"