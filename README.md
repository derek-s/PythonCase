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

## 更新日志
#### 2017-12-23
1.  增加PIL压缩JPEG为连续加载形式JPG，可搜索代码文件所在目录下所有jpg文件，压缩并重新存储。

#### 2018-1-4
1. 增加doc.lagout.org.py trf.org.py 两个网站的整站下载爬虫，没有对样式表等数据进行下载，目录浏览型网页，没有样式表也一样能正常用。