import requests
from pprint import pprint
from readability import Document

from sumy.parsers.html import HtmlParser
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words

def strip_tags(url):
    summary = []
    parser = HtmlParser.from_url(url, Tokenizer("english"))
    stemmer = Stemmer("english")

    summarizer = Summarizer(stemmer)
    summarizer.stop_words = get_stop_words("english")
    
    for sentence in summarizer(parser.document, 10): # summarise in 10 sentences
        summary.append(sentence)
        
    return summary

url = "https://hacker-news.firebaseio.com/v0/beststories.json?print=pretty"

res = requests.get(url)
ids = str(res.content, encoding="utf-8").strip("[]\n").strip().split(", ")[:10]

summaries = []

for i in range(len(ids)):
    cur_id = ids[i]
    
    hn_post_url = "https://hacker-news.firebaseio.com/v0/item/{}.json?print=pretty".format(cur_id)
    hn_post = requests.get(hn_post_url)
    hn_post_content = hn_post.json()
    
    op_id = hn_post_content['by'] if hn_post_content['by'] else None
    post_title = hn_post_content['title'] if hn_post_content['title'] else None
    post_url = hn_post_content['url'] if hn_post_content['url'] else None
    post_type = hn_post_content['type'] if hn_post_content['type'] else None
    
    if post_url != None:
        url_summary = strip_tags(post_url)
        if len(url_summary) >= 5:
            summaries.append(url_summary)
        
for i in range(len(summaries)):
    with open("../output/outputs_{}.txt".format(i+1), "a+") as f:
        for j in range(len(summaries[i])):
            f.write(repr(summaries[i][j]).strip("<>").replace("Sentence: ", "") + "\n")