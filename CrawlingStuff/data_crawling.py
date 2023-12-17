import requests
from lxml import etree
from urllib.parse import quote
from datetime import datetime
from data_processing import merge_to_csv
from tqdm import trange

weibo_cookies = {
    "SUB": "_2A25IehvkDeRhGeFG7FQZ-CrMyTuIHXVr9hEsrDV8PUNbmtANLVnzkW9NeMOQzQXE2ovsA6XuvU7LOwyQ9weBk0UO",
}


def create_weibo_search_url(topic):
    base_url = "https://s.weibo.com/realtime?q=" + quote(topic) + "&rd=realtime&tw=realtime&Refer=weibo_realtime&page="
    url_list = []
    for i in range(1, 51):
        url_list.append(base_url + str(i))
    return url_list


def extract_data_from_response(rsp):
    results = []
    html = rsp.text
    tree = etree.HTML(html)
    comments = tree.xpath('//*[@id="pl_feedlist_index"]/div[3]/div')
    for comment in comments:
        texts = comment.xpath('./div/div[1]/div[2]/p/text()')
        comment_time = comment.xpath('./div/div[1]/div[2]/div[2]/a[1]/text()')
        processed_text = processed_time =''
        for string in texts:
            string = string.strip()
            if not string:
                continue
            processed_text += string
        for string in comment_time:
            string = string.strip()
            if not string:
                continue
            processed_time += string
        results.append([processed_text, processed_time])
    return results


def crawl_topic(topic, result_file_path):
    url_list = create_weibo_search_url(topic)
    print(f"Ready to crawl [{len(url_list)}] url, the first is {url_list[0]}")

    weibo_session = requests.Session()
    weibo_session.cookies.update(weibo_cookies)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36',
    }
    total_rst = []
    for i in trange(len(url_list)):
        target_url =url_list[i]
        try:
            request_rsp = weibo_session.get(target_url, headers=headers)
            if request_rsp.status_code == 200:
                page_rst = extract_data_from_response(request_rsp)
                total_rst += page_rst
            else:
                print("Failed to crawl the page:", request_rsp.status_code)
        except Exception as e:
            print("ERROR:", e, " in url:", target_url)
    merge_to_csv(total_rst, result_file_path,topic,'Query time: ' + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
