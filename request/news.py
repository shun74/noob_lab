import os
import datetime
import requests
import pandas as pd
import ast
from requests_html import HTML
import sys

BASE_DIR = os.path.dirname(__file__)

def get_html(url):
    r = requests.get(url)
    if r.status_code == 200:
        html_text = r.text
        r_html = HTML(html=html_text)
        return r_html
    return ""


def get_article(url):
    r_html = get_html(url)
    topics_class = ".k-hub-card--no-ellipsis"
    r_topics = r_html.find(topics_class)

    article_titles = []
    article_links = []
    article_texts = []

    # Get titles
    for i,data in enumerate(r_topics):
        title_object = data.find(".k-card",first=True)
        title_dict = ast.literal_eval(title_object.attrs["data-rn-track-value"])
        title_text = title_dict["title"].replace("\u3000","")
        article_titles.append(title_text)

    # Get links
    for i,data in enumerate(r_topics):
        link_object = data.find(".k-card__block-link",first=True)
        link_text = link_object.attrs["href"]
        if link_text[:8] == "/article":
            text = f"https://www.nikkei.com{link_text}"
        else:
            text = None
        article_links.append(text)

    # Get article text
    for i,data in enumerate(r_topics):
        article_url = article_links[i]
        if article_url != None:
            html_text = get_html(article_url)
            r_article_text = html_text.find(".cmn-article_text",first=True)
            text = []
            for article_text in r_article_text.find("p"):
                text.append(article_text.text)
            article_texts.append("\n".join(text))
        else:
            article_texts.append("No data found.")

    return article_titles, article_texts


def make_txt(url,name="article"):
    titles, texts = get_article(url)
    assert len(titles) == len(texts)
    num = len(titles)
    # articles = [titles,texts]
    path = os.path.join("article")
    os.makedirs(path, exist_ok=True)
    os.chdir("./article")
    for i in range(num):
        filename = f"{titles[i]}.txt"
        with open(filename, "w",encoding="UTF-8") as f:
            f.write("Title:")
            f.write(titles[i])
            f.write("\n")
            f.write("Text:\n")
            f.write(texts[i])
if __name__ == "__main__":
    url = "https://www.nikkei.com/"
    make_txt(url)