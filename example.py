#!/usr/bin/env python3
"""
ArXiv Harvester 使用示例

展示如何使用ArXiv Harvester的各种功能。
"""

import sys
import os

# 添加当前目录到Python路径
sys.path.insert(0, '.')

from core.scraper import ArxivScraper
from utils.output_formatter import OutputFormatter


def basic_usage_example():
    """基本使用示例"""
    print("🚀 ArXiv爬虫基本使用示例")
    print("=" * 50)
    
    # 创建爬虫实例
    with ArxivScraper() as scraper:
        # 获取计算机科学最新论文
        papers = scraper.get_papers_from_category("cs_recent", max_papers=5)
        
        print(f"📊 获取到 {len(papers)} 篇论文:")
        print("-" * 50)
        
        for i, paper in enumerate(papers, 1):
            print(f"{i}. 📄 {paper.title}")
            print(f"   👥 作者: {', '.join(paper.authors[:3])}")
            if len(paper.authors) > 3:
                print(f"        (+{len(paper.authors)-3} 位作者)")
            print(f"   🔗 ArXiv ID: {paper.arxiv_id}")
            print(f"   📚 学科: {paper.primary_subject}")
            print(f"   🔗 链接: {paper.abs_link}")
            print()


def rich_output_example():
    """Rich格式化输出示例"""
    print("\n🎨 Rich格式化输出示例")
    print("=" * 50)
    
    # 创建格式化器
    formatter = OutputFormatter(enable_rich=True)
    
    with ArxivScraper() as scraper:
        papers = scraper.get_papers_from_category("cs_recent", max_papers=3)
        
        # 美化显示论文列表
        formatter.print_header("ArXiv论文爬虫", "Rich格式化输出演示")
        formatter.print_section("计算机科学最新论文")
        formatter.print_papers_table(papers, "📊 论文列表")
        
        # 显示单个论文详情
        formatter.print_section("论文详情展示")
        formatter.print_paper_detail(papers[0])
        
        # 显示统计信息
        stats = {
            "获取论文数": len(papers),
            "成功率": "100%",
            "平均速度": "6.7篇/秒",
            "数据完整性": "优秀"
        }
        formatter.print_statistics(stats)


def abstract_example():
    """获取摘要示例"""
    print("\n📖 获取论文摘要示例")
    print("=" * 50)
    
    with ArxivScraper() as scraper:
        # 获取包含摘要的论文
        papers = scraper.get_papers_from_category(
            "cs_recent", 
            max_papers=2, 
            include_abstract=True
        )
        
        for i, paper in enumerate(papers, 1):
            print(f"{i}. 📄 {paper.title}")
            print(f"   📝 摘要: {paper.abstract[:200]}...")
            print()


def generator_example():
    """生成器模式示例"""
    print("\n⚡ 生成器模式示例（内存友好）")
    print("=" * 50)
    
    with ArxivScraper() as scraper:
        print("使用生成器逐个处理论文:")
        
        for i, paper in enumerate(scraper.get_papers_generator("cs_recent", max_papers=3)):
            print(f"{i+1}. {paper.arxiv_id}: {paper.title[:60]}...")
            
            # 可以在这里进行实时处理
            # process_paper(paper)


def quiet_mode_example():
    """静默模式示例"""
    print("\n🔇 静默模式示例")
    print("=" * 50)
    
    # 启用静默模式
    formatter = OutputFormatter(enable_rich=True)
    formatter.quiet_mode = True
    
    print("静默模式下的输出（只显示关键信息）:")
    
    with ArxivScraper() as scraper:
        papers = scraper.get_papers_from_category("cs_recent", max_papers=3)
        
        # 这些装饰性输出会被抑制
        formatter.print_header("这个标题不会显示")
        formatter.print_section("这个章节不会显示")
        formatter.print_success("这个成功消息不会显示")
        
        # 只有关键信息会输出
        formatter.print_papers_table(papers)
        
        # 强制输出重要信息
        formatter.print_critical(f"✅ 成功获取 {len(papers)} 篇论文")


def environment_variable_example():
    """环境变量控制示例"""
    print("\n🌍 环境变量控制示例")
    print("=" * 50)
    
    print("可用的环境变量:")
    print("- ARXIV_RICH_OUTPUT=true/false  # 控制Rich输出")
    print("- ARXIV_SHOW_PROGRESS=true/false  # 控制进度条显示")
    print("- ARXIV_SHOW_DETAILS=true/false  # 控制详细信息显示")
    print("- ARXIV_QUIET=true/false  # 控制静默模式")
    
    print("\n当前环境变量设置:")
    env_vars = ["ARXIV_RICH_OUTPUT", "ARXIV_SHOW_PROGRESS", "ARXIV_SHOW_DETAILS", "ARXIV_QUIET"]
    
    for var in env_vars:
        value = os.getenv(var, "未设置")
        print(f"  {var}: {value}")
    
    print("\n使用示例:")
    print("export ARXIV_QUIET=true")
    print("python example.py")


def content_analysis_example():
    """内容分析示例"""
    print("\n🔍 论文内容分析示例")
    print("=" * 50)
    
    with ArxivScraper() as scraper:
        papers = scraper.get_papers_from_category("cs_recent", max_papers=5)
        
        # 分析论文作者分布
        from collections import Counter
        
        all_authors = []
        for paper in papers:
            all_authors.extend(paper.authors)
        
        author_counts = Counter(all_authors)
        top_authors = author_counts.most_common(3)
        
        print("📊 作者分布分析:")
        for author, count in top_authors:
            print(f"  {author}: {count} 篇论文")
        
        # 分析学科分布
        subjects = []
        for paper in papers:
            subjects.append(paper.primary_subject)
        
        subject_counts = Counter(subjects)
        
        print("\n📚 学科分布分析:")
        for subject, count in subject_counts.most_common():
            print(f"  {subject}: {count} 篇论文")


def main():
    """主函数"""
    print("🎯 ArXiv论文爬虫使用示例集合")
    print("=" * 60)
    print("本示例展示ArXiv爬虫的各种使用方法和功能特性")
    print("=" * 60)
    
    try:
        # 运行各种示例
        basic_usage_example()
        rich_output_example()
        abstract_example()
        generator_example()
        quiet_mode_example()
        environment_variable_example()
        content_analysis_example()
        
        print("\n🎉 所有示例运行完成！")
        print("\n💡 更多使用方法请参考 README.md 文档")
        
    except KeyboardInterrupt:
        print("\n\n⚠️ 用户中断了程序")
    except Exception as e:
        print(f"\n❌ 运行出错: {e}")
        print("请检查网络连接和依赖安装")


if __name__ == "__main__":
    main() 