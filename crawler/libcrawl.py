import asyncio
from typing import *
from bilibili_api import video
import json
import requests
import time
import json
import emoji
import random
import os


def get_video_info(bv: str) -> Dict:
    """
    input:
    - bv : string like:"BV1uv411q7Mv"

    returns:
    Dict:{
        "video_bid": str,
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

    pubdate = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(info['pubdate']))

    res['video_bid'] = info['bvid']
    res['video_aid'] = str(info['aid'])
    res['owner_uid'] = str(info['owner']['mid'])
    res['owner_name'] = info['owner']['name']
    res['video_title'] = info['title']
    res['video_partition'] = info['tname']
    res['video_tables'] = info['tname']
    res['video_pubdate'] = pubdate
    res['video_duration'] = info['duration']
    res['video_like'] = info['stat']['like']
    res['video_coin'] = info['stat']['coin']
    res['video_favorite'] = info['stat']['favorite']
    res['video_share'] = info['stat']['share']
    res['video_reply'] = info['stat']['reply']
    res['video_dislike'] = info['stat']['dislike']
    res['video_cid'] = str(info['cid'])
    return res


def fetchURL(url: str, cookie: str) -> str:
    """
    input:
    - url: str, like:'https://api.bilibili.com'

    returns:
    - html: str, json string
    """
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
        'cookie': cookie
    }
    try:
        r = requests.get(url,headers=headers)
        r.raise_for_status()
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
    commentlist: List[Any] = []

    if s is None:
        return commentlist
    
    if s['code'] != 0:
        return commentlist

    if s['data'] is None or s['data']['replies'] is None:
        return commentlist

    for i in range(len(s['data']['replies'])):
        comment = s['data']['replies'][i]
        comment_dict: Dict[str, Any] = {}

        username = comment['member']['uname']
        user_uid = comment['member']['mid']
        if 'location' in comment['reply_control'] is not None:
            ip_string = comment['reply_control']['location']
            user_ip = ip_string.replace("IP属地：", "")
        else:
            user_ip = '未知'
        # places = ['基沃托斯', '星穹铁道', '提瓦特', '交界地', '洛斯里克高墙', '罗德兰', '苇名']
        # user_ip = random.choice(places)
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


def replace_emoji(text: str) -> str:
    """
    input:
    - text: str

    returns:
    - text: str
    """
    return emoji.demojize(text)


def crawl_comment(oid: int, cookie: str) -> List:
    oid_str = str(oid)
    comments: List = []
    for page in range(1,100):
        url = 'https://api.bilibili.com/x/v2/reply?type=1&oid=' + oid_str + '&pn=' + str(page)
        html = fetchURL(url, cookie)
        commentlist = parserHtml(html)
        if len(commentlist) == 0:
            break
        comments += commentlist
    for i in range(len(comments)):
        comments[i]['comment_text'] = replace_emoji(comments[i]['comment_text'])
    return comments


def get_cookie(config_path: str) -> str:
    """
    input:
    - config_path: str

    returns:
    - cookie: str
    """
    with open(config_path, 'r') as f:
        config = json.load(f)
    cookie = config['cookie']
    return cookie


def get_default_config_file_path() -> str:
    """
    returns:
    - config_file_path: str
    """
    script_path = os.path.realpath(__file__)
    script_dir = os.path.dirname(script_path)
    config_file_path = os.path.join(script_dir, 'config.json')
    return config_file_path


def crawl_all_info_of_video(bv: str, cookie: str) -> Dict:
    """
    input:
    - bv: str

    returns:
    - final_dict: Dict
    """
    video_dict = get_video_info(bv)
    video_aid = int(video_dict['video_aid'])
    video_comments = crawl_comment(video_aid, cookie)
    video_data = {
        'video': video_dict,
        'comments': video_comments
    }
    final_dict = {
        'code': 0,
        'msg': '',
        'data': video_data
    }
    return final_dict


def remove_non_utf8mb3_chars(input_str):
    encoded_str = input_str.encode('utf-8', 'ignore')
    decoded_str = encoded_str.decode('utf-8')
    return decoded_str


if __name__ == '__main__':
    info = crawl_all_info_of_video("BV1uv411q7Mv", "")
    print(info)


# bvid="BV1uv411q7Mv"
# aid=243922477
# cid=214334689
# https://api.bilibili.com/x/v2/reply?type=1&oid=214334689&pn=1

# bvid="BV1Dw411P7iP"
# aid=278833997
# cid=1343348373
# https://api.bilibili.com/x/v2/reply?type=1&oid=278833997&pn=1

# bvid="BV1Dd4y1B7uP"

# bvid=‘BV1M94y1G7q5’

# bvid='BV1f4411M7QC'
