MLS_STANDINGS_URL = 'http://www.mlssoccer.com/standings'

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

  def __init__(self, name, abbreviation, conference, subreddit, franchise_number,
      rank=0, points=0, games_played=0, goal_difference=0, goals_for=0):
    self.name = name
    self.abbreviation = abbreviation
    self.conference = conference
    self.subreddit = subreddit
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

ATL  = Club('Atlanta United FC',         'ATL',  'Eastern', '/r/atlantaunited',         11091)
CHI  = Club('Chicago Fire',              'CHI',  'Eastern', '/r/chicagofire',           1207)
COL  = Club('Colorado Rapids',           'COL',  'Western', '/r/rapids',                436)
CLB  = Club('Columbus Crew SC',          'CLB',  'Eastern', '/r/thremassive',           454)
DC   = Club('D.C. United',               'DC',   'Eastern', '/r/dcunited',              1326)
FCD  = Club('FC Dallas',                 'DAL',  'Western', '/r/fcdallas',              1903)
HOU  = Club('Houston Dynamo',            'HOU',  'Western', '/r/dynamo',                1897)
LAFC = Club('Los Angeles Football Club', 'LAFC', 'Western', '/r/LAFC',                  1230)
LAG  = Club('LA Galaxy',                 'LA',   'Western', '/r/lagalaxy',              11690)
MNU  = Club('Minnesota United FC',       'MNU',  'Western', '/r/minnesotaunited',       6977)
MTL  = Club('Montreal Impact',           'MTL',  'Eastern', '/r/montrealimpact',        1616)
NE   = Club('New England Revolution',    'NE',   'Eastern', '/r/newenglandrevolution',  928)
NYC  = Club('New York City FC',          'NYC',  'Eastern', '/r/nycfc',                 9668)
NYRB = Club('New York Red Bulls',        'NYRB', 'Eastern', '/r/rbny',                  399)
OCSC = Club('Orlando City SC',           'OCSC', 'Eastern', '/r/oclions',               6900)
PHI  = Club('Philadelphia Union',        'PHI',  'Eastern', '/r/phillyunion',           5513)
POR  = Club('Portland Timbers',          'POR',  'Western', '/r/timbers',               1581)
RSL  = Club('Real Salt Lake',            'RSL',  'Western', '/r/realsaltlake',          1899)
SJ   = Club('San Jose Earthquakes',      'SJ',   'Western', '/r/sjearthquakes',         1131)
SEA  = Club('Seattle Sounders FC',       'SEA',  'Western', '/r/soundersfc',            3500)
SKC  = Club('Sporting Kansas City',      'SKC',  'Western', '/r/sportingkc',            421)
TOR  = Club('Toronto FC',                'TFC',  'Eastern', '/r/tfc',                   2077)
VAN  = Club('Vancouver Whitecaps FC',    'VAN',  'Western', '/r/whitecapsfc',           1708)

ALL_CLUBS = {
  ATL, CHI, COL, CLB, DC, FCD, HOU, LAFC, LAG, MNU, MTL, NE, NYC, NYRB, OCSC,
  PHI, POR, RSL, SJ, SEA, SKC, TOR, VAN
}

def __strip_text(text):
  return text.get_text().strip();

def __find_club(name):
  for club in ALL_CLUBS:
    # playoffs really mess this up
    if name.startswith(("x", "y", "s")):
      name = name[4:]
    if club.name.lower() == name.lower():
      return club

  sys.exit("Could not find club %s" % name)

def setup(data):
  for row in data:
    cells = row.find_all('td')
    rank = __strip_text(cells[0])
    # skip first row of tables as it's a psuedo table header
    if rank == "#":
      continue
    # the table has classes to show the club name or abbreviation for
    # desktop and mobile browsers, the below class is the full club name
    name = __strip_text(cells[1].select('.hide-on-mobile-inline')[0]);
    points = __strip_text(cells[2])
    gp = __strip_text(cells[5])
    gd = __strip_text(cells[11])
    gf = __strip_text(cells[9])
    # Set Club's option attributes
    club = __find_club(name)
    club.rank = rank
    club.points = points
    club.games_played = gp
    club.goal_difference = gd
    club.goals_for = gf

def standings(conference):
  clubs = sorted(ALL_CLUBS, key=lambda c: int(c.rank))
  print "Pos|Club|Pts|GP|GD|GF"
  print ":--:|:--|:--:|:--:|:--:|:--:"
  for club in clubs:
    if club.conference.lower() == conference.lower():
      print club

def stats(data, type):
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
