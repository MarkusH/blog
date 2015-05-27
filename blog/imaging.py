import os
import pprint
import subprocess

from os.path import basename, dirname, exists, join, splitext

COVER_IMAGE_SIZES = (
    # index
    (520, 293),  # 1 col, small
    (382, 215),  # 2 col, medium
    (397, 224),  # 3 col, large
    # detail
    # 1 col, small: as above
    (786, 230),  # 1 col, medium
    (1026, 300),  # 1 col, large
)


def gen_article_thumbnails(source, sizes=None):
    out = []
    img_base_dir = join('content', 'images')
    thumb_base_dir = join(img_base_dir, 'thumb')
    source_dir = dirname(source)
    source_name = basename(source)
    name, ext = splitext(source_name)
    dest_dir = join(thumb_base_dir, source_dir)
    if not exists(dest_dir):
        os.makedirs(dest_dir)
    if sizes is None:
        sizes = COVER_IMAGE_SIZES
    for width, height in sizes:
        dest_name = '{0}-{1}x{2}{3}'.format(name, width, height, ext)
        dest = join(dest_dir, dest_name)
        out.append(join(source_dir, dest_name))
        if exists(dest):
            continue
        cmd = [
            'convert',
            join(img_base_dir, source),
            '-resize', '{0}x{1}^'.format(width, height),
            '-gravity', 'center',
            '-crop', '{0}x{1}+0+0'.format(width, height),
            dest,
        ]
        subprocess.call(cmd)
    return out
