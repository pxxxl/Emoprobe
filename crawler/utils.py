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
import libcrawl


logging = True


def replace_emoji(text: str) -> str:
    """
    Replace emoji in text.

    input:
    - text: str

    returns:
    - text: str
    """
    return emoji.demojize(text)


def remove_non_utf8mb3_chars(input_str):
    """
    Remove non-UTF-8-MB3 chars in input_str.
    
    input:
    - input_str: str

    returns:
    - decoded_str: str
    """
    encoded_str = input_str.encode('utf-8', 'ignore')
    decoded_str = encoded_str.decode('utf-8')
    return decoded_str


def get_cookie(config_path: str) -> str:
    """
    Read cookie from config file.

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
    Get default config file path.

    returns:
    - config_file_path: str
    """
    script_path = os.path.realpath(__file__)
    script_dir = os.path.dirname(script_path)
    config_file_path = os.path.join(script_dir, 'config.json')
    return config_file_path


def get_default_log_file_path() -> str:
    """
    Get default log file path.

    returns:
    - log_file_path: str
    """
    script_path = os.path.realpath(__file__)
    script_dir = os.path.dirname(script_path)
    cache_folder_path = os.path.join(script_dir, 'cache')
    if not os.path.exists(cache_folder_path):
        os.mkdir(cache_folder_path)
    log_file_path = os.path.join(cache_folder_path, 'log.txt')
    if not os.path.exists(log_file_path):
        with open(log_file_path, 'w') as f:
            f.write('')
    return log_file_path


def log(log_str: str, log_file_path: Any=None) -> None:
    """
    Log log_str to log_file_path.

    input:
    - log_str: str
    - log_file_path: str

    returns:
    - None
    """
    if not log_file_path:
        log_file_path = get_default_log_file_path()
    with open(log_file_path, 'a') as f:
        f.write(log_str + '\n')


def output_comment_mode_txt_w(comment_text_list: list[str], output_path: str) -> None:
    """
    Output comment list as txt format. Use 'w' mode.

    txt format:
    - one line for one comment
    - no '\n' in comment

    input:
    - comment_text_list: list[str]
    - output_path: str

    returns:
    - None
    """
    with open(output_path, 'w', encoding='utf-8') as file:
        for comment_text in comment_text_list:
            comment_text = comment_text.replace('\n', '')
            file.write(comment_text + '\n')


def output_comment_mode_txt_a(comment_text_list: list[str], output_path: str, max_num: int=100):
    """
    Output comment list as txt format. Use 'a' mode.

    txt format:
    - one line for one comment
    - no '\n' in comment

    input:
    - comment_text_list: list[str]
    - output_path: str
    - max_num: int
    
    returns:
    - None
    """
    random.shuffle(comment_text_list)
    with open(output_path, 'a', encoding='utf-8') as file:
        count = 0
        for comment_text in comment_text_list:
            if count >= max_num:
                break
            # remove '\n' in comment_text
            comment_text = comment_text.replace('\n', '')
            file.write(comment_text + '\n')
            count += 1


def output_comment_mode_json(comment_text_list: list[str], output_path: str):
    """
    Output comment list as json format.

    json format:
    {"comments": ["comment_text1", "comment_text2", ...]}

    input:
    - comment_text_list: list[str]
    - output_path: str

    returns:
    - None
    """
    res_json = {
        'comments': comment_text_list
    }
    with open(output_path, 'w', encoding='utf-8') as file:
        json.dump(res_json, file, ensure_ascii=False)


def build_txt_batch(bv_list: List[str], comment_num_per_bv: int, output_path: str):
    for bv in bv_list:
        comment_text_list = libcrawl.get_comment_text_list(bv)
        output_comment_mode_txt_a(comment_text_list, output_path)
        print(bv + ' done.')