#!/usr/bin/python
import cgi
import requests

from youtube_client import YoutubeClient

if __name__ == "__main__":
    print('Status: 200')
    print("Content-type: text/plain; utf-8\r\n\r\n")

    fs = cgi.FieldStorage()
    video_url = fs["text"].value
    user_name = fs["user_name"].value
    response_url = "https://hooks.slack.com/services/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"

    playlist_id = "PLnqRT9qVgyIDvGJm32xds8BvKwhGJ0526"
    yc = YoutubeClient(playlist_id)

    code, song = yc.add_new_item_to_playlist(video_url)
    payload = {
        "channel": "#성수_신청곡_받습니다",
        "username": "MusicBot",
        "text": f"{user_name}님께서 {song}를 추가하셨습니다.",
        "icon_emoji": ":musical_note:",
    }
    requests.post(
        response_url,
        json=payload,
    )