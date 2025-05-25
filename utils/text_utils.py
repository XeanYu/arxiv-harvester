"""
文本处理工具

提供各种文本处理和清理功能。
"""

import re
import math
from typing import Optional, List, Generator


def extract_total_count(text: str) -> Optional[int]:
    """
    从文本中提取总数
    
    支持多种格式：
    - "Total of 123 entries"
    - "showing first 50 of 768 entries"
    - "123 entries"
    
    Args:
        text: 包含总数信息的文本
        
    Returns:
        提取的总数，如果未找到则返回None
        
    Examples:
        >>> extract_total_count("Total of 123 entries")
        123
        >>> extract_total_count("showing first 50 of 768 entries")
        768
        >>> extract_total_count("No entries found")
        None
    """
    if not text:
        return None
    
    # 正则表达式模式列表，按优先级排序
    patterns = [
        r'Total of (\d+) entries',  # "Total of 123 entries"
        r'showing first \d+ of (\d+) entries',  # "showing first 50 of 768 entries"
        r'of (\d+) entries',  # "of 123 entries"
        r'(\d+) entries',  # "123 entries"
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return int(match.group(1))
    
    return None


def clean_text(text: str, remove_prefix: str = "") -> str:
    """
    清理文本内容
    
    Args:
        text: 原始文本
        remove_prefix: 要移除的前缀
        
    Returns:
        清理后的文本
    """
    if not text:
        return ""
    
    # 移除前缀
    if remove_prefix and text.startswith(remove_prefix):
        text = text[len(remove_prefix):]
    
    # 清理空白字符
    return text.strip()


def split_subjects(subjects_text: str, delimiter: str = ";") -> List[str]:
    """
    分割学科文本
    
    Args:
        subjects_text: 学科文本
        delimiter: 分隔符
        
    Returns:
        学科列表
    """
    if not subjects_text:
        return []
    
    subjects = subjects_text.split(delimiter)
    return [subject.strip() for subject in subjects if subject.strip()]


def generate_page_params(total_count: int, 
                        papers_per_page: int = 50) -> Generator[str, None, None]:
    """
    生成分页参数
    
    Args:
        total_count: 总论文数
        papers_per_page: 每页论文数
        
    Yields:
        分页参数字符串
        
    Examples:
        >>> list(generate_page_params(120, 50))
        ['?skip=0&show=50', '?skip=50&show=50', '?skip=100&show=50']
    """
    if total_count <= papers_per_page:
        yield f"?skip=0&show={papers_per_page}"
        return
    
    total_pages = math.ceil(total_count / papers_per_page)
    
    for page in range(total_pages):
        skip = page * papers_per_page
        yield f"?skip={skip}&show={papers_per_page}"


def extract_arxiv_id(abs_link: str) -> str:
    """
    从摘要链接中提取ArXiv ID
    
    Args:
        abs_link: 摘要链接
        
    Returns:
        ArXiv ID
        
    Examples:
        >>> extract_arxiv_id("https://arxiv.org/abs/2301.12345")
        "2301.12345"
    """
    if not abs_link:
        return ""
    
    return abs_link.split("/")[-1]


def normalize_url(url: str, base_url: str = "https://arxiv.org") -> str:
    """
    标准化URL
    
    Args:
        url: 原始URL
        base_url: 基础URL
        
    Returns:
        标准化后的URL
    """
    if not url:
        return ""
    
    if url.startswith("http"):
        return url
    
    if url.startswith("/"):
        return base_url + url
    
    return base_url + "/" + url


def clean_html_content(content: str) -> str:
    """
    清理HTML内容中的特殊字符和无用信息
    
    Args:
        content: HTML内容
        
    Returns:
        清理后的内容
    """
    if not content:
        return ""
    
    # 移除特定的无用文本
    content = content.replace("Report issue for preceding element", "")
    
    # 清理多余的空白字符
    content = re.sub(r'\s+', ' ', content)
    
    return content.strip() 