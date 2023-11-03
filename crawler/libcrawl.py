import asyncio
from typing import *
from bilibili_api import video
import json
import requests
import time
import json


def get_video_info(bv: str) -> Dict:
    """
    input:
    - bv : string like:"BV1uv411q7Mv"

    returns:
    Dict:{
        "video_bvid": str,
        "video_aid": str,
        "owner_uid": str,
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
        "video_cid": str
    }
    """
    v = video.Video(bvid=bv)
    res: Dict = {}

    async def async_get_video_info(v: video.Video) -> Dict:
        info = await v.get_info()
        return info

    info = asyncio.run(async_get_video_info(v))
    res['video_bvid'] = info['bvid']
    res['video_aid'] = str(info['aid'])
    res['owner_uid'] = str(info['owner']['mid'])
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
    res['video_cid'] = str(info['cid'])
    return res


def fetchURL(url: str) -> str:
    """
    input:
    - url: str, like:'https://api.bilibili.com'

    returns:
    Dict:{
        "video_bvid": str,
        "video_aid": str,
        "owner_uid": str,
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
        "video_cid": str
    }
    """
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
    except requests.RequestException as e:
        print(e)
    except:
        print("Unknown Error !")
    return ''


def parserHtml(html) -> List:
    s = json.loads(html)
    commentlist = []

    for i in range(len(s['data']['replies'])):
        comment = s['data']['replies'][i]
        comment_dict: Dict[str, Any] = {}

        username = comment['member']['uname']
        user_uid = '未知'
        user_ip = '未知'
        sex = comment['member']['sex']
        ctime = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(comment['ctime']))
        content = comment['content']['message']
        likes = comment['like']
        rcounts = comment['rcount']

        comment_dict['user_uid'] = str(user_uid)
        comment_dict['user_name'] = str(username)
        comment_dict['user_ip'] = str(user_ip)
        comment_dict['user_sex'] = str(sex)
        comment_dict['comment_date'] = str(ctime)
        comment_dict['comment_text'] = str(content)
        comment_dict['comment_like'] = int(likes)
        comment_dict['comment_reply'] = int(rcounts)

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


def crawl_all_info_of_video(bv: str) -> Dict:
    video_dict = get_video_info(bv)
    video_cid = int(video_dict['cid'])
    video_aid = int(video_dict['aid'])
    video_comments = crawl_comment(video_cid)
    return video_dict


if __name__ == '__main__':
    info = get_video_info("BV1uv411q7Mv")
    print(info)

# bvid="BV1uv411q7Mv"
# aid=243922477
# cid=214334689