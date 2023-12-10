import asyncio
from typing import *
from bilibili_api import video
import bilibili_api
import json
import requests
import time
import json
import emoji
import random
import os
import utils
from utils import log


def get_video_info(bv: str) -> Dict:
    """
    Crawl video info from bilibili_api, and return a dict.

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

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    info = loop.run_until_complete(async_get_video_info(v))

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
    Get html from url.

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
    except:
        return ''


def parserHtml(html) -> List:
    """
    Parse html and return a list of comments.

    input:
    - html: str, json string

    returns:
    - commentlist: List

        comment = {
            'user_uid',
            'user_name',
            'user_ip',
            'user_sex',
            'comment_date',
            'comment_text',
            'comment_like',
            'comment_reply'
        }
    """
    try:
        s = json.loads(html)
    except:
        log('parserHtml failed: json.loads(html) failed, html: ' + html)
        return []
    commentlist: List[Any] = []

    if s is None:
        log('parserHtml failed: s is None')
        return commentlist
    
    if s['code'] != 0:
        log('parserHtml failed: s[code] != 0')
        return commentlist

    if s['data'] is None or s['data']['replies'] is None:
        log('parserHtml failed: s[data] is None or s[data][replies] is None')
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


def crawl_comment(oid: int, cookie: str) -> List:
    """
    Get comments from a video.

    input:
    - oid: int, video_aid
    - cookie: str

    returns:
    - comments: List

        comment = {
            'user_uid',
            'user_name',
            'user_ip',
            'user_sex',
            'comment_date',
            'comment_text',
            'comment_like',
            'comment_reply'
        }
    """
    log('crawl_comment. video oid: ' + str(oid))
    oid_str = str(oid)
    comments: List = []
    for page in range(1,100):
        url = 'https://api.bilibili.com/x/v2/reply?type=1&oid=' + oid_str + '&pn=' + str(page)
        html = fetchURL(url, cookie)
        try:
            commentlist = parserHtml(html)
            if len(commentlist) == 0:
                break
        except:
            commentlist = []
        comments += commentlist
    for i in range(len(comments)):
        comments[i]['comment_text'] = utils.replace_emoji(comments[i]['comment_text'])
        comments[i]['comment_text'] = utils.remove_non_utf8mb3_chars(comments[i]['comment_text'])
    return comments


def crawl_all_info_of_video(bv: str, cookie: str) -> Dict:
    """
    Crawl all info of a video, including video info and comments.

    input:
    - bv: str

    returns:
    - final_dict: Dict
    """
    log('crawl_all_info_of_video: ' + bv)
    try:
        video_dict = get_video_info(bv)
    except Exception as e:
        log('crawl failed, exception occured while calling get_video_info(), exception: ' + str(e))
        final_dict = {
            'code': 1,
            'msg': 'An error occurred while crawling the video.',
            'data': None
        }
        return final_dict
    log('crawl video basic info successful')
    video_aid = int(video_dict['video_aid'])
    video_comments = crawl_comment(video_aid, cookie)
    log('crawl video comments successful, total comments num:' + str(len(video_comments)))
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


def crawl_popular_bv_list(page_lower_bound: int, page_upper_bound: int) -> List:
    """
    Crawl popular bv list from page_lower_bound to page_upper_bound.

    input:
    - page_lower_bound: int
    - page_upper_bound: int
        page_bound: for i in range(page_lower_bound, page_upper_bound)

    returns:
    - bvidList: List
    """
    POPULAR_URL = "https://api.bilibili.com/x/web-interface/popular"
    HEADERS = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'referer': 'https://www.bilibili.com/',
        'x-csrf-token': '',
        'x-requested-with': 'XMLHttpRequest',
        'cookie': ''
        ,
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'
    }
    bvidList = []
    for i in range(page_lower_bound, page_upper_bound):
        query = "pn=" + str(i)
        r = requests.get(POPULAR_URL, headers=HEADERS, params=query)
        resultList = r.json()['data']['list']
        for item in resultList:
            bvidList.append(
                bilibili_api.aid2bvid(
                    item['aid']
                )
            )
    return bvidList


def get_comment_text_list(bv: str, cookie: str='') -> list:
    """
    Get comment text list from a video.

    input:
    - bv: str
    - cookie: str

    returns:
    - comment_text_list: list

        comment_text: str
    """
    log('get_comment_text_list: ' + bv)
    result_dict = crawl_all_info_of_video(bv, cookie)
    if result_dict['code'] != 0:
        return []
    result_dict = result_dict['data']
    comments = result_dict['comments']
    comment_text_list = []
    for comment in comments:
        comment_text = comment['comment_text']
        comment_text_list.append(comment_text)
    return comment_text_list


def get_result_json_string(bv: str, cookie: str='', pure: bool=False) -> str:
    """
    Get crawl result json string, support both standard and pure mode.

    input:
    - bv: str
    - cookie: str
    - pure: bool

    returns:
    - result_json_string: str
    """
    log('get_result_json_string: ' + bv)
    result_dict = crawl_all_info_of_video(bv, cookie)
    if pure:
        result_dict = result_dict['data']
    result_json_string = json.dumps(result_dict)
    return result_json_string


def get_error_json_string() -> str:
    """
    Get error json string.

    returns:
    - result_json_string: str
    """
    log('get_error_json_string')
    result_dict = {
        "code": 1,
        'msg': 'An error occurred while crawling the video.',
        'data': None
    }
    result_json_string = json.dumps(result_dict)
    return result_json_string


if __name__ == '__main__':
    info = crawl_all_info_of_video("BV1p14y1P73X", "")
    print(info)
