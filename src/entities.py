from dataclasses import dataclass
from datetime import datetime


@dataclass
class ArticleInfo:
    title: str
    pub_date: datetime
    author_url: str
    author_username: str
    text: str = ""
    article_url: str = ""
    hub_url: str = ""


@dataclass
class HubInfo:
    name: str
    url: str
