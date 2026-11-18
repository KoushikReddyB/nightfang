#!/usr/bin/env python3
"""Ingest PayloadsAllTheThings into a structured catalog for nightfang.

Creates references/payloads/index.json mapping:
vuln_class -> {
    cwe: str,
    owasp: str,
    safe_default: bool,
    payload_files: [rel_path_to_ref_repo]
}
"""
import os, json

PAYLOADS = "D:/Playground4Hermes/refs/payloadsallthethings"
OUT = "D:/Playground4Hermes/nightfang/references/payloads"

# Mapping to help agents map payloads to standards
# This is a baseline; agents should refine this via CTI/GRC workflows.
VULN_MAP = {
    "SQL Injection": {"cwe": "CWE-89", "owasp": "A03:2021", "safe": False},
    "Server Side Template Injection": {"cwe": "CWE-94", "owasp": "A03:2021", "safe": False},
    "Server Side Request Forgery": {"cwe": "CWE-918", "owasp": "A10:2021", "safe": False},
    "XSS Injection": {"cwe": "CWE-79", "owasp": "A03:2021", "safe": True},
    "Command Injection": {"cwe": "CWE-77", "owasp": "A03:2021", "safe": False},
    "File Inclusion": {"cwe": "CWE-22", "owasp": "A01:2021", "safe": False},
    "Directory Traversal": {"cwe": "CWE-22", "owasp": "A01:2021", "safe": True},
}

def main():
    os.makedirs(OUT, exist_ok=True)
    catalog = {}

    for entry in sorted(os.listdir(PAYLOADS)):
        if entry.startswith(("_", ".")):
            continue
        
        path = os.path.join(PAYLOADS, entry)
        if not os.path.isdir(path):
            continue

        meta = VULN_MAP.get(entry, {"cwe": "N/A", "owasp": "N/A", "safe": False})
        
        # Discover md/txt/payload files
        files = []
        for root, _, fs in os.walk(path):
            for f in fs:
                if f.endswith((".md", ".txt", ".js", ".py", ".sh")):
                    rel = os.path.relpath(os.path.join(root, f), PAYLOADS)
                    files.append(rel)
        
        catalog[entry] = {
            "cwe": meta["cwe"],
            "owasp": meta["owasp"],
            "safe_default": meta["safe"],
            "payload_files": files
        }

    with open(os.path.join(OUT, "index.json"), "w", encoding="utf-8") as f:
        json.dump(catalog, f, indent=2)
    print(f"Payload catalog written: {len(catalog)} classes")

if __name__ == "__main__":
    main()