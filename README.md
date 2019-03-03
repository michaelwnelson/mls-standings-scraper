## MLS Standings Scraper

This is a simple web scraper written in Python to retrieve the standings from [mlssoccer.com](http://www.mlssoccer.com/).

The idea stemmed from the desire to quickly interpret the standings in to a Markdown friendly format for the [FC Dallas subreddit](http://www.reddit.com/r/fcdallas/) sidebar.

## Dependencies

python, pip, requests, beautifulsoup4

## Installation

Clone with git:

```
git clone https://github.com/michaelwnelson/mls-standings-scraper
```

Resolve dependencies:

```
pip install --user -r requirements.txt
```

Don't have pip? Refer to [their documentation for installation](https://pip.pypa.io/en/stable/installing/).

## Usage

**Note**: Provide the `--help` argument for command line usage descriptions.

Executing the script without any arguments:

```
./mls.py
```

Will provide a Markdown friendly output of both conference tables:

```
=== Eastern Conference ===
1|[NYC](/r/nycfc)|5|3|2|3
2|[NYRB](/r/rbny)|4|2|2|3
3|[OCSC](/r/oclions)|4|3|0|2
4|[CLB](/r/thremassive)|3|2|1|2
5|[TFC](/r/tfc)|3|2|0|3
6|[DC](/r/dcunited)|3|2|-1|1
7|[PHI](/r/phillyunion)|2|3|-2|3
8|[MTL](/r/montrealimpact)|1|2|-1|0
9|[NE](/r/newenglandrevolution)|1|3|-5|0
10|[CHI](/r/chicagofire)|0|3|-4|1

=== Western Conference ===
1|[DAL](/r/fcdallas)|9|3|5|6
2|[SJ](/r/sjearthquakes)|6|3|1|5
3|[VAN](/r/whitecapsfc)|6|3|0|3
4|[LA](/r/lagalaxy)|5|3|2|5
5|[HOU](/r/dynamo)|4|3|0|2
6|[SEA](/r/soundersfc)|3|2|2|5
7|[POR](/r/timbers)|3|3|0|2
8|[COL](/r/rapids)|2|2|0|0
9|[RSL](/r/realsaltlake)|2|2|0|3
10|[SKC](/r/sportingkc)|2|3|-2|2
```

Use the `--club` argument to get a club's respective conference table. The club will emphasized with bolded formatting:

```
$ ./mls --club dal

=== Western Conference ===
**1**|**[DAL](/r/fcdallas)**|**9**|**3**|**5**|**6**
2|[SJ](/r/sjearthquakes)|6|3|1|5
3|[VAN](/r/whitecapsfc)|6|3|0|3
4|[LA](/r/lagalaxy)|5|3|2|5
5|[HOU](/r/dynamo)|4|3|0|2
6|[SEA](/r/soundersfc)|3|2|2|5
7|[POR](/r/timbers)|3|3|0|2
8|[COL](/r/rapids)|2|2|0|0
9|[RSL](/r/realsaltlake)|2|2|0|3
10|[SKC](/r/sportingkc)|2|3|-2|2
```

If you add the `--stats` argument, you will get both goals and assists statistics for the league.

Combine the club `--club dal` argument with the `--stats` argument to get goals and assists specific to the club provided.

Example output:

```
$ ./mls --club dal --stats

=== GOALS ===
[Blas Perez](http://www.mlssoccer.com/players/blas-perez "Blas Perez")|3
[Tesho Akindele](http://www.mlssoccer.com/players/tesho-akindele "Tesho Akindele")|2
[Fabian Castillo](http://www.mlssoccer.com/players/fabian-castillo "Fabian Castillo")|1
[Ryan Hollingshead](http://www.mlssoccer.com/players/ryan-hollingshead "Ryan Hollingshead")|1
[Michel](http://www.mlssoccer.com/players/michel-garbini-pereira "Michel")|0

=== ASSISTS ===
[Michel](http://www.mlssoccer.com/players/michel-garbini-pereira "Michel")|3
[Fabian Castillo](http://www.mlssoccer.com/players/fabian-castillo "Fabian Castillo")|2
[Atiba Harris](http://www.mlssoccer.com/players/atiba-harris "Atiba Harris")|1
[Moises Hernandez](http://www.mlssoccer.com/players/moises-hernandez "Moises Hernandez")|1
[Ryan Hollingshead](http://www.mlssoccer.com/players/ryan-hollingshead "Ryan Hollingshead")|1
```

## Contributing

If you would like to contribute a new feature or bug fix:

1.  Fork it
2.  Create your feature branch (`git checkout -b my-new-feature`)
3.  Commit your changes (`git commit -am 'Add some feature'`)
4.  Push to the branch (`git push origin my-new-feature`)
5.  Create a new Pull Request
