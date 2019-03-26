import re
import os
import html
from pyquery import PyQuery
import requests

def get_path(title, save_path):
    # re.sub(pattern, str, text, count=0)
    # re.sub()将text中符合pattern的所有字符转换为str（指定字符）, count 模式匹配后替换的最大次数，默认0替换所有的匹配
    clean_title = re.sub(re.compile(r'[\\/:：\*\?‘’“”"><\|]'), '', title)
    path = os.path.join(save_path, clean_title)
    if not os.path.exists(path):
        os.mkdir(path)
    return path

def download_imgs(url, headers, save_path):
    response = requests.get(url, headers=headers, timeout=2)
    artical_info_pattern = re.compile(r'articleInfo\:\s\{(.*?)\}', re.S)
    img_pattern = re.compile(r"JSON.parse\((.*?)\)")
    img_match = re.search(img_pattern, response.text)
    artical_info_match = re.search(artical_info_pattern, response.text)

    # 如果页面格式是artical_info， 则执行以下代码。
    if artical_info_match:
        title_pattern = re.compile(r'title.*?\'(.*?)\'')
        artical_info = html.unescape(artical_info_match.group(0))
        title_match = re.search(title_pattern, artical_info)
        if title_match:
            title = title_match.group(1)
        else:
            title = "other"
        path = get_path(title, save_path)

        # 在文件夹下创建一个保存来源网址的文本文件
        with open(os.path.join(path, '来源网址.txt'), 'w+', encoding='utf-8') as fo:
            fo.write(url)

        pq_obj = PyQuery(artical_info)
        hrefs = []
        for each in pq_obj('img').items():
            hrefs.append(each.attr('src'))
        for index,href in enumerate(hrefs):
            response = requests.get(href)
            if response.status_code == 200:
                with open(os.path.join(path, '%s.jpg'%index), 'wb+') as fo:
                    fo.write(response.content)
            else:
                pass

    # 如果页面形式为JSON.parse类型， 则执行以下代码
    elif img_match:
        title_pattern = re.compile(r"title:.*?\'(.*?)\'")
        href_pattern = re.compile(r'\"url\":\"(.*?)\".*?width"')
        title_match =  re.search(title_pattern, response.text)
        if title_match:
            title = title_match.group(1)
        else:
           title =  'other'
        path = get_path(title, save_path)
        if img_match:
            img_info = img_match.group(1)
            img_info = img_info.replace('\\', '')
            hrefs = re.findall(href_pattern, img_info)
            hrefs = set(hrefs)
            for index, href in enumerate(hrefs):
                response = requests.get(href)
                if response.status_code == 200:
                    with open(os.path.join(path, str(index)+'.jpg'), 'wb+') as fo:
                        fo.write(response.content)
                else:
                    pass
    # 如果都不是，返回url
    else:
        return url