# -*- coding: utf-8 -*-

from sqlalchemy.orm import sessionmaker
from bookcontents.models import Channels, db_connect

class BookcontentsPipeline(object):
    def __init__(self):
        """
        Initializes database connection and sessionmaker.
        Creates deals table.
        """
        engine = db_connect()
        # create_table(engine)
        self.Session = sessionmaker(bind=engine)
        self.session = self.Session()

    def process_item(self, item, spider):
        """Save deals in the database.

        This method is called for every item pipeline component.
        """
        channels = Channels()

        try:
            channels.title = item['title']
            channels.img = item['img']
            channels.text = item['text']
            channels.url = item['url']
            channels.description = item['description']
            
            self.session.add(channels)
            self.session.commit()
        except:
            self.session.rollback()
            raise
        finally:
            self.session.close()

        return item
