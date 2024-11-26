import argparse
import json
from collections import defaultdict

from jinja2 import Environment, FileSystemLoader


def is_backend_secure(domains) -> bool:
    """Check if a backend only has HTTPS connections"""
    return all(d["protocol"].lower() == "https" for d in domains)


def generate_mermaid_diagram(config_data: dict) -> str:
    """Generate a Mermaid network diagram from the configuration."""

    # Group backends by host to avoid duplicates
    backends = defaultdict(list)
    for domain, config in config_data["domains"].items():
        host = config["host"]
        port = config.get("port", "")
        protocol = config.get("protocol", "http")
        backends[host].append({"domain": domain, "protocol": protocol, "port": port})

    # Separate secured and unsecured backends
    secured_backends = {
        backend: domains
        for backend, domains in backends.items()
        if is_backend_secure(domains)
    }
    unsecured_backends = {
        backend: domains
        for backend, domains in backends.items()
        if not is_backend_secure(domains)
    }

    # Load the Jinja template
    env = Environment(loader=FileSystemLoader("."))
    template = env.get_template("templates/mermaid.j2")

    # Render the template with the configuration
    return template.render(
        secured_backends=secured_backends, unsecured_backends=unsecured_backends
    )


def main():
    parser = argparse.ArgumentParser(
        description="Generate a Mermaid network diagram from a JSON configuration file."
    )
    parser.add_argument("input_file", help="Path to the input JSON configuration file")
    parser.add_argument("output_file", help="Path to the output Mermaid diagram file")
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

    # Generate the Mermaid diagram
    mermaid_diagram = generate_mermaid_diagram(config_data)

    # Write the diagram to a file
    try:
        with open(args.output_file, "w") as f:
            f.write(mermaid_diagram)
        print("Network diagram generated successfully!")
    except Exception as e:
        print(f"Error writing network diagram: {e}")


if __name__ == "__main__":
    main()
