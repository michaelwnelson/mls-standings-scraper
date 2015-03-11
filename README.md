## MLS Standings Scraper

This is a simple web scraper written in Python to retrieve the standings from [mlssoccer.com][1].

The idea stemmed from the desire to quickly interpret the standings in to a Markdown friendly format for the [FCD subreddit][2] sidebar.

## Dependencies

python, requests, beautifulsoup4

## Installation

Clone with git:

```
git clone https://github.com/michaelwnelson/mls-standings-scraper
```

Resolve dependencies:

```
pip install -r requirements.txt
```

## Contributing

Currently the script is setup to only parse the Western Table. Adding support for the Eastern table is trivial, and eventually I'd like to extend this to allow the user to pick which data points they desire.

If you would like to contribute a new feature or bug fix:

1. Fork it
2. Create your feature branch (`git checkout -b my-new-feature`)
3. Commit your changes (`git commit -am 'Add some feature'`)
3. Push to the branch (`git push origin my-new-feature`)
4. Create a new Pull Request

## License
[Apache License 2.0][3]

[1]: http://www.mlssoccer.com/
[2]: http://www.reddit.com/r/fcdallas/
[3]: http://www.apache.org/licenses/LICENSE-2.0
