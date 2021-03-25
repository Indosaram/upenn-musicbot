#!/usr/bin/python

import httplib2
import os
import sys
import json
import re
import requests

from apiclient.discovery import build
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow


class YoutubeClient:
    def _check_auth(self):
        with open("client_secrets.json", "w") as f:
            json.dump(json.loads(os.environ.get('client_secrets')), f)
        CLIENT_SECRETS_FILE = "client_secrets.json"

        # This variable defines a message to display if the CLIENT_SECRETS_FILE is
        # missing.
        MISSING_CLIENT_SECRETS_MESSAGE = """
        WARNING: Please configure OAuth 2.0

        To make this sample run you will need to populate the client_secrets.json file
        found at:

        %s

        with information from the API Console
        https://console.developers.google.com/

        For more information about the client_secrets.json file format, please visit:
        https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
        """ % os.path.abspath(
            os.path.join(os.path.dirname(__file__), CLIENT_SECRETS_FILE)
        )

        flow = flow_from_clientsecrets(
            CLIENT_SECRETS_FILE,
            message=MISSING_CLIENT_SECRETS_MESSAGE,
            scope=self.YOUTUBE_READ_WRITE_SCOPE,
        )

        storage = Storage("%s-oauth2.json" % sys.argv[0])
        self.credentials = storage.get()

        if self.credentials is None or self.credentials.invalid:
            flags = argparser.parse_args()
            self.credentials = run_flow(flow, storage, flags)

    def __init__(self, playlist_id) -> None:
        # This OAuth 2.0 access scope allows for full read/write access to the
        # authenticated user's account.
        self.YOUTUBE_READ_WRITE_SCOPE = (
            "https://www.googleapis.com/auth/youtube"
        )
        self.YOUTUBE_API_SERVICE_NAME = "youtube"
        self.YOUTUBE_API_VERSION = "v3"
        self.credentials = None
        self.playlist_id = playlist_id

        self._check_auth()
        self._init_youtube_client()

    def _init_youtube_client(self):
        self.youtube = build(
            self.YOUTUBE_API_SERVICE_NAME,
            self.YOUTUBE_API_VERSION,
            http=self.credentials.authorize(httplib2.Http()),
        )

    def create_new_playlist(self):
        # This code creates a new, private playlist in the authorized user's channel.
        playlists_insert_response = (
            self.youtube.playlists()
            .insert(
                part="snippet,status",
                body=dict(
                    snippet=dict(
                        title="Test Playlist",
                        description="A private playlist created with the YouTube API v3",
                    ),
                    status=dict(privacyStatus="private"),
                ),
            )
            .execute()
        )

        print("New playlist id: %s" % playlists_insert_response["id"])

    def add_new_item_to_playlist(self, url):
        video_id = self._get_video_id(url)
        if video_id is None:
            response = "잘못된 URL입니다."
            code = "404"

        else:
            snippet_body = {
                "snippet": {
                    "playlistId": self.playlist_id,
                    "resourceId": {
                        "kind": "youtube#video",
                        "videoId": video_id,
                    },
                }
            }
            try:
                pl_add_res = (
                    self.youtube.playlistItems()
                    .insert(part="snippet", body=snippet_body)
                    .execute()
                )

                response = self._get_video_title(video_id)
                code = "200 OK"
            except Exception as e:
                code = "404"
                response = f"{e}"
        return code, response

    def delete_new_item_from_playlist(self, url):
        # TODO: parse error code
        playlist_items = self._get_playlist_items()
        video_id = self._get_video_id(url)
        title = self._get_video_title(video_id)
        video_id_in_playlist = playlist_items[title]
        pl_del_res = self.youtube.playlistItems().delete(video_id_in_playlist)

    def _get_playlist_items(self):
        req = self.youtube.playlistItems().list(
            playlistId=self.playlist_id, part="snippet"
        )
        playlist_items = {}
        while req:
            res = req.execute()

            # Print information about each video.
            for playlist_item in res["items"]:
                title = playlist_item["snippet"]["title"]
                video_id = playlist_item["snippet"]["resourceId"]["videoId"]
                playlist_items[title] = video_id

            req = self.youtube.playlistItems().list_next(req, res)

        return playlist_items

    def _get_video_id(self, url):
        if "?v=" in url:
            return url.split("?v=")[1]
        else:
            return None

    def _get_video_title(self, id):
        search_response = (
            self.youtube.search()
            .list(q=id, part="id,snippet", maxResults=1)
            .execute()
        )

        title = search_response['items'][0]['snippet']['title']

        return title
