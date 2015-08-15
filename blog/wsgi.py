# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import math
from os.path import abspath, dirname, join

from elasticsearch import Elasticsearch
from flask import Flask, request, render_template

app = Flask(__name__)
BASE_DIR = abspath(dirname(dirname(__file__)))
app.jinja_loader.searchpath = [join(BASE_DIR, 'build'), join(BASE_DIR, 'theme', 'templates')]
app.debug = True
client = Elasticsearch()

DEFAULT_PAGINATION = 15.0  # Need a float
SITEURL = 'http://markusholtermann.local'
SEARCHURL = SITEURL + '/search/'


class Article(object):

    def __init__(self, hit):
        self.hit = hit

    def __str__(self):
        return self.title

    __unicode__ = __str__

    @property
    def authors(self):
        return self.hit['_source']['authors']

    @property
    def category(self):
        return self.hit['_source']['category']

    @property
    def tags(self):
        return self.hit['_source']['tags']

    @property
    def published(self):
        return self.hit['_source']['published']

    @property
    def image(self):
        return self.hit['_source']['image']

    @property
    def image_credits(self):
        return self.hit['_source']['image_credits']

    @property
    def url(self):
        return self.hit['_source']['link']

    @property
    def title(self):
        title = self.hit['highlight'].get('title')
        if title:
            return ''.join(title)
        return self.hit['_source']['title']

    @property
    def summary(self):
        return self.hit['_source']['summary']

    @property
    def text(self):
        text = self.hit['highlight'].get('text')
        if text:
            return ' … '.join(text)
        return self.hit['_source']['text']


@app.route('/search/')
def hello_world():
    query = request.args.get('q', '')
    ctx = {
        'SEARCHURL': SEARCHURL,
        'SITEURL': SITEURL,
        'articles': [],
        'has_next_page': False,
        'has_previous_page': False,
        'num_pages': 1,
        'page': 1,
        'query': query,
    }
    if query:
        page = int(request.args.get('p', 1))
        if page < 1:
            page = 1
        response = client.search(
            index='markusholtermann_*',
            doc_type='article',
            body={
                'query': {
                    'simple_query_string': {
                        'query': query,
                        'fields': ['title^5', 'text'],
                    }
                },
                'highlight': {
                    'fields': {
                        'title': {},
                        'text': {},
                    }
                },
                'from': (page - 1) * DEFAULT_PAGINATION,
                'size': DEFAULT_PAGINATION,
            }
        )
        ctx['articles'] = [Article(hit) for hit in response['hits']['hits']]
        pages_total = int(math.ceil(response['hits']['total'] / DEFAULT_PAGINATION))
        ctx.update({
            'has_next_page': page < pages_total,
            'has_previous_page': page > 1,
            'num_pages': pages_total,
            'page': page,
        })

    return render_template('search.html', **ctx)


if __name__ == '__main__':
    app.run()
