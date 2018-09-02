# trfind
Trip report search tool used by ClimbPlan, hosted at https://climbplan.com.

# Contributing
This is mostly a weekend project, Pull requests are welcome!

## Wishlist
Ideas are tracked using the (issues page)[https://github.com/thatneat/trfind/issues].

# Setup and Running
* Clone the github repo
* `python3 -m venv env`
* `source env/bin/activate`
* `pip install -r requirements.txt`

## CLI Testing
* `pip install --no-deps .`
* `trfind 48.51152 -121.05789 "Forbidden Peak"`

## Browser Testing
* `python app.py`
* visit [http://localhost:5000/test](http://localhost:5000/test)

## Tox
* tox can be used to automate creation of virtual environment and to run the unit tests (pytest)
* `tox`
* `source .tox/py36/bin/activate`
* `trfind 48.51152 -121.05789 "Forbidden Peak"`

# Contributors
* [thatneat](https://github.com/thatneat)
* [jaimemarijke](https://github.com/jaimemarijke)
* [priti-wright](https://github.com/priti-wright)
* [Spectre5](https://github.com/Spectre5)
