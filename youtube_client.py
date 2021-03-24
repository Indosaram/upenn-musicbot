#!/usr/bin/python

import httplib2
import os
import sys

from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow


class YoutubeClient:
    def _check_auth(self):
        # The CLIENT_SECRETS_FILE variable specifies the name of a file that contains
        # the OAuth 2.0 information for this application, including its client_id and
        # client_secret. You can acquire an OAuth 2.0 client ID and client secret from
        # the Google API Console at
        # https://console.developers.google.com/.
        # Please ensure that you have enabled the YouTube Data API for your project.
        # For more information about using OAuth2 to access the YouTube Data API, see:
        #   https://developers.google.com/youtube/v3/guides/authentication
        # For more information about the client_secrets.json file format, see:
        #   https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
        CLIENT_SECRETS_FILE = os.environ['client_secrets']

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
        # TODO: return response from API
        video_id = self._get_video_id(url)
        if video_id is None:
            print("잘못된 URL입니다.")
        else:
            snippet_body = {
                "snippet": {
                    "playlistId": self.playlist_id,
                    "resourceId": {"kind": "youtube#video", "videoId": video_id},
                }
            }
            pl_add_res = (
                self.youtube.playlistItems()
                .insert(part="snippet", body=snippet_body)
                .execute()
            )

            print("재생목록에 추가되었습니다!")

    def _get_video_id(self, url):
        if "?v=" in url:
            return url.split("?v=")[1]
        else:
            return None


# Unit test
if __name__ == "__main__":
    playlist_id = "PLnqRT9qVgyIDMGZeV45CFoQa_QK2iKFc6"
    video_url = "https://www.youtube.com/watch?v=RmVcOfHJWGU"
    yc = YoutubeClient(playlist_id)
    yc.add_new_item_to_playlist(video_url)
    print('Successful')