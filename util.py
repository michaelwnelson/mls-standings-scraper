import bs4
import json
import requests
import sys

MLS_STANDINGS_URL = 'http://www.mlssoccer.com/standings'
ALL_CLUBS = set()

class Club:
  """A MLS Club

  Required Attributes:
    name: The name of the club.
    abbreviation: The common abbreviation for the club.
    subreddit: The subreddit (per /r/mls) for the club.
  Optional Attributes:
    points: Total accumulated points.
    games_played: Number of games played.
    goal_difference: The positive or negative goal difference. This is
      the sum of goals for and goals against.
    goals_for: Total number of goals scored.
  """
  def __init__(self, name, abbreviation, conference, subreddit, franchise,
      rank=0, points=0, games_played=0, goal_difference=0, goals_for=0):
    self.name = name
    self.abbreviation = abbreviation
    self.conference = conference
    self.subreddit = subreddit
    self.franchise = franchise
    self.rank = rank
    self.points = points
    self.games_played = games_played
    self.goal_difference = goal_difference
    self.goals_for = goals_for


  def __str__(self):
    if self.abbreviation == 'DAL':
      fmt = '**%s**|**[%s](%s)**|**%s**|**%s**|**%s**|**%s**'
    else:
      fmt = '%s|[%s](%s)|%s|%s|%s|%s'

    return fmt % (self.rank, self.abbreviation, self.subreddit, self.points,
        self.games_played, self.goal_difference, self.goals_for)



def __strip_text(text):
  return text.get_text().strip()



def __setup_clubs():
  with open("clubs.json") as data:
    clubs = json.load(data)

  for club in clubs:
    name = club['name']
    # playoffs really mess this up
    if name.startswith(("x", "y", "s")):
      name = name[4:]

    abbreviation = club['abbreviation']
    conference = club['conference']
    subreddit = club['subreddit']
    franchise = club['franchise']

    club_object = Club(name, abbreviation, conference, subreddit, franchise)
    ALL_CLUBS.add(club_object)



def __find_club_by_abbreviation(abbr):
  for club in ALL_CLUBS:
    if club.abbreviation.lower() == abbr.lower():
      return club

  sys.exit("Could not find club by abbreviation: %s" % abbr)



def __add_data_to_clubs(data):
  for row in data:
    cells = row.find_all('td')
    rank = __strip_text(cells[0])
    # skip first row of tables as it's a psuedo table header
    if rank == "#":
      continue
    # the table has classes to show the club name or abbreviation for
    # desktop and mobile browsers, the below class is the full club name
    name = __strip_text(cells[1].select('.hide-on-mobile-inline')[0])
    abbreviation = __strip_text(cells[1].select('.show-on-mobile-inline')[0])
    points = __strip_text(cells[2])
    games_played = __strip_text(cells[5])
    goal_difference = __strip_text(cells[11])
    goals_for = __strip_text(cells[9])
    # Set Club's optional attributes
    club = __find_club_by_abbreviation(abbreviation)
    club.rank = rank
    club.points = points
    club.games_played = games_played
    club.goal_difference = goal_difference
    club.goals_for = goals_for



def __standings(conference):
  clubs = sorted(ALL_CLUBS, key=lambda c: int(c.rank))
  print "Pos|Club|Pts|GP|GD|GF"
  print ":--:|:--|:--:|:--:|:--:|:--:"
  for club in clubs:
    if club.conference.lower() == conference.lower():
      print club



def __stats(data, type):
  idx = 5 if type.lower() == "goals" else 4
  for row in data[:5]:
    cells = row.find_all('td')
    if cells[0].find('a') is not None:
      player_name = __strip_text(cells[0].find('a'))
    else:
      player_name = __strip_text(cells[0])
    url = cells[0].find('a').get('href')
    goals = __strip_text(cells[idx])
    print '[%s](http://www.fcdallas.com%s "%s")|%s' \
      % (player_name, url, player_name, goals)



def __get_standings():
  data = requests.get(MLS_STANDINGS_URL)
  return bs4.BeautifulSoup(data.text, "html.parser")



def __get_conference(standings, conference):
  # East Conference is the 1st table
  table_index = 0
  if conference == "Western":
    # Western Conference is the 2nd table
    table_index = 1

  table = standings.select('.standings_table')[table_index]
  return table.find('tbody').find_all('tr')



def scrape(args):
  __setup_clubs()
  standings = __get_standings()
  eastern = __get_conference(standings, "Eastern")
  western = __get_conference(standings, "Western")

  all_data = eastern + western
  __add_data_to_clubs(all_data)
  print "=== Eastern Conference ==="
  __standings("Eastern")
  print "\n=== Western Conference ==="
  __standings("Western")
