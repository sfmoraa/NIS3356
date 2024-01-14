import requests
import json
import execjs
import pandas as pd
from datetime import datetime


def search(keyword):
    headers = {
        "authority": "edith.xiaohongshu.com",
        "accept": "application/json, text/plain, */*",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "content-type": "application/json;charset=UTF-8",
        "origin": "https://www.xiaohongshu.com",
        "referer": "https://www.xiaohongshu.com/",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.188",
        "x-s": "",
        "x-t": ""
    }
    cookies = {

    }
    datas = {
        "keyword": keyword,
        "page": 1,
        "page_size": 20,
        "search_id": "2blciviwfc1cdapvnknmj",
        "sort": "general",
        "note_type": 0
    }
    total = []
    try:
        while True:
            data_json = json.dumps(datas, ensure_ascii=False, separators=(",", ":"))
            # 调用js签名算法，获取x-s,xt。需要js的v
            exc = execjs.compile(open('./info.js', 'r', encoding='utf-8').read())
            xs_xt = exc.call('get_xs', '/api/sns/web/v1/search/notes', data_json, cookies["a1"])
            xs_xt['X-t'] = str(xs_xt['X-t'])
            headers.update(xs_xt)
            api_url = 'https://edith.xiaohongshu.com/api/sns/web/v1/search/notes'
            page = 1
            response = requests.post(url=api_url, data=data_json.encode(), headers=headers, cookies=cookies)
            data = response.json()
            datas["page"] += 1

            items = data["data"]["items"]
            for item in items:
                note_id = item.get("id")  # 获取笔记的ID
                print(f"笔记ID: {note_id}")
                page = 1
                while True:
                    if page == 1:
                        url = 'https://edith.xiaohongshu.com/api/sns/web/v2/comment/page?note_id={}&top_comment_id=&image_scenes=FD_WM_WEBP,CRD_WM_WEBP'.format(
                            note_id)
                    else:
                        url = 'https://edith.xiaohongshu.com/api/sns/web/v2/comment/page?note_id={}&top_comment_id=&image_scenes=FD_WM_WEBP,CRD_WM_WEBP&cursor={}'.format(
                            note_id, next_cursor)
                    # 发送请求
                    try:
                        r = requests.get(url, headers=headers, cookies=cookies)
                        # 解析数据
                        json_data = r.json()
                        comments = json_data["data"]["comments"]
                        for comment in comments:
                            total.append((comment["content"], datetime.fromtimestamp(comment["create_time"] / 1000).strftime("%Y-%m-%d %H:%M"), comment["like_count"], len(comment["sub_comments"]), comment["user_info"]["nickname"], comment["ip_location"]))
                        if json_data['data']['has_more'] is False:
                            break
                        # 得到下一页的游标
                        next_cursor = json_data['data']["cursor"]
                    except Exception as e:
                        if str(e) == "'ip_location'":
                            total.append((comment["content"], datetime.fromtimestamp(comment["create_time"] / 1000).strftime("%Y-%m-%d %H:%M"), comment["like_count"], len(comment["sub_comments"]), comment["user_info"]["nickname"], '无'))
                        else:
                            print(e, json_data)
                            break
                    page += 1
            if data["data"]["has_more"] is False:
                break
    except Exception as e:
        print(datas["page"], page, e)
    df = pd.DataFrame(total, columns=[keyword, "Querytime:{}".format(datetime.now().strftime("%Y-%m-%d %H:%M")), "点赞数", "点评数", "用户昵称", "IP位置"])
    df.to_csv("./CrawlResult/小红书评论_{}.csv".format(keyword), index=False)
    # df.to_csv("小红书评论_{}.csv".format(keyword), mode='a', header=False, index=False)


if __name__ == '__main__':
    search("张雪峰文科就是服务业")
