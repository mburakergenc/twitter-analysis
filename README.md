# twitter-analysis

Analysis of tweets for kahoot

# How to run the application

- Have Docker installed on your system
- If you don't have docker installed, you can run the src/assignment/handler.py file after filling the src/assignment/credentials.py file with your credentials.
- Run the command below to pull the docker image;
  - `docker pull mburakergenc/kahootassignment`
- Run the command below to run the container;
  - `docker run -ti mburakergenc/kahootassignment`
- Enter a search term when requested by the application such as "Donald"
- Please try to select a high volume keyword to see all the details analysis. You'll get warnings printed when the keyword doesn't have any tweets within the last 1, 5, 60 minutes.
- Results are limited to **500 tweets** for performance reasons. It should take a few seconds for 500 tweets to be loaded from Twitter.

# How to run the tests

- cd into the project directory
  - `cd twitter-analysis`
- `py.test`
