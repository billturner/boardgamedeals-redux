from datetime import datetime
import os
from sqlmodel import Session, select, update

from data.db import engine
from data.models import Forum, ForumPost
from collectors.reddit import get_token
from collectors import bgg, reddit

GET_FORUM_POSTS = False
GET_DOTD = True

def check_for_existing(session, forum_id, external_id):
  return session.exec(
    select(ForumPost)
      .where(ForumPost.forum_id == forum_id)
      .where(ForumPost.external_id == external_id)
  ).first()

def main():
  session = Session(engine)
  # First, get Deal of the Day posts

  # Second, run through grabbing forum posts from BGG & Reddit
  if GET_FORUM_POSTS:
    forums = session.exec(select(Forum).where(Forum.is_active == True)).all()

    # get reddit token
    username = os.getenv('REDDIT_USERNAME')
    password = os.getenv('REDDIT_PASSWORD')
    client_id = os.getenv('REDDIT_CLIENT_ID')
    client_secret = os.getenv('REDDIT_CLIENT_SECRET')

    reddit_token = get_token(username, password, client_id, client_secret)
    print('reddit_token', reddit_token)

    new_posts = []
    for forum in forums:
      print(f'Name: {forum.name}')
      posts = []

      # Grab posts from BGG or Reddit
      if forum.source == 'bgg':
        posts = bgg.collect(forum)
      elif forum.source == 'reddit':
        if reddit_token == None:
          print(f"No auth token for reddit. Skipping...")
        else:
          posts = reddit.collect(forum, reddit_token)

      # process found posts from forum
      for post in posts:
        existing = None

        # check if forum post exists
        existing = check_for_existing(session, forum.id, post['external_id'])
        if existing == None:
          print('Found new post, adding...')
          new_posts.append(post)
        else:
          print('Found existing post, skipping (for now)...')
          next

      forum.collected_at = datetime.utcnow()

    # update forums
    for forum in forums:
      forum.collected_at = datetime.utcnow()
      session.add(forum)
    # add new ForumPosts
    for new_post in new_posts:
      session.add(ForumPost(**new_post))
    session.commit()

  # close session
  session.close()

if __name__ == '__main__':
  main()
