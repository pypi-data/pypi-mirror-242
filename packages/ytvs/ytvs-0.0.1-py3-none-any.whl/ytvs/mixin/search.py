import json

import requests

from ytvs.mixin.common import YOUTUBE_ENDPOINT


class SearchMixin:
    def search(self, keyword: str, with_playlist=False, limit=10, options=[]):
        youtubeEndpoint = YOUTUBE_ENDPOINT
        endpoint = f'{youtubeEndpoint}/results?search_query={keyword}'

        try:
            for option in options:
                if option == 'video':
                    endpoint = f'{endpoint}&sp=EgIQAQ%3D%3D';
                elif option == 'channel':
                    endpoint = f'{endpoint}&sp=EgIQAg%3D%3D'
                elif option == 'playlist':
                    endpoint = f'{endpoint}&sp=EgIQAw%3D%3D'
                elif option == 'movie':
                    endpoint = f'{endpoint}&sp=EgIQBA%3D%3D'

            page = self._get_youtube_init_data(endpoint)
            section_list_renderer = page["init_data"]["contents"]["twoColumnSearchResultsRenderer"]["primaryContents"][
                "sectionListRenderer"]
            cont_token = {}
            items = []

            for content in section_list_renderer["contents"]:
                if "continuationItemRenderer" in content:
                    cont_token = content["continuationItemRenderer"]["continuationEndpoint"]["continuationCommand"][
                        "token"]
                elif "itemSectionRenderer" in content:
                    for item in content["itemSectionRenderer"]["contents"]:
                        if "channelRenderer" in item:
                            channel_renderer = item["channelRenderer"]
                            items.append({
                                "id": channel_renderer["channelId"],
                                "type": "channel",
                                "thumbnail": channel_renderer["thumbnail"],
                                "title": channel_renderer["title"]["simpleText"]
                            })
                        else:
                            video_render = item.get("videoRenderer")
                            playlist_render = item.get("playlistRenderer")

                            if video_render and video_render.get("videoId"):
                                items.append(self._render_video(video_render))
                            if with_playlist:
                                if playlist_render and playlist_render.get("playlistId"):
                                    items.append({
                                        "id": playlist_render["playlistId"],
                                        "type": "playlist",
                                        "thumbnail": playlist_render["thumbnails"],
                                        "title": playlist_render["title"]["simpleText"],
                                        "length": playlist_render["videoCount"],
                                        "videos": playlist_render["videos"],
                                        "videoCount": playlist_render["videoCount"],
                                        "isLive": False
                                    })

            api_token = page.get("apiToken")
            context = page.get("context")
            next_page_context = {"context": context, "continuation": cont_token}
            items_result = items[:limit] if limit != 0 else items
            return {
                "items": items_result,
                "nextPage": {"nextPageToken": api_token, "nextPageContext": next_page_context}
            }
        except Exception as e:
            print("e: ", e)

    def next_page(self, nextPage, withPlaylist=False, limit=0):
        youtubeEndpoint = YOUTUBE_ENDPOINT
        endpoint = f"{youtubeEndpoint}/youtubei/v1/search?key={nextPage['nextPageToken']}"
        try:
            page = requests.post(endpoint, data=nextPage['nextPageContext'])
            item1 = page.json()['onResponseReceivedCommands'][0]['appendContinuationItemsAction']
            items = []

            for con_item in item1['continuationItems']:
                if 'itemSectionRenderer' in con_item:
                    for item in con_item['itemSectionRenderer']['contents']:
                        video_render = item.get('videoRenderer')
                        playlist_render = item.get('playlistRenderer')

                        if video_render and video_render.get('videoId'):
                            items.append(self._render_video(item))
                        if withPlaylist:
                            if playlist_render and playlist_render.get('playlistId'):
                                items.append({
                                    'id': playlist_render['playlistId'],
                                    'type': 'playlist',
                                    'thumbnail': playlist_render['thumbnails'],
                                    'title': playlist_render['title']['simpleText'],
                                    'length': playlist_render['videoCount'],
                                    # 'videos': await GetPlaylistData(playlist_render['playlistId'])
                                })
                elif 'continuationItemRenderer' in con_item:
                    nextPage['nextPageContext']['continuation'] = \
                        con_item['continuationItemRenderer']['continuationEndpoint']['continuationCommand']['token']

            items_result = items[:limit] if limit != 0 else items
            return {'items': items_result, 'nextPage': nextPage}
        except Exception as ex:
            print(ex)
            return None

    def _render_video(self, json_data):
        try:
            if json_data and "videoId" in json_data:
                video_renderer = json_data
                video_id = video_renderer["videoId"]
                thumbnail = video_renderer["thumbnail"]
                title = video_renderer["title"]["runs"][0]["text"]
                short_byline_text = video_renderer.get("shortBylineText", "")
                length_text = video_renderer.get("lengthText", "")
                channel_title = video_renderer.get("ownerText", {}).get("runs", [{}])[0].get("text", "")

                return {
                    "id": video_id,
                    "type": "video",
                    "thumbnail": thumbnail,
                    "title": title,
                    "channelTitle": channel_title,
                    "shortBylineText": short_byline_text,
                    "length": length_text,
                }

            if json_data and ("videoRenderer" in json_data or "playlistVideoRenderer" in json_data):
                video_renderer = None
                if "videoRenderer" in json_data:
                    video_renderer = json_data["videoRenderer"]
                elif "playlistVideoRenderer" in json_data:
                    video_renderer = json_data["playlistVideoRenderer"]

                is_live = False

                if video_renderer.get("badges") and len(video_renderer["badges"]) > 0 and \
                        video_renderer["badges"][0].get("metadataBadgeRenderer") and \
                        video_renderer["badges"][0]["metadataBadgeRenderer"]["style"] == "BADGE_STYLE_TYPE_LIVE_NOW":
                    is_live = True

                if video_renderer.get("thumbnailOverlays"):
                    for item in video_renderer["thumbnailOverlays"]:
                        if item.get("thumbnailOverlayTimeStatusRenderer") and \
                                item["thumbnailOverlayTimeStatusRenderer"].get("style") == "LIVE":
                            is_live = True

                video_id = video_renderer["videoId"]
                thumbnail = video_renderer["thumbnail"]
                title = video_renderer["title"]["runs"][0]["text"]
                short_byline_text = video_renderer.get("shortBylineText", "")
                length_text = video_renderer.get("lengthText", "")
                channel_title = video_renderer.get("ownerText", {}).get("runs", [{}])[0].get("text", "")

                return {
                    "id": video_id,
                    "type": "video",
                    "thumbnail": thumbnail,
                    "title": title,
                    "channelTitle": channel_title,
                    "shortBylineText": short_byline_text,
                    "length": length_text,
                    "isLive": is_live
                }
            else:
                return {}
        except Exception as ex:
            raise ex

    def _get_youtube_init_data(self, url):
        init_data = {}
        api_token = None
        context = None
        try:
            page = requests.get(url)
            yt_init_data = page.text.split("var ytInitialData =")
            if yt_init_data and len(yt_init_data) > 1:
                data = yt_init_data[1].split("</script>")[0].strip()[:-1]

                if "innertubeApiKey" in page.text:
                    api_token = page.text.split("innertubeApiKey")[1].strip().split(",")[0].split('"')[2]

                if "INNERTUBE_CONTEXT" in page.text:
                    context = json.loads(page.text.split("INNERTUBE_CONTEXT")[1].strip()[2:-2])

                init_data = json.loads(data)
                return {"init_data": init_data, "api_token": api_token, "context": context}
            else:
                print("cannot_get_init_data")
                return None
        except Exception as ex:
            print(ex)
            return None
