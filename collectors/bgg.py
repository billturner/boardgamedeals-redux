from datetime import datetime
from requests import get
from xml.etree import ElementTree

from collectors.common import USER_AGENT
from data.models import Forum, ForumPost
from collectors.common import build_forum_post

def collect(forum: Forum):
  url = f'{forum.api_url}?{forum.default_params}'
  response = get(url, headers={'User-agent': USER_AGENT})

  if response.status_code == 200:
    all_posts = []

    results = response.content
    tree = ElementTree.fromstring(results)
    items = 0
    for item in tree.iter('thread'):
      new_post = build_forum_post(forum, item)
      all_posts.append(new_post)
    return all_posts
  else:
    print(f'API Request Failure ({response.status_code}): {forum.name}')
