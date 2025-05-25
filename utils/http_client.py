"""
HTTP客户端工具

提供统一的HTTP请求功能，包含重试机制和错误处理。
"""

import requests
import time
import logging
from typing import Optional, Dict, Any
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from ..config.settings import Config


class HttpClient:
    """HTTP客户端类"""
    
    def __init__(self, 
                 timeout: int = Config.REQUEST_TIMEOUT,
                 max_retries: int = Config.MAX_RETRIES,
                 retry_delay: float = Config.RETRY_DELAY,
                 headers: Optional[Dict[str, str]] = None):
        """
        初始化HTTP客户端
        
        Args:
            timeout: 请求超时时间
            max_retries: 最大重试次数
            retry_delay: 重试延迟时间
            headers: 默认请求头
        """
        self.timeout = timeout
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.logger = logging.getLogger(__name__)
        
        # 创建session
        self.session = requests.Session()
        
        # 设置默认请求头
        default_headers = Config.REQUEST_HEADERS.copy()
        if headers:
            default_headers.update(headers)
        self.session.headers.update(default_headers)
        
        # 配置重试策略
        retry_strategy = Retry(
            total=max_retries,
            backoff_factor=retry_delay,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
    
    def get(self, url: str, **kwargs) -> requests.Response:
        """
        发送GET请求
        
        Args:
            url: 请求URL
            **kwargs: 其他请求参数
            
        Returns:
            Response对象
            
        Raises:
            requests.RequestException: 请求失败
        """
        try:
            self.logger.debug(f"发送GET请求: {url}")
            response = self.session.get(url, timeout=self.timeout, **kwargs)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            self.logger.error(f"请求失败: {url}, 错误: {e}")
            raise
    
    def get_text(self, url: str, **kwargs) -> str:
        """
        获取页面文本内容
        
        Args:
            url: 请求URL
            **kwargs: 其他请求参数
            
        Returns:
            页面文本内容
        """
        response = self.get(url, **kwargs)
        return response.text
    
    def close(self):
        """关闭session"""
        self.session.close()
    
    def __enter__(self):
        """上下文管理器入口"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """上下文管理器出口"""
        self.close()


# 全局HTTP客户端实例
_default_client = None


def get_default_client() -> HttpClient:
    """获取默认的HTTP客户端实例"""
    global _default_client
    if _default_client is None:
        _default_client = HttpClient()
    return _default_client


def get_html(url: str, client: Optional[HttpClient] = None) -> str:
    """
    获取网页HTML内容的便捷函数
    
    Args:
        url: 网页URL
        client: HTTP客户端实例，如果为None则使用默认客户端
        
    Returns:
        HTML文本内容
    """
    if client is None:
        client = get_default_client()
    return client.get_text(url) 