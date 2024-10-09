import platform
import subprocess
from pathlib import Path
from typing import Union

FFMPEG_EXE = './ffmpeg/ffmpeg' if platform.system() == 'Linux' else './ffmpeg/ffmpeg.exe'


def get_video_info(video_path: Union[str, Path]):
    # subprocess.run([FFMPEG_EXE, '-i', video_path, '-hide_banner'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # subprocess.Popen([FFMPEG_EXE, '-i', video_path, '-hide_banner'])
    p = subprocess.Popen([FFMPEG_EXE, '-i', video_path, '-hide_banner'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print('out:', p.stdout.read())
    print('err:', p.stderr.read().decode('gbk'))


get_video_info('../static/video_app/2024-09-24/Crab_Rave.mp4.9ccd75eb2ae84bba885b543d1ce1df53')
