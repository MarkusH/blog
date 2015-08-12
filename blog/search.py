import hashlib
import itertools

from elasticsearch_dsl import DocType, String, Date
from elasticsearch_dsl.connections import connections

from jinja2.filters import do_striptags as striptags

LANGUAGES = (
    ('english', 'en'),
    ('german', 'de'),
)
article_classes = {}


def gen_article_class(language, code):
    class Article(DocType):
        authors = String(index='not_analyzed')
        category = String(index='not_analyzed')
        tags = String(index='not_analyzed')
        published = Date()
        image = String(index='not_analyzed')
        image_credits = String(index='not_analyzed')

        link = String(index='not_analyzed')
        title = String(analyzer=language)
        summary = String(analyzer=language)
        text = String(analyzer=language)

        class Meta:
            index = 'markusholtermann_%s' % code

    article_classes[code] = Article


def connect():
    """
    Define a default Elasticsearch client
    """
    connections.create_connection(hosts=['localhost'])
    for l in LANGUAGES:
        gen_article_class(*l)


def init():
    """
    Create the mappings in elasticsearch
    """
    for Article in article_classes.values():
        Article.init()


def index(article):
    """
    Create and save and article
    """
    md5 = hashlib.md5()
    md5.update(article.get_relative_source_path())
    id_ = md5.hexdigest()

    for translation in itertools.chain([article], article.translations):
        Article = article_classes[translation.lang]
        search_article = Article(
            meta={'id': id_},
            authors=[a.name for a in translation.authors],
            category=translation.category.name,
            tags=[t.name for t in translation.tags],
            published=translation.date,
            image=getattr(translation, 'image', ''),
            image_credits=striptags(getattr(translation, 'image_credits', '')),
            link=translation.url,
            title=striptags(translation.title),
            summary=striptags(translation.summary),
            text=striptags(translation.content),
        )
        search_article.save()
