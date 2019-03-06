import bs4
import datetime
import json
import requests
import sys

MLS_URL = 'http://www.mlssoccer.com'
MLS_STANDINGS_URL = 'http://www.mlssoccer.com/standings'
MLS_STATS_URL = 'https://www.mlssoccer.com/stats/season'
MLS_INJURIES_URL = 'https://www.mlssoccer.com/injuries'
ALL_CLUBS = set()



class Club:
  """
  A MLS Club

  Required Attributes:
    name: The name of the club.
    abbreviation: The common abbreviation for the club.
    conference: The conferences of the club.
    subreddit: The subreddit (per /r/mls) for the club.
    website: The club's official website.
    franchise: The unique ID of the club used for querying statistics
    selected: Whether this club was specified by input.
  Optional Attributes:
    rank: The club's rank.
    points: Total accumulated points.
    games_played: Number of games played.
    goal_difference: The positive or negative goal difference. This is the sum
      of goals for and goals against.
    goals_for: Total number of goals scored.
  """
  def __init__(self, name, abbreviation, conference, subreddit, website,
      franchise, selected, rank=0, points=0, games_played=0, goal_difference=0,
      goals_for=0):
    self.name = name
    self.abbreviation = abbreviation
    self.conference = conference
    self.subreddit = subreddit
    self.website = website
    self.franchise = franchise
    self.selected = selected
    self.rank = rank
    self.points = points
    self.games_played = games_played
    self.goal_difference = goal_difference
    self.goals_for = goals_for

  def __str__(self):
    if self.selected:
      fmt = '**%s**|**[%s](%s)**|**%s**|**%s**|**%s**|**%s**'
    else:
      fmt = '%s|[%s](%s)|%s|%s|%s|%s'

    return fmt % (self.rank, self.abbreviation, self.subreddit, self.points,
        self.games_played, self.goal_difference, self.goals_for)

  def print_injuries(self):
    tmp = []
    for injury in self.injuries:
      tmp.append(injury)

    return '\n'.join(tmp)




def __strip_text(text):
  return text.get_text().strip()



def __setup_clubs(selected_club):
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
    website = club['website']
    franchise = club['franchise']
    selected = False

    if (selected_club):
      selected = selected_club.lower() == abbreviation.lower()

    club_object = Club(name, abbreviation, conference, subreddit, website, franchise, selected)
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



def __stats_table(data, group, club_abbreviation = None):
  table = ''

  if (club_abbreviation):
    # if a club_abbreviation is provided the Club column is not present
    idx = 5 if group.lower() == "goals" else 4
  else:
    idx = 6 if group.lower() == "goals" else 5

  for row in data[:5]:
    cells = row.find_all('td')
    if cells[0].find('a') is not None:
      player_name = __strip_text(cells[0].find('a'))
    else:
      player_name = __strip_text(cells[0])
    url = cells[0].find('a').get('href')
    goals = __strip_text(cells[idx])

    # default to MLS_URL, if club is provided use club's website to link to the player's profile
    website = MLS_URL
    if (club_abbreviation):
      club = __find_club_by_abbreviation(club_abbreviation)
      website = club.website

    table += '[%s](%s "%s")|%s \n' \
      % (player_name, website + url, player_name, goals)

  return table



def __get_standings():
  data = requests.get(MLS_STANDINGS_URL)
  return bs4.BeautifulSoup(data.text, "html.parser")



def __print_standings(club_abbreviation):
  standings = __get_standings()
  eastern = __get_conference(standings, "Eastern")
  western = __get_conference(standings, "Western")
  all_data = eastern + western
  __add_data_to_clubs(all_data)

  if (club_abbreviation):
    club = __find_club_by_abbreviation(club_abbreviation)
    print "=== %s Conference ===" % club.conference
    __standings(club.conference)
  else:
    print "=== Eastern Conference ==="
    __standings("Eastern")
    print "\n=== Western Conference ==="
    __standings("Western")



def __get_conference(standings, conference):
  # East Conference is the 1st table
  table_index = 0
  if conference == "Western":
    # Western Conference is the 2nd table
    table_index = 1

  table = standings.select('.standings_table')[table_index]
  return table.find('tbody').find_all('tr')



def __get_stats(club, group):
  # set defaults for year and season_type (where season_type is regular or post)
  # TODO allow the user to specify year and season_type
  year = datetime.datetime.now().year
  season_type = 'REG'

  url = MLS_STATS_URL + '?year=%s&season_type=%s' % (year, season_type)

  if (club):
    url += '&franchise=%s' % __find_club_by_abbreviation(club).franchise

  if (group):
    url += '&group=%s' % group

  req = requests.get(url)
  soup = bs4.BeautifulSoup(req.text, "html.parser")
  table = soup.select('.season_stats')[0]
  data = table.find('tbody').find_all('tr')

  return __stats_table(data, group, club)



def __set_injuries():
  data = requests.get(MLS_INJURIES_URL)
  soup = bs4.BeautifulSoup(data.text, "html.parser")

  containers = soup.select('.card-container')
  for container in containers:
    container_id = container.get('id')
    club_name = __strip_text(container.select('.clb-name h2')[0])
    all_injuries = container.select('.card-body ul li')
    stripped_injuries = [__strip_text(injury) for injury in all_injuries]
    club = __find_club_by_abbreviation(container_id)
    club.injuries = stripped_injuries



def __print_stats(club):
  goals = __get_stats(club, 'goals')
  print "\n=== GOALS ==="
  print "Player|Goals"
  print ":--:|:--:"
  print goals
  assists = __get_stats(club, 'assists')
  print "=== ASSISTS ==="
  print "Player|Assists"
  print ":--:|:--:"
  print assists



def __print_injuries(club):
  injuries = __set_injuries()

  print "\n=== INJURIES ==="

  if (club):
    c = __find_club_by_abbreviation(club)
    print c.print_injuries()
  else:
    clubs = sorted(ALL_CLUBS, key=lambda c: c.abbreviation)
    for club in clubs:
      print "# %s" % club.name
      print club.print_injuries()
      print ""



def scrape(args):
  __setup_clubs(args.club)

  __print_standings(args.club)

  if(args.stats):
    __print_stats(args.club)

  if(args.injuries):
    __print_injuries(args.club)
