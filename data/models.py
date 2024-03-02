from typing import List, Optional
from datetime import datetime
from sqlalchemy import TEXT, Column
from sqlmodel import Field, SQLModel, ForeignKey, Index, Relationship

class DailyDealSites(SQLModel, table=True):
  __tablename__ = 'daily_deal_sites'

  id: Optional[int] = Field(primary_key=True, index=True)
  name: str
  url: str
  collected_at: Optional[datetime]
  created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
  updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

class DailyDeal(SQLModel, table=True):
  __tablename__ = 'daily_deals'

  id: Optional[int] = Field(primary_key=True, index=True)
  daily_deal_site_id: int = Field(ForeignKey("daily_deal_sites.id"), index=True)
  name: str
  url: str
  price: str
  image: str
  in_stock: bool = Field(default=True, nullable=False)
  created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
  updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

class Forum(SQLModel, table=True):
  __tablename__: str = 'forums'

  id: Optional[int] = Field(primary_key=True, index=True)
  source: Optional[str]
  name: str
  description: Optional[str] = Field(Column(TEXT))
  collected_at: Optional[datetime]
  created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
  updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
  url: str
  api_url: str
  default_params: Optional[str]
  region: str
  content_type: str
  id_field: str
  subject_field: str
  body_field: Optional[str]
  url_field: str
  url_prefix_field: Optional[str]
  date_field: str
  external_url_field: Optional[str]
  author_field: Optional[str]
  # forum_posts: List['ForumPost'] = Relationship(back_populates='forum')
  is_active: bool = Field(default=True, nullable=False)


class ForumPost(SQLModel, table=True):
  __tablename__: str = 'forum_posts'

  id: Optional[int] = Field(primary_key=True, index=True)
  forum_id: int = Field(ForeignKey("forums.id"), index=True)
  external_id: str
  subject: str = Field(Column(TEXT))
  body: Optional[str]
  author: str
  url: str
  external_url: Optional[str]
  posted_at: datetime = Field(nullable=False, index=True)
  created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
  updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
  # forum: Forum = Relationship(back_populates='forum_posts')

  __table_args__ = (
    Index(
      "idx_forum_posts_forum_id_external_id",
      "forum_id",
      "external_id",
      unique=True,
    ),
  )
