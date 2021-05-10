import shutil
import os
import time
# 下载视频
def out_received_video(response, video_name, outFile):
    with open(outFile + '%s_video.mp4' % video_name, 'ab') as output:
        output.write(response.content)
    print("视频下载结束：%s" % video_name)


# 下载音频
def out_received_audio(response, video_name, outFile):
    with open(outFile+'%s_audio.mp4' % video_name, 'ab') as output:
        output.write(response.content)
    print("音频下载结束：%s" % video_name)

def video_audio_merge_single(video_name,outFile):
    '''使用ffmpeg单个视频音频合并'''
    print("视频合成开始：%s" % video_name)
    import subprocess
    command = 'ffmpeg -i %s_video.mp4 -i %s_audio.mp4 -c copy %s.mp4 -y -loglevel quiet' % (
        outFile+video_name, outFile+video_name, "bilibili_version/video/"+video_name)
    subprocess.Popen(command)
    print("视频合成结束：%s" % video_name)

def video_audio_merge_batch(result):
    '''使用ffmpeg批量视频音频合并'''
    video_name = result.result()[0]

    import subprocess
    # video_final = video_name.replace('video', 'video_final')
    command = 'ffmpeg -i %s_video.mp4 -i %s_audio.mp4 -c copy %s.mp4 -y -loglevel quiet' % (
        "bilibili_version/video_final/"+video_name, "bilibili_version/video_final/"+video_name, "bilibili_version/video/"+video_name)
    subprocess.Popen(command, shell=True)
    print(command)
    print("视频下载结束：%s" % (video_name))

# 删除文件
def remove(outFile):
    shutil.rmtree(outFile)

def create_folder(output):
    '''创建文件夹'''
    if not os.path.exists(output):
        os.mkdir(output)