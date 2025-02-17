"""
Script Name: voice_downloader.py

Description:
This script downloads voices from Bestdori based on the story files.

Usage:
An example of how to use the script:
>>> python voice_downloader.py --cid 1

Author: zhaomaoniu
Date: 2025-02-17
Version: 0.1.0
License: MIT License
"""

import json
import asyncio
import aiohttp
import argparse
from pathlib import Path


EVENT_NUM = 300


async def main(character_id):
    global session
    session = aiohttp.ClientSession()
    file_path_template = "eventstory/event{}-{}.json"
    tasks = []
    download_payloads = set()
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
                    download_payloads.add(
                        (event_id, event_chapter, entry["voiceId"], character_id)
                    )

    print(f"Need to download {len(download_payloads)} voices in total")

    for payload in download_payloads:
        tasks.append(download_voice(*payload))

    await asyncio.gather(*tasks)

    await session.close()


async def download_voice(event_id, event_chapter, voice_id, character_id):
    url = f"https://bestdori.com/assets/jp/sound/voice/scenario/eventstory{event_id}_{event_chapter - 1}_rip/{voice_id}.mp3"
    try:
        async with session.get(url) as response:
            if not response.ok:
                print(f"Error {response.status}: Failed to download {url}")
                return

            content = await response.content.read()
            if len(content) == 14413:
                print(f"Error: Received placeholder content from {url}")
                return

            filename = f"voice/{character_id}/{voice_id}.mp3"
            # Ensure the directory exists before writing the file.
            Path(filename).parent.mkdir(parents=True, exist_ok=True)
            with open(filename, "wb") as file:
                file.write(content)
            print(f"Downloaded {filename} from {url}")
    except Exception as e:
        print(f"Exception occurred while downloading {url}: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Voice Downloader for Bestdori")
    parser.add_argument(
        "--cid", type=int, required=True, help="Character ID to download voices for"
    )
    args = parser.parse_args()

    asyncio.run(main(args.cid))
