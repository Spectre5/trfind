# trfind

Trip report search tool used by ClimbPlan, hosted at https://climbplan.com.

# Contributing

This is mostly a weekend project, Pull requests are welcome!

## Wishlist

Ideas are tracked using the (issues page)[https://github.com/thatneat/trfind/issues].

## Setup and Running

* Clone the github repo
* `python3 -m venv env`
* `source env/bin/activate`
* `pip install -r requirements.txt`

### CLI Testing
* `pip install --no-deps .`
* `trfind 48.51152 -121.05789 "Forbidden Peak"`

### Browser Testing
* Edit the app.py (see the 2 comments in the file)
* `python app.py`
* visit [http://localhost:5000/find](http://localhost:5000/find)

## Contributors

* [thatneat](https://github.com/thatneat)
* [jaimemarijke](https://github.com/jaimemarijke)
* [priti-wright](https://github.com/priti-wright)
