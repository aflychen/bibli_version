import json

import re

# 利用正则表达式匹配出视频信息并转化成json
def get_video_info(text, pattern):
    match = re.search(pattern, text)
    return json.loads(match.group(1))

def get_video_info_title(text, pattern):
    match = re.search(pattern, text)
    return get_title(json.loads(match.group(1)+"}"))

def get_title(json):
     list=[]
     for titls  in json['videoData']['pages'] :
       list.append(titls['part'])
     return list
def getJson(JsonData,acc_quality):
    video_infos = {}
    # 获取视频质量
    video_infos['quality'] = JsonData['data']['accept_description'][acc_quality]
    # 获取视频时长
    video_infos['video_info']= JsonData['data']['dash']['duration']
    # 获取视频链接
    video_infos ['video_url'] = JsonData['data']['dash']['video'][acc_quality]['baseUrl']
    # 获取音频链接
    video_infos['audio_url'] = JsonData['data']['dash']['audio'][acc_quality]['baseUrl']
    # 计算视频时长
    video_time = int(video_infos.get('video_info',0))
    video_minute = video_time // 60
    video_second = video_time % 60
    print('当前下载视频清晰度为{}，时长{}分{}秒'.format(video_infos.get('quality',0), video_minute, video_second))
    return  video_infos