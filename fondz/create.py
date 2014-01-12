import os
import json
import logging
from os.path import join, isdir, abspath

from fondz.topics import topics
from fondz.convert import convert
from fondz.identify import identify, summarize
from fondz.utils import render_to, write_json, read_json


def create(fondz_dir, *bags, **kwargs):
    init(fondz_dir)

    # add all the bags
    for bag in bags:
        add_bag(fondz_dir, bag)
   
    # try to convert what we can to html
    convert(fondz_dir)

    # identify formats
    formats = identify(fondz_dir)
    write_json(formats, join(fondz_dir, "js", "formats.json"))

    # topic model on the html
    topic_model = topics(join(fondz_dir, "derivatives"))
    write_json(topic_model, join(fondz_dir, "js", "topics.json"))

    # ideas:
    # ocr?
    # thumbnails?
    # dzi files?
    # move/copy log file into fondz_dir?

    # finally, write out the description
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
    link_name = join(fondz_dir, "originals", next_orig)
    bag_dir = os.path.abspath(bag_dir)
    logging.info("symlinking %s to %s", bag_dir, link_name)
    os.symlink(bag_dir, link_name)


def write_index(fondz_dir):
    index_file = join(fondz_dir, "index.html")
    topics = read_json(join(fondz_dir, "js", "topics.json"))
    formats = read_json(join(fondz_dir, "js", "formats.json"))
    format_summary = summarize(formats)

    render_to('index.html', index_file, topics=topics,
            format_summary=format_summary)


def mkdir(*parts):
    path = join(*parts)
    if not isdir(path):
        os.makedirs(path)
