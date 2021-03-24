#!/usr/bin/python
import cgi
import json
import requests

from youtube_client import YoutubeClient

if __name__ == "__main__":
    print('Status: 200')
    print("Content-type: application/json; utf-8\r\n\r\n")

    fs = cgi.FieldStorage()
    video_url = fs["text"].value
    response_url = fs["response_url"].value

    playlist_id = "PLnqRT9qVgyIDvGJm32xds8BvKwhGJ0526"
    yc = YoutubeClient(playlist_id)

    code, text = yc.add_new_item_to_playlist(video_url)
    response = {
        "blocks": [
            {
                "type": "section",
                "response_type": "in_channel",
                "text": {
                    "type": "mrkdwn",
                    "text": text,
                },
            },
        ]
    }
    requests.post(
        response_url,
        data=json.dumps(response),
        headers={"Content-Type": "application/json"},
    )

    print(response)