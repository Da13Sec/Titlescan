# -*- coding:utf-8 -*-
#====#====#====#====
#FileName: *.py
#python-Version:3.8
#auther:Da13
#====#====#====#====
import requests
import re
import asyncio
import time
import warnings
import codecs
import aiohttp
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
options = Options()
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--aggressive-cache-discard")
options.add_argument("--disable-cache")
options.add_argument("--disable-application-cache")
options.add_argument("--disable-offline-load-stale-cache")
options.add_argument("--disk-cache-size=0")
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--dns-prefetch-disable")
options.add_argument("--no-proxy-server")
options.add_argument("--log-level=3")
options.add_argument("--silent")
options.add_argument("--disable-browser-side-navigation")
driver = webdriver.Chrome(chrome_options=options)
headers={
         'Accept-Language': 'zh-CN,zh;q=0.9',
         'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.106 Safari/537.36',
         'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
         'onnection': 'keep-alive'
}


def get_url():
    try:
        with open('./1.txt', 'r', encoding='utf-8') as f:
            data = f.readlines()
            return data
    except Exception:  # 文件不存在则返回False
        return False

def verdictUrl():
    get_url_res = get_url()
    if get_url_res:
        for url in get_url_res:
            workQueue.put_nowait(url.strip())

    else:
        print('文件不存在或者没有请求的url......')

async def get_req(session, url):
    try:
        response = await session.get(url, allow_redirects=True,headers=headers,timeout=20)
        html =await response.text()
        return response, html
    except Exception as e:
        response = None
        html = None
        return response, html






async def get_title(session,workqueue):

    global list_titles,list_urls, title
    while not workqueue.empty():
        url = workqueue.get_nowait()

        if "http" not in url:
            url = "http://"+url
        if "sss" not in url:
            random_url = url+'/sssss'

        root_url_res,root_url_html =await get_req(session,url)
        random_url_res,random_url_html = await get_req(session,random_url)
        if root_url_res is not None:
            root_url_res.encoding='utf-8'
        if random_url_res is not None:
            random_url_res.encoding = 'utf-8'
        try:
            if random_url_res is not None or root_url_res is not None:
                if random_url_res is not None:
                    if  random_url_res.status == 400:
                        if "https" in url:
                            result[url]="极有可能不是一个网站"
                        else:
                            tmp_url =url.replace("http://","https://")
                            workqueue.put_nowait(tmp_url)       #如果是https就重放进队列进行请求
                    elif random_url_res.status == 200:
                        title = two00(root_url_res, random_url_res,root_url_html,random_url_html)
                        result[url] = title
                    elif random_url_res.status == 404:
                        title = four0four(root_url_res,root_url_html)
                        result[url] = title
                    elif random_url_res.status in [401,415]:
                        result[url] = "需要基础认证"
                    elif random_url_res.status in [301,302]:
                        direct_url = random_url_res.headers['location']
                        if not re.match("http|https", direct_url):
                            direct_url = url + direct_url
                        try:
                            driver.get(direct_url)

                            if (driver.title):
                                title = driver.title

                            else:
                                title = str(random_url_res.status)
                        except:
                            res = requests.get(direct_url, headers=headers, verify=False, timeout=20)
                            if (re.search("<title>(.*?)</title>", res.text)):
                                title = (re.search("<title>(.*?)</title>", res.text).group(1).strip())

                            else:
                                title = '302'
                        result[url] = title
                    elif random_url_res.status == 403:

                        result[url] = "无权限"
                    elif random_url_res.status in [402,500,501,502,503,504]:
                        result[url] ="极有可能不是一个网站"
                    else:
                        result[url] = "不是一个网站"
                else:
                    if root_url_res is not None:
                        if root_url_res.status in [200,301,302]:
                            if (re.search('<title>(.*?)</title>', root_url_html, re.S)):
                                title = re.search('<title>(.*?)</title>', root_url_html, re.S).group(1).strip()
                                if title == '':
                                    title = str(root_url_res.status)

                            elif (re.search('[url|URL]=(.*?)"', root_url_html)):
                                refresh_url = re.search('[url|URL]=(.*?)"', root_url_html).group(1)
                                if "http" in refresh_url:
                                    root_url = refresh_url
                                else:
                                    root_url = str(root_url_res.url) + '/' + refresh_url
                                res = requests.get(root_url, headers=headers, verify=False, timeout=20)
                                res.encoding = 'utf-8'
                                if (re.search("<title>(.*?)</title>", res.text)):
                                    title = (re.search("<title>(.*?)</title>", res.text).group(1).strip())

                                else:
                                    title = str(root_url_res.status)
                            else:
                                driver.get(str(root_url_res.url))
                                if driver.title:
                                    title = driver.title

                                else:
                                    title = str(root_url_res.status)
                        else:
                            title = '不是一个网站'
                    else:
                        title = '不是一个网站'
                    result[url] = title
            else:
                if "https" in url:
                    result[url] = '不是一个网站'
                else:
                    https_url = url.replace('http','https')
                    workqueue.put_nowait(https_url)
        except Exception as e:
            print(url+'解析错误')
            print(e)
            result[url] = 'exception'
        finally:
            if root_url_res is not None:
                print(url+'-----'+str(root_url_res.status))
            else:
                print(url+'-----网站不存在')


#如果随机目录是返回404的判断
def four0four(root_url_res,root_url_html):
    global list_urls,list_titles

    if root_url_res is not None:
        try:
            if root_url_res.status in [301, 302]:
                if root_url_res.headers['location']:
                    location_url=root_url_res.headers['location']
                    if "http" in location_url:
                        root_url = location_url
                    else:
                        root_url = str(root_url_res.url)+location_url
                else:
                    root_url = str(root_url_res.url)
                try:
                    driver.get(root_url)

                    if (driver.title):
                        title = driver.title

                    else:
                        title = str(root_url_res.status)
                except:
                    res = requests.get(root_url,headers = headers,verify=False,timeout = 10)
                    if (re.search("<title>(.*?)</title>", res.text)):
                        title = (re.search("<title>(.*?)</title>", res.text).group(1).strip())

                    else:
                        title = str(root_url_res.status)
            elif root_url_res.status==200:
                root_url = str(root_url_res.url)

                if (re.search('<title>(.*?)</title>', root_url_html, re.S)):
                    title = re.search('<title>(.*?)</title>', root_url_html, re.S).group(1).strip()
                    if title =='':
                        title = str(root_url_res.status)

                elif (re.search('[url|URL]=(.*?)"', root_url_html)):
                    refresh_url = re.search('[url|URL]=(.*?)"', root_url_html).group(1)
                    if "http" in refresh_url:
                        root_url = refresh_url
                    else:
                        root_url = str(root_url_res.url) + '/'+refresh_url
                    res = requests.get(root_url,headers = headers,verify=False,timeout = 20)
                    res.encoding = 'utf-8'
                    if (re.search("<title>(.*?)</title>", res.text)):
                        title = (re.search("<title>(.*?)</title>", res.text).group(1).strip())

                    else:
                        title = str(root_url_res.status)
                else:
                    driver.get(root_url)
                    if driver.title:
                        title = driver.title

                    else:
                        title = str(root_url_res.status)
            elif root_url_res.status in [403, 404, 415]:
                title = str(root_url_res.status)
            elif root_url_res.status in [500,501, 502, 503, 504]:
                title  = "极有可能不是一个网站"

            else:
                driver.get(str(root_url_res.url))
                if driver.title:
                    title = driver.title
                else:
                    title = '不是一个网站'
        except Exception as e:
            title ='网站存在但是没有标题'
            print(e)
            print(str(root_url_res.url)+"解析错误")
            print(e)
    else:
        try:
            url = root_url_res.url
            res = requests.get(url,headers = headers,verify=False,timeout = 20)
            res.encoding = 'utf-8'
            if (re.search("<title>(.*?)</title>", res.text)):
                title = (re.search("<title>(.*?)</title>", res.text).group(1).strip())

            else:
                title = str(root_url_res.status)
        except:
            title = "网站可能存在"
    return title
#如果随机目录是返回200的判断
def two00(root_url_res,random_url_res,root_url_html,random_url_html):
    if root_url_res is not None:
        if root_url_res.status == 200:
            if "404.css" in random_url_html or "404.js" in random_url_html or "404.html" in random_url_html or "404" in random_url_html or "not found" in random_url_html:
                if (re.search('<title>(.*)</title>', root_url_html, re.S)):
                    title = re.search('<title>(.*)</title>', root_url_html, re.S).group(1).strip()

                else:
                    title =str(root_url_res.status)
            else:
                random_content_length = random_url_res.headers.get('Content-Length', 'None')
                root_content_length = root_url_res.headers.get('Content-Length', 'None')
                if random_content_length != "None" or root_content_length != "None":
                    if (re.search("<title>(.*?)</title>", root_url_html)):
                        title = (re.search("<title>(.*?)</title>", root_url_html).group(1).strip())

                    else:
                        title = str(root_url_res.status)
                else:
                    random_content_length = len(random_url_html)
                    root_content_length = len(root_url_html)
                    if root_content_length == random_content_length:  # 小概率网站正常
                        if (re.search("<title>(.*?)</title>", root_url_html)):
                            title = (re.search("<title>(.*?)</title>", root_url_html).group(1).strip())

                        else:
                            title = str(root_url_res.status)
                    else:  # content-length不相等说明网站有大概率正常，访问正常网站和随机url正常来说content-length就应该不一样
                        if (re.search('<title>(.*)</title>', root_url_html, re.S)):
                            title = re.search('<title>(.*)</title>', root_url_html, re.S).group(1).strip()

                        else:
                            title = str(root_url_res.status)
        elif root_url_res.status in [301, 302]:
            url2 = str(root_url_res.url)
            try:
                direct_url = root_url_res.headers['location']
                if not re.match("http|https", direct_url):
                    direct_url = url2+direct_url
                res = requests.get(direct_url, headers=headers, timeout=20)
                res.encoding = 'utf-8'
                if (re.search("<title>(.*?)</title>", res.text)):
                    title = (re.search("<title>(.*?)</title>", res.text).group(1).strip())

                else:
                    title = str(root_url_res.status)
            except Exception as e:
                print(str(root_url_res.url)+'解析失败')
                print(e)
                title = "网站可能存在"

        elif root_url_res.status in [403, 404, 415, 500]:
            title = str(root_url_res.status)
        elif root_url_res.status in [501, 502, 503, 504]:
            title = "极有可能不是一个网站"
        else:
            title = "不是一个网站"
    else:
        try:
            url = root_url_res.url
            res = requests.get(url, headers=headers, verify=False, timeout=20)
            res.encoding = 'utf-8'
            if (re.search("<title>(.*?)</title>", res.text)):
                title = (re.search("<title>(.*?)</title>", res.text).group(1).strip())

            else:
                title = str(root_url_res.status)
        except:
            title = "网站可能存在"
    return title

async def main():
    verdictUrl()
    print('开始请求，现在的数量为%s' % workQueue.qsize())
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:  # 创建session
        tasks = []
        for _ in range(100):
            task = get_title(session, workQueue)
            tasks.append(task)
        await asyncio.wait(tasks)




https_urllist = set()
result = {}
workQueue = asyncio.Queue()
if __name__ == '__main__':
    warnings.simplefilter('ignore', RuntimeWarning)
    requests.packages.urllib3.disable_warnings()
    time1 = time.time()
    asyncio.run(main())
    time2 = time.time()
    print(time2-time1)
#往文件写url_list和url_titles
    fA = codecs.open("A.txt", "w+",'utf-8')
    fB = codecs.open("B.txt", "w+", 'utf-8')
    fC = codecs.open("C.txt", "w+", 'utf-8')
    fD = codecs.open("D.txt", "w+", 'utf-8')
    ex = codecs.open('except.txt', 'w+', 'utf-8')
    for url,title in result.items():
        if title in ['网站可能存在','403 Forbidden','需要认证','403','404','415','500']:
            fB.write(str(url)+"==>"+str(title)+'\n')
        elif title in ['极有可能不是一个网站',"502 Bad Gateway",'无权限']:
            fC.write(str(url)+"==>"+str(title)+'\n')
        elif title in ['不是一个网站','网站不存在']:
            fD.write(str(url)+"==>"+str(title)+'\n')
        elif title == 'exception':
            ex.write(str(url)+"==>"+str(title)+'\n')
        else:
            fA.write(str(url) + "==>" + str(title) + '\n')
    fA.close()
    fB.close()
    fC.close()
    fD.close()
    print('爬取成功')

