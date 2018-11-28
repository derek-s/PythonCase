# Python little Case

## 存储一些平时写的小工具

### PIL 压缩JPEG并设置为连续（渐进式）

自己博客上用的小工具

`c-progression.jpg.py`

##### 依赖

`PIL(Pillow)`


### doc.lagout.org/tfr.org 整站爬虫下载器，支持代理

给 [老谢](https://www.xj123.info) 写的两个小工具

`downloader\doc.lagout.org.py`
`downloader\trf.org.py`

##### 依赖

`Requests progressbar BeautifulSoup`

### 网页在线监控

L同学说他单位网站有点神奇问题，为了解决这个神奇问题，于是写了个在线监控。

#### SiteUptime

通过Ping和curl分别检测网络连通性和HTTP访问状态码、DNS解析时间、连接时间测试。

在Ubuntu+Python3环境下开发测试，支持日志和向监控人发送微信信息。

运行程序时会在终端下输出二维码，手机扫码后登录微信，如果不需要该功能，请将源码中wechat相关内容注释。

如下行：

```
# 开启wechat及登陆
self.wechat = weChat()
self.wechat.login()

self.wechat.send_mes(self.url + "Ping测试失败")

self.wechat.send_mes(self.url + "curl http测试失败" + str(e))
```

日志以运行当日日期+"_log"为文件名，可以实时查看，不影响写入。

##### 依赖

`pycurl argparse subprocess itchat arrow`

#### 用法

`python3 main.py "需要监控的URL"`

例如：

`python3 main.py "http://www.abc.com"` 

或

`python3 main.py "www.abc.com"`

#### Excel文件内多个同名Sheet合并工具

源码位于megerExcel内。

`python3 main.py -i filename.xlsx filename2.xlsx -o hb.xlsx`

`-i 为待合并文件文件名，支持多文件`
`-o 合并后文件名`

## 更新日志

#### 2018-11-28
1. 添加合并多个Excel文件内同名sheet的工具

#### 2018-04-15

1. 添加SiteUptime小工具。
#### 2018-01-14

1. 网站下载爬虫增加多线程提高下载速度。

#### 2018-1-4
1. 增加doc.lagout.org.py trf.org.py 两个网站的整站下载爬虫，没有对样式表等数据进行下载，目录浏览型网页，没有样式表也一样能正常用。

#### 2017-12-23
1.  增加PIL压缩JPEG为连续加载形式JPG，可搜索代码文件所在目录下所有jpg文件，压缩并重新存储。