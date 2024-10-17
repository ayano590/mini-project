First step is to get acquainted with the MusicBrainz API.

Find a website where you can find a list of jazz albums. (for web scraping)

Then create project folder with .gitignore, Git repo and link it.

Create the python modules (+ tests) and main script.

Create a Dockerfile and set it up as dev env.

Add the necessary modules to requirements.txt. (more will be added later)

Initial commit.

Add Andreas Schaubmaier and ICMaurer as collaborators.

Write code for the web scraper. (might not work as intended yet)

Commit.

Fix git user.

Issue: web scraper status code 403 due to empty user agent (UA) string. Fix.

Import the scraper into the main script and tested for output.

Commit.

Write code for the musicbrainz API and test it with 'Ella Fitzgerald'.

Change aim of the project to count the number of events, where the artists perform,
rather than trying to extract the country info.
Name of place can be queried easily, but the area code points to a table
outside the simple database representation.

Commit.

Add module psycopg2 to requirements.txt.

Write code for the database API. (not finished)

Commit.

add_artists() takes a list of artists, while add_events takes only one artist and event.

Change api_event() lucene query to search for two artists separately.

Change api_event() to return zip turned to list of tuples, also needs a number in addition to artist name.
(number will be the index in the artists table and has to be fetched first)

Change web_scrape() to return a list of tuples to feed it all in one transaction into the artists table.

Create structure of the main script.

Add get_event_count() method to MBPostgres class. (after lunch break)

Commit.