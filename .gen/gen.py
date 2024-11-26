import argparse
import json

from jinja2 import Environment, FileSystemLoader


def generate_caddy_config(config_data):
    # Load the Jinja template
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template('Caddyfile.j2')

    # Render the template with the configuration
    return template.render(config_data)

def main():
    parser = argparse.ArgumentParser(
        description="Generate Caddy configuration from JSON file."
    )
    parser.add_argument("input_file", help="Path to the input JSON file")
    parser.add_argument("output_file", help="Path to the output Caddyfile")
    args = parser.parse_args()

    # Read the JSON configuration file
    try:
        with open(args.input_file, "r") as f:
            config_data = json.load(f)
    except FileNotFoundError:
        print(f"Error: {args.input_file} file not found")
        return
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in {args.input_file}")
        return

    # Generate the Caddy configuration
    caddy_config = generate_caddy_config(config_data)

    # Write the configuration to a file
    try:
        with open(args.output_file, "w") as f:
            f.write(caddy_config)
        print(f"Caddyfile generated successfully at {args.output_file}!")
    except Exception as e:
        print(f"Error writing Caddyfile: {e}")

if __name__ == "__main__":
    main()
