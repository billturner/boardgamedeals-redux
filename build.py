from sqlmodel import Session, select

from data.db import engine
from data.models import Forum, ForumPost

def main():
  session = Session(engine)
  forums = session.exec(select(Forum).where(Forum.is_active == True)).all()

  for forum in forums:
    print(f'Getting posts from {forum.name}')
    posts = session.exec(select(ForumPost).where(ForumPost.forum_id == forum.id).limit(5))
    for post in posts:
      print(f'Found post: {post.subject}')

if __name__ == '__main__':
  main()
