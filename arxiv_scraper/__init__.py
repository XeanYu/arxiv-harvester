"""
ArXiv论文爬虫包

一个用于从ArXiv网站抓取和解析学术论文信息的Python包。

主要功能：
- 抓取ArXiv论文列表
- 解析论文基本信息
- 获取论文摘要和详细内容
- 支持多种输出格式
"""

__version__ = "0.0.1"
__author__ = "XeanYu"

from .core.scraper import ArxivScraper
from .models.paper import Paper
from .config.settings import Config

__all__ = ["ArxivScraper", "Paper", "Config"] 