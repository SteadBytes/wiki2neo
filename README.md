# wiki2neo

Produce [Neo4j](https://neo4j.com/) import CSVs from [Wikipedia database dumps](https://en.wikipedia.org/wiki/Wikipedia:Database_download#English-language_Wikipedia)
to build a graph of links between Wikipedia pages.

```
Usage: wiki2neo [OPTIONS] [WIKI_XML_INFILE]

  Parse Wikipedia pages-articles-multistream.xml dump into two Neo4j import
  CSV files:

      Node (Page) import, headers=["title:ID", "wiki_page_id"]
      Relationships (Links) import, headers=[":START_ID", ":END_ID"]

  Reads from stdin by default, pass [WIKI_XML_INFILE] to read from file.

Options:
  -p, --pages-outfile FILENAME  Node (Pages) CSV output file
  -l, --links-outfile FILENAME  Relationshiphs (Links) CSV output file
  --help                        Show this message and exit.
```
