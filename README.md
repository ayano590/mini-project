---PROJECT GOALS---

This project aims to fetch the artists (and groups) from the best 50 Jazz Albums.
(according to https://jazzfuel.com/best-jazz-albums/)

The API then looks up all events linked to them, be it festivals, concerts and the like.

The artists and the events are then saved in their respective tables with PostgreSQL.

The user is asked to provide an artist name, in order to get the events and an image, if there is one.
The image is saved into the project folder.

The program outputs a csv file with the event count for each artist, as well as a graphical representation,
split into two png files.

---SETUP---

Create a PostgreSQL database.

In the db_config.py file, the user can change the credentials for their server.

In order to run this program, start Docker Desktop first.

Then open the IDE of your choice. (PyCharm Professional was used for development)

Add a Docker Interpreter and select the Dockerfile from this project.

DISCLAIMER: According to stackoverflow it is possible to use the Conda Environment,
but it requires you to activate Conda within the Docker Container.
Use a preinstalled version of Python instead.

Link on how to use Conda in Docker: https://stackoverflow.com/questions/52049202/how-to-use-docker-and-conda-in-pycharm

In the IDE terminal, go to the project folder and run these commands
(replace <imagename> with a name of your choice):

docker build -t <imagename> .
docker run -it --rm -v "${PWD}:/app" <imagename>

When the program terminates without error, the csv and png files will be overwritten.

The database tables are accessible via pgAdmin for example.