import libcrawl
import json
import argparse


def get_result_json_string(bv: str, cookie: str='', pure: bool=False) -> str:
    result_dict = libcrawl.crawl_all_info_of_video(bv, cookie)
    if pure:
        result_dict = result_dict['data']
    result_json_string = json.dumps(result_dict)
    result_json_string = libcrawl.remove_non_utf8mb3_chars(result_json_string)
    return result_json_string





def write_comment_text_list_to_file(bv: str, cookie: str='', output_path: str='') -> None:
    comment_text_list = libcrawl.get_comment_text_list(bv, cookie)
    if not output_path:
        output_path = bv + '.txt'
    # use UTF-8 encoding
    with open(output_path, 'w', encoding='utf-8') as file:
        for comment_text in comment_text_list:
            # remove '\n' in comment_text
            comment_text = comment_text.replace('\n', '')
            file.write(comment_text + '\n')


def get_error_json_string(bv: str) -> str:
    result_dict = {
        "code": 1,
        'msg': 'An error occurred while crawling the video.',
        'data': None
    }
    result_json_string = json.dumps(result_dict)
    return result_json_string


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


def main():
    try:
        parser = argparse.ArgumentParser(description='Video Crawler')
        parser.add_argument('-bv', help=r'Video BV number, form "BVXXXXXXX"', required=True)
        parser.add_argument('-o', help='File save path')
        parser.add_argument('-config', help='Config file path')
        parser.add_argument('-p', help='Pure output mode', action='store_true')
        args = parser.parse_args()
    
        bv = args.bv
        output_path = args.o
        config_path = args.config
        pure_output = args.p

        if not config_path:
            config_path = libcrawl.get_default_config_file_path()
        
        cookie = get_cookie(config_path)

        if pure_output:
            result_json_string = get_result_json_string(bv, cookie, True)
        else:
            result_json_string = get_result_json_string(bv, cookie)
    
        if output_path:
            with open(output_path, 'w') as file:
                file.write(result_json_string)
        else:
            print(result_json_string)
        
    except:
        result_json_string = get_error_json_string(bv)
        print(result_json_string)


if __name__ == '__main__':
    # write_comment_text_list_to_file("BV1tN4116787", "", "D:\Personal\Program\Comprehensive\Emoprobe\crawler\cache\BV1tN4116787.txt")
    main()