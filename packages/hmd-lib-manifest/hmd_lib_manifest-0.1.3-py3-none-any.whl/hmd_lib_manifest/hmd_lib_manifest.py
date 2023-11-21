import json
from .types import Manifest


def read_manifest() -> Manifest:
    """Read manifest.json at standard location

    Returns:
        Manifest: instance of Manifest class
    """
    with open("./meta-data/manifest.json", "r") as mf:
        return Manifest(json.load(mf))


def write_manifest(manifest: Manifest) -> None:
    """Writes Manifest to standard location

    Args:
        manifest (Manifest): Manifest instance to write out
    """
    with open("./meta-data/manifest.json", "w") as mf:
        manifest.to_json(mf)
