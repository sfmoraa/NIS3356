import re

import requests
from lxml import etree
from urllib.parse import quote
from datetime import datetime, timedelta
from data_processing import *
from tqdm import trange
from bs4 import BeautifulSoup
import time

weibo_cookies = {
    "SUB": "_2A25Ig8-MDeRhGeFG7FQZ-CrMyTuIHXVr4U1ErDV8PUNbmtANLUPykW9NeMOQzWnbw8Ve_JWnxE7yEXFE2XeopVoL",
}
assert weibo_cookies['SUB'] != "你的cookies"


def _debug_show_resp(resp, addition_msg=None):
    print("----------------------------------------------------")
    if addition_msg is not None:
        print("*****", addition_msg, "*****")
    print("request:", resp.request.url)
    print("req headers:", resp.request.headers)
    print("response:", resp.url)
    print(resp.headers)
    print(resp.cookies)
    print(resp.status_code)
    if resp.status_code == 302:
        print("Redirecting->", resp.headers['Location'])
    print("----------------------------------------------------")


def create_weibo_search_url(topic, search_days_range, weibo_session):
    print(f"Preparing url within {search_days_range} in weibo to search...\n")
    start_datetime = datetime.strptime(search_days_range[0], "%Y-%m-%d")
    end_datetime = datetime.strptime(search_days_range[1], "%Y-%m-%d")
    current_datetime = start_datetime
    date_range = []
    while current_datetime <= end_datetime:
        date_range.append(current_datetime.strftime("%Y-%m-%d-%H"))
        current_datetime += timedelta(days=1)

    url_list = []
    for day_idx in trange(len(date_range) - 1):
        base_url = "https://s.weibo.com/weibo?q=" + quote(topic) + "&typeall=1&suball=1&timescope=custom%3A" + date_range[day_idx] + "%3A" + date_range[day_idx + 1] + "&Refer=g&page="
        test = weibo_session.get(base_url + '1')
        html = test.text
        tree = etree.HTML(html)
        pages = tree.xpath('//*[@id="pl_feedlist_index"]/div[5]/div/span/ul/li')
        # print(len(pages),base_url+'1')
        if len(pages) == 0:
            url_list.append(base_url + '1')
        elif len(pages) == 50:
            this_day = datetime.strptime(date_range[day_idx], "%Y-%m-%d-%H")
            for hour in range(23):
                this_day_base_url = "https://s.weibo.com/weibo?q=" + quote(topic) + "&typeall=1&suball=1&timescope=custom%3A" + this_day.strftime("%Y-%m-%d-%H") + "%3A"
                this_day += timedelta(hours=1)
                this_day_base_url += this_day.strftime("%Y-%m-%d-%H") + "&Refer=g&page="
                test = weibo_session.get(this_day_base_url + '1')
                html = test.text
                tree = etree.HTML(html)
                pages = tree.xpath('//*[@id="pl_feedlist_index"]/div[5]/div/span/ul/li')
                if len(pages) == 0:
                    url_list.append(base_url + '1')
                else:
                    for i in range(1, len(pages) + 1):
                        url_list.append(base_url + str(i))
        else:
            for i in range(1, len(pages) + 1):
                url_list.append(base_url + str(i))
    return url_list


def get_weibo_user_info(user_id):
    try:
        user_info = requests.get("https://weibo.com/ajax/profile/info?custom=" + user_id, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36'}, cookies=weibo_cookies).json()
        location=user_info['data']['user']["location"].split()
        if len(location)>1:
            location=location[0]
        else:
            location=user_info['data']['user']["location"]
        return [location, user_info['data']['user']["gender"]]
    except:
        print("Too many requests!sleeping")
        time.sleep(20)
        return get_weibo_user_info(user_id)


def extract_data_from_weibo_response(rsp):
    results = []
    html = rsp.text
    tree = etree.HTML(html)
    comments = tree.xpath('//*[@id="pl_feedlist_index"]/div[4]/div')
    for comment in comments:
        texts = comment.xpath('./div/div[1]/div[2]/p/text()')
        comment_time = comment.xpath('./div/div[1]/div[2]/div[2]/a[1]/text()')
        likes = comment.xpath('./div/div[2]/ul/li[3]/a/button/span[2]/text()')
        selflink = comment.xpath('./div/div[1]/div[2]/div[1]/div[2]/a')[0].get('href')
        userid = re.search(r"//weibo.com/(\d+)\?refer_flag", selflink).group(1)
        location, gender = get_weibo_user_info(userid)
        processed_text = processed_time = ''
        for string in texts:
            string = string.strip().replace('\u200b', '')
            if not string:
                continue
            processed_text += string
        for string in comment_time:
            string = string.strip()
            if not string:
                continue
            processed_time += convert_weibo_time_format(string, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        if likes[0] == '赞':
            likes = 0
        else:
            likes = int(likes[0])
        results.append([processed_text, processed_time, likes, location, gender])
    return results


def weibo_crawl_topic(topic, result_file_path, search_days_range):
    weibo_session = requests.Session()
    weibo_session.cookies.update(weibo_cookies)

    url_list = create_weibo_search_url(topic, search_days_range, weibo_session)
    print(f"Ready to crawl [{len(url_list)}] url of weibo, the first is {url_list[0]}", '\n')
    time.sleep(1)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36',
    }
    total_rst = []
    for i in trange(len(url_list)):
        target_url = url_list[i]
        # try:
        #     request_rsp = weibo_session.get(target_url, headers=headers)
        #     if request_rsp.status_code == 200:
        #         page_rst = extract_data_from_weibo_response(request_rsp)
        #         total_rst += page_rst
        #     else:
        #         print("Failed to crawl the page:", request_rsp.status_code)
        # except Exception as e:
        #     print("ERROR:", e, " in url:", target_url)

        request_rsp = weibo_session.get(target_url, headers=headers)
        if request_rsp.status_code == 200:
            page_rst = extract_data_from_weibo_response(request_rsp)
            total_rst += page_rst
        else:
            print("Failed to crawl the page:", request_rsp.status_code)

    weibo_store_data(total_rst, result_file_path, topic, 'Query time: ' + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))


def extract_data_from_zhihu_response(json_data):
    mydata = []
    for data in json_data['data']:
        # print(data["target_type"], data["target"]["answer_type"], data["target"]["author"]["user_type"], data["target"]["author"]["type"], data["target"]["author"]["gender"], data["target"]["comment_count"], datetime.fromtimestamp(data["target"]["updated_time"]).strftime('%Y-%m-%d %H:%M:%S'),
        #       data["target"]["voteup_count"],data["target"]["excerpt"])

        mydata.append([BeautifulSoup(data["target"]["content"], 'html.parser').get_text(), data["target"]["author"]["gender"], data["target"]["comment_count"], data["target"]["voteup_count"], datetime.fromtimestamp(data["target"]["updated_time"]).strftime('%Y-%m-%d %H:%M')])
    return mydata


def zhihu_search(question_number, zhihu_session, result_file_path):
    questions_url = "https://www.zhihu.com/api/v4/questions/" + str(
        question_number) + "/feeds?include=data%5B*%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cattachment%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Cis_labeled%2Cpaid_info%2Cpaid_info_content%2Creaction_instruction%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%3Bdata%5B*%5D.mark_infos%5B*%5D.url%3Bdata%5B*%5D.author.follower_count%2Cvip_info%2Cbadge%5B*%5D.topics%3Bdata%5B*%5D.settings.table_of_content.enabled&offset=0&limit=5&order=updated"
    zhihu_first_rsp = zhihu_session.get(questions_url)
    json_data = zhihu_first_rsp.json()
    topic_name = json_data['data'][0]["target"]["question"]["title"]
    topic_created_time = datetime.fromtimestamp(json_data['data'][0]["target"]["question"]["updated_time"])
    topic_id = json_data['data'][0]["target"]["question"]["id"]

    total_data = []
    page_count = 1
    print("Ready to search zhihu question [", topic_name, "] created at", topic_created_time, 'with id', topic_id)
    while not json_data['paging']['is_end']:
        total_data += extract_data_from_zhihu_response(json_data)
        next_url = json_data['paging']['next']
        if page_count % 10 == 0:
            print("In", page_count, "turns collected", len(total_data), "answers")
        json_data = zhihu_session.get(next_url).json()
        page_count += 1

    print(len(total_data))
    zhihu_store_data(total_data, result_file_path, topic_name)


def zhihu_crawl_topic(question_number, result_file_path):
    zhihu_session = requests.Session()
    zhihu_search(question_number, zhihu_session, result_file_path)


# get_weibo_user_info('1279809032')
