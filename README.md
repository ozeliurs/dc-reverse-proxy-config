# Reverse Proxy Configuration

This project automates the generation of a Caddyfile and a Mermaid diagram for visualizing the reverse proxy configuration.

## Adding a Domain

1. Open `reverse-proxy-config/domains.json`.
2. Add a new entry under `domains`:

```json
{
  "domains": {
    "newdomain.example.com": {
      "protocol": "https",
      "host": "192.168.1.100",
      "port": 443,
      "wildcard": true
    }
  }
}
```

3. Save the file.

## Generating Configuration

The configuration files are automatically generated and updated using a GitHub Actions workflow on every push to the `main` branch.

## Mermaid Diagram

Below is the Mermaid diagram visualizing the reverse proxy configuration:

<!-- Mermaid Diagram Start -->
```mermaid
graph LR
    %% Style definitions
    classDef internet fill:#f9f,stroke:#333,stroke-width:2px;
    classDef proxy fill:#bbf,stroke:#333,stroke-width:2px;
    classDef backend fill:#bfb,stroke:#333,stroke-width:2px;
    classDef secure fill:#9f9,stroke:#333,stroke-width:2px;
    classDef unsecure fill:#ff9,stroke:#333,stroke-width:2px;

    %% Nodes
    I[Internet]
    C[Caddy Server]

    %% Apply styles
    class I internet
    class C proxy

    %% Base connections
    I -->|HTTP & HTTPS| C

    %% Backend groups
    subgraph Secured[Secured Zone]
        style Secured fill:#e6ffe6,stroke:#333,stroke-width:2px
        S0[192.168.1.134]
        class S0 secure
        S1[192.168.1.169]
        class S1 secure
        S2[192.168.1.68]
        class S2 secure
        S3[192.168.1.143]
        class S3 secure
    end

    subgraph Unsecured[Unsecured Zone]
        style Unsecured fill:#fff6e6,stroke:#333,stroke-width:2px
        U0[192.168.1.69]
        class U0 unsecure
        U1[192.168.1.126]
        class U1 unsecure
        U2[192.168.1.199]
        class U2 unsecure
    end

    C -->|HTTPS<br>adakite.ozeliurs.com| S0
    C -->|HTTP<br>jellyfin.ozeliurs.com<br>HTTP<br>wizarr.ozeliurs.com<br>HTTP<br>kavita.ozeliurs.com| U0
    C -->|HTTPS:8006<br>granite.ozeliurs.com| S1
    C -->|HTTPS:8443<br>mc.ozeliurs.com| S2
    C -->|HTTP<br>obsidian.ozeliurs.com| U1
    C -->|HTTPS<br>weakspotter.ozeliurs.com| S3
    C -->|HTTP:5601<br>kibana.main.kubernetes.ozeliurs.com<br>HTTP:9200<br>elastic.main.kubernetes.ozeliurs.com<br>HTTP:8220<br>fleet.main.kubernetes.ozeliurs.com| U2
```
<!-- Mermaid Diagram End -->

## License

This project is licensed under the MIT License.
