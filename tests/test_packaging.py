import json
import re
from pathlib import Path

import common

REPO = Path(__file__).resolve().parents[1]


def load(rel):
    return json.loads((REPO / rel).read_text(encoding="utf-8"))


def test_versions_agree():
    plugin = load(".claude-plugin/plugin.json")
    market = load(".claude-plugin/marketplace.json")
    versions = {common.__version__, plugin["version"], market["metadata"]["version"], market["plugins"][0]["version"]}
    assert len(versions) == 1 and re.fullmatch(r"\d+\.\d+\.\d+", common.__version__)


def test_manifest_shape():
    plugin = load(".claude-plugin/plugin.json")
    market = load(".claude-plugin/marketplace.json")
    assert plugin["name"] == "vibe-ledger" == market["plugins"][0]["name"]
    assert market["plugins"][0]["source"] == "./"
    assert plugin["description"] and len(plugin["description"]) < 600


def test_readme_and_license_exist():
    readme = (REPO / "README.md").read_text(encoding="utf-8")
    assert "vl.py start" in readme and "MIT" in (REPO / "LICENSE").read_text(encoding="utf-8")
