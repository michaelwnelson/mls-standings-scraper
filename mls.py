#!/usr/bin/python
import sys
import requests
import bs4
from util import setup, standings, stats

def main():
  # Setup our variables for URLs and data to parse
  standings_url = requests.get('http://www.mlssoccer.com/standings')
  standing_soup = bs4.BeautifulSoup(standings_url.text, "html.parser")

  # East Conference is the 1st table
  eastern_table = standing_soup.select('.standings_table')[0]
  eastern_data = eastern_table.find('tbody').find_all('tr')

  # Western Conference is the 2nd table
  western_table = standing_soup.select('.standings_table')[1]
  western_data = western_table.find('tbody').find_all('tr')

  all_data = eastern_data + western_data
  setup(all_data)
  print "=== Eastern Conference ==="
  standings("Eastern")
  print "\n=== Western Conference ==="
  standings("Western")

if __name__ == '__main__':
  main()
