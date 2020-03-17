# 前言
在做渗透测试时，一般甲方都会直接给上万个url，然后需要我们从中挖到漏洞。那么第一步就是从这些url中筛选出是否是正常存活状态的网站，并且找出哪些网站是可值得去挖掘的。



# 项目介绍

该项目运用了asyncio的异步协程，以及通过正则和headless chrome获取标题的思路。

文件名: Titlescan.py

开发语言: python3.8

第三方库：asyncio
codecs
aiohttp
selenium


# 用法

1. pip3 install -r requirements.txt

2. 将要测试的urls保存为Titlescan.py同级目录下的urls.txt。
3. python3 Titlescan.py也可以直接放进编辑器中运行

# 结果说明

这里对example文件下的test.txt文件里面的urls进行了测试。结果保存在example目录下的A.txt,B.txt,C.txt,D.txt。

A是存在的正常网站

B是可能存在的网站

C是极大可能不存在的网站

D不是一个网站

测试时间：16-20min

# 致谢

最后感谢硬糖师傅的指导！

相关代码的分析参观我博客

https://da13.fun/2020/02/20/%E4%BF%A1%E6%81%AF%E6%94%B6%E9%9B%86%E6%95%B4%E7%90%86%E5%B0%8F%E5%B7%A5%E5%85%B7%E2%80%94%E2%80%94%E5%BF%AB%E9%80%9F%E7%AD%9B%E9%80%89%E5%88%86%E7%B1%BB%E6%AD%A3%E5%B8%B8%E5%AD%98%E6%B4%BB%E7%BD%91%E7%AB%99%E5%B9%B6%E8%8E%B7%E5%8F%96%E6%A0%87%E9%A2%98/

如果有师傅们还有更好的建议，非常欢迎一起交流！
