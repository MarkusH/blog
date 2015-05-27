import os
import subprocess

from os.path import basename, dirname, exists, join, splitext

SIZES = (
    # index
    (520, 293),  # 1 col, small
    (382, 215),  # 2 col, medium
    (397, 224),  # 3 col, large
    # detail
    # 1 col, small: as above
    (786, 230),  # 1 col, medium
    (1026, 300),  # 1 col, large
)


def gen_article_thumbnails(source):
    out = []
    for width, height in SIZES:
        source_dir = dirname(source)
        source_name = basename(source)
        name, ext = splitext(source_name)
        dest_dir = join(source_dir, 'thumb')
        if not exists(dest_dir):
            os.makedirs(dest_dir)
        dest_name = '{0}-{1}x{2}{3}'.format(name, width, height, ext)
        dest = join(dest_dir, dest_name)
        out.append(dest)
        if exists(dest):
            continue
        cmd = [
            'convert',
            source,
            '-resize', '{0}x{1}^'.format(width, height),
            '-gravity', 'center',
            '-crop', '{0}x{1}+0+0'.format(width, height),
            dest,
        ]
        subprocess.call(cmd)
    return out
