import asyncio
from typing import *
from bilibili_api import video
import json
import requests
import time


def get_video_info(bv: str) -> Dict:
    """
    input:
    - bv : string like:"BV1uv411q7Mv"

    returns:
    Dict:{
        "video_bvid": str,
        "video_aid": int,
        "owner_uid": int,
        "owner_name": str,
        "video_title": str,
        "video_partition": str,
        "video_tables": str,
        "video_pubdate": int,
        "video_duration": int,
        "video_like": int,
        "video_coin": int,
        "video_favorite": int,
        "video_share": int,
        "video_reply": int,
        "video_dislike": int,
        "video_cid": int
    }
    """
    v = video.Video(bvid=bv)
    res: Dict = {}

    async def async_get_video_info(v: video.Video) -> Dict:
        info = await v.get_info()
        return info

    info = asyncio.run(async_get_video_info(v))
    res['video_bvid'] = info['bvid']
    res['video_aid'] = info['aid']
    res['owner_uid'] = info['owner']['mid']
    res['owner_name'] = info['owner']['name']
    res['video_title'] = info['title']
    res['video_partition'] = info['tname']
    res['video_tables'] = info['tname']
    res['video_pubdate'] = info['pubdate']
    res['video_duration'] = info['duration']
    res['video_like'] = info['stat']['like']
    res['video_coin'] = info['stat']['coin']
    res['video_favorite'] = info['stat']['favorite']
    res['video_share'] = info['stat']['share']
    res['video_reply'] = info['stat']['reply']
    res['video_dislike'] = info['stat']['dislike']
    res['video_cid'] = info['cid']
    return res


def fetchURL(url) -> str:
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
    }
    try:
        r = requests.get(url,headers=headers)
        r.raise_for_status()
        print(r.url)
        return r.text
    except requests.HTTPError as e:
        print(e)
        print("HTTPError")
    except requests.RequestException as e:
        print(e)
    except:
        print("Unknown Error !")


def parserHtml(html) -> List:
    try:
        s = json.loads(html)
    except:
        print('error')
    commentlist = []

    for i in range(len(s['data']['replies'])):
        comment = s['data']['replies'][i]
        comment_dict = {}

        username = comment['member']['uname']
        user_uid = '未知'
        user_ip = '未知'
        sex = comment['member']['sex']
        ctime = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(comment['ctime']))
        content = comment['content']['message']
        likes = comment['like']
        rcounts = comment['rcount']

        comment_dict['user_uid'] = user_uid
        comment_dict['user_name'] = username
        comment_dict['user_ip'] = user_ip
        comment_dict['user_sex'] = sex
        comment_dict['comment_date'] = ctime
        comment_dict['comment_text'] = content
        comment_dict['comment_like'] = likes
        comment_dict['comment_reply'] = rcounts

        commentlist.append(comment_dict)

    return commentlist


def crawl_comment(oid: int) -> List:
    oid_str = str(oid)
    comments: List = []
    for page in range(0,10):
        url = 'https://api.bilibili.com/x/v2/reply?type=1&oid=' + oid_str + '&pn=' + str(page)
        html = fetchURL(url)
        commentlist = parserHtml(html)
        comments += commentlist

    return comments


if __name__ == '__main__':
    info = get_video_info("BV1uv411q7Mv")
    print(info)

# bvid="BV1uv411q7Mv"
# aid=243922477
# cid=214334689