"""
视频操作

ffmpeg 命令
查看 FFMPEG 支持的编解码器：ffmpeg -codecs
查看 FFMPEG 支持的封装格式：ffmpeg -formats
"""
import dataclasses
import os
import platform
import queue
import re
import subprocess
import threading
from pathlib import Path
from typing import Union, Optional

# FFMPEG 路径
FFMPEG_DIR = os.path.join(os.path.dirname(__file__), 'ffmpeg')
if platform.system() == 'Linux':
    FFMPEG_EXE = os.path.join(FFMPEG_DIR, 'ffmpeg')
    ENCODING = 'UTF-8'
else:
    FFMPEG_EXE = os.path.join(FFMPEG_DIR, 'ffmpeg.exe')
    ENCODING = 'GBK'


@dataclasses.dataclass
class VideoInfo:
    """
    视频信息
    """
    video_name: str
    duration_str: str  # ffmpeg 输出的原始时间
    duration_seconds: float  # 转换为秒数
    bitrate: str
    encoding: str
    width: str
    height: str
    fps: int

    def __str__(self) -> str:
        return (f'时长：{self.duration_str} '
                f'编码：{self.encoding} '
                f'分辨率：{self.width}x{self.height} '
                f'帧率：{self.fps}')


def parse_ffmpeg_progress(line: str):
    """
    解析 ffmpeg 输出中的进度信息，并转换为秒数
    """
    match = re.match(r'frame.*time=(\d+:\d+:\d+\.\d+)',
                     line, flags=re.DOTALL)
    if match:
        # 将 "HH:MM:SS.ms" 格式转换为秒数
        time_str = match.group(1)
        hours, minutes, seconds = map(float, time_str.split(':'))
        return hours * 3600 + minutes * 60 + seconds
    return None


def stream_reader(popen: subprocess.Popen, total_duration: int, progress_q: queue.Queue):
    """
    读取 stderr 输出并计算进度百分比

    :param popen: 输入流对象
    :param total_duration: 总时长（秒）
    :param progress_q: 进度队列
    """
    buffer = ''
    while True:
        chunk = popen.stderr.read(256)
        if not chunk:
            break
        buffer += chunk.decode()
        # 检查是否有错误输出，停止子进程
        if 'Error' in buffer:
            print(buffer)
            if popen.poll() is None:
                popen.kill()
            progress_q.put(-1)
        # 查找 '\r' 代表的一行结束
        elif '\r' in buffer:
            # 按 '\r' 分割并获取最新的进度行
            lines = buffer.split('\r')
            buffer = lines[-1]  # 保留缓冲区中最后一部分（不完整的行）
            progress_output = lines[-2]  # 获取最后完整的一行
            # 解析进度并计算百分比
            current_time = parse_ffmpeg_progress(progress_output)
            if current_time:
                percent = (current_time / total_duration) * 100
                # print(f'Progress: {percent:.2f}%')
                progress_q.put(percent)
    progress_q.put(100)


class VideoOperator:
    """
    视频转换器

    :param video_path: 视频路径
    """
    # 解析 FFMPEG 输出的视频信息正则表达式
    VideoInfoReStr = (r'.+Duration: (?P<duration_str>\d+:\d+:\d+.\d+), start.+'
                      r'bitrate: (?P<bitrate>\d+) kb/s.+'
                      r'Video: (?P<encoding>.+?),.+, (?P<width>\d+)x(?P<height>\d+)'
                      r'.+, (?P<fps>\d+.?\d*) fps,.+')

    def __init__(self, video_path: Union[str, Path]):
        if not os.path.exists(FFMPEG_EXE):
            raise FileNotFoundError(f'FFmpeg executable not found at {FFMPEG_EXE}')
        if not os.path.exists(video_path):
            raise FileNotFoundError(f'Source video not found: {video_path}')
        self.source_video_path = video_path
        self.video_info = self.get_video_info()
        self.progress_q = queue.Queue()  # 创建一个队列接收进度信息

    def get_video_info(self) -> Optional[VideoInfo]:
        """
        获取视频信息
        """
        cmd = [FFMPEG_EXE, '-i', self.source_video_path, '-hide_banner']
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        _, stderr_data = p.communicate()  # FFMPEG 的所有输出信息都在 err 中
        video_info_str = stderr_data.decode()
        # 检查视频文件错误
        if 'Error opening input files: Invalid data found when processing input' in video_info_str:
            raise FileExistsError('Invalid data found when processing input')
        match_res = re.match(self.VideoInfoReStr, video_info_str, flags=re.DOTALL)
        if match_res:
            # 计算视频时长
            hours, minutes, seconds = map(float, match_res.groupdict()['duration_str'].split(':'))
            duration_time = hours * 3600 + minutes * 60 + seconds
            video_info = VideoInfo(
                video_name=os.path.basename(self.source_video_path),
                duration_seconds=duration_time,
                **match_res.groupdict())
            return video_info
        return None

    def convert_video(self, out_video_path: Union[str, Path],
                      video_decoder: str = None,
                      out_video_encoder: str = None,
                      out_video_format: str = None,
                      out_video_bitrate: int = None,
                      out_video_fps: str = None,
                      out_video_res: str = None):
        """
        视频转换

        :param out_video_path: 输出视频路径
        :param video_decoder: 输入视频解码器
        :param out_video_encoder: 输出视频编码器
        :param out_video_format: 输出视频格式
        :param out_video_bitrate: 输出视频码率
        :param out_video_fps: 输出视频帧率
        :param out_video_res: 输出视频分辨率
        :return: 
        """
        cmd = [FFMPEG_EXE]
        if video_decoder:
            cmd.extend(['-c:v', video_decoder])  # h264_qsv
        cmd.extend(['-i', self.source_video_path, '-hide_banner', '-y'])
        if out_video_encoder:
            cmd.extend(['-c:v', out_video_encoder])
        if out_video_format:
            cmd.extend(['-f', out_video_format])
        if out_video_bitrate:
            cmd.extend(['-b:v', f'{out_video_bitrate}k'])
        if out_video_fps:
            cmd.extend(['-r', out_video_fps])
        if out_video_res:
            cmd.extend(['-s', out_video_res])
        cmd.append(out_video_path)
        # print(cmd)
        # print(' '.join(cmd))
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stderr_thread = threading.Thread(
            target=stream_reader,
            args=(p, self.video_info.duration_seconds, self.progress_q)
        )
        stderr_thread.start()


if __name__ == '__main__':
    video_path = r'C:\Users\sjdd\Downloads\Crab_Rave.mp4'
    vo = VideoOperator(video_path)
    print(vo.video_info)
