import argparse
import json
from pathlib import Path

from jinja2 import Environment, FileSystemLoader


def generate_dockerfile(input_file, output_file):
    # Load the configuration from the JSON file
    with input_file.open("r") as config_file:
        config = json.load(config_file)

    # Load the Jinja template
    env = Environment(loader=FileSystemLoader("."))
    template = env.get_template("templates/Dockerfile.j2")

    # Render the template with the configuration
    dockerfile_content = template.render(config)

    # Write the Dockerfile content to the Dockerfile
    with output_file.open("w") as dockerfile:
        dockerfile.write(dockerfile_content)

    print("Dockerfile has been generated successfully.")


def main():
    parser = argparse.ArgumentParser(
        description="Generate a Dockerfile from a JSON configuration."
    )
    parser.add_argument(
        "input", type=Path, help="Path to the input JSON configuration file."
    )
    parser.add_argument("output", type=Path, help="Path to the output Dockerfile.")

    args = parser.parse_args()

    generate_dockerfile(args.input, args.output)


if __name__ == "__main__":
    main()
