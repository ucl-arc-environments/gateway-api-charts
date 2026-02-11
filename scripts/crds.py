import argparse
from pathlib import Path

import requests
import yaml
from yaml.loader import SafeLoader


def fetch_crds(url: str) -> list[dict]:
    """Fetch CRDs from the given URL.

    Args:
        url: The URL to fetch CRDs from.
    Returns:
        A list of CRD dictionaries.
    """
    response = requests.get(url)
    response.raise_for_status()
    return list(yaml.load_all(response.text, Loader=SafeLoader))


def save_all_crds_to_file(crds: dict, channel: str, filename: str) -> None:
    """Save a single CRD to a file.

    Args:
        crd: The CRD dictionary to save.
        channel: The channel name (used for file paths).
        filename: The path to the file where the CRD should be saved.
    """
    with open(filename, "w") as file:
        yaml.dump_all(crds, file, sort_keys=False)


def save_crd_to_file(crd: dict, channel: str, filename: str) -> None:
    """Save a single CRD to a file.

    Args:
        crd: The CRD dictionary to save.
        channel: The channel name (used for file paths).
        filename: The path to the file where the CRD should be saved.
    """
    with open(filename, "w") as file:
        file.write("---\n")
        yaml.dump(crd, file, sort_keys=False)


def save_crds(crds_list: list[dict], channel: str, merge: bool) -> None:
    """Save each CRD in the list to a separate file.

    Args:
        crds_list: List of CRD dictionaries to save.
        channel: The channel name (used for file paths).
        merge: Whether to merge all CRDs into a single file.
    """
    script_dir = Path(__file__).parent.parent
    charts_dir = script_dir / f"charts/{channel}-crds/crds"
    if not charts_dir.exists():
        charts_dir.mkdir(parents=True)

    if merge:
        filename = "install.yaml"
        save_all_crds_to_file(crds_list, channel, charts_dir / filename)
    else:
        for crd in crds_list:
            name = crd.get("metadata", {}).get("name").replace(".", "-")
            filename = charts_dir / f"{name}.yaml"
            print(f"Saving CRD '{name}' to file '{filename}'")

            save_crd_to_file(crd, channel, filename)

def run(url: str, channel: str, split: bool) -> None:
    """Fetch CRDs from the given URL and save them to files.

    Args:
        url: The URL to fetch CRDs from.
        channel: The channel name (used for file paths).
        split: Whether to split the YAML documents.
    """
    crds = fetch_crds(url)
    save_crds(crds, channel, merge=not split)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-c","--channel",
        choices=["experimental", "standard"],
        default="standard",
        help="Channel to fetch CRDs from (default: standard)")
    parser.add_argument(
        "-v", "--version",
        default="v1.4.1",
        help="Gateway API version to fetch CRDs for"
    )
    parser.add_argument(
        "--split",
        dest="split",
        action="store_true",
        help="Whether to split the YAML documents"
    )
    parser.add_argument(
        "--no-split",
        dest="split",
        action="store_false",
        help="Keep all CRDs in a single YAML document"
    )
    parser.set_defaults(split=False)

    args = parser.parse_args()
    version = args.version
    channel = args.channel
    split = args.split
    url = f"https://github.com/kubernetes-sigs/gateway-api/releases/download/{version}/{channel}-install.yaml"
    run(url, channel, split)
