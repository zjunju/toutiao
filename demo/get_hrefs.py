import os
import time
import requests
from urllib import parse


# 获取搜索到的页面的所有含有图片的url
def get_search_data(url, headers):
    hrefs = []
    base_href = 'https://www.toutiao.com/a'
    response = requests.get(url, headers=headers, timeout=2)
    if response.status_code == 200:
        response_json = response.json()
        # 这里获取的data还是一个列表类型，里面的每一项元素是一个字典，包含了每一条内容里的详细信息
        # 可以获取has_image的值，判断是否有图片，has_video判断是否有视频
        # 只要图片不要视频，进行图片视频判断
        # data里的id属性的值是每个页面的跳转连接的值（组成部分）
        # url返回的不一定有结果，offset可能已经超出了搜索结果所给出的范围
        # 在返回的json数据中，有一个key为has_more，里面保存的值是1或0，如果是1则表示往后还有数据，如果保存的是0，则表示offset后面已经没有数据了，不要再往后了

        data = response_json.get('data', None)
        if data:
            for each in data:
                if each.get('has_image', False) and not each.get('has_video', False):
                    each_id = each.get('id', None)
                    if each_id:
                        hrefs.append(base_href+each_id)
        else:
            print(url, '  获取搜索结果失败')

        has_more = response_json.get('has_more', 0)

        return hrefs, has_more
    else:
        print(url, 'error')


def get_hrefs_run(keyword="街拍", max_offset = 100, headers=None,base_path="img"):
    base_url = "https://www.toutiao.com/api/search/content/?"
    params = {
        'aid': '24',
        'app_name': 'web_search',
        'offset': '0',
        'format': 'json',
        'keyword': keyword,
        'autoload': 'true',
        'count': '20',
        'en_qc': '1',
        'cur_tab': '1',
        'from': 'search_tab',
        'pd': 'synthesis',
        'timestamp': '1553419251686'
    }
    # 因为 range是[)，左边为开区间，右边为闭区间，所以如果要max_offset量，则需要加一
    max_offset += 1

    hrefs = []

    # 在img文件夹下创建keyword文件夹，该keyword抓取的所有图片都保存到keywrod文件夹
    save_path = os.path.join(base_path, keyword)
    if not os.path.exists(save_path):
        os.mkdir(save_path)

    for offset in range (0,max_offset,20):
        # 更新offset的值，继续获取数据
        params.update({'offset': offset})
        # 构建GET请求参数
        query = parse.urlencode(params)
        # 构建url
        url = base_url + query
        # has_more是判断后面是否还有数据,1表示有，0表示没有
        each_url_hrefs, has_more = get_search_data(url, headers)
        if has_more != 0:
            hrefs.append(each_url_hrefs)
            # 休眠2s
            time.sleep(2)
        else:
            break
    return hrefs, save_path