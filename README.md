# 🚀 ArXiv Harvester

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Status](https://img.shields.io/badge/Status-Active-brightgreen.svg)

一个功能强大、模块化的ArXiv学术论文采集工具，支持多种输出格式和美化显示。

[功能特性](#-功能特性) • [快速开始](#-快速开始) • [详细使用](#-详细使用) • [配置选项](#-配置选项) • [API文档](#-api文档)

</div>

## ✨ 功能特性

### 🎯 核心功能
- **🔍 全面类别支持**: 支持ArXiv所有40个类别，覆盖16个学科分组
- **📄 完整信息提取**: 提取论文标题、作者、摘要、学科、评论等完整信息
- **📖 详细内容解析**: 支持解析论文的正文、参考文献、附录等详细内容
- **🚀 高性能设计**: 支持生成器模式，内存友好的大批量数据处理
- **🔄 智能重试**: 内置HTTP请求重试和错误处理机制

### 🎨 输出与显示
- **🎨 Rich格式化输出**: 支持美化的表格、面板、进度条等输出效果
- **🔇 静默模式**: 支持只输出关键信息，抑制所有装饰性输出
- **📊 多种输出格式**: 支持JSON、CSV等多种数据格式
- **🎯 灵活配置**: 支持自定义配置和环境变量控制

### 🏗️ 架构设计
- **📦 模块化设计**: 低耦合、高扩展性的架构
- **🔧 易于扩展**: 支持自定义解析器和输出格式
- **⚡ 高效解析**: 优化的HTML解析和数据提取
- **🛡️ 错误处理**: 完善的异常处理和日志记录

## 🚀 快速开始

### 安装依赖

```bash
# 克隆项目
git clone https://github.com/XeanYu/arxiv-harvester.git
cd arxiv-harvester

# 安装依赖
pip install -r requirements.txt
```

### 基本使用

```python
from core.scraper import ArxivScraper

# 创建爬虫实例
with ArxivScraper() as scraper:
    # 获取计算机科学最新论文
    papers = scraper.get_papers_from_category("cs_recent", max_papers=10)
    
    for paper in papers:
        print(f"📄 {paper.title}")
        print(f"👥 作者: {', '.join(paper.authors)}")
        print(f"🔗 ArXiv ID: {paper.arxiv_id}")
        print("-" * 50)
```

### 美化输出

```python
from core.scraper import ArxivScraper
from utils.output_formatter import OutputFormatter

# 创建格式化器
formatter = OutputFormatter(enable_rich=True)

with ArxivScraper() as scraper:
    papers = scraper.get_papers_from_category("cs_recent", max_papers=5)
    
    # 美化显示论文列表
    formatter.print_papers_table(papers, "🔬 计算机科学最新论文")
    
    # 显示统计信息
    stats = {
        "获取论文数": len(papers),
        "成功率": "100%",
        "平均速度": "2.5篇/秒"
    }
    formatter.print_statistics(stats)
```

## 📚 详细使用

### 支持的类别

ArXiv爬虫现在支持**40个类别**，覆盖**16个学科分组**：

#### 🔬 主要学科类别

| 学科分组 | 类别数量 | 示例类别 | 描述 |
|----------|----------|----------|------|
| **计算机科学** | 2 | `cs_recent`, `cs_new` | 机器学习、计算机视觉、人工智能等 |
| **数学** | 2 | `math_recent`, `math_new` | 数学各分支最新研究 |
| **物理学** | 2 | `physics_recent`, `physics_new` | 物理学各领域论文 |
| **天体物理学** | 2 | `astro-ph_recent`, `astro-ph_new` | 天体物理和宇宙学 |
| **量子物理** | 2 | `quant-ph_recent`, `quant-ph_new` | 量子力学和量子信息 |
| **高能物理** | 8 | `hep-th_recent`, `hep-ph_recent` | 理论、现象学、实验、格点 |
| **凝聚态物理** | 2 | `cond-mat_recent`, `cond-mat_new` | 凝聚态物理和材料科学 |
| **核物理** | 4 | `nucl-th_recent`, `nucl-ex_recent` | 核理论和核实验 |
| **数学物理** | 2 | `math-ph_recent`, `math-ph_new` | 数学物理方法 |
| **统计力学** | 2 | `stat_recent`, `stat_new` | 统计物理和复杂系统 |
| **非线性科学** | 2 | `nlin_recent`, `nlin_new` | 非线性动力学和混沌 |
| **广义相对论** | 2 | `gr-qc_recent`, `gr-qc_new` | 广义相对论和量子宇宙学 |
| **工程科学** | 2 | `eess_recent`, `eess_new` | 电气工程和系统科学 |
| **经济学** | 2 | `econ_recent`, `econ_new` | 经济学和金融数学 |
| **生物学** | 2 | `q-bio_recent`, `q-bio_new` | 定量生物学和生物信息学 |
| **金融学** | 2 | `q-fin_recent`, `q-fin_new` | 定量金融和风险管理 |

#### 📋 类别命名规则

- **`*_recent`**: 该学科的最新论文（通常包含最近一周的论文）
- **`*_new`**: 该学科的新提交论文（通常是最新提交的论文）

#### 🔍 类别搜索和管理

```python
from config.settings import Config

# 获取所有支持的类别
all_categories = Config.get_all_categories()
print(f"总共支持 {len(all_categories)} 个类别")

# 按学科分组查看
subjects = Config.get_all_subjects()
for subject in subjects:
    categories = Config.get_categories_by_subject(subject)
    print(f"{subject}: {categories}")

# 搜索特定类别
physics_categories = Config.search_categories("物理")
math_categories = Config.search_categories("数学")

# 获取类别详细信息
info = Config.get_category_info("cs_recent")
print(f"类别: {info['category']}")
print(f"描述: {info['description']}")
print(f"学科: {info['subject']}")
print(f"URL: {info['url']}")
```

### 获取论文信息

#### 基本获取
```python
# 获取基本论文信息
papers = scraper.get_papers_from_category("cs_recent", max_papers=20)
```

#### 包含摘要
```python
# 获取包含摘要的论文
papers = scraper.get_papers_from_category(
    category="cs_recent",
    include_abstract=True,
    max_papers=10
)

for paper in papers:
    print(f"摘要: {paper.abstract[:200]}...")
```

#### 包含详细内容
```python
# 获取包含详细内容的论文
papers = scraper.get_papers_from_category(
    category="cs_recent",
    include_content=True,
    max_papers=5
)

for paper in papers:
    if paper.full_content:
        content = paper.full_content
        print(f"正文章节数: {len(content.body_sections)}")
        print(f"参考文献数: {len(content.bibliography)}")
```

#### 分页获取
```python
# 分页获取论文
page1 = scraper.get_papers_from_category("cs_recent", max_papers=10, start_index=0)
page2 = scraper.get_papers_from_category("cs_recent", max_papers=10, start_index=10)
page3 = scraper.get_papers_from_category("cs_recent", max_papers=10, start_index=20)
```

### 生成器模式（推荐用于大量数据）

```python
# 内存友好的大批量处理
for paper in scraper.get_papers_generator("cs_recent", max_papers=1000):
    # 逐个处理论文，避免内存溢出
    process_paper(paper)
    
    # 可以随时中断
    if some_condition:
        break
```

### 获取论文总数

```python
# 获取某类别的论文总数
total_cs_papers = scraper.get_total_papers("cs_recent")
print(f"CS类别总论文数: {total_cs_papers}")
```

## 🎨 格式化输出

### Rich美化输出

```python
from utils.output_formatter import OutputFormatter

# 启用Rich格式化
formatter = OutputFormatter(enable_rich=True)

# 显示论文表格
formatter.print_papers_table(papers, "📊 论文列表")

# 显示单个论文详情
formatter.print_paper_detail(papers[0])

# 显示论文内容结构
if papers[0].full_content:
    formatter.print_paper_content(papers[0].full_content)
```

### 静默模式

```python
# 只输出关键信息，适用于脚本自动化
from utils.output_formatter import OutputFormatter

formatter = OutputFormatter(enable_rich=True)
formatter.quiet_mode = True

# 这些装饰性输出会被抑制
formatter.print_header("这不会显示")
formatter.print_section("这也不会显示")
formatter.print_success("成功消息不显示")

# 只有关键信息会输出
formatter.print_papers_table(papers)  # 只显示ID和标题
formatter.print_critical("重要信息会显示")  # 强制输出
```

### 纯文本输出

```python
# 关闭Rich，使用纯文本
from utils.output_formatter import OutputFormatter

formatter = OutputFormatter(enable_rich=False)
formatter.print_papers_table(papers)
```

## ⚙️ 配置选项

### 环境变量配置

```bash
# 输出控制
export ARXIV_RICH_OUTPUT=true          # 启用Rich格式化输出
export ARXIV_SHOW_PROGRESS=true        # 显示进度条
export ARXIV_SHOW_DETAILS=true         # 显示详细信息
export ARXIV_QUIET=true                # 静默模式，只输出关键信息

# 网络配置
export ARXIV_TIMEOUT=60                # 请求超时时间（秒）
export ARXIV_MAX_RETRIES=5             # 最大重试次数
export ARXIV_LOG_LEVEL=INFO            # 日志级别
```

### 代码配置

```python
from utils.http_client import HttpClient
from utils.output_formatter import OutputFormatter
from core.scraper import ArxivScraper

# 自定义HTTP客户端
http_client = HttpClient(timeout=60, max_retries=5)
scraper = ArxivScraper(http_client=http_client)

# 自定义输出格式化器
formatter = OutputFormatter(enable_rich=True)
formatter.quiet_mode = True  # 启用静默模式

# 全局设置Rich输出
from utils.output_formatter import set_rich_output
set_rich_output(False)  # 全局关闭Rich输出
```

## 📖 API文档

### ArxivScraper类

#### 主要方法

```python
class ArxivScraper:
    def get_papers_from_category(
        self, 
        category: str, 
        max_papers: int = 50,
        start_index: int = 0,
        include_abstract: bool = False,
        include_content: bool = False
    ) -> List[Paper]:
        """获取指定类别的论文列表"""
    
    def get_papers_generator(
        self, 
        category: str, 
        max_papers: int = None
    ) -> Generator[Paper, None, None]:
        """生成器模式获取论文"""
    
    def get_total_papers(self, category: str) -> int:
        """获取指定类别的论文总数"""
    
    def get_paper_content(self, html_url: str, title: str) -> PaperContent:
        """获取论文详细内容"""
```

### Paper数据模型

```python
@dataclass
class Paper:
    arxiv_id: str                    # ArXiv ID
    title: str                       # 论文标题
    authors: List[str]               # 作者列表
    abstract: str                    # 摘要
    subjects: List[str]              # 学科列表
    comments: str                    # 评论
    abs_link: str                    # 摘要链接
    pdf_link: str                    # PDF链接
    html_link: str                    # HTML链接
    submission_date: Optional[datetime] # 提交日期
    full_content: Optional[Dict]     # 详细内容
    
    @property
    def primary_subject(self) -> str:
        """主要学科"""
    
    @property
    def has_pdf(self) -> bool:
        """是否有PDF版本"""
    
    @property
    def has_html(self) -> bool:
        """是否有HTML版本"""
    
    def to_dict(self) -> Dict:
        """转换为字典"""
```

### OutputFormatter类

```python
class OutputFormatter:
    def __init__(self, enable_rich: Optional[bool] = None):
        """初始化输出格式化器"""
    
    def print_papers_table(self, papers: List[Paper], title: str = "论文列表"):
        """打印论文表格"""
    
    def print_paper_detail(self, paper: Paper):
        """打印单个论文详情"""
    
    def print_paper_content(self, content: PaperContent):
        """打印论文详细内容"""
    
    def print_statistics(self, stats: Dict[str, Any]):
        """打印统计信息"""
    
    def print_critical(self, *args, **kwargs):
        """打印关键信息（即使在静默模式下也会输出）"""
```

## 🔧 高级用法

### 自定义解析器

```python
from parsers.html_parser import ArxivHtmlParser

class CustomParser(ArxivHtmlParser):
    def parse_custom_field(self, soup):
        """自定义解析逻辑"""
        # 实现自定义解析
        pass

# 使用自定义解析器
scraper = ArxivScraper()
scraper.parser = CustomParser()
```

### 批量处理和导出

```python
import json
import csv

# 批量获取并导出为JSON
papers = scraper.get_papers_from_category("cs_recent", max_papers=100)
papers_data = [paper.to_dict() for paper in papers]

with open("papers.json", "w", encoding="utf-8") as f:
    json.dump(papers_data, f, ensure_ascii=False, indent=2)

# 导出为CSV
with open("papers.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=papers_data[0].keys())
    writer.writeheader()
    writer.writerows(papers_data)
```

### 错误处理和日志

```python
import logging
from core.scraper import ArxivScraper

# 配置日志
logging.basicConfig(level=logging.INFO)

try:
    with ArxivScraper() as scraper:
        papers = scraper.get_papers_from_category("cs_recent", max_papers=10)
        print(f"成功获取 {len(papers)} 篇论文")
        
except Exception as e:
    logging.error(f"获取论文失败: {e}")
```

## 🎯 使用场景

### 1. 学术研究
```python
# 获取特定领域的最新论文
papers = scraper.get_papers_from_category("cs_recent", include_abstract=True)
ml_papers = [p for p in papers if "machine learning" in p.abstract.lower()]
```

### 2. 数据分析
```python
# 分析论文作者分布
from collections import Counter

all_authors = []
for paper in papers:
    all_authors.extend(paper.authors)

author_counts = Counter(all_authors)
top_authors = author_counts.most_common(10)
```

### 3. 自动化脚本
```bash
# 使用静默模式进行自动化
export ARXIV_QUIET=true
python your_script.py > daily_papers.txt
```


## 🧪 测试

运行全面测试：

```bash
python comprehensive_test.py
```

测试特定功能：

```bash
# 测试静默模式
python -c "
from arxiv_scraper.utils import OutputFormatter
formatter = OutputFormatter()
formatter.quiet_mode = True
print('测试静默模式')
"

# 测试环境变量
ARXIV_QUIET=true python -c "
from arxiv_scraper.utils import OutputFormatter
formatter = OutputFormatter()
print(f'静默模式: {formatter.quiet_mode}')
"
```

## 📋 依赖

- **Python 3.8+**
- **requests** >= 2.28.0 - HTTP请求
- **beautifulsoup4** >= 4.11.0 - HTML解析
- **rich** >= 12.0.0 - 美化输出（可选）
- **pandas** >= 1.5.0 - 数据处理（可选）

## 🤝 贡献

欢迎提交Issue和Pull Request来改进这个项目！

### 开发指南

1. Fork项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开Pull Request

## 📄 许可证

本项目采用MIT许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## ⚠️ 注意事项

- 请遵守ArXiv的使用条款和robots.txt
- 建议在请求之间添加适当的延迟
- 大批量抓取时请使用生成器模式以节省内存
- 尊重服务器资源，避免过于频繁的请求

## 🔗 相关链接

- [ArXiv官网](https://arxiv.org/)
- [ArXiv API文档](https://arxiv.org/help/api)
- [Rich文档](https://rich.readthedocs.io/)

---

<div align="center">

**如果这个项目对你有帮助，请给它一个⭐️！**

Made with ❤️ by XeanYu

</div> 