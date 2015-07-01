# ai-at-the-web-scale
Final project for "AI at the web scale" course. This project involves maximizing the cumulative reward for simulated visitors on a website by serving ads with various parameters. This is a contextual bandit problem.



##Dependencies
* Python 2.7
* **numpy**, **pandas**, **sklearn**, **matplotlib**, **scipy**.
* **plotta-python** (`pip install plotta`). You should run [Plotta](https://github.com/gzuidhof/plotta) locally for live plotting of some stats.


##Directions
Add a `credentials.py` file with two variables, `TEAM_ID` and `PASSWORD` with your team name and password for the API.

####Data retrieval and analysis
* `context_get_pool.py` contains a parallel generator of contexts (so that at least one is always ready), this halves the running time more or less.
* `scraper.py` Parallel scraper, uses random actions.
* `analysis.py` Ad-hoc script for exploring the scraped data. 
* `api.py` Wrapper for the REST API.

###Model/learning
* `bts.py` [Bootstrap Thompson Sampling](http://arxiv.org/pdf/1410.4009v1.pdf) implementation.
* `models.py` Contains all models (Random, Linear model, Thompson sampling model)
* `decode.py, encode.py` Used for encoding and decoding of actions and contexts from and into a feature vector.
* `linmod.py` Offline linear model.

###Misc
* `constants.py` Contains domain information of the assignment.
* `run.py` Entry point.

