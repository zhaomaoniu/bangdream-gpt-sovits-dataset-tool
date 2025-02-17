"""
Script Name: list_generator.py

Description:
This script creates GPT-SoVITS dataset from the given story files and voice files.

Usage:
An example of how to use the script:
>>> python list_generator.py --cid 1 --cname 戸山香澄 --length 200

Author: zhaomaoniu
Date: 2025-02-17
Version: 0.1.0
License: MIT License
"""

import json
import random
import argparse
from pathlib import Path


EVENT_NUM = 300


def main(character_id, character_name, dataset_length):
    voice_path = Path(f"voice/{character_id}")
    if not voice_path.exists():
        print(
            f"Character {character_id}'s voices have not been downloaded yet, please run voice_downloader.py first."
        )
        return

    file_path_template = "eventstory/event{}-{}.json"

    dataset = []

    for event_id in range(1, EVENT_NUM + 1):
        for event_chapter in range(999):
            file_path = Path(
                file_path_template.format(
                    str(event_id).zfill(2), str(event_chapter).zfill(2)
                )
            )
            if not file_path.exists():
                continue

            data = json.loads(file_path.read_text(encoding="utf-8"))

            for entry in data:
                if character_id == entry["characterId"]:
                    voice_id = entry["voiceId"]
                    text = entry["Content"].replace("\n", "").replace("　", "")
                    voice_path = Path(f"voice/{character_id}/{voice_id}.mp3")
                    if not voice_path.exists():
                        continue
                    dataset.append(
                        f"{voice_path.absolute().as_posix()}|{character_name}|JA|{text}"
                    )

    random.shuffle(dataset)
    dataset = dataset[:dataset_length]

    with open(
        f"{character_id}_{character_name}_{dataset_length}.list", "w", encoding="utf-8"
    ) as f:
        for line in dataset:
            f.write(f"{line}\n")

    print(f"Generated {character_id}_{character_name}_{dataset_length}.list")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate GPT-SoVITS dataset")
    parser.add_argument(
        "--cid", type=int, required=True, help="Character ID of the character"
    )
    parser.add_argument(
        "--cname", type=str, required=True, help="Character name of the character"
    )
    parser.add_argument(
        "--length", type=int, required=True, help="Length of the dataset"
    )

    args = parser.parse_args()

    character_id = args.cid
    character_name = args.cname
    dataset_length = args.length

    main(character_id, character_name, dataset_length)
