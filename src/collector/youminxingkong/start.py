"""
    Created by howie.hu at 2022-02-08.
    Description: 抓取目标链接的目录信息
        - 命令: PIPENV_DOTENV_LOCATION=./pro.env pipenv run python src/collector/book_common/start.py
    Changelog: all notable changes to this file will be documented
"""

import time

from src.collector.utils import load_data_to_articlles
from src.common.remote import get_html_by_requests
from src.config import Config
from src.processor.text_utils import (
    extract_youminxingkong_news,
    extract_keyword_list,
    html_to_text_h2t,
)
from src.utils.log import LOGGER
from src.utils.tools import md5_encryption, text_compress


def run(collect_config: dict):
    """游民星空抓取爬虫

    Args:
        collect_config (dict, optional): 采集器配置
    """
    source_name = "游民星空"
    delta_time = collect_config.get("delta_time", 5)
    url = "https://www.gamersky.com/news/"
    resp_text = get_html_by_requests(url)
    all_news = extract_youminxingkong_news(html=resp_text)
    for item in all_news:
        doc_name = item.get("title")
        doc_link = item.get("url")
        # 休眠
        time.sleep(delta_time)
        input_data = {
            "doc_date": item.get("dt"),
            "doc_image": item.get("cover_img"),
            "doc_name": doc_name,
            "doc_ts": int(time.time()),
            "doc_link": doc_link,
            "doc_source_meta_list": [],
            "doc_keywords": " ".join(extract_keyword_list(html_to_text_h2t(resp_text))),
            "doc_des": item.get("desc"),
            "doc_type": "youminxingkong",
            "doc_author": "",
            "doc_source_name": source_name,
            "doc_id": md5_encryption(f"{doc_name}_{source_name}"),
            "doc_source": "liuli_youminxingkong",
            "doc_content": "",
            "doc_html": "",
        }
        # 持久化，必须执行
        load_data_to_articlles(input_data)
    msg = "🤗 liuli_youminxingkong 采集器执行完毕"
    LOGGER.info(msg)


if __name__ == "__main__":
    t_cc = {
        "book_dict": {"谁还不是个修行者了": "http://www.bqxs520.com/112386/"},
        "delta_time": 5,
        "latest_chapter_nums": 3,
    }
    run(t_cc)
