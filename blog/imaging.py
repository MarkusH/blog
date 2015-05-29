import hashlib
import json
import os
import shutil
import subprocess
import tempfile

from os.path import basename, dirname, exists, join, splitext

FILENAME = object()


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

IMG_BASE_DIR = join('content', 'images')
EQUATION_BASE_DIR = join(IMG_BASE_DIR, 'equation')
THUMB_BASE_DIR = join(IMG_BASE_DIR, 'thumb')
MANIFEST_FILE = join(THUMB_BASE_DIR, '.manifest.json')

OPTIMIZE_COMMANDS = {
    '.jpg': ['jpegtran', '-copy', 'none', '-optimize', '-outfile', FILENAME, FILENAME],
    '.png': ['optipng', FILENAME],
}


def load_manifest():
    data = {}
    if exists(MANIFEST_FILE):
        with open(MANIFEST_FILE) as fp:
            data = json.load(fp)
    return data


def write_manifest(data):
    with open(MANIFEST_FILE, 'w') as fp:
        json.dump(data, fp)


def get_hash(filename):
    with open(filename, 'rb') as fp:
        data = fp.read()
    m = hashlib.md5()
    m.update(data)
    return m.hexdigest()


def get_optimize_command(ext, filename):
    if ext not in OPTIMIZE_COMMANDS:
        return None
    cmd = OPTIMIZE_COMMANDS[ext]
    return [(filename if part is FILENAME else part) for part in cmd]


def gen_article_thumbnails(source, sizes=None):
    out = []
    source_dir = dirname(source)
    source_name = basename(source)
    name, ext = splitext(source_name)
    source_file = join(IMG_BASE_DIR, source)
    dest_dir = join(THUMB_BASE_DIR, source_dir)
    if not exists(dest_dir):
        os.makedirs(dest_dir)

    manifest = load_manifest()
    hash = get_hash(source_file)
    if hash == manifest.get(source, ''):
        skip = True
    else:
        skip = False
        manifest[source] = hash

    if sizes is None:
        sizes = COVER_IMAGE_SIZES
    for width, height in sizes:
        dest_name = '{0}-{1}x{2}{3}'.format(name, width, height, ext)
        dest = join(dest_dir, dest_name)
        out.append(join(source_dir, dest_name))
        if skip and exists(dest):
            continue
        cmd = [
            'convert', '-verbose',
            source_file,
            '-resize', '{0}x{1}^'.format(width, height),
            '-gravity', 'center',
            '-crop', '{0}x{1}+0+0'.format(width, height),
            dest,
        ]
        subprocess.call(cmd)

        optimize = get_optimize_command(ext, dest)
        if optimize:
            subprocess.call(optimize)

    if not skip:
        write_manifest(manifest)
    return out


def gen_equation_image(equation):
    if not exists(EQUATION_BASE_DIR):
        os.makedirs(EQUATION_BASE_DIR)

    content = [
        r'\documentclass[convert={density=150},preview]{standalone}',
        r'\usepackage{amsmath}',
        r'\begin{document}',
    ]
    content.extend(equation)
    content.extend([
        r'\end{document}'
    ])

    text = '\n'.join(content)
    hash = hashlib.md5(text).hexdigest()
    dest_file = join(EQUATION_BASE_DIR, hash + '.png')

    out = dest_file[len('content'):]

    if exists(dest_file):
        return out

    with tempfile.NamedTemporaryFile('w', suffix='.tex') as tfp:
        tfp.write(text)
        tfp.flush()
        subprocess.check_call(
            ['pdflatex', '-shell-escape', tfp.name],
            cwd=dirname(tfp.name)
        )
        name, ext = splitext(tfp.name)
        source_file = name + '.png'
        subprocess.check_call(
            ['convert', '-trim', source_file, source_file],
            cwd=dirname(tfp.name)
        )
        shutil.move(source_file, dest_file)

    return out
