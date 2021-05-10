#导入自己的工具类
from bilibili_version import RequestUtil
from bilibili_version import FileUtil
import time


def main(version, id,quality):
    if version == "单个":
        FileUtil.create_folder("bilibili_version/video_final/")
        FileUtil.create_folder("bilibili_version/video/")
        RequestUtil.single_download(quality,'https://www.bilibili.com/video/'+id,"")
        # 删除临时文件
        time.sleep(5)
        FileUtil.remove("bilibili_version/video_final")
    elif version=="批量":
        FileUtil.create_folder("bilibili_version/video_final/")
        FileUtil.create_folder("bilibili_version/video/")
        RequestUtil.multiple_download(id,quality)
        time.sleep(5)
        FileUtil.remove("bilibili_version/video_final")
    elif version=="系列":
        FileUtil.create_folder("bilibili_version/video_final/")
        FileUtil.create_folder("bilibili_version/video/")
        RequestUtil.batch_download(id,quality)
        time.sleep(5)
        FileUtil.remove("bilibili_version/video_final")