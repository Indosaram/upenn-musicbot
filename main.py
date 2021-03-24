#!/usr/bin/python
import cgi

from youtube_client import YoutubeClient

if __name__ == "__main__":

    fs = cgi.FieldStorage()
    video_url = fs["text"].value
    response_url = fs["response_url"].value

    playlist_id = "PLnqRT9qVgyIDvGJm32xds8BvKwhGJ0526"
    yc = YoutubeClient(playlist_id)

    code, response = yc.add_new_item_to_playlist(video_url)

    print(f'Status: {code}')
    print("Content-type: application/json\r\n\r\n")
    print(response)