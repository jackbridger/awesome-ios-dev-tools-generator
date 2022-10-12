import json
import mdutils
from mdutils.tools.TableOfContents import TableOfContents
import os
from dotenv import load_dotenv
from summarize_body import summarize_body
import csv
import time

CSV_OUTPUT_FILE = 'tool_id_to_summary.csv'

INPUT_FILE_PATH = './data/tools.json'
OUTPUT_FILE_NAME = 'awesome-ios'
PAGE_TITLE = 'Awesome iOS Dev Tools'
load_dotenv()

def open_markdown():
    mdFile = mdutils.MdUtils(file_name=OUTPUT_FILE_NAME,title=PAGE_TITLE)
    return mdFile

def create_file(mdFile):
    mdFile.create_md_file()

def get_tag(title):
    return ''.join(title.split())

def add_table_of_contents(mdFile,data):
    mdFile.new_header(level=1, title="Table of categories")
    for category in data:
        formatted_category = json.loads(category['json_agg'])
        category_title = formatted_category[0]['category_title']
        category_tag = get_tag(category_title)
        mdFile.new_paragraph("[{}](#{})".format(category_title,category_tag))

def add_category_header(mdFile,category_title):
    category_tag = get_tag(category_title)
    title_with_tag = "{}<a id='{}'></a>".format(category_title,category_tag)
    mdFile.new_header(level=1, title=title_with_tag)

def send_summary_to_csv(tool_id,summary):
    with open(CSV_OUTPUT_FILE, 'a', newline='') as outcsv:
        writer = csv.writer(outcsv)
        writer.writerow([tool_id, summary])

def add_tool_bullet_point(mdFile,tool):
    id = tool['id']
    long_description = tool['long_body']
    summary = summarize_tool_description(long_description)
    send_summary_to_csv(id,summary)
    mdFile.new_paragraph("* [{}]({}) - {}".format(tool['title'], tool['link'], summary))

def loop_through_categories(mdFile,data):
    for category in data:
        formatted_category = json.loads(category['json_agg'])
        category_title = formatted_category[0]['category_title']
        add_category_header(mdFile,category_title)
        loop_through_tools_in_each_category(formatted_category,mdFile)

def loop_through_tools_in_each_category(category,mdFile):
        for tool in category:
            add_tool_bullet_point(mdFile,tool)

def summarize_tool_description(description):
    summary = summarize_body(description)
    time.sleep(2)
    clean_summary = summary.strip()
    return clean_summary

def add_introduction(mdFile):
    mdFile.new_paragraph("Maintained by [iOS Dev Tools](https://iosdev.tools/)")

def init_summary_csv():
    with open(CSV_OUTPUT_FILE, 'w', newline='') as csvfile:
        fieldnames = ['tool_id', 'summary']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

def main():
    init_summary_csv()
    f = open(INPUT_FILE_PATH)
    data = json.load(f)
    mdFile = open_markdown()
    add_introduction(mdFile)
    add_table_of_contents(mdFile,data)
    loop_through_categories(mdFile,data)
    create_file(mdFile)
    f.close()

main()
