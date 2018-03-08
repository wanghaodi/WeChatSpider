import re
import urllib.request
import time
import urllib.error


def downloader(url):
    headers = ("User-Agent", "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 "
                             "(KHTML, like Gecko) Chrome/63.0.3239.26 Safari/537.36 "
                             "Core/1.63.4793.400 QQBrowser/10.0.702.400")
    opener = urllib.request.build_opener()
    opener.addheaders = [headers]
    urllib.request.install_opener(opener)
    try:
        data = urllib.request.urlopen(url).read()
        data = data.decode('utf-8')
        return data
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)
        time.sleep(10)
    except Exception as e:
        print("exception:" + str(e))
        time.sleep(1)


def getlisturl(key, pagestart, pageend):
    try:
        page = pagestart
        keycode = urllib.request.quote(key)
        pagecode = urllib.request.quote("&page")
        for page in range(pagestart, pageend+1):
            url = "http://weixin.sogou.com/weixin?type=2&query=" + keycode + pagecode + str(page)
            data1 = downloader(url)
            listurlpat = '<div class="txt-box">.*?(http://.*?)"'
            data2 = re.compile(listurlpat, re.S)
            result = data2.findall(data1)
            listurl.append(result)
            print(listurl)
        print("共获取到" + str(len(listurl)) + "页")
        return listurl
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)
        time.sleep(10)
    except Exception as e:
        print("exception:" + str(e))
        time.sleep(1)


def getcontent(listurl):
    i = 0
    html1 = '''<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
    <html xmlns="http://www.w3.org/1999/xhtml">
    <head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <title>微信文章页面</title>
    </head>
    <body>'''
    fh = open("C://Users/59574/Desktop/python/test/WeChatSpider/1.html", "wb")
    fh.write(html1.encode("utf-8"))
    fh.close()
    fh = open("C://Users/59574/Desktop/python/test/WeChatSpider/1.html", "ab")
    for i in range(0, len(listurl)):
        for j in range(0, len(listurl[i])):
            try:
                url = listurl[i][j]
                url = url.replace("amp;", "")
                data = downloader(url)
                titlepat = "<title>(.*?)</title>"
                contentpat = 'id="js_content">(.*?)id="js_sg_bar"'
                title = re.compile(titlepat).findall(data)
                content = re.compile(contentpat, re.S).findall(data)
                if (title != []):
                    thistitle = title[0]
                if (content != []):
                    thiscontent = content[0]
                dataall = "<p>标题为:" + thistitle + "</p><p>内容为:" + thiscontent + "</p><br>"
                fh.write(dataall.encode("utf-8"))
                print("第"+str(i+1) + "个网页第" + str(j+1) + "条内容保存")
            except urllib.error.URLError as e:
                if hasattr(e, "code"):
                    print(e.code)
                if hasattr(e, "reason"):
                    print(e.reason)
                time.sleep(10)
            except Exception as e:
                print("exception:" + str(e))
                time.sleep(1)
    fh.close()
    html2 = '''</body>
    </html>
    '''
    fh = open("C://Users/59574/Desktop/python/test/WeChatSpider/1.html", "ab")
    fh.write(html2.encode("utf-8"))
    fh.close()


if __name__ == '__main__':
    listurl = list()
    key = str(input('请输入要查询的关键词：'))
    #proxy = "110.73.31.131:8123"
    pagestart = 1
    pageend = int(input('请输入结束页码(每页保存10条内容)'))
    listurl = getlisturl(key, pagestart, pageend)
    getcontent(listurl)


