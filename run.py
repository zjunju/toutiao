import time
from demo.download_img import download_imgs
from demo.get_hrefs import get_hrefs_run


class Headers(object):
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36'


if __name__ == '__main__':
    headers = {
        "User-Agent": Headers.user_agent,
    }
    # offset 是有限制的，也就是搜索出的结果是有数量限制的，如果到达了极致，就获取不到后面的数据了
    hrefs, save_path = get_hrefs_run(keyword='艺术', max_offset=200, headers=headers)
    print('抓取所有连接完成')
    for href_list in hrefs:
        for href in href_list:
            # 传入一个文章href， 然后下载文章的所有图片
            download_imgs(href, headers, save_path)
            print(href, 'done')
            time.sleep(2)
