import argparse
import json
from collections import defaultdict


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

    # Start building the diagram
    diagram = [
        "```mermaid",
        "graph LR",
        "    %% Style definitions",
        "    classDef internet fill:#f9f,stroke:#333,stroke-width:2px;",
        "    classDef proxy fill:#bbf,stroke:#333,stroke-width:2px;",
        "    classDef backend fill:#bfb,stroke:#333,stroke-width:2px;",
        "    classDef secure fill:#9f9,stroke:#333,stroke-width:2px;",
        "    classDef unsecure fill:#ff9,stroke:#333,stroke-width:2px;",
        "",
        "    %% Nodes",
        "    I[Internet]",
        "    C[Caddy Server]",
        "",
        "    %% Apply styles",
        "    class I internet",
        "    class C proxy",
        "",
        "    %% Base connections",
        "    I -->|HTTP & HTTPS| C",
        "",
        "    %% Backend groups",
        "    subgraph Secured[Secured Zone]",
        "        style Secured fill:#e6ffe6,stroke:#333,stroke-width:2px",
    ]

    # Add secured backends
    secure_count = 0
    unsecure_count = 0

    # First pass for secured backends
    for backend, domains in backends.items():
        if is_backend_secure(domains):
            backend_id = f"S{secure_count}"
            diagram.append(f"        {backend_id}[{backend}]")
            diagram.append(f"        class {backend_id} secure")
            secure_count += 1

    diagram.extend(
        [
            "    end",
            "",
            "    subgraph Unsecured[Unsecured Zone]",
            "        style Unsecured fill:#fff6e6,stroke:#333,stroke-width:2px",
        ]
    )

    # Second pass for unsecured backends
    for backend, domains in backends.items():
        if not is_backend_secure(domains):
            backend_id = f"U{unsecure_count}"
            diagram.append(f"        {backend_id}[{backend}]")
            diagram.append(f"        class {backend_id} unsecure")
            unsecure_count += 1

    diagram.append("    end")
    diagram.append("")

    # Add connections
    secure_count = 0
    unsecure_count = 0

    for backend, domains in backends.items():
        backend_id = (
            f"S{secure_count}" if is_backend_secure(domains) else f"U{unsecure_count}"
        )

        # Create connection with domain names as labels
        domain_connections = [
            f"{domain_info['protocol'].upper()}{':' + str(domain_info['port']) if domain_info['port'] else ''}<br>{domain_info['domain']}"
            for domain_info in domains
        ]

        domain_labels = "<br>".join(domain_connections)
        diagram.append(f"    C -->|{domain_labels}| {backend_id}")

        if is_backend_secure(domains):
            secure_count += 1
        else:
            unsecure_count += 1

    diagram.append("```\n")

    return "\n".join(diagram)


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
