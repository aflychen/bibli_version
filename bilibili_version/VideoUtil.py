from bilibili_version import RequestUtil
from bilibili_version import FileUtil


def download_video_single(referer_url, video_url, audio_url, video_name):
    print("视频下载开始：%s" % video_name)
    video_content = RequestUtil.getVideRequest(referer_url, video_url)
    print('%s\t视频大小：' % video_name, round(int(video_content.headers.get('content-length', 0)) / 1024 / 1024, 2), '\tMB')
    FileUtil.out_received_video(video_content, video_name, "bilibili_version/video_final/")
    print("音频下载开始：%s" % video_name)
    audio_content = RequestUtil.getVideRequest(referer_url, audio_url)
    print('%s\t音频大小：' % video_name, round(int(audio_content.headers.get('content-length', 0)) / 1024 / 1024, 2), '\tMB')
    FileUtil.out_received_audio(audio_content, video_name, "bilibili_version/video_final/")
    FileUtil.video_audio_merge_single(video_name, "bilibili_version/video_final/")


