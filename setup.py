import csv
from sqlmodel import SQLModel, Session

from data.models import Forum, DailyDealSites
from data.db import engine

def seed_forums(session):
  # Add the daily deals websites
  with open('data/deals_seed.csv') as f:
    rows = csv.DictReader(f)
    for row in rows:
      session.add(DailyDealSites(**row))

  # Add the forum sites
  with open('data/forums_seed.csv') as f:
    rows = csv.DictReader(f)
    for row in rows:
      row['is_active'] = row['is_active'] == 'True'
      session.add(Forum(**row))
  # Commit changes
  session.commit()

def reset_database():
  SQLModel.metadata.drop_all(engine)
  SQLModel.metadata.create_all(engine)

def main():
  session = Session(engine)

  reset_database()
  seed_forums(session)

if __name__ == '__main__':
  main()
