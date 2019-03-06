#!/usr/bin/python
import argparse
from util import scrape

parser = argparse.ArgumentParser(description='''A simple web scraper to retrieve
the standings from mlssoccer.com. The output will provide the MLS standings in a
markdown format. If no club abbreviation is provided, it will generate both
conference tables. Otherwise, if a club abbreviation is provided the conference
table for the respective club will be generated.
''')
parser.add_argument('--stats', action='store_true', help='''Generate the top 5
players with goals and assists, respectively. If a club is specified, the
statistics will be unique to the club. Otherwise, it will be the league leaders.
''')
parser.add_argument('--club', help='''Generate the conference table for the
appropriate club. Example: --club dal (for FC Dallas).''')
parser.add_argument('--injuries', action='store_true', help='''Generate a table,
per club, of injured players. If a club is specified, the table will be unique
to the club.''')

def main():
  args = parser.parse_args()
  scrape(args)

if __name__ == '__main__':
  main()
