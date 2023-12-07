import libcrawl
import json
import argparse
import utils


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
        
        cookie = utils.get_cookie(config_path)

        if pure_output:
            result_json_string = libcrawl.get_result_json_string(bv, cookie, True)
        else:
            result_json_string = libcrawl.get_result_json_string(bv, cookie)
    
        if output_path:
            with open(output_path, 'w') as file:
                file.write(result_json_string)
        else:
            print(result_json_string)
        
    except:
        result_json_string = libcrawl.get_error_json_string()
        print(result_json_string)


if __name__ == '__main__':
    main()