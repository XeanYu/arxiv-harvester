"""
输出格式化工具

提供Rich美化输出功能，支持表格、面板、进度条等。
"""

import sys
from typing import List, Optional, Dict, Any, Union
from datetime import datetime

try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
    from rich.text import Text
    from rich.columns import Columns
    from rich.tree import Tree
    from rich.syntax import Syntax
    from rich.markdown import Markdown
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False

from ..config.settings import Config, get_env_config
from ..models.paper import Paper, PaperContent


class OutputFormatter:
    """输出格式化器"""
    
    def __init__(self, enable_rich: Optional[bool] = None):
        """
        初始化输出格式化器
        
        Args:
            enable_rich: 是否启用Rich输出，None时从配置读取
        """
        env_config = get_env_config()
        
        if enable_rich is None:
            self.enable_rich = env_config.get("enable_rich_output", Config.ENABLE_RICH_OUTPUT)
        else:
            self.enable_rich = enable_rich
        
        self.show_progress = env_config.get("show_progress", Config.SHOW_PROGRESS)
        self.show_detailed_info = env_config.get("show_detailed_info", Config.SHOW_DETAILED_INFO)
        self.quiet_mode = env_config.get("quiet_mode", Config.QUIET_MODE)
        
        # 静默模式下强制关闭某些功能
        if self.quiet_mode:
            self.show_progress = False
            self.show_detailed_info = False
        
        # 初始化Rich控制台
        if self.enable_rich and RICH_AVAILABLE:
            self.console = Console(width=Config.TABLE_MAX_WIDTH)
        else:
            self.console = None
            self.enable_rich = False  # 如果Rich不可用，强制关闭
    
    def print(self, *args, **kwargs):
        """统一的打印方法"""
        if self.quiet_mode:
            return  # 静默模式下不输出
        
        if self.console:
            self.console.print(*args, **kwargs)
        else:
            print(*args, **kwargs)
    
    def print_header(self, title: str, subtitle: str = ""):
        """打印标题头部"""
        if self.quiet_mode:
            return  # 静默模式下不输出标题
        
        if self.enable_rich:
            if subtitle:
                header_text = f"[bold blue]{title}[/bold blue]\n[dim]{subtitle}[/dim]"
            else:
                header_text = f"[bold blue]{title}[/bold blue]"
            
            panel = Panel(
                header_text,
                border_style="blue",
                padding=(1, 2)
            )
            self.console.print(panel)
        else:
            print(f"\n{'='*50}")
            print(f"{title}")
            if subtitle:
                print(f"{subtitle}")
            print(f"{'='*50}")
    
    def print_section(self, title: str, content: str = ""):
        """打印章节"""
        if self.quiet_mode:
            return  # 静默模式下不输出章节
        
        if self.enable_rich:
            if content:
                self.console.print(f"\n[yellow]📋 {title}[/yellow]")
                if self.show_detailed_info:
                    self.console.print(f"[dim]{content}[/dim]")
            else:
                self.console.print(f"\n[yellow]📋 {title}[/yellow]")
        else:
            print(f"\n{title}")
            if content and self.show_detailed_info:
                print(content)
    
    def print_success(self, message: str):
        """打印成功信息"""
        if self.quiet_mode:
            return  # 静默模式下不输出
        
        if self.enable_rich:
            self.console.print(f"[green]✓ {message}[/green]")
        else:
            print(f"✓ {message}")
    
    def print_warning(self, message: str):
        """打印警告信息"""
        if self.quiet_mode:
            return  # 静默模式下不输出
        
        if self.enable_rich:
            self.console.print(f"[yellow]⚠ {message}[/yellow]")
        else:
            print(f"⚠ {message}")
    
    def print_error(self, message: str):
        """打印错误信息"""
        if self.quiet_mode:
            return  # 静默模式下不输出
        
        if self.enable_rich:
            self.console.print(f"[red]✗ {message}[/red]")
        else:
            print(f"✗ {message}")
    
    def print_info(self, message: str):
        """打印信息"""
        if self.quiet_mode:
            return  # 静默模式下不输出
        
        if self.enable_rich:
            self.console.print(f"[blue]ℹ {message}[/blue]")
        else:
            print(f"ℹ {message}")
    
    def print_papers_simple(self, papers: List[Paper], title: str = "论文列表"):
        """简化的论文输出（只显示关键信息）"""
        if not papers:
            return
        
        # 即使在静默模式下也输出关键信息
        if self.enable_rich and not self.quiet_mode:
            # 使用Rich格式但只显示核心信息
            table = Table(title=title, show_header=True, header_style="bold magenta")
            table.add_column("ArXiv ID", style="cyan", no_wrap=True)
            table.add_column("标题", style="green", max_width=80)
            
            for paper in papers:
                title_text = paper.title
                if len(title_text) > 80:
                    title_text = title_text[:77] + "..."
                table.add_row(paper.arxiv_id, title_text)
            
            self.console.print(table)
        else:
            # 纯文本输出，只显示ID和标题
            for paper in papers:
                print(f"{paper.arxiv_id}: {paper.title}")
    
    def print_papers_table(self, papers: List[Paper], title: str = "论文列表"):
        """打印论文表格"""
        if not papers:
            if not self.quiet_mode:
                self.print_warning("没有论文数据")
            return
        
        # 静默模式下使用简化输出
        if self.quiet_mode:
            self.print_papers_simple(papers, title)
            return
        
        if self.enable_rich:
            table = Table(title=title, show_header=True, header_style="bold magenta")
            table.add_column("ArXiv ID", style="cyan", no_wrap=True)
            table.add_column("标题", style="green", max_width=Config.TRUNCATE_TITLE_LENGTH)
            table.add_column("作者", style="yellow", max_width=30)
            table.add_column("学科", style="blue", max_width=20)
            
            if self.show_detailed_info:
                table.add_column("PDF", style="magenta", justify="center")
                table.add_column("HTML", style="red", justify="center")
                table.add_column("评论", style="dim", max_width=30)
            
            for paper in papers:
                # 处理标题
                title_text = paper.title
                if len(title_text) > Config.TRUNCATE_TITLE_LENGTH:
                    title_text = title_text[:Config.TRUNCATE_TITLE_LENGTH-3] + "..."
                
                # 处理作者
                authors_text = ", ".join(paper.authors[:3])
                if len(paper.authors) > 3:
                    authors_text += f" (+{len(paper.authors)-3})"
                
                # 处理学科
                subjects_text = paper.primary_subject
                if len(paper.subjects) > 1:
                    subjects_text += f" (+{len(paper.subjects)-1})"
                
                row_data = [
                    paper.arxiv_id,
                    title_text,
                    authors_text,
                    subjects_text
                ]
                
                if self.show_detailed_info:
                    row_data.extend([
                        "✓" if paper.has_pdf else "✗",
                        "✓" if paper.has_html else "✗",
                        paper.comments[:27] + "..." if len(paper.comments) > 30 else paper.comments
                    ])
                
                table.add_row(*row_data)
            
            self.console.print(table)
        else:
            # 简单文本输出
            print(f"\n{title}")
            print("-" * 80)
            for i, paper in enumerate(papers, 1):
                print(f"{i}. {paper.arxiv_id}: {paper.title}")
                if self.show_detailed_info:
                    print(f"   作者: {', '.join(paper.authors[:3])}")
                    print(f"   学科: {paper.primary_subject}")
                    print(f"   PDF: {'有' if paper.has_pdf else '无'}, HTML: {'有' if paper.has_html else '无'}")
                print()
    
    def print_paper_detail(self, paper: Paper):
        """打印单个论文的详细信息"""
        if self.quiet_mode:
            # 静默模式下只输出基本信息
            print(f"{paper.arxiv_id}: {paper.title}")
            return
        
        if self.enable_rich:
            # 创建论文信息面板
            info_text = f"[bold]ArXiv ID:[/bold] {paper.arxiv_id}\n"
            info_text += f"[bold]标题:[/bold] {paper.title}\n"
            info_text += f"[bold]作者:[/bold] {', '.join(paper.authors)}\n"
            info_text += f"[bold]学科:[/bold] {', '.join(paper.subjects)}\n"
            
            if paper.comments:
                info_text += f"[bold]评论:[/bold] {paper.comments}\n"
            
            info_text += f"[bold]链接:[/bold]\n"
            info_text += f"  • 摘要: {paper.abs_link}\n"
            if paper.pdf_link:
                info_text += f"  • PDF: {paper.pdf_link}\n"
            if paper.html_link:
                info_text += f"  • HTML: {paper.html_link}\n"
            
            panel = Panel(
                info_text,
                title="[bold blue]论文详情[/bold blue]",
                border_style="blue",
                padding=(1, 2)
            )
            self.console.print(panel)
            
            # 显示摘要
            if paper.abstract and self.show_detailed_info:
                abstract_text = paper.abstract
                if len(abstract_text) > Config.TRUNCATE_ABSTRACT_LENGTH:
                    abstract_text = abstract_text[:Config.TRUNCATE_ABSTRACT_LENGTH] + "..."
                
                abstract_panel = Panel(
                    abstract_text,
                    title="[bold green]摘要[/bold green]",
                    border_style="green",
                    padding=(1, 2)
                )
                self.console.print(abstract_panel)
        else:
            # 简单文本输出
            print(f"\n论文详情:")
            print(f"ArXiv ID: {paper.arxiv_id}")
            print(f"标题: {paper.title}")
            print(f"作者: {', '.join(paper.authors)}")
            print(f"学科: {', '.join(paper.subjects)}")
            if paper.comments:
                print(f"评论: {paper.comments}")
            print(f"摘要链接: {paper.abs_link}")
            if paper.pdf_link:
                print(f"PDF链接: {paper.pdf_link}")
            if paper.html_link:
                print(f"HTML链接: {paper.html_link}")
            
            if paper.abstract and self.show_detailed_info:
                print(f"\n摘要:")
                abstract_text = paper.abstract
                if len(abstract_text) > Config.TRUNCATE_ABSTRACT_LENGTH:
                    abstract_text = abstract_text[:Config.TRUNCATE_ABSTRACT_LENGTH] + "..."
                print(abstract_text)
    
    def print_paper_content(self, content: PaperContent):
        """打印论文详细内容"""
        if not content:
            if not self.quiet_mode:
                self.print_warning("没有论文内容数据")
            return
        
        if self.quiet_mode:
            # 静默模式下只输出标题
            print(f"内容: {content.title}")
            return
        
        if self.enable_rich:
            # 创建内容树结构
            tree = Tree(f"[bold blue]{content.title}[/bold blue]")
            
            # 添加摘要
            if content.abstract:
                abstract_node = tree.add("[bold green]摘要[/bold green]")
                abstract_text = content.abstract
                if len(abstract_text) > 200:
                    abstract_text = abstract_text[:200] + "..."
                abstract_node.add(abstract_text)
            
            # 添加正文章节
            if content.body_sections:
                sections_node = tree.add(f"[bold yellow]正文章节 ({len(content.body_sections)})[/bold yellow]")
                for section in content.body_sections[:5]:  # 只显示前5个章节
                    for title, text in section.items():
                        section_node = sections_node.add(f"[cyan]{title}[/cyan]")
                        if self.show_detailed_info:
                            preview = text[:100] + "..." if len(text) > 100 else text
                            section_node.add(f"[dim]{preview}[/dim]")
            
            # 添加参考文献
            if content.bibliography:
                bib_node = tree.add(f"[bold magenta]参考文献 ({len(content.bibliography)})[/bold magenta]")
                for ref in content.bibliography[:3]:  # 只显示前3个参考文献
                    bib_node.add(f"[dim]{ref[:80]}...[/dim]" if len(ref) > 80 else f"[dim]{ref}[/dim]")
            
            # 添加附录
            if content.appendix_sections:
                appendix_node = tree.add(f"[bold red]附录 ({len(content.appendix_sections)})[/bold red]")
                for appendix in content.appendix_sections:
                    for title, text in appendix.items():
                        appendix_node.add(f"[red]{title}[/red]")
            
            self.console.print(tree)
        else:
            # 简单文本输出
            print(f"\n论文内容: {content.title}")
            print("-" * 80)
            
            if content.abstract:
                print(f"摘要: {content.abstract[:200]}...")
            
            if content.body_sections:
                print(f"\n正文章节 ({len(content.body_sections)}):")
                for i, section in enumerate(content.body_sections[:5], 1):
                    for title, text in section.items():
                        print(f"  {i}. {title}")
                        if self.show_detailed_info:
                            print(f"     {text[:100]}...")
            
            if content.bibliography:
                print(f"\n参考文献 ({len(content.bibliography)}):")
                for i, ref in enumerate(content.bibliography[:3], 1):
                    print(f"  {i}. {ref[:80]}...")
            
            if content.appendix_sections:
                print(f"\n附录 ({len(content.appendix_sections)}):")
                for i, appendix in enumerate(content.appendix_sections, 1):
                    for title, text in appendix.items():
                        print(f"  {i}. {title}")
    
    def print_statistics(self, stats: Dict[str, Any]):
        """打印统计信息"""
        if self.quiet_mode:
            return  # 静默模式下不输出统计信息
        
        if self.enable_rich:
            table = Table(title="统计信息", show_header=True, header_style="bold cyan")
            table.add_column("项目", style="yellow")
            table.add_column("数值", style="green", justify="right")
            
            for key, value in stats.items():
                table.add_row(key, str(value))
            
            self.console.print(table)
        else:
            print("\n统计信息:")
            print("-" * 30)
            for key, value in stats.items():
                print(f"{key}: {value}")
    
    def create_progress(self, description: str = "处理中...") -> Optional[Progress]:
        """创建进度条"""
        if self.quiet_mode:
            return None  # 静默模式下不显示进度条
        
        if self.enable_rich and self.show_progress:
            progress = Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                TaskProgressColumn(),
                console=self.console
            )
            return progress
        return None
    
    def print_config_info(self, config_dict: Dict[str, Any]):
        """打印配置信息"""
        if self.quiet_mode:
            return  # 静默模式下不输出配置信息
        
        if self.enable_rich:
            table = Table(title="配置信息", show_header=True, header_style="bold blue")
            table.add_column("配置项", style="cyan")
            table.add_column("值", style="yellow")
            
            for key, value in config_dict.items():
                table.add_row(key, str(value))
            
            self.console.print(table)
        else:
            print("\n配置信息:")
            print("-" * 40)
            for key, value in config_dict.items():
                print(f"{key}: {value}")
    
    def print_critical(self, *args, **kwargs):
        """打印关键信息（即使在静默模式下也会输出）"""
        if self.console:
            self.console.print(*args, **kwargs)
        else:
            print(*args, **kwargs)


# 全局格式化器实例
_default_formatter = None


def get_default_formatter() -> OutputFormatter:
    """获取默认的输出格式化器实例"""
    global _default_formatter
    if _default_formatter is None:
        _default_formatter = OutputFormatter()
    return _default_formatter


def set_rich_output(enabled: bool):
    """设置Rich输出开关"""
    global _default_formatter
    _default_formatter = OutputFormatter(enable_rich=enabled) 