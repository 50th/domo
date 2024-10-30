import datetime
import hashlib
import logging
from pathlib import Path

from django.core.files.uploadedfile import TemporaryUploadedFile
from magika import Magika

from sumy.nlp.tokenizers import Tokenizer
from sumy.parsers.plaintext import PlaintextParser
# from sumy.summarizers.lex_rank import LexRankSummarizer
# from sumy.summarizers.lsa import LsaSummarizer
from sumy.summarizers.text_rank import TextRankSummarizer

logger = logging.getLogger(__name__)


def generate_article(content: str) -> str:
    """
    根据文章内容生成文章摘要
    :param content: 文章内容
    """
    # 使用 sumy 库提取文章摘要信息
    # 初始化解析器
    parser = PlaintextParser.from_string(content, Tokenizer('chinese'))
    # 初始化摘要器
    summarizer = TextRankSummarizer()
    # 使用摘要器提取摘要
    summary = summarizer(parser.document, 3)  # 这里的 3 表示你想要的摘要句子的数量
    if summary:
        abstract = ''.join([str(_) for _ in summary])
    else:
        abstract = content[:50] + '...'
    return abstract


def save_article_file(title: str, content: str, file_dir: Path) -> Path:
    """
    将数据另外单独保存为文件
    :param title: 文章标题
    :param content: 文章内容
    :param file_dir: 保存目录
    """
    if not file_dir.exists():
        file_dir.mkdir(parents=True)
    file_path = file_dir / f'{title}_{datetime.datetime.now().timestamp()}.md'
    with open(file_path, 'w', encoding='utf-8') as wf:
        wf.write(content)
    return file_path


def check_file_type(file: TemporaryUploadedFile = None):
    m = Magika()
    res = m.identify_bytes(file.read())
    logger.info('%s file type: %s',  file.name, res.output)
    return f'{res.output.ct_label}: {res.output.description}'


def generate_md5(content) -> str:
    """
    生成 md5 值
    :param content:
    :return:
    """
    md5_hash = hashlib.md5()
    while chunk := content.read(512 * 1024):
        md5_hash.update(chunk)  # 更新 MD5 值
    return md5_hash.hexdigest()
