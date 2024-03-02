from datetime import datetime, timezone
import requests

from collectors.common import API_USER_AGENT, build_forum_post
from data.models import Forum

def get_token(reddit_username: str, reddit_password: str, reddit_client_id: str, reddit_client_secret: str):
  client_auth = requests.auth.HTTPBasicAuth(reddit_client_id, reddit_client_secret)
  res = requests.post(
    url="https://www.reddit.com/api/v1/access_token",
    auth=client_auth,
    data={
        "grant_type": "password",
        "username": reddit_username,
        "password": reddit_password
    },
    headers={
        "User-Agent": API_USER_AGENT
    }
  )

  if res.status_code == 200:
    auth_response = res.json()
    return auth_response['access_token']
  else:
    print('AUTH response', res.content)
    return None

def collect(forum: Forum, token: str):
  if token:
    response = requests.get(
      url = forum.api_url,
      headers = {
        "Authorization": f"Bearer {token}",
        "User-Agent": API_USER_AGENT
      }
    )

    if response.status_code == 200:
      json = response.json()

      all_posts = []
      for item in json['data']['children']:
        clean_item = item['data']
        # convert created date from unix timestamp -> formatted UTC
        clean_item['created'] = datetime.fromtimestamp(clean_item['created'], timezone.utc).strftime("%Y-%m-%d %H:%M:%S %Z")
        new_post = build_forum_post(forum, clean_item)
        all_posts.append(new_post)
      return all_posts
    else:
      print(f'API Request Failure ({response.status_code}): {forum.name}')


  else:
    print('Could not get a token. Skipping...')
