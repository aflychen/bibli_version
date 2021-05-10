from random import choice
import requests
from lxml import etree
from bilibili_version import JsonUtil
from bilibili_version import FileUtil
from bilibili_version import VideoUtil
import time
from concurrent.futures import ThreadPoolExecutor

# 设置请求头等参数，防止被反爬
def getHeaders():
    headers = {
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36'
    }
    return headers


# 请求视频
def getVideRequest(referer_url, video_url):
    headers = getHeaders()
    headers.update({"Referer": referer_url})
    return requests.get(video_url, headers=headers)


# 随机获取一个用户的代理
def get_user_random_agent():
    # 获取随机用户代理
    user_agents = [
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
        "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
        "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
        "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
        "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
        "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
        "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
        "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 LBBROWSER",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; 360SE)",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
        "Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5",
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b13pre) Gecko/20110307 Firefox/4.0b13pre",
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:16.0) Gecko/20100101 Firefox/16.0",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
        "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10",
        "MQQBrowser/26 Mozilla/5.0 (Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1",
        "Mozilla/5.0 (Linux; Android 5.1.1; Nexus 6 Build/LYZ28E) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.23 Mobile Safari/537.36",
        "Mozilla/5.0 (iPod; U; CPU iPhone OS 2_1 like Mac OS X; ja-jp) AppleWebKit/525.18.1 (KHTML, like Gecko) Version/3.1.1 Mobile/5F137 Safari/525.20",
        "Mozilla/5.0 (Linux;u;Android 4.2.2;zh-cn;) AppleWebKit/534.46 (KHTML,like Gecko) Version/5.1 Mobile Safari/10600.6.3 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)",
        "Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html��"
    ]
    # 在user_agent列表中随机产生一个代理，作为模拟的浏览器
    user_agent = choice(user_agents)
    return user_agent


def getRequestHtml(origin_video_url):
    res_data = requests.get(origin_video_url, headers=getHeaders())
    # 判断异常请求
    if res_data.ok != True:
        print("请求的页面 " + origin_video_url + "  异常请检查")
        return
    return res_data


def single_download(quality,referer_url,res):

    res_data = getRequestHtml( referer_url)
    res_html = etree.HTML(res_data.text)
    # 获取当前视频的title
    if res =="":
        title = res_html.xpath('//*[@id="viewbox_report"]/h1/span/text()')[0]
        print("您当前正在下载,", title)
    else:
        title=res

    # 获取视频信息
    video_info_temp = JsonUtil.get_video_info(res_data.text, '__playinfo__=(.*?)</script><script>')

    video_info = JsonUtil.getJson(video_info_temp, quality)

    VideoUtil.download_video_single(referer_url, video_info.get('video_url', 0), video_info.get('audio_url', 0), title)


def multiple_download(id, quality):
    aids = id.split(' ')
    for aid in aids:

        single_download( quality, 'https://www.bilibili.com/video/' + aid,"")



def batch_download(id, quality):
    res_data = getRequestHtml('https://www.bilibili.com/video/' + id + '?p=%d' % (1))
    res_html = etree.HTML(res_data.text)
    title_list = JsonUtil.get_video_info_title(res_data.text, '__INITIAL_STATE__=(.*?),"insertScripts":')
    # 获取当前视频的title
    video_name_list = res_html.xpath('//*[@id="multi_page"]/div[2]/ul/li')
    print('共下载视频{}个'.format(len(video_name_list)))
    pool = ThreadPoolExecutor(12)
    for i  in range(0, len(video_name_list)):
        # 请求视频，获取信息
        res = requests.get('https://www.bilibili.com/video/' + id + '?p=%d' % (i+1), headers=getHeaders())
        # 解析出视频详情的json
        video_info_temp = JsonUtil.get_video_info(res.text, '__playinfo__=(.*?)</script><script>')

        video_infos = {}
        # 获取视频质量
        video_infos['quality'] = video_info_temp['data']['accept_description'][quality]
        # 获取视频时长
        video_infos['video_info']= video_info_temp['data']['dash']['duration']
        # 获取视频链接
        video_infos ['video_url'] = video_info_temp['data']['dash']['video'][quality]['baseUrl']
        # 获取音频链接
        video_infos['audio_url'] = video_info_temp['data']['dash']['audio'][quality]['baseUrl']
        # 计算视频时长
        video_time = int(video_infos.get('video_info',0))
        video_minute = video_time // 60
        video_second = video_time % 60
        print('当前下载视频清晰度为{}，时长{}分{}秒'.format(video_infos.get('quality',0), video_minute, video_second))
        title=title_list[i]
        # 获取视频信息
        pool.submit(download_video_batch,'https://www.bilibili.com/video/' + id + '?p=%d' % (i+1),video_infos.get('video_url', 0), video_infos.get('audio_url', 0),title, i+1)

    pool.shutdown(wait=True)



def download_video_batch(referer_url, video_url, audio_url, video_name, index):
    '''批量下载系列视频'''
    # 更新请求头
    headers = {
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36'
    }
    headers.update({"Referer": referer_url})

    print("%d.\t视频下载开始：%s" % (index, video_name))
    # 下载并保存视频
    video_content = requests.get(video_url, headers=headers)
    print('%d.\t%s\t视频大小：' % (index, video_name),
          round(int(video_content.headers.get('content-length', 0)) / 1024 / 1024, 2), '\tMB')
    received_video = 0
    with open("bilibili_version/video_final/"+'%s_video.mp4' % video_name, 'ab') as output:
        headers['Range'] = 'bytes=' + str(received_video) + '-'
        response = requests.get(video_url, headers=headers)
        output.write(response.content)
    # 下载并保存音频
    audio_content = requests.get(audio_url, headers=headers)
    print('%d.\t%s\t音频大小：' % (index, video_name),
          round(int(audio_content.headers.get('content-length', 0)) / 1024 / 1024, 2), '\tMB')
    received_audio = 0
    with open("bilibili_version/video_final/"+'%s_audio.mp4' % video_name, 'ab') as output:
        headers['Range'] = 'bytes=' + str(received_audio) + '-'
        response = requests.get(audio_url, headers=headers)
        output.write(response.content)
        received_audio += len(response.content)
    import subprocess
    # video_final = video_name.replace('video', 'video_final')
    command = 'ffmpeg -i %s_video.mp4 -i %s_audio.mp4 -c copy %s.mp4 -y -loglevel quiet' % (
        "bilibili_version/video_final/"+video_name, "bilibili_version/video_final/"+video_name, "bilibili_version/video/"+video_name)
    subprocess.Popen(command, shell=True)

    # return video_name, index

