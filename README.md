# PlayTime

PlayTime is a tool to help fitness instructors create the perfect playlist for every class.  Using OAuth2 protocols, a user can log in via their Spotify account to connect their playlists. They then create custom categories, profiles for different types of songs which allow a user to specify a range for duration, tempo, energy level, and/or other qualitative criteria. Categories can be applied to existing playlists, which can then be edited directly in the app. If a user needs some inspiration, they can request recommendations based on their custom category, and PlayTime will use the specifications provided by the user, the songs they already like, and Spotify's API to provide a list of new songs that perfectly match their needs.

## Table of Contents

* [Tech Stack](#tech-stack)
* [Features](#features)
* [Setup/Installation](#installation)
* [Version 2.0](#future)

## <a name="tech-stack"></a>Tech Stack

__Frontend:__ HTML5, CSS3, Bootstrap, Javascript, jQuery, jQueryUI, React
__Backend:__ Python, Flask, PostgreSQL, SQLAlchemy
__API:__ Spotify

## <a name="features"></a>Features

View and edit a playlist, including additional audio features like tempo and energy level.

![Edit playlist](/static/images/_readme/playlist.gif)
</br>

Create custom categories based on song criteria.

![Create category](/static/images/_readme/create_category.png)
</br>

Get recommended songs that conform to your category criteria, based on songs already in your playlists.

![Get recommendations](/static/images/_readme/recommendations.png)
</br>

## <a name="installation"></a>Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Requirements
* PostgreSQL
* Python 2.7
* Spotify API keys

### Installing

To run this app locally:

Clone repository:
```
$ git clone https://github.com/thevalerie/playtime.git
```
Create a virtual environment:
```
$ virtualenv env
```
Activate the virtual environment:
```
$ source env/bin/activate
```
Install dependencies:
```
$ pip install -r requirements.txt
```
Get your own API keys for [Spotify](https://developer.spotify.com/). Save them to a file `secrets.py`:
```
export SPOTIFY_CONSUMER_KEY="abc"
export SPOTIFY_CONSUMER_SECRET="xyz"
```
Source your secrets in your virtual environment:
```
$ source secrets.sh
```
Create database 'playtime'.
```
$ createdb playtime
```
Create your database tables data.
```
$ python model.py
```
Run the app from the command line.
```
$ python server.py
```

## <a name="future"></a>Version 2.0 Plans

 * update all pages to a React frontend
 * add in-app song play capabilities
 * allow user to select the seed data for category recommendations

## About the Author

PlayTime was created by **Valerie Moy**, a software engineer in San Francisco, CA.
</br>
More about Valerie:
</br>
https://www.linkedin.com/in/valeriemoy/
</br>
Say hi:
thevalerie@gmail.com
</br>
