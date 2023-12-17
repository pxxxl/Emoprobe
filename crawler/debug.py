import libcrawl

info = libcrawl.crawl_all_info_of_video("BV1sN411y7mX", "")
print(info)
with open("debug.txt", "w", encoding='utf-8') as file:
    for com in info['data']['comments']:
        file.write(com['comment_text'] + "\n")
