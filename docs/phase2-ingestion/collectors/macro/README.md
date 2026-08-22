# Shared FRED transport client

`fred_client.py` fetches one FRED observations series, validates the JSON shape,
preserves the raw response, calculates SHA-256, and writes a manifest. It does
not calculate proxies or produce variable-specific output.

The client first reads `FRED_API_KEY` from the environment. If it is not set,
it reads the local-only file `docs/phase2-ingestion/data/macro/secrets/fred_api_key`.
The environment variable takes precedence when both are present.

Create the local key file with the key on one line:

```bash
mkdir -p docs/phase2-ingestion/data/macro/secrets
printf '%s\n' 'your_fred_key' > docs/phase2-ingestion/data/macro/secrets/fred_api_key
chmod 600 docs/phase2-ingestion/data/macro/secrets/fred_api_key
```

Then run:

```bash
python fred_client.py DFII10 --start-date 2023-01-01
```

The key file is protected by a local `.gitignore` and is never written to
manifests, logs, or request metadata. Use `--api-key-file PATH` only when a
different local path is needed.

Repeated runs preserve the existing raw response when the SHA-256 is unchanged.
Use `--force` only for deliberate regression testing. Variable parsers under
`L1/` and `L4/` consume the preserved raw response and own their schemas,
validation, and transformations.
