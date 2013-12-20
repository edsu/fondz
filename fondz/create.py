import os

from os.path import join
from fondz.topics import topics
from fondz.convert import convert_dir
from fondz.identify import identify_dir
from fondz.utils import render_to, write_json


def create(fondz_dir, *bags, **kwargs):
    init(fondz_dir)

    # add all the bags
    for bag in bags:
        add_bag(fondz_dir, bag)
   
    # try to convert what we can to html
    convert_dir(join(fondz_dir, "originals"), 
                join(fondz_dir, "derivatives"))

    # topic model on the html
    topic_model = topics(join(fondz_dir, "derivatives"))
    write_json(topic_model, join(fondz_dir, "js", "topics.json"))

    # identify formats
    formats = identify_dir(fondz_dir, "originals")
    write_json(formats, join(fondz_dir, "js", "formats.json"))

    # write out the description
    write_index(fondz_dir)


def init(fondz_dir):
    mkdir(fondz_dir, "css")
    mkdir(fondz_dir, "images")
    mkdir(fondz_dir, "js")
    mkdir(fondz_dir, "originals")
    mkdir(fondz_dir, "derivatives")


def add_bag(fondz_dir, bag_dir):
    # TODO: make sure bag_dir is actually a valid bag
    current_bags = os.listdir(join(fondz_dir, "originals"))
    next_orig = str(len(current_bags) + 1)
    src = os.path.abspath(join(bag_dir, "data"))
    link_name = join(fondz_dir, "originals", next_orig)
    os.symlink(src, link_name)


def write_index(fondz_dir):
    index_file = os.path.join(fondz_dir, "index.html")
    html = render_to('index.html', index_file)


def mkdir(*parts):
    path = join(*parts)
    if not os.path.isdir(path):
        os.makedirs(path)
