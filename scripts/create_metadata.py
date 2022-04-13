from brownie import ErcCollectible, network
from scripts.utils import get_type
from metadata.sample_metadata import metadata_template
from metadata.sample_uri import metadata_uri_template
from pathlib import Path
import requests
import json
import os


description = {
    "BAT": "Serious batman ready to save the world",
    "BAT_GAD": "Funny Batman holding a high-tech gadget",
    "BAT_SYM": "The symbol of Batman",
}


def main():
    collectible = ErcCollectible[-1]
    n_collectibles = collectible.tokenCounter()
    print(f"Created {n_collectibles} collectibles!")

    for token_id in range(n_collectibles):
        type = get_type(collectible.tokenIdToType(token_id))
        metadata_filename = f"./metadata/{network.show_active()}/{token_id}-{type}.json"
        metadata_uri_file = f"./metadata/uri/{token_id}-{type}.json"

        collectible_metadata = metadata_template
        collectible_metadata_uri = metadata_uri_template

        if Path(metadata_filename).exists():
            print(f"{metadata_filename} already exists! Delete it to overwrite")
        elif Path(metadata_uri_file).exists():
            print(f"{metadata_uri_file} already exists! Delete it to overwrite")
        else:
            print(f"Creating {metadata_filename}")
            collectible_metadata["name"] = type
            collectible_metadata["description"] = description[type]
            image_path = "./img/" + type.lower().replace("_", "-") + ".png"
            image_uri = upload_to_ipfs(image_path)
            collectible_metadata["image"] = image_uri

            with open(metadata_filename, "w") as fw:
                json.dump(collectible_metadata, fw)

            metadata_uri = upload_to_ipfs(metadata_filename)
            collectible_metadata_uri["uri"] = metadata_uri

            with open(metadata_uri_file, "w") as f:
                json.dump(collectible_metadata_uri, f)


def upload_to_ipfs(filepath):
    with Path(filepath).open("rb") as fp:
        image_binary = fp.read()
        ipfs_url = "http://127.0.0.1:5001"
        endpoint = "/api/v0/add"
        response = requests.post(ipfs_url + endpoint, files={"file": image_binary})
        ipfs_hash = response.json()["Hash"]
        filename = filepath.split("/")[-1:][0]
        file_uri = f"ipfs://{ipfs_hash}?filename={filename}"
        print(file_uri)
    return file_uri
