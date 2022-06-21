import requests  # 数据请求模块 第三方模块 
import parsel  # 数据解析模块 第三方模块 
import csv  # 保存csv表格数据模块 内置模块
import time  # 时间模块 
# headers 请求头 字典数据类型
headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
        }
# 创建打开一个文件 进行保存
f = open(r'C:\Users\17313\Desktop\2,源代码\当当图书.csv', mode='a', encoding='utf-8', newline='')
csv_writer = csv.DictWriter(f, fieldnames=[
            '标题',
            '评论数',
            '推荐量',
            '作者',
            '出版社',
            '售价',
            '原价',
            '折扣',
            '电子书价格',
            '详情页',
        ])
csv_writer.writeheader()  # 写入表头
for series in range (2,13):
    for page in range (1,26):
        print(f'正在爬取第{series}系列第{page}页的数据内容')
        # time.sleep(1.5)
        if(series>9):
            url=f'http://bang.dangdang.com/books/bestsellers/01.54.{series}.00.00.00-24hours-0-0-1-{page}'.format(series,page)
        else:url=f'http://bang.dangdang.com/books/bestsellers/01.54.0{series}.00.00.00-24hours-0-0-1-{page}'.format(series,page)
        response = requests.get(url=url, headers=headers)
        selector = parsel.Selector(response.text)  # 对于获取到的html字符串数据进行转换 selector 对象
        # css选择器 就是根据标签属性提取相应的数据
        lis = selector.css('ul.bang_list li')
        for li in lis:
            # .name 定位 class类名name标签 a 标签 attr() 属性选择器 取a标签里面title属性 get() 获取数据
            title = li.css('.name a::attr(title)').get()  # 标题
            # 获取标签里面文本数据 直接text
            comment = li.css('.star a::text').get().replace('条评论', '')  # 评论
            recommend = li.css('.star .tuijian::text').get().replace('推荐', '')  # 推荐
            author = li.css('.publisher_info a:nth-child(1)::attr(title)').get()  # 作者
            publish = li.css('div:nth-child(6) a::text').get()  # 出版社
            price_n = li.css('.price .price_n::text').get()  # 售价
            price_r = li.css('.price .price_r::text').get()  # 原价
            price_s = li.css('.price .price_s::text').get()  # 折扣
            price_e = li.css('.price .price_e .price_n::text').get()  # 电子书价格
            href = li.css('.name a::attr(href)').get()  # 详情页
            dit = {
                '标题': title,
                '评论数': comment,
                '推荐量': recommend,
                '作者': author,
                '出版社': publish,
                '售价': price_n,
                '原价': price_r,
                '折扣': price_s,
                '电子书价格': price_e,
                '详情页': href,
            }
            csv_writer.writerow(dit)  # 数据保存到csv
print("--------爬取完毕--------")
