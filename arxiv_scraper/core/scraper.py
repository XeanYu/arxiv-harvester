"""
ArXiv爬虫核心类

提供完整的ArXiv论文抓取功能。
"""

import logging
from typing import List, Optional, Generator, Dict, Any

from ..models.paper import Paper, PaperContent
from ..parsers.html_parser import ArxivHtmlParser
from ..utils.http_client import HttpClient, get_html
from ..utils.text_utils import generate_page_params
from ..config.settings import Config


class ArxivScraper:
    """ArXiv论文爬虫"""
    
    def __init__(self, 
                 http_client: Optional[HttpClient] = None,
                 html_parser: Optional[ArxivHtmlParser] = None):
        """
        初始化爬虫
        
        Args:
            http_client: HTTP客户端实例
            html_parser: HTML解析器实例
        """
        self.http_client = http_client or HttpClient()
        self.html_parser = html_parser or ArxivHtmlParser()
        self.logger = logging.getLogger(__name__)
    
    def get_papers_from_category(self, 
                                category: str, 
                                include_abstract: bool = False,
                                include_content: bool = False,
                                max_papers: Optional[int] = None) -> List[Paper]:
        """
        从指定类别获取论文列表
        
        Args:
            category: 论文类别 (如 'cs_recent', 'cs_new')
            include_abstract: 是否包含摘要
            include_content: 是否包含详细内容
            max_papers: 最大论文数量限制
            
        Returns:
            论文列表
        """
        url = Config.get_arxiv_url(category)
        if not url:
            raise ValueError(f"不支持的类别: {category}")
        
        self.logger.info(f"开始抓取类别 {category} 的论文")
        
        # 获取第一页以确定总数
        html = self.http_client.get_text(url)
        soup = self.html_parser.parse_html(html)
        total_count = self.html_parser.extract_total_count(soup)
        
        if total_count is None:
            self.logger.warning("无法获取论文总数")
            total_count = Config.PAPERS_PER_PAGE
        
        self.logger.info(f"发现 {total_count} 篇论文")
        
        # 如果设置了最大数量限制
        if max_papers and max_papers < total_count:
            total_count = max_papers
        
        papers = []
        collected_count = 0
        
        # 分页获取论文
        for page_param in generate_page_params(total_count, Config.PAPERS_PER_PAGE):
            if max_papers and collected_count >= max_papers:
                break
            
            page_url = url + page_param
            self.logger.debug(f"抓取页面: {page_url}")
            
            try:
                page_html = self.http_client.get_text(page_url)
                page_soup = self.html_parser.parse_html(page_html)
                page_papers = self.html_parser.parse_paper_list(page_soup)
                
                for paper in page_papers:
                    if max_papers and collected_count >= max_papers:
                        break
                    
                    # 获取摘要
                    if include_abstract and paper.abs_link:
                        paper.abstract = self.get_paper_abstract(paper.abs_link)
                    
                    # 获取详细内容
                    if include_content and paper.html_link:
                        content = self.get_paper_content(paper.html_link, paper.title)
                        if content:
                            paper.full_content = content.to_dict()
                    
                    papers.append(paper)
                    collected_count += 1
                
            except Exception as e:
                self.logger.error(f"抓取页面失败: {page_url}, 错误: {e}")
                continue
        
        self.logger.info(f"成功抓取 {len(papers)} 篇论文")
        return papers
    
    def get_papers_generator(self, 
                           category: str,
                           include_abstract: bool = False,
                           include_content: bool = False,
                           max_papers: Optional[int] = None) -> Generator[Paper, None, None]:
        """
        生成器方式获取论文
        
        Args:
            category: 论文类别
            include_abstract: 是否包含摘要
            include_content: 是否包含详细内容
            max_papers: 最大论文数量限制
            
        Yields:
            Paper对象
        """
        url = Config.get_arxiv_url(category)
        if not url:
            raise ValueError(f"不支持的类别: {category}")
        
        self.logger.info(f"开始生成器方式抓取类别 {category} 的论文")
        
        # 获取第一页以确定总数
        html = self.http_client.get_text(url)
        soup = self.html_parser.parse_html(html)
        total_count = self.html_parser.extract_total_count(soup)
        
        if total_count is None:
            total_count = Config.PAPERS_PER_PAGE
        
        if max_papers and max_papers < total_count:
            total_count = max_papers
        
        collected_count = 0
        
        # 分页获取论文
        for page_param in generate_page_params(total_count, Config.PAPERS_PER_PAGE):
            if max_papers and collected_count >= max_papers:
                break
            
            page_url = url + page_param
            
            try:
                page_html = self.http_client.get_text(page_url)
                page_soup = self.html_parser.parse_html(page_html)
                
                for paper in self.html_parser.parse_papers_generator(page_soup):
                    if max_papers and collected_count >= max_papers:
                        break
                    
                    # 获取摘要
                    if include_abstract and paper.abs_link:
                        paper.abstract = self.get_paper_abstract(paper.abs_link)
                    
                    # 获取详细内容
                    if include_content and paper.html_link:
                        content = self.get_paper_content(paper.html_link, paper.title)
                        if content:
                            paper.full_content = content.to_dict()
                    
                    yield paper
                    collected_count += 1
                
            except Exception as e:
                self.logger.error(f"抓取页面失败: {page_url}, 错误: {e}")
                continue
    
    def get_paper_abstract(self, abs_url: str) -> str:
        """
        获取论文摘要
        
        Args:
            abs_url: 摘要页面URL
            
        Returns:
            论文摘要
        """
        try:
            html = self.http_client.get_text(abs_url)
            soup = self.html_parser.parse_html(html)
            return self.html_parser.parse_paper_abstract(soup)
        except Exception as e:
            self.logger.error(f"获取论文摘要失败: {abs_url}, 错误: {e}")
            return ""
    
    def get_paper_content(self, html_url: str, title: str = "") -> Optional[PaperContent]:
        """
        获取论文详细内容
        
        Args:
            html_url: 论文HTML页面URL
            title: 论文标题
            
        Returns:
            PaperContent对象
        """
        try:
            html = self.http_client.get_text(html_url)
            soup = self.html_parser.parse_html(html)
            return self.html_parser.parse_paper_content(soup, title)
        except Exception as e:
            self.logger.error(f"获取论文详细内容失败: {html_url}, 错误: {e}")
            return None
    
    def get_supported_categories(self) -> List[str]:
        """
        获取支持的论文类别
        
        Returns:
            类别列表
        """
        return Config.get_all_categories()
    
    def close(self):
        """关闭爬虫，释放资源"""
        if hasattr(self.http_client, 'close'):
            self.http_client.close()
    
    def __enter__(self):
        """上下文管理器入口"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """上下文管理器出口"""
        self.close() 