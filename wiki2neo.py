import csv
import re
import sys
import time
from datetime import timedelta
from xml.etree import ElementTree

import click

PAGES_CSV_FILENAME = "pages.csv"
LINKS_CSV_FILENAME = "links.csv"
PROGRESS_N = 100_000

LINK_RE = re.compile(r"\[\[(?:[^|\]]*\|)?([^\]]+)\]\]")


def strip_tag_name(element):
    t = element.tag
    idx = t.rfind("}")
    return t[idx + 1 :] if idx != -1 else t


def parse_links(text):
    links = set()
    for m in LINK_RE.finditer(text):
        link_text = m.group(1)
        if ":" not in link_text:
            links.add(link_text.strip())
    return links


def parse_pages(wiki_xml_f, pages_f, links_f):
    """
    Parse Wikipedia XML dump into two files:
        - `pages_fp`: Neo4j Node import CSV ["title:ID", "wiki_page_id"]
        - `links_fp`: Intermediary CSV of links [":START_ID", "END_TITLE"]
    """
    pages_writer = csv.writer(pages_f)
    links_writer = csv.writer(links_f)
    pages_writer.writerow(["title:ID", "wiki_page_id"])
    links_writer.writerow([":START_ID", ":END_ID"])

    page_count = link_count = 0

    title = ""
    _id = -1
    links = set()
    in_revision = False

    for event, element in ElementTree.iterparse(wiki_xml_f, events=("start", "end")):
        tname = strip_tag_name(element)

        if event == "start":
            if tname == "page":
                title = ""
                _id = -1
                in_revision = False
                links = set()
            if tname == "revision":
                in_revision = True
        else:
            if tname == "title":
                title = element.text.strip()
            elif tname == "id" and not in_revision:
                _id = element.text
            elif tname == "text":
                if element.text:
                    links = parse_links(element.text)
                    link_count += len(links)
            elif tname == "page":
                pages_writer.writerow([title, _id])
                links_writer.writerows([title, l] for l in links if l != title)
                page_count += 1

                if page_count > 1 and page_count % PROGRESS_N == 0:
                    print(f"Pages processed: {page_count}")
                    print(f"Links found: {link_count}")

            element.clear()
    return page_count, link_count


@click.command()
@click.argument("wiki-xml-infile", required=False, default=sys.stdin, type=click.File())
@click.option(
    "-p", "--pages-outfile", default=PAGES_CSV_FILENAME, type=click.File(mode="w")
)
@click.option(
    "-l", "--links-outfile", default=LINKS_CSV_FILENAME, type=click.File(mode="w")
)
def main(wiki_xml_infile, pages_outfile, links_outfile):
    """
    Parse Wikipedia XML dump into two Neo4j import CSV files:
        - `pages_outfile`: Node (Page) import ["title:ID", "wiki_page_id"]
        - `links_outfile`: Relationships (Links) import [":START_ID", ":END_ID"]
    """
    start = time.time()
    page_count, link_count = parse_pages(
        wiki_xml_infile, pages_outfile, links_outfile
    )
    end = time.time()
    print(f"Processed {page_count} pages to {pages_outfile.name}")
    print(f"Extracted {link_count} links to {links_outfile.name}")
    print(f"Total Time: {timedelta(seconds=end - start)}")
    print(f"Import CSVs into Neo4j:")
    print(
        (
            f"\t$ neo4j-admin import --nodes:Page {pages_outfile.name}"
            f" --relationships:LINKS_TO {links_outfile.name}"
        )
    )


if __name__ == "__main__":
    main()
