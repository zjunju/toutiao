# toutiao
通过关键词搜索，抓取搜索得到的数据，再将数据中的每个页面的图片保存到本地
在run.py中的
  hrefs, save_path = get_hrefs_run(keyword='艺术', max_offset=200, headers=headers)
这一句的代码中，可以修改keyword的值，抓取相应搜索到的结果的图片。
max_offset为最大的偏移量，在搜索得到的返回结果中，数据是有限的，
所以如果设置max_offset的值很大，也得不到这么多数据，只会得到搜索所得到的所有结果，
不过可以限制获取的数据数量。
