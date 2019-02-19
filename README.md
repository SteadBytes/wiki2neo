# wiki2neo

[![PyPI version shields.io](https://img.shields.io/pypi/v/wiki2neo.svg)](https://pypi.python.org/pypi/wiki2neo/)

Produce [Neo4j](https://neo4j.com/) import CSVs from [Wikipedia database dumps](https://en.wikipedia.org/wiki/Wikipedia:Database_download#English-language_Wikipedia)
to build a graph of links between Wikipedia pages.

## Installation

```bash
$ pip install wiki2neo
```

## Usage

```
Usage: wiki2neo [OPTIONS] [WIKI_XML_INFILE]

  Parse Wikipedia pages-articles-multistream.xml dump into two Neo4j import
  CSV files:

      Node (Page) import, headers=["title:ID", "wiki_page_id"]
      Relationships (Links) import, headers=[":START_ID", ":END_ID"]

  Reads from stdin by default, pass [WIKI_XML_INFILE] to read from file.

Options:
  -p, --pages-outfile FILENAME  Node (Pages) CSV output file  [default:pages.csv]
  -l, --links-outfile FILENAME  Relationships (Links) CSV output file [default: links.csv]
  --help                        Show this message and exit.

Import resulting CSVs into Neo4j:
$ neo4j-admin import --nodes:Page pages.csv \
        --relationships:LINKS_TO links.csv \
        --ignore-duplicate-nodes --ignore-missing-nodes --multiline-fields
```
