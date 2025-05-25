#!/usr/bin/env python3
"""
ArXiv所有类别使用示例

展示如何使用新增的所有ArXiv类别功能。
"""

import sys
import os

# 添加当前目录到Python路径
sys.path.insert(0, '.')

from arxiv_scraper import ArxivScraper, Config
from arxiv_scraper.utils import OutputFormatter


def show_all_categories():
    """展示所有支持的类别"""
    print("📚 ArXiv支持的所有类别")
    print("=" * 60)
    
    formatter = OutputFormatter(enable_rich=True)
    
    # 显示总体统计
    all_categories = Config.get_all_categories()
    all_subjects = Config.get_all_subjects()
    
    stats = {
        "支持类别总数": len(all_categories),
        "学科分组数": len(all_subjects),
        "平均每组类别数": f"{len(all_categories)/len(all_subjects):.1f}"
    }
    
    formatter.print_header("ArXiv类别统计", "全面支持ArXiv所有主要学科")
    formatter.print_statistics(stats)
    
    # 按学科分组显示
    formatter.print_section("按学科分组的类别详情")
    
    for subject in all_subjects:
        categories = Config.get_categories_by_subject(subject)
        print(f"\n🔬 {subject} ({len(categories)} 个类别):")
        
        for category in categories:
            description = Config.get_category_description(category)
            category_type = "最新" if "recent" in category else "新提交"
            print(f"  • {category:<20} - {description} ({category_type})")


def demonstrate_category_search():
    """演示类别搜索功能"""
    print("\n🔍 类别搜索功能演示")
    print("=" * 60)
    
    formatter = OutputFormatter(enable_rich=True)
    formatter.print_section("智能类别搜索")
    
    # 演示不同的搜索关键词
    search_examples = [
        ("物理", "搜索所有物理相关类别"),
        ("高能", "搜索高能物理类别"),
        ("数学", "搜索数学相关类别"),
        ("计算机", "搜索计算机科学类别"),
        ("生物", "搜索生物学类别"),
        ("经济", "搜索经济学类别"),
    ]
    
    for keyword, description in search_examples:
        results = Config.search_categories(keyword)
        print(f"\n🔎 {description} (关键词: '{keyword}')")
        print(f"   找到 {len(results)} 个匹配类别:")
        
        for category in results[:5]:  # 只显示前5个
            desc = Config.get_category_description(category)
            print(f"   • {category}: {desc}")
        
        if len(results) > 5:
            print(f"   ... 还有 {len(results)-5} 个类别")


def sample_papers_from_different_subjects():
    """从不同学科获取论文样本"""
    print("\n📄 多学科论文样本获取")
    print("=" * 60)
    
    formatter = OutputFormatter(enable_rich=True)
    
    # 选择不同学科的代表性类别
    sample_categories = [
        ("cs_recent", "计算机科学"),
        ("math_recent", "数学"),
        ("physics_recent", "物理学"),
        ("astro-ph_recent", "天体物理学"),
        ("quant-ph_recent", "量子物理"),
        ("econ_recent", "经济学"),
        ("q-bio_recent", "生物学"),
        ("eess_recent", "工程科学"),
    ]
    
    formatter.print_section("多学科论文展示")
    
    with ArxivScraper() as scraper:
        for category, subject_name in sample_categories:
            try:
                print(f"\n🔬 {subject_name} ({category})")
                papers = scraper.get_papers_from_category(category, max_papers=2)
                
                if papers:
                    for i, paper in enumerate(papers, 1):
                        print(f"  {i}. {paper.title[:70]}...")
                        print(f"     作者: {', '.join(paper.authors[:2])}")
                        if len(paper.authors) > 2:
                            print(f"           (+{len(paper.authors)-2} 位作者)")
                        print(f"     ID: {paper.arxiv_id}")
                else:
                    print("  暂无论文数据")
                    
            except Exception as e:
                print(f"  ❌ 获取失败: {e}")


def compare_recent_vs_new():
    """比较recent和new类别的差异"""
    print("\n🆚 Recent vs New 类别对比")
    print("=" * 60)
    
    formatter = OutputFormatter(enable_rich=True)
    formatter.print_section("类别类型对比分析")
    
    # 选择几个学科进行对比
    comparison_subjects = ["cs", "math", "physics", "astro-ph"]
    
    with ArxivScraper() as scraper:
        for subject in comparison_subjects:
            recent_cat = f"{subject}_recent"
            new_cat = f"{subject}_new"
            
            print(f"\n📊 {subject.upper()} 学科对比:")
            
            try:
                recent_papers = scraper.get_papers_from_category(recent_cat, max_papers=5)
                new_papers = scraper.get_papers_from_category(new_cat, max_papers=5)
                
                print(f"  📈 {recent_cat}: {len(recent_papers)} 篇论文")
                print(f"  🆕 {new_cat}: {len(new_papers)} 篇论文")
                
                # 分析重叠情况
                if recent_papers and new_papers:
                    recent_ids = {p.arxiv_id for p in recent_papers}
                    new_ids = {p.arxiv_id for p in new_papers}
                    overlap = len(recent_ids & recent_ids)
                    unique_recent = len(recent_ids - new_ids)
                    unique_new = len(new_ids - recent_ids)
                    
                    print(f"  🔄 重叠论文: {overlap} 篇")
                    print(f"  📈 仅在recent: {unique_recent} 篇")
                    print(f"  🆕 仅在new: {unique_new} 篇")
                
            except Exception as e:
                print(f"  ❌ 对比失败: {e}")


def demonstrate_category_info():
    """演示类别信息获取"""
    print("\n📋 类别详细信息获取")
    print("=" * 60)
    
    formatter = OutputFormatter(enable_rich=True)
    formatter.print_section("类别信息详情")
    
    # 展示不同类型的类别信息
    demo_categories = [
        "cs_recent", "hep-th_recent", "q-bio_recent", 
        "econ_recent", "math-ph_recent", "stat_recent"
    ]
    
    for category in demo_categories:
        info = Config.get_category_info(category)
        if info:
            print(f"\n📌 {category}")
            print(f"   描述: {info['description']}")
            print(f"   学科: {info['subject']}")
            print(f"   类型: {info['type']}")
            print(f"   URL: {info['url']}")


def show_usage_examples():
    """显示使用示例"""
    print("\n💡 使用示例代码")
    print("=" * 60)
    
    examples = [
        ("获取量子物理论文", """
# 获取量子物理最新论文
with ArxivScraper() as scraper:
    papers = scraper.get_papers_from_category("quant-ph_recent", max_papers=10)
    for paper in papers:
        print(f"{paper.arxiv_id}: {paper.title}")
"""),
        
        ("搜索高能物理类别", """
# 搜索所有高能物理相关类别
hep_categories = Config.search_categories("高能")
for category in hep_categories:
    description = Config.get_category_description(category)
    print(f"{category}: {description}")
"""),
        
        ("按学科获取类别", """
# 获取所有物理学相关类别
physics_categories = Config.get_categories_by_subject("物理学")
print(f"物理学类别: {physics_categories}")

# 获取所有学科
all_subjects = Config.get_all_subjects()
print(f"支持的学科: {all_subjects}")
"""),
        
        ("批量获取多学科论文", """
# 批量获取多个学科的论文
subjects_to_fetch = ["计算机科学", "数学", "物理学"]
all_papers = {}

with ArxivScraper() as scraper:
    for subject in subjects_to_fetch:
        categories = Config.get_categories_by_subject(subject)
        for category in categories:
            if "recent" in category:  # 只获取recent类别
                papers = scraper.get_papers_from_category(category, max_papers=5)
                all_papers[category] = papers
"""),
    ]
    
    for title, code in examples:
        print(f"\n📝 {title}:")
        print(code)


def main():
    """主函数"""
    print("🚀 ArXiv所有类别功能演示")
    print("=" * 80)
    print("展示ArXiv爬虫对所有40个类别的完整支持")
    print("=" * 80)
    
    try:
        show_all_categories()
        demonstrate_category_search()
        sample_papers_from_different_subjects()
        compare_recent_vs_new()
        demonstrate_category_info()
        show_usage_examples()
        
        print(f"\n🎉 演示完成！")
        print(f"📊 ArXiv爬虫现在支持 {len(Config.get_all_categories())} 个类别")
        print(f"🔬 覆盖 {len(Config.get_all_subjects())} 个主要学科分组")
        print(f"\n💡 你现在可以获取任何ArXiv学科的论文数据！")
        
    except KeyboardInterrupt:
        print("\n\n⚠️ 用户中断了演示")
    except Exception as e:
        print(f"\n❌ 演示出错: {e}")


if __name__ == "__main__":
    main() 