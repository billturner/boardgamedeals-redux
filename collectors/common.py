from dateutil.parser import parse

from data.models import Forum, ForumPost

USER_AGENT = "bestboardgamedeals.com/0.3"
API_USER_AGENT = 'script:boardgame-deals bot v0.3 (by /u/BoardGameDeals)'

def build_forum_post(forum: Forum, item: dict) -> ForumPost:
  new_post = {
    'subject': item.get(forum.subject_field),
    'forum_id': forum.id,
    'external_id': item.get(forum.id_field),
    'author': item.get(forum.author_field),
    'body': item.get(forum.body_field) if forum.body_field is not None else None,
    'url': f'{forum.url_prefix_field}{item.get(forum.url_field)}' if forum.url_prefix_field is not None else item.get(forum.url_field),
    'external_url': item.get(forum.external_url_field) if forum.external_url_field is not None else None,
    'posted_at': parse(item.get(forum.date_field))
  }

  return new_post
  # return ForumPost(**new_post)
