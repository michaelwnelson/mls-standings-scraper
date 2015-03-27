#!/usr/bin/python

import requests
import bs4

class Club:
	"""A MLS Club"""
	def __init__(self, name, abbreviation, subreddit):
		self.name = name
		self.abbreviation = abbreviation
		self.subreddit = subreddit

# Setup data for club information
all_clubs = {
	# MLS Club Name: Abbreviation, Subreddit
	'Colorado Rapids': ['COL', '/r/rapids'],
	'FC Dallas': ['DAL', '/r/fcdallas'],
	'Houston Dynamo': ['HOU', '/r/dynamo'],
	'LA Galaxy': ['LA', '/r/lagalaxy'],
	'Portland Timbers': ['POR', '/r/timbers'],
	'Real Salt Lake': ['RSL', '/r/realsaltlake'],
	'San Jose Earthquakes': ['SJ', '/r/sjearthquakes'],
	'Seattle Sounders FC': ['SEA', '/r/soundersfc'],
	'Sporting Kansas City': ['SKC', '/r/sportingkc'],
	'Vancouver Whitecaps FC': ['VAN', '/r/whitecapsfc']
}

# Setup our variables for URLs and data to parse
standings_url = requests.get('http://www.mlssoccer.com/standings')
standing_soup = bs4.BeautifulSoup(standings_url.text)

# Western Conference is the 2nd table
standings = standing_soup.select('.stats-table')[1]
standings_data = standings.find('tbody').find_all('tr')

def strip_text(text):
	return text.get_text().strip();

def link_club(_club):
	abbr = all_clubs[_club][0]
	sub = all_clubs[_club][1]
	club = '[%s](%s)' % (abbr, sub)
	return club

def format_club(_club):
	club = strip_text(_club)
	club = link_club(club)
	return club

# Print the standings to stdout
for row in standings_data:
	cells = row.find_all('td')
	rank = strip_text(cells[0])
	club = format_club(cells[1].find('a')) # find 'a' to ignore playoff indicator
	points = '**%s**' % strip_text(cells[2])
	gp = strip_text(cells[3])
	gd = strip_text(cells[10])
	gf = strip_text(cells[8])
	print '%s|%s|%s|%s|%s|%s' % (rank, club, points, gp, gd, gf)
