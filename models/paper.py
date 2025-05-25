"""
论文数据模型

定义论文相关的数据结构和模型。
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from datetime import datetime


@dataclass
class Paper:
    """论文数据模型"""
    
    arxiv_id: str
    title: str
    authors: List[str]
    abstract: str = ""
    subjects: List[str] = field(default_factory=list)
    comments: str = ""
    abs_link: str = ""
    pdf_link: Optional[str] = None
    html_link: Optional[str] = None
    submission_date: Optional[datetime] = None
    
    # 详细内容（可选）
    full_content: Optional[Dict[str, Any]] = None
    
    def __post_init__(self):
        """初始化后处理"""
        # 清理标题
        if self.title:
            self.title = self.title.strip()
        
        # 清理作者列表
        self.authors = [author.strip() for author in self.authors if author.strip()]
        
        # 清理学科列表
        self.subjects = [subject.strip() for subject in self.subjects if subject.strip()]
    
    @property
    def has_pdf(self) -> bool:
        """是否有PDF链接"""
        return bool(self.pdf_link)
    
    @property
    def has_html(self) -> bool:
        """是否有HTML链接"""
        return bool(self.html_link)
    
    @property
    def primary_subject(self) -> str:
        """主要学科"""
        return self.subjects[0] if self.subjects else ""
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            "arxiv_id": self.arxiv_id,
            "title": self.title,
            "authors": self.authors,
            "abstract": self.abstract,
            "subjects": self.subjects,
            "comments": self.comments,
            "abs_link": self.abs_link,
            "pdf_link": self.pdf_link,
            "html_link": self.html_link,
            "submission_date": self.submission_date.isoformat() if self.submission_date else None,
            "has_pdf": self.has_pdf,
            "has_html": self.has_html,
            "primary_subject": self.primary_subject,
            "full_content": self.full_content
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Paper":
        """从字典创建Paper实例"""
        submission_date = None
        if data.get("submission_date"):
            submission_date = datetime.fromisoformat(data["submission_date"])
        
        return cls(
            arxiv_id=data["arxiv_id"],
            title=data["title"],
            authors=data["authors"],
            abstract=data.get("abstract", ""),
            subjects=data.get("subjects", []),
            comments=data.get("comments", ""),
            abs_link=data.get("abs_link", ""),
            pdf_link=data.get("pdf_link"),
            html_link=data.get("html_link"),
            submission_date=submission_date,
            full_content=data.get("full_content")
        )


@dataclass
class PaperContent:
    """论文详细内容模型"""
    
    title: str
    abstract: str
    body_sections: List[Dict[str, str]] = field(default_factory=list)
    bibliography: List[str] = field(default_factory=list)
    appendix_sections: List[Dict[str, str]] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            "title": self.title,
            "abstract": self.abstract,
            "body_sections": self.body_sections,
            "bibliography": self.bibliography,
            "appendix_sections": self.appendix_sections
        } 