#!/usr/bin/python
import sys
import requests
import bs4
from util import setup, standings, stats

def main():
  # Setup our variables for URLs and data to parse
  standings_url = requests.get('http://www.mlssoccer.com/standings')
  goals_url = requests.get('http://www.mlssoccer.com/stats/season?franchise=1903&year=2018&season_type=REG&group=goals')
  assists_url = requests.get('http://www.mlssoccer.com/stats/season?franchise=1903&year=2018&season_type=REG&group=assists')
  standing_soup = bs4.BeautifulSoup(standings_url.text, "html.parser")
  goals_soup = bs4.BeautifulSoup(goals_url.text, "html.parser")
  assits_soup = bs4.BeautifulSoup(assists_url.text, "html.parser")

  # Western Conference is the 2nd table
  western_table = standing_soup.select('.standings_table')[1]
  western_data = western_table.find('tbody').find_all('tr')

  # Grab the goals table
  goals = goals_soup.select('.season_stats')[0]
  goals_data = goals.find('tbody').find_all('tr')

  # Grab the assists table
  assists = assits_soup.select('.season_stats')[0]
  assists_data = assists.find('tbody').find_all('tr')

  setup(western_data)
  print "\n=== STANDINGS ==="
  standings("Western")
  print "\n=== GOALS ==="
  stats(goals_data, "goals")
  print "\n=== ASSISTS ==="
  stats(assists_data, "assists")

if __name__ == '__main__':
  main()
