"""Sync conf.py's Sphinx version/release from the pyvolution package's setup.py.

Run by both the docs GHA workflow and Read the Docs' pre_build job, so the
built docs always reflect pyvolution/pyvolution/setup.py's version regardless
of which side is building.
"""
import re
from pathlib import Path

SETUP_PY = Path(__file__).resolve().parent.parent / "pyvolution" / "setup.py"
CONF_PY = Path(__file__).resolve().parent / "conf.py"


def main():
    setup_src = SETUP_PY.read_text()
    match = re.search(r"version\s*=\s*[\"']([^\"']+)[\"']", setup_src)
    if not match:
        raise SystemExit(f"Could not find version in {SETUP_PY}")
    version = match.group(1)

    conf_src = CONF_PY.read_text()
    conf_src = re.sub(r"version = '.*'", f"version = '{version}'", conf_src)
    conf_src = re.sub(r"release = '.*'", f"release = '{version}'", conf_src)
    CONF_PY.write_text(conf_src)
    print(f"Synced conf.py version/release to '{version}'")


if __name__ == "__main__":
    main()
