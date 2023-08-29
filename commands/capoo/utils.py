
import json
import os

import urllib3


BASE_VIDEO_URL = 'https://www.youtube.com/watch?v='
BASE_SEARCH_URL = 'https://www.googleapis.com/youtube/v3/search?'

def get_videos_from_channel(channel_id, max_results=100):
    api_key = os.getenv("YOUTUBE_API_KEY")

    url = BASE_SEARCH_URL + \
        'key={}&channelId={}&part=snippet,id&order=date&maxResults={}'.format(
            api_key, channel_id, max_results)

    video_links = []
    htm_content = urllib3.PoolManager().request('GET', url).data
    video_json = json.loads(htm_content)
    for video_item in video_json['items']:
      if video_item['kind'] == "youtube#searchResult":
        video_links.append(BASE_VIDEO_URL + video_item['id']['videoId'])

    return video_links
