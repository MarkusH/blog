#!/usr/bin/env python
# -*- coding: utf-8 -*-

import click
import datetime
import re
import os
import unicodedata


DATE_FORMAT = '%Y-%m-%d'
FILE_NAME_FORMAT = '{date}__{lang}__{slug}.rst'


def now_str():
    return datetime.datetime.now().strftime(DATE_FORMAT)


def check_content_dir_exists(ctx, param, value):
    if not os.path.exists(value):
        click.secho('Content directory "%s" does not exist' % value, fg='red')
        raise ctx.abort()
    return value


def slugify(value):
    """
    Converts to ASCII. Converts spaces to hyphens. Removes characters that
    aren't alphanumerics, underscores, or hyphens. Converts to lowercase.
    Also strips leading and trailing whitespace.
    """
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub('[^\w\s-]', '', value).strip().lower()
    return re.sub('[-\s]+', '-', value)


def get_filename(date, lang, title):
    slug = slugify(title)
    return FILE_NAME_FORMAT.format(date=date, lang=lang, slug=slug)


@click.command()
@click.option('--content-dir', required=True, is_eager=True, type=click.Path(), callback=check_content_dir_exists)
@click.option('-v', '--verbose', default=False, is_flag=True)
@click.option('-t', '--title', prompt=True)
@click.option('-c', '--category', prompt=True)
@click.option('-d', '--date', prompt=True, default=now_str, metavar='today')
@click.option('-l', '--language', prompt=True, type=click.Choice(['de', 'en']), default='en')
@click.pass_context
def main(ctx, content_dir, verbose, title, category, date, language):
    # Create category
    cat_dir = os.path.join(content_dir, category)
    if not os.path.exists(cat_dir):
        click.secho('Category "%s" does not exist. Create? [yn]' % category, fg='yellow')
        while True:
            c = click.getchar().lower()
            if c == 'y':
                if verbose:
                    click.echo('Creating directory %s' % click.format_filename(cat_dir))
                os.makedirs(cat_dir)
                break
            elif c == 'n':
                ctx.abort()

    # Create file
    filename = get_filename(date, language, title)
    file_path = os.path.join(cat_dir, filename)
    if not os.path.exists(file_path):
        click.secho('Creating new article "%s"' % title, fg='green')
        if verbose:
            click.echo('Creating file %s' % click.format_filename(file_path))
        title_length = len(title)
        content = '\n'.join([
            '=' * title_length,
            title,
            '=' * title_length,
            '',
            ':tags: ',
            ':author: Markus Holtermann',
            '',
        ])
        with click.open_file(file_path, mode='w') as f:
            f.write(content)
        click.edit(extension='.rst', filename=file_path)


if __name__ == '__main__':
    main()
