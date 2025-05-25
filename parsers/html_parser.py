"""
HTML解析器

负责解析ArXiv网页的HTML内容，提取论文信息。
"""

from bs4 import BeautifulSoup
from typing import List, Optional, Dict, Any, Generator
import logging

from models.paper import Paper, PaperContent
from utils.text_utils import (
    clean_text, 
    split_subjects, 
    extract_arxiv_id, 
    normalize_url,
    clean_html_content,
    extract_total_count as extract_count_from_text
)
from config.settings import Config


class ArxivHtmlParser:
    """ArXiv HTML解析器"""
    
    def __init__(self, parser: str = Config.HTML_PARSER):
        """
        初始化解析器
        
        Args:
            parser: BeautifulSoup解析器类型
        """
        self.parser = parser
        self.logger = logging.getLogger(__name__)
    
    def parse_html(self, html: str) -> BeautifulSoup:
        """
        解析HTML文本
        
        Args:
            html: HTML文本
            
        Returns:
            BeautifulSoup对象
        """
        return BeautifulSoup(html, self.parser)
    
    def extract_total_count(self, soup: BeautifulSoup) -> Optional[int]:
        """
        提取论文总数
        
        从HTML页面中的div class="paging"元素中提取总数信息，然后使用正则表达式提取数字。
        
        Args:
            soup: BeautifulSoup对象
            
        Returns:
            论文总数，如果未找到则返回None
        """
        try:
            # 从div class="paging"中获取总数信息
            paging_element = soup.find("div", {"class": "paging"})
            if paging_element:
                paging_text = paging_element.get_text(strip=True)
                self.logger.debug(f"找到paging元素，文本内容: {paging_text}")
                
                total_count = extract_count_from_text(paging_text)
                if total_count is not None:
                    self.logger.debug(f"从paging元素成功提取论文总数: {total_count}")
                    return total_count
                else:
                    self.logger.warning(f"无法从paging文本中提取总数: {paging_text}")
            else:
                self.logger.warning("未找到paging元素")
            
            return None
            
        except Exception as e:
            self.logger.error(f"提取论文总数失败: {e}")
            return None
    
    def parse_paper_list(self, soup: BeautifulSoup) -> List[Paper]:
        """
        解析论文列表
        
        Args:
            soup: BeautifulSoup对象
            
        Returns:
            论文列表
        """
        papers = []
        try:
            for paper in self._parse_papers_generator(soup):
                if paper:
                    papers.append(paper)
        except Exception as e:
            self.logger.error(f"解析论文列表失败: {e}")
        
        return papers
    
    def parse_papers_generator(self, soup: BeautifulSoup) -> Generator[Paper, None, None]:
        """
        生成器方式解析论文列表
        
        Args:
            soup: BeautifulSoup对象
            
        Yields:
            Paper对象
        """
        yield from self._parse_papers_generator(soup)
    
    def _parse_papers_generator(self, soup: BeautifulSoup) -> Generator[Paper, None, None]:
        """
        内部生成器方法
        
        Args:
            soup: BeautifulSoup对象
            
        Yields:
            Paper对象
        """
        articles_section = soup.find("dl", {"id": "articles"})
        if not articles_section:
            self.logger.warning("未找到论文列表区域")
            return
        
        papers_link = articles_section.find_all("dt")
        papers_detail = articles_section.find_all("dd")
        
        if len(papers_link) != len(papers_detail):
            self.logger.warning("论文链接和详情数量不匹配")
        
        for dt, dd in zip(papers_link, papers_detail):
            try:
                paper = self._parse_single_paper(dt, dd)
                if paper:
                    yield paper
            except Exception as e:
                self.logger.error(f"解析单个论文失败: {e}")
                continue
    
    def _parse_single_paper(self, dt_element, dd_element) -> Optional[Paper]:
        """
        解析单个论文
        
        Args:
            dt_element: 论文链接元素
            dd_element: 论文详情元素
            
        Returns:
            Paper对象
        """
        try:
            # 提取链接信息
            abs_link_element = dt_element.find("a", {"title": "Abstract"})
            if not abs_link_element:
                return None
            
            abs_link = normalize_url(abs_link_element["href"])
            arxiv_id = extract_arxiv_id(abs_link)
            
            # PDF链接
            pdf_link_element = dt_element.find("a", {"title": "Download PDF"})
            pdf_link = normalize_url(pdf_link_element["href"]) if pdf_link_element else None
            
            # HTML链接
            html_link_element = dt_element.find("a", {"title": "View HTML"})
            html_link = html_link_element.get("href") if html_link_element else None
            if html_link:
                html_link = normalize_url(html_link)
            
            # 提取详情信息
            title = self._extract_title(dd_element)
            authors = self._extract_authors(dd_element)
            comments = self._extract_comments(dd_element)
            subjects = self._extract_subjects(dd_element)
            
            return Paper(
                arxiv_id=arxiv_id,
                title=title,
                authors=authors,
                subjects=subjects,
                comments=comments,
                abs_link=abs_link,
                pdf_link=pdf_link,
                html_link=html_link
            )
        except Exception as e:
            self.logger.error(f"解析单个论文失败: {e}")
            return None
    
    def _extract_title(self, dd_element) -> str:
        """提取标题"""
        title_element = dd_element.find("div", {"class": "list-title"})
        if title_element:
            return clean_text(title_element.get_text(strip=True), "Title:")
        return ""
    
    def _extract_authors(self, dd_element) -> List[str]:
        """提取作者列表"""
        authors_element = dd_element.find("div", {"class": "list-authors"})
        if authors_element:
            author_links = authors_element.find_all("a")
            return [author.get_text(strip=True) for author in author_links]
        return []
    
    def _extract_comments(self, dd_element) -> str:
        """提取评论"""
        comments_element = dd_element.find("div", {"class": "list-comments"})
        if comments_element:
            return clean_text(comments_element.get_text(strip=True), "Comments:")
        return ""
    
    def _extract_subjects(self, dd_element) -> List[str]:
        """提取学科列表"""
        subjects_element = dd_element.find("div", {"class": "list-subjects"})
        if subjects_element:
            subjects_text = clean_text(subjects_element.get_text(strip=True), "Subjects:")
            return split_subjects(subjects_text)
        return []
    
    def parse_paper_abstract(self, soup: BeautifulSoup) -> str:
        """
        解析论文摘要
        
        Args:
            soup: 论文摘要页面的BeautifulSoup对象
            
        Returns:
            论文摘要
        """
        try:
            abstract_element = soup.find("blockquote", {"class": "abstract"})
            if abstract_element:
                return clean_text(abstract_element.get_text(strip=True), "Abstract:")
            return ""
        except Exception as e:
            self.logger.error(f"解析论文摘要失败: {e}")
            return ""
    
    def parse_paper_content(self, soup: BeautifulSoup, title: str = "") -> Optional[PaperContent]:
        """
        解析论文详细内容
        
        Args:
            soup: 论文HTML页面的BeautifulSoup对象
            title: 论文标题
            
        Returns:
            PaperContent对象
        """
        try:
            # 提取摘要
            abstract = ""
            abstract_element = soup.find("div", {"class": "ltx_abstract"})
            if abstract_element:
                abstract = abstract_element.get_text(strip=True)
            
            # 提取正文部分
            body_sections = self._extract_body_sections(soup)
            
            # 提取参考文献
            bibliography = self._extract_bibliography(soup)
            
            # 提取附录
            appendix_sections = self._extract_appendix_sections(soup)
            
            return PaperContent(
                title=title,
                abstract=abstract,
                body_sections=body_sections,
                bibliography=bibliography,
                appendix_sections=appendix_sections
            )
        except Exception as e:
            self.logger.error(f"解析论文详细内容失败: {e}")
            return None
    
    def _extract_body_sections(self, soup: BeautifulSoup) -> List[Dict[str, str]]:
        """提取正文部分"""
        sections = []
        try:
            body_sections = soup.find_all("section", {"class": "ltx_section"})
            for section in body_sections:
                title_element = section.find("h2", {"class": "ltx_title_section"})
                if title_element:
                    section_title = title_element.get_text(strip=True)
                    section_content = section.get_text(strip=True)
                    # 移除标题部分
                    section_content = section_content.replace(section_title, "", 1)
                    sections.append({section_title: section_content.strip()})
        except Exception as e:
            self.logger.error(f"提取正文部分失败: {e}")
        
        return sections
    
    def _extract_bibliography(self, soup: BeautifulSoup) -> List[str]:
        """提取参考文献"""
        bibliography = []
        try:
            bib_section = soup.find("section", {"class": "ltx_bibliography"})
            if bib_section:
                bib_items = bib_section.find_all("li", {"class": "ltx_bibitem"})
                bibliography = [item.get_text(strip=True) for item in bib_items]
        except Exception as e:
            self.logger.error(f"提取参考文献失败: {e}")
        
        return bibliography
    
    def _extract_appendix_sections(self, soup: BeautifulSoup) -> List[Dict[str, str]]:
        """提取附录部分"""
        appendix_sections = []
        try:
            appendix_elements = soup.find_all("section", {"class": "ltx_appendix"})
            for appendix in appendix_elements:
                title_element = appendix.find("h2", {"class": "ltx_title_appendix"})
                if title_element:
                    appendix_title = title_element.get_text(strip=True)
                    appendix_content = appendix.get_text(strip=True)
                    # 移除标题部分
                    appendix_content = appendix_content.replace(appendix_title, "", 1)
                    appendix_sections.append({appendix_title: appendix_content.strip()})
        except Exception as e:
            self.logger.error(f"提取附录部分失败: {e}")
        
        return appendix_sections 