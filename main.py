import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd
from rich import print
import re
import numpy as np
import math
# from publicConfig import ArXiv_Pool
ArXiv_Pool = {
    "cs_recent": "https://arxiv.org/list/cs/recent",
    "cs_new": "https://arxiv.org/list/cs/new",
}

# 生成arxiv页面url
def gen_arxiv_page_args(total_count):
    """
    1. 获取总论文数
    2. 获取每页的论文数量
    3. 判断 总论文数 是否大于 每页的论文数量
    3.1. 如果大于，则 (总论文数/每页的论文数量)向上取整 + 1 = 总页数
    3.2. 如果小于，则返回 1
    4. 根据总页数，生成所有页面的url，分割参数为?skip=[(页-1)*50]&show=50
    5. 返回所有页面的url
    """
    
    if total_count > 50:
        total_page = math.ceil(total_count / 50) + 1
    else:
        total_page = 1
    
    for page in range(1,total_page+1):
        yield f"?skip={(page-1)*50}&show=50"
    
# 获取arxiv页面html
def get_arxiv_html(url):
    response = requests.get(url)
    response.raise_for_status() # 如果请求失败，抛出异常
    return response.text

# 解析html
def html_parser(html):
    soup = BeautifulSoup(html, "html.parser")
    return soup

# 获取arxiv页面中论文数量
def get_arxiv_data(html):
    soup = html_parser(html)
    total_count = extract_total_count(soup.find("dl",{"id":"articles"}).find_next("h3").text)
    return soup,total_count

# 从文本中提取总数
def extract_total_count(text):
    """
    从文本中提取总数
    匹配模式：Total of X entries
    返回X的值
    """
    # 正则表达式模式：匹配 "Total of 数字 entries"
    pattern = r'Total of (\d+) entries'
    match = re.search(pattern, text) 
    if match:
        return int(match.group(1))
    return None

# 获取论文卡片
def get_papers_card_yield(soup):
    if soup.find("dl",{"id":"articles"}):
        papers_link = soup.find("dl",{"id":"articles"}).find_all("dt")
        papers_detail = soup.find("dl",{"id":"articles"}).find_all("dd")
        papers_list = [[dt,dd] for dt,dd in zip(papers_link,papers_detail)]
        for paper in papers_list:
            abslink = "https://arxiv.org"+paper[0].find("a",{"title":"Abstract"})["href"]
            arxiv_id = abslink.split("/")[-1]
            has_pdf = "https://arxiv.org"+paper[0].find("a",{"title":"Download PDF"})["href"] if (paper[0].find("a",{"title":"Download PDF"}) is not None) else False
            has_html = paper[0].find("a",{"title":"View HTML"}).get("href") if (paper[0].find("a",{"title":"View HTML"}) is not None) else False
            title = paper[1].find("div",{"class":"list-title"}).get_text(strip=True).replace("Title:","").strip()
            autors = [author.get_text(strip=True) for author in paper[1].find("div",{"class":"list-authors"}).find_all("a")]
            comments = paper[1].find("div",{"class":"list-comments"})
            if comments:
                comments = comments.get_text(strip=True).replace("Comments:","").strip()
            else:
                comments = ""
            subjects = paper[1].find("div",{"class":"list-subjects"}).get_text(strip=True).replace("Subjects:",'').split(";")
            paper_card = {
                "arxiv_id":arxiv_id,
                "abslink":abslink,
                "has_html":has_html,
                "has_pdf":has_pdf,
                "title":title,
                "autors":autors,
                "comments":comments,
                "subjects":subjects
            }
            yield paper_card
    else:
        yield None

# 获取论文卡片
def get_papers_card(soup):
    ret_data = []
    if soup.find("dl",{"id":"articles"}):
        papers_link = soup.find("dl",{"id":"articles"}).find_all("dt")
        papers_detail = soup.find("dl",{"id":"articles"}).find_all("dd")
        papers_list = [[dt,dd] for dt,dd in zip(papers_link,papers_detail)]
        for paper in papers_list:
            abslink = "https://arxiv.org"+paper[0].find("a",{"title":"Abstract"})["href"]
            arxiv_id = abslink.split("/")[-1]
            has_pdf = "https://arxiv.org"+paper[0].find("a",{"title":"Download PDF"})["href"] if (paper[0].find("a",{"title":"Download PDF"}) is not None) else False
            has_html = paper[0].find("a",{"title":"View HTML"}).get("href") if (paper[0].find("a",{"title":"View HTML"}) is not None) else False
            title = paper[1].find("div",{"class":"list-title"}).get_text(strip=True).replace("Title:","").strip()
            autors = [author.get_text(strip=True) for author in paper[1].find("div",{"class":"list-authors"}).find_all("a")]
            comments = paper[1].find("div",{"class":"list-comments"})
            if comments:
                comments = comments.get_text(strip=True).replace("Comments:","").strip()
            else:
                comments = ""
            subjects = paper[1].find("div",{"class":"list-subjects"}).get_text(strip=True).replace("Subjects:",'').split(";")
            paper_card = {
                "arxiv_id":arxiv_id,
                "abslink":abslink,
                "has_html":has_html,
                "has_pdf":has_pdf,
                "title":title,
                "autors":autors,
                "comments":comments,
                "subjects":subjects
            }
            ret_data.append(paper_card)
    else:
        ret_data = None
    return ret_data

# 获取论文摘要
def get_paper_abstract(url):
    html = get_arxiv_html(url)
    soup = html_parser(html)
    abstract = soup.find("blockquote",{"class":"abstract"}).get_text(strip=True).replace("Abstract:","")
    return abstract

# 插入论文摘要
def insert_paper_abstract(data):
    for paper in data:
        abstract = get_paper_abstract(paper["abslink"])
        paper["abstract"] = abstract
        yield paper
    # return data


def get_paper_context_from_html(paper_card):
    paper_context = {}
    if not paper_card.get("has_html"):
        return None

    html = get_arxiv_html(paper_card.get("has_html"))
    html.replace("Report issue for preceding element","")
    soup = html_parser(html)

    # 获取标题
    title = paper_card.get("title")
    paper_context["title"] = title

    # 获取摘要部分
    abstract = soup.find("div",{"class":"ltx_abstract"}).get_text(strip=True)
    paper_context["abstract"] = abstract

    # 获取正文部分
    body_sections = soup.find_all("section",{"class":"ltx_section"})
    sections_name = [section.find("h2",{"class":"ltx_title_section"}).get_text(strip=True) for section in body_sections]
    sections_content = [section.get_text(strip=True) for section in body_sections]
    paper_context["body_sections"] = [{title:text.replace(f"{title}","")} for title,text in zip(sections_name,sections_content)]


    # 获取参考文献部分
    bib_section = soup.find("section",{"class":"ltx_bibliography"}).find_all("li",{"class":"ltx_bibitem"})
    bib_section_content = [bib.get_text(strip=True) for bib in bib_section]
    paper_context["bib_section"] = bib_section_content

    # 获取附录部分
    appendix_section = soup.find_all("section",{"class":"ltx_appendix"})
    appendix_section_title = [appendix.find("h2",{"class":"ltx_title_appendix"}).get_text(strip=True) for appendix in appendix_section]
    appendix_section_content = [appendix.get_text(strip=True) for appendix in appendix_section]
    appendix_section_content = [{title:text.replace(f"{title}","")} for title,text in zip(appendix_section_title,appendix_section_content)]
    paper_context["appendix_sections"] = appendix_section_content

    return paper_context

if __name__ == "__main__":
    html = get_arxiv_html(ArXiv_Pool["cs_recent"])
    soup,total_count = get_arxiv_data(html)
    data = get_papers_card(soup)
    data = insert_paper_abstract(data)
    first_paper = next(data)
    second_paper = next(data)
    print(second_paper)
    paper_context = get_paper_context_from_html(second_paper)
    # print(paper_context)
    second_paper["context"] = paper_context
    # print(second_paper)
    print(second_paper.keys())


