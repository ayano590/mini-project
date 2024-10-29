---PROJECT GOALS---

This project aims to fetch the artists (and groups) from the best 50 Jazz Albums
(according to https://jazzfuel.com/best-jazz-albums/),
as well as the best 30 Rock Bands.
(according to https://www.forbes.com/sites/entertainment/article/best-rock-bands/)

The API then looks up all events linked to them, be it festivals, concerts and the like.

The genres, artists and events are then saved in their respective tables with PostGreSQL.

The user is asked to provide an artist name, in order to get the events and an image, if there is one.
The image is saved into the project folder.

The program outputs a csv file with all events found, as well as a graphical representation:
event count for each artist/group split by genre, and a comparison of event counts for jazz and rock.

---SETUP---

DISCLAIMER: For unit testing or in order to create all tables from scratch,
uncomment line 18 from save_data.py located in the my_packages folder.
The program is set to skip the API requests if all artists are already in the database,
irrespective of the saved events.

Create a PostGreSQL database in pgAdmin and give it a name.

In the db_config.py file, the user can change the credentials for their server, including the database name.

In order to run this program, start Docker Desktop and the PostGreSQL server.

Then open the IDE of your choice. (PyCharm Professional was used for development)

There are two options to run the Docker container:

1. DOCKER INTERPRETER:

Add a Docker interpreter and select the Dockerfile from this project.
Optional: Define a tag for the Docker image.
Select the system Python interpreter.

DISCLAIMER: According to stackoverflow it is possible to use the Conda Environment,
but it requires you to activate Conda within the Docker Container.
Use a preinstalled version of Python instead.

Link on how to use Conda in Docker: https://stackoverflow.com/questions/52049202/how-to-use-docker-and-conda-in-pycharm

2. CLI (COMMAND LINE INTERFACE):

In the IDE terminal, go to the project folder and run these commands
(replace "imagename" with a name of your choice, without the quotes):

```console
docker build -t "imagename" .
docker run -it --rm -v "${PWD}:/app" "imagename"
```

---OUTPUT---

When the program terminates without error, the preloaded csv and png files will be overwritten.
If the artist image was found, an artist.png file will be added.

The database tables are accessible via pgAdmin for example.