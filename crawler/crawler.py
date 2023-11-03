import libcrawl
import json
import argparse


def get_result_json_string(bv: str) -> str:
    result_dict = libcrawl.crawl_all_info_of_video(bv)
    result_json_string = json.dumps(result_dict)
    return result_json_string


def main():
    parser = argparse.ArgumentParser(description='Video Crawler')
    parser.add_argument('-bv', help=r'Video BV number, form "BVXXXXXXX"', required=True)
    parser.add_argument('-o', help='File save path')
    args = parser.parse_args()
    
    bv = args.bv
    output_path = args.o
    
    result_json_string = get_result_json_string(bv)
    
    if output_path:
        with open(output_path, 'w') as file:
            file.write(result_json_string)
    else:
        print(result_json_string)


if __name__ == '__main__':
    main()