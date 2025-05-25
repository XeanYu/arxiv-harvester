"""
配置文件

包含ArXiv爬虫的所有配置常量和设置。
"""

from typing import Dict, Any
import os


class Config:
    """配置类，包含所有的配置常量"""
    
    # ArXiv URL配置 - 支持所有主要类别
    ARXIV_URLS = {
        # 计算机科学 (Computer Science)
        "cs_recent": "https://arxiv.org/list/cs/recent",
        "cs_new": "https://arxiv.org/list/cs/new",
        
        # 数学 (Mathematics)
        "math_recent": "https://arxiv.org/list/math/recent",
        "math_new": "https://arxiv.org/list/math/new",
        
        # 物理 (Physics)
        "physics_recent": "https://arxiv.org/list/physics/recent",
        "physics_new": "https://arxiv.org/list/physics/new",
        
        # 天体物理 (Astrophysics)
        "astro-ph_recent": "https://arxiv.org/list/astro-ph/recent",
        "astro-ph_new": "https://arxiv.org/list/astro-ph/new",
        
        # 凝聚态物理 (Condensed Matter)
        "cond-mat_recent": "https://arxiv.org/list/cond-mat/recent",
        "cond-mat_new": "https://arxiv.org/list/cond-mat/new",
        
        # 广义相对论和量子宇宙学 (General Relativity and Quantum Cosmology)
        "gr-qc_recent": "https://arxiv.org/list/gr-qc/recent",
        "gr-qc_new": "https://arxiv.org/list/gr-qc/new",
        
        # 高能物理 - 实验 (High Energy Physics - Experiment)
        "hep-ex_recent": "https://arxiv.org/list/hep-ex/recent",
        "hep-ex_new": "https://arxiv.org/list/hep-ex/new",
        
        # 高能物理 - 格点 (High Energy Physics - Lattice)
        "hep-lat_recent": "https://arxiv.org/list/hep-lat/recent",
        "hep-lat_new": "https://arxiv.org/list/hep-lat/new",
        
        # 高能物理 - 现象学 (High Energy Physics - Phenomenology)
        "hep-ph_recent": "https://arxiv.org/list/hep-ph/recent",
        "hep-ph_new": "https://arxiv.org/list/hep-ph/new",
        
        # 高能物理 - 理论 (High Energy Physics - Theory)
        "hep-th_recent": "https://arxiv.org/list/hep-th/recent",
        "hep-th_new": "https://arxiv.org/list/hep-th/new",
        
        # 数学物理 (Mathematical Physics)
        "math-ph_recent": "https://arxiv.org/list/math-ph/recent",
        "math-ph_new": "https://arxiv.org/list/math-ph/new",
        
        # 非线性科学 (Nonlinear Sciences)
        "nlin_recent": "https://arxiv.org/list/nlin/recent",
        "nlin_new": "https://arxiv.org/list/nlin/new",
        
        # 核理论 (Nuclear Theory)
        "nucl-th_recent": "https://arxiv.org/list/nucl-th/recent",
        "nucl-th_new": "https://arxiv.org/list/nucl-th/new",
        
        # 核实验 (Nuclear Experiment)
        "nucl-ex_recent": "https://arxiv.org/list/nucl-ex/recent",
        "nucl-ex_new": "https://arxiv.org/list/nucl-ex/new",
        
        # 量子物理 (Quantum Physics)
        "quant-ph_recent": "https://arxiv.org/list/quant-ph/recent",
        "quant-ph_new": "https://arxiv.org/list/quant-ph/new",
        
        # 统计力学 (Statistical Mechanics)
        "stat_recent": "https://arxiv.org/list/stat/recent",
        "stat_new": "https://arxiv.org/list/stat/new",
        
        # 电气工程和系统科学 (Electrical Engineering and Systems Science)
        "eess_recent": "https://arxiv.org/list/eess/recent",
        "eess_new": "https://arxiv.org/list/eess/new",
        
        # 经济学 (Economics)
        "econ_recent": "https://arxiv.org/list/econ/recent",
        "econ_new": "https://arxiv.org/list/econ/new",
        
        # 定量生物学 (Quantitative Biology)
        "q-bio_recent": "https://arxiv.org/list/q-bio/recent",
        "q-bio_new": "https://arxiv.org/list/q-bio/new",
        
        # 定量金融 (Quantitative Finance)
        "q-fin_recent": "https://arxiv.org/list/q-fin/recent",
        "q-fin_new": "https://arxiv.org/list/q-fin/new",
    }
    
    # 类别描述信息
    CATEGORY_DESCRIPTIONS = {
        # 计算机科学
        "cs_recent": "计算机科学最新论文",
        "cs_new": "计算机科学新提交论文",
        
        # 数学
        "math_recent": "数学最新论文",
        "math_new": "数学新提交论文",
        
        # 物理
        "physics_recent": "物理学最新论文",
        "physics_new": "物理学新提交论文",
        
        # 天体物理
        "astro-ph_recent": "天体物理学最新论文",
        "astro-ph_new": "天体物理学新提交论文",
        
        # 凝聚态物理
        "cond-mat_recent": "凝聚态物理最新论文",
        "cond-mat_new": "凝聚态物理新提交论文",
        
        # 广义相对论和量子宇宙学
        "gr-qc_recent": "广义相对论和量子宇宙学最新论文",
        "gr-qc_new": "广义相对论和量子宇宙学新提交论文",
        
        # 高能物理
        "hep-ex_recent": "高能物理实验最新论文",
        "hep-ex_new": "高能物理实验新提交论文",
        "hep-lat_recent": "高能物理格点最新论文",
        "hep-lat_new": "高能物理格点新提交论文",
        "hep-ph_recent": "高能物理现象学最新论文",
        "hep-ph_new": "高能物理现象学新提交论文",
        "hep-th_recent": "高能物理理论最新论文",
        "hep-th_new": "高能物理理论新提交论文",
        
        # 数学物理
        "math-ph_recent": "数学物理最新论文",
        "math-ph_new": "数学物理新提交论文",
        
        # 非线性科学
        "nlin_recent": "非线性科学最新论文",
        "nlin_new": "非线性科学新提交论文",
        
        # 核物理
        "nucl-th_recent": "核理论最新论文",
        "nucl-th_new": "核理论新提交论文",
        "nucl-ex_recent": "核实验最新论文",
        "nucl-ex_new": "核实验新提交论文",
        
        # 量子物理
        "quant-ph_recent": "量子物理最新论文",
        "quant-ph_new": "量子物理新提交论文",
        
        # 统计力学
        "stat_recent": "统计力学最新论文",
        "stat_new": "统计力学新提交论文",
        
        # 电气工程和系统科学
        "eess_recent": "电气工程和系统科学最新论文",
        "eess_new": "电气工程和系统科学新提交论文",
        
        # 经济学
        "econ_recent": "经济学最新论文",
        "econ_new": "经济学新提交论文",
        
        # 定量生物学
        "q-bio_recent": "定量生物学最新论文",
        "q-bio_new": "定量生物学新提交论文",
        
        # 定量金融
        "q-fin_recent": "定量金融最新论文",
        "q-fin_new": "定量金融新提交论文",
    }
    
    # 学科分组
    SUBJECT_GROUPS = {
        "计算机科学": ["cs_recent", "cs_new"],
        "数学": ["math_recent", "math_new"],
        "物理学": ["physics_recent", "physics_new"],
        "天体物理学": ["astro-ph_recent", "astro-ph_new"],
        "凝聚态物理": ["cond-mat_recent", "cond-mat_new"],
        "广义相对论": ["gr-qc_recent", "gr-qc_new"],
        "高能物理": [
            "hep-ex_recent", "hep-ex_new",
            "hep-lat_recent", "hep-lat_new", 
            "hep-ph_recent", "hep-ph_new",
            "hep-th_recent", "hep-th_new"
        ],
        "数学物理": ["math-ph_recent", "math-ph_new"],
        "非线性科学": ["nlin_recent", "nlin_new"],
        "核物理": ["nucl-th_recent", "nucl-th_new", "nucl-ex_recent", "nucl-ex_new"],
        "量子物理": ["quant-ph_recent", "quant-ph_new"],
        "统计力学": ["stat_recent", "stat_new"],
        "工程科学": ["eess_recent", "eess_new"],
        "经济学": ["econ_recent", "econ_new"],
        "生物学": ["q-bio_recent", "q-bio_new"],
        "金融学": ["q-fin_recent", "q-fin_new"],
    }
    
    # 分页配置
    PAPERS_PER_PAGE = 50
    
    # 请求配置
    REQUEST_TIMEOUT = 30
    REQUEST_HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    # 重试配置
    MAX_RETRIES = 3
    RETRY_DELAY = 1  # 秒
    
    # 解析配置
    HTML_PARSER = "html.parser"
    
    # 输出配置
    DEFAULT_OUTPUT_FORMAT = "json"
    SUPPORTED_FORMATS = ["json", "csv", "xlsx"]
    
    # 日志配置
    LOG_LEVEL = "INFO"
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # 输出格式化配置
    ENABLE_RICH_OUTPUT = True  # 是否启用Rich格式化输出
    RICH_THEME = "default"  # Rich主题
    SHOW_PROGRESS = True  # 是否显示进度条
    SHOW_DETAILED_INFO = True  # 是否显示详细信息
    QUIET_MODE = False  # 静默模式，只输出关键信息
    TABLE_MAX_WIDTH = 120  # 表格最大宽度
    TRUNCATE_TITLE_LENGTH = 60  # 标题截断长度
    TRUNCATE_ABSTRACT_LENGTH = 200  # 摘要截断长度
    
    @classmethod
    def get_arxiv_url(cls, category: str) -> str:
        """获取指定类别的ArXiv URL"""
        return cls.ARXIV_URLS.get(category)
    
    @classmethod
    def get_all_categories(cls) -> list:
        """获取所有支持的类别"""
        return list(cls.ARXIV_URLS.keys())
    
    @classmethod
    def get_category_description(cls, category: str) -> str:
        """获取类别描述"""
        return cls.CATEGORY_DESCRIPTIONS.get(category, "未知类别")
    
    @classmethod
    def get_categories_by_subject(cls, subject: str) -> list:
        """根据学科获取类别列表"""
        return cls.SUBJECT_GROUPS.get(subject, [])
    
    @classmethod
    def get_all_subjects(cls) -> list:
        """获取所有学科分组"""
        return list(cls.SUBJECT_GROUPS.keys())
    
    @classmethod
    def search_categories(cls, keyword: str) -> list:
        """根据关键词搜索类别"""
        keyword = keyword.lower()
        results = []
        
        for category, description in cls.CATEGORY_DESCRIPTIONS.items():
            if keyword in category.lower() or keyword in description.lower():
                results.append(category)
        
        return results
    
    @classmethod
    def get_category_info(cls, category: str) -> dict:
        """获取类别的完整信息"""
        if category not in cls.ARXIV_URLS:
            return None
        
        # 找到所属学科
        subject = None
        for subj, cats in cls.SUBJECT_GROUPS.items():
            if category in cats:
                subject = subj
                break
        
        return {
            "category": category,
            "description": cls.get_category_description(category),
            "url": cls.get_arxiv_url(category),
            "subject": subject,
            "type": "recent" if "recent" in category else "new"
        }


# 环境变量配置
def get_env_config() -> Dict[str, Any]:
    """从环境变量获取配置"""
    return {
        "timeout": int(os.getenv("ARXIV_TIMEOUT", Config.REQUEST_TIMEOUT)),
        "max_retries": int(os.getenv("ARXIV_MAX_RETRIES", Config.MAX_RETRIES)),
        "log_level": os.getenv("ARXIV_LOG_LEVEL", Config.LOG_LEVEL),
        "enable_rich_output": os.getenv("ARXIV_RICH_OUTPUT", str(Config.ENABLE_RICH_OUTPUT)).lower() == "true",
        "show_progress": os.getenv("ARXIV_SHOW_PROGRESS", str(Config.SHOW_PROGRESS)).lower() == "true",
        "show_detailed_info": os.getenv("ARXIV_SHOW_DETAILS", str(Config.SHOW_DETAILED_INFO)).lower() == "true",
        "quiet_mode": os.getenv("ARXIV_QUIET", str(Config.QUIET_MODE)).lower() == "true",
    } 