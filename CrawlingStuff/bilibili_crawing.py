import requests
from lxml import etree
from urllib.parse import quote
from datetime import datetime, timedelta
from data_processing import bilibili_store_data
from tqdm import trange
import emoji
import re
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
    # 添加其他必要的Headers
}
cookies = {
    "bmg_src_def_domain": "i2.hdslb.com",
    "b_lsid": "C1BEBCE5_18C7BACBC51",
    "browser_resolution": "1528-742",
    "bp_video_offset_1826123766": "875938771633176646",
    "bili_ticket_expires": "1702987211",
    "bili_ticket": "eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MDI5ODcyNzEsImlhdCI6MTcwMjcyODAxMSwicGx0IjotMX0.WFQize_9Qmub_mAiSQYFQs0LPIuuQSPrvTvGVd_-G54",
    "sid": "691srbf3",
    "bili_jct": "3e344af1e6c9d9513acc4ccac02a91bb",
    "bmg_af_switch": "1",
    "CURRENT_QUALITY": "80",
    "home_feed_column": "5",
    "buvid_fp": "ece2f41e6308a4df3256f7ae6aef9b2f",
    "is-2022-channel": "1",
    "PVID": "2",
    "FEED_LIVE_VERSION": "V8",
    "fingerprint": "ece2f41e6308a4df3256f7ae6aef9b2f",
    "SESSDATA": "6ec636a0%2C1718280062%2C8d324%2Ac2CjA5itCIzgNdg9ETxvNJZSyX4118h2Ajhdvm47BT0pe1W9ixPkh77LhSQXe0sa5nzCASVkhZRC1GazFMSTlnbHk4ZUtscVdWOUh2Ymo3NlgyRVZyeWUxWE1ZZlVuTmpURlp4aXBTYU1ydjNTejVSbTVfVHJKQ2ZLSFhSZlpVdmFMV3NuWE5pbnBRIIEC",
    "i-wanna-go-back": "-1",
    "header_theme_version": "CLOSE",
    "DedeUserID__ckMd5": "0e898ac6eae5487e",
    "CURRENT_FNVAL": "16",
    "hit-new-style-dyn": "1",
    "rpdid": "|(JJmY)YRkRu0J'uY)Rm)mJ|)",
    "nostalgia_conf": "-1",
    "hit-dyn-v2": "1",
    "b_ut": "5",
    "CURRENT_BLACKGAP": "0",
    "DedeUserID": "1826123766",
    "_uuid": "1D68B769-AE4D-1358-5257-9CCFDEDAA2D1089975infoc",
    "buvid3": "DF2F5173-CB34-A680-A82C-D99D44F838BB91526infoc",
    "enable_web_push": "DISABLE",
    "buvid4": "C5B5574A-C227-1D96-8E35-235E831297FD92963-023052512-hGpvobNRkZ9UuqB%2B4ijuTg%3D%3D",
    "buvid_fp_plain": "undefined",
    "LIVE_BUVID": "AUTO1216990885422372",
    "b_nut": "1684989291",
}
def remove_animation_code(string):
    # 定义要匹配和替换的正则表达式模式
    pattern = r'【】'  # 假设动画编码是方括号内的字符序列
    # 使用 re.sub() 函数进行替换
    result = re.sub(pattern, '', string)
    result = emoji.demojize(result)
    pattern = r':[A-Za-z0-9_]+:'  # 匹配形如 :smiling_face_with_halo: 的编码
    result = re.sub(pattern, '', result)
    return result

def create_search_url(topic):
    url_list = []
    base_url = "https://search.bilibili.com/all?&keyword="+ quote(topic) + "&from_source=webtop_search&spm_id_from=333.1007&search_source="
    url_list.append(base_url+'5')
    for i in range(2,50):
        url_list.append(base_url + "5&page="+str(i)+"&o="+str((i-1)*30))
    return url_list
def crawl_topic(topic, result_file_path):
    bilibili_session = requests.Session()
    bilibili_session.cookies.update(cookies)
    url_list = create_search_url(topic)

    total_rst = []
    for i in trange(len(url_list)):
        target_url = url_list[i]
        print("第{}页查询url:".format(i+1),target_url)
        try:
            request_rsp = bilibili_session.get(target_url,headers=headers)
            if request_rsp.status_code == 200:
                page_rst = extract_data_from_response(request_rsp)
                if not page_rst:
                    break
                page_rst = extract_comment(results=page_rst)
                total_rst += page_rst
            else:
                print("Failed to crawl the page:", request_rsp.status_code)
        except Exception as e:
            print("ERROR:", e, " in url:", target_url)
    bilibili_store_data(total_rst, result_file_path, topic, 'Query time: ' + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

def  extract_data_from_response(rsp):
    results = []
    html = rsp.text
    tree = etree.HTML(html)
    if re.search(r"page=\d+&o=\d+", rsp.url):
        # 匹配 "page=数字&o=数字" 的字符串
        # 执行相应的操作
        comments = tree.xpath('// *[ @ id = "i_cecream"] / div / div[2] / div[2] / div / div / div[1]/div')
    else:
        comments = tree.xpath('//*[@id="i_cecream"]/div/div[2]/div[2]/div/div/div/div[2]/div/div')
    for comment in comments:
        elements = comment.xpath('./div/div[2]/a')
        if elements:
            href ='https:'+elements[0].get('href')+'?spm_id_from=333.337.search-card.all.click&vd_source=35ec86bd8cd36f3273b6f82b14486361'
        elements = comment.xpath("./div/div[2]/div/div/a/h3")
        if elements:
            title = elements[0].get('title')
        results.append((href,title))
    return results
def extract_comment(results):
    total=[]
    for href,title in results:
        video_id=extract_video_id(href)
        print(href)
        if video_id:
            # 获取所有评论数据
            comments = fetch_all_comments(video_id)
            for comment in comments:
                timestamp = comment['ctime']
                # 将时间戳转换为datetime对象
                dt = datetime.fromtimestamp(timestamp)
                # 格式化datetime对象为指定的时间字符串
                formatted_time = dt.strftime('%Y-%m-%d %H:%M')
                total.append((remove_animation_code(comment['content']['message'].replace('\n', ' ')),formatted_time,comment['like'],comment['rcount'],comment['member']['uname']))
    return total
def extract_video_id(url):
    # 通过正则表达式提取视频ID（oid）
    regex_pattern = r"\/(BV\w+)"
    match = re.search(regex_pattern, url)
    if match:
        video_id = match.group(1)
        return video_id
    else:
        return None

def construct_api_url(video_id, page):
    api_url = f"https://api.bilibili.com/x/v2/reply?jsonp=jsonp&pn={page}&type=1&oid={video_id}&sort=2"
    return api_url

def fetch_comments(api_url):
    response = requests.get(api_url,headers=headers)
    data = response.json()
    comments = data['data']['replies']
    return comments

def fetch_all_comments(video_id):
    page = 1
    all_comments = []
    while True:
        api_url = construct_api_url(video_id, page)
        comments = fetch_comments(api_url)
        if len(comments) == 0:
            break
        all_comments.extend(comments)
        page += 1
    return all_comments
if __name__ == "__main__":
    topic="#除夕不放假#"
    result_file_path="./CrawlResult/bilibili_comments_"+topic+".csv"
    crawl_topic(topic,result_file_path)

