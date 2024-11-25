import argparse
import json
from typing import Any, Dict


def generate_reverse_proxy_block(domain: str, backend: Dict[str, Any]) -> str:
    """Generate a reverse proxy block for a single domain."""

    # Extract backend details with defaults
    protocol = backend.get("protocol", "http")
    host = backend.get("host", "localhost")
    port = f":{backend.get('port', '')}" if backend.get("port") else ""
    wildcard = backend.get("wildcard", False)

    # Build the domain string (add wildcard if requested)
    domain_str = f"{domain}, *.{domain}" if wildcard else domain

    # Determine if we need TLS skip verify
    needs_tls_skip = protocol == "https"

    # Build the reverse proxy configuration
    config = [
        f"{domain_str} {{",
        f"    reverse_proxy {protocol}://{host}{port} {{",
        "        header_up Host {host}",
        "        header_up X-Real-IP {remote}",
        "        header_up X-Forwarded-For {remote}",
        "        header_up X-Forwarded-Proto {scheme}",
    ]

    # Add TLS skip verify if needed
    if needs_tls_skip:
        config.extend(
            [
                "        transport http {",
                "            tls_insecure_skip_verify",
                "        }",
            ]
        )

    config.extend(["    }", "}"])

    return "\n".join(config)


def generate_caddy_config(config_data: Dict) -> str:
    """Generate the complete Caddy configuration."""

    # Start with the global configuration
    config_blocks = [
        "{",
        "    log {",
        "        output file /var/log/caddy/access.log",
        "        format json",
        "    }",
        "}",
        "",  # Empty line for separation
    ]

    # Generate blocks for each domain
    for domain, backend in config_data.get("domains", {}).items():
        config_blocks.append(generate_reverse_proxy_block(domain, backend))
        config_blocks.append("")  # Empty line between blocks

    return "\n".join(config_blocks)


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
