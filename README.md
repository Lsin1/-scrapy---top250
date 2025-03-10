1.创建项目
scrapy startproject 工程名
出现：
![image](https://github.com/user-attachments/assets/92fa5d21-f8c3-405a-98cb-0073df6d3eb5)
代表创建成功
创建 scrapy 项目以后，在 settings 文件中有这样的一条默认开启的语句。
POBOTSOXT_OBEY = True
robots.txt 是遵循 Robot 协议的一个文件，在 Scrapy 启动后，首先会访问网站的 robots.txt 文件，然后决定该网站的爬取范围。有时我们需要将此配置项设置为 False。在 settings.py 文件中，修改文件属性的方法如下。
ROBOTSTXT_OBEY=False

2.明确爬虫目标
构建 item 模型（model）
![image](https://github.com/user-attachments/assets/fe554d01-e604-4842-808d-5b8f46248186)
3.制作爬虫
在编写爬虫逻辑之前，需要在 stockstar/spider 子文件下创建 .py 文件，用于定义爬虫的范围，也就是初始 URL。接下来定义一个名为 parse 的函数，用于解析服务器返回的内容。

首先在 CMD 中输入代码，并生成 spider 代码，如下所示(需先定位至相应子文件夹下)：
scrapy genspider stock url
此时spider 子文件夹下会出现 stock.py 的文件
生成代码如下：
![image](https://github.com/user-attachments/assets/53500249-59f2-4c55-b19a-7dc476144713)

Start_urls即最终爬取网址
再定义parse前需要编辑请求头等相关信息如下
![image](https://github.com/user-attachments/assets/c3b503a8-9098-4fb8-a20b-dd10b5763883)
重新定义函数start_request来请求
For循环遍历获取start_urls下的所有网址
最终爬虫逻辑，如下：
![image](https://github.com/user-attachments/assets/91be7e12-4ec1-4b94-a681-46d557158ad3)
Yield item这一句映射方便后续保存
Return item返回最终数据

运行并保存数据
Json: scrapy crawl 工程名 -o 文件名.json
![image](https://github.com/user-attachments/assets/569bf521-acd2-40f1-a776-d05fd76cfc78)
Csv: scrapy crawl 工程名 -o 文件名.csv
![image](https://github.com/user-attachments/assets/1d87ca3c-75e2-4c05-9509-8efdd62be775)
还有xml以及jsonl格式 只需修改文件后缀名即可
需要在settings.py中设置编码格式防止乱码
FEED_EXPORT_ENCODING = "utf-8"
最终保存JSON文件：
![image](https://github.com/user-attachments/assets/3432a685-7f23-4b32-9f07-61a7aeaf151b)

注：如果有数据无法正常显示，一般都是编码格式不匹配的问题
