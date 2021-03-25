#!/usr/bin/python
import os
import requests

from youtube_client import YoutubeClient
from cgi_manager import CGIManager


if __name__ == "__main__":
    cm = CGIManager()

    yc = YoutubeClient(os.environ.get('playlist_id'))

    code, song = yc.add_new_item_to_playlist(cm.video_url)

    user_name = cm.get_username_by_id()

    payload = {
        "channel": "#성수_신청곡_받습니다",
        "username": "MusicBot",
        "text": f"{user_name}님께서 {song}를 추가하셨습니다.",
        "icon_emoji": ":musical_note:",
    }
    requests.post(
        os.environ.get('webhook_url'),
        json=payload,
    )

    print("새로운 노래가 추가됐어요😁️")