import requests
from pprint import pprint

url = "https://hacker-news.firebaseio.com/v0/beststories.json?print=pretty"

res = requests.get(url)
ids = str(res.content, encoding="utf-8").strip("[]\n").strip().split(", ")[:10]

for i in range(len(ids)):
    cur_id = ids[i]
    
    hn_post_url = "https://hacker-news.firebaseio.com/v0/item/{}.json?print=pretty".format(cur_id)
    hn_post = requests.get(hn_post_url)
    hn_post_content = hn_post.json()
    
    op_id = hn_post_content['by'] if hn_post_content['by'] else None
    post_title = hn_post_content['title'] if hn_post_content['title'] else None
    post_url = hn_post_content['url'] if hn_post_content['url'] else None
    post_type = hn_post_content['type'] if hn_post_content['type'] else None
    
    if post_type == "story":
        print (post_title)