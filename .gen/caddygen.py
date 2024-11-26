import argparse
import json
from pathlib import Path


def generate_dockerfile(input_file, output_file):
    # Load the configuration from the JSON file
    with input_file.open("r") as config_file:
        config = json.load(config_file)

    version = config["version"]
    modules = config["modules"]

    # Create the Dockerfile content
    dockerfile_content = (
        f"""FROM caddy:{version}-builder AS builder\n\nRUN xcaddy build \\\n"""
    )

    for i, module in enumerate(modules):
        if i < len(modules) - 1:
            dockerfile_content += f"\t--with {module} \\\n"
        else:
            dockerfile_content += f"\t--with {module}\n"

    dockerfile_content += f"""\nFROM caddy:{version}\n\nCOPY --from=builder /usr/bin/caddy /usr/bin/caddy\n"""

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
