#!/usr/bin/python
import os
import requests

from youtube_client import YoutubeClient
from cgi_manager import CGIManager


if __name__ == "__main__":
    cm = CGIManager()

    yc = YoutubeClient(os.environ.get('playlist_id'))

    code, song = yc.delete_new_item_from_playlist(cm.video_url)

    user_name = cm.get_username_by_id(cm.user_id)

    payload = {
        "channel": "#성수_신청곡_받습니다",
        "username": "MusicBot",
        "text": f"{user_name}님께서 {song}를 삭제하셨습니다.",
        "icon_emoji": ":musical_note:",
    }
    requests.post(
        os.environ.get('webhook_url'),
        json=payload,
    )

    print("몰래 지울 순 없답니다.")