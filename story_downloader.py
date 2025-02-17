"""
Script Name: story_downloader.py

Description:
This script downloads stories from Bestdori and restrucures them into a more readable format.

Usage:
An example of how to use the script:
>>> python story_downloader.py

Author: zhaomaoniu
Date: 2025-02-17
Version: 0.1.0
License: MIT License
"""

import json
import asyncio
import aiohttp
from pathlib import Path


EVENT_NUM = 300
BAND_EVENTS = [235]


class EventStoryDownload:
    def __init__(self):
        self.session = None

    async def fetch_data(self, url):
        try:
            async with self.session.get(url) as response:
                response.raise_for_status()
                return json.loads(await response.text())
        except Exception as e:
            print(f"Failed to fetch data from {url}: {e}")

    async def get_chapter_num(self, event_id) -> int:
        data = await self.fetch_data(f"https://bestdori.com/api/events/{event_id}.json")
        return len(data["stories"]) + 1 if data is not None else 0

    def simplify(self, data):
        simplified_data = []
        talk_datas = data["Base"]["talkData"]
        for talk_data in talk_datas:
            for voice_data in talk_data["voices"]:
                voice_id = voice_data["voiceId"]
                character_id = voice_data["characterId"]
                voice_content = talk_data["body"]
                simplified_data.append(
                    {
                        "voiceId": voice_id,
                        "characterId": character_id,
                        "Content": voice_content,
                    }
                )
        return simplified_data

    async def download(self, event_id):
        chapter_range = range(await self.get_chapter_num(event_id))
        for event_chapter in chapter_range:
            if event_id not in BAND_EVENTS:
                url = f"https://bestdori.com/assets/jp/scenario/eventstory/event{event_id}_rip/Scenarioevent{str(event_id).zfill(2)}-{str(event_chapter).zfill(2)}.asset"
            else:
                # 此处仍不完善
                url = f"https://bestdori.com/assets/jp/scenario/eventstory/event{event_id}_rip/Scenarioband8-{str(event_chapter).zfill(3)}.asset"

            filename = (
                Path("eventstory")
                / f"event{str(event_id).zfill(2)}-{str(event_chapter).zfill(2)}.json"
            )

            if filename.exists():
                print(f"File {filename} already exists")
                return

            if content := await self.fetch_data(url):
                simplified_content = self.simplify(content)
                filename.write_text(
                    json.dumps(simplified_content, indent=4, ensure_ascii=False),
                    encoding="utf-8",
                )
                print(f"Downloaded {filename}")

    async def run(self):
        Path("eventstory").mkdir(exist_ok=True)
        self.session = aiohttp.ClientSession()
        tasks = [self.download(event_id) for event_id in range(1, EVENT_NUM + 1)]
        await asyncio.gather(*tasks)
        await self.session.close()


if __name__ == "__main__":
    event_story = EventStoryDownload()
    asyncio.run(event_story.run())
    print("Finished downloading event stories")
