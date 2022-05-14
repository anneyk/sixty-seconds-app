# sixty-seconds-app
This is a flask application that allows users to post one minute pitches and also allows other users who have signed up to comment and upvote or downvote a pitch. It also allows a person to signup to be able to access the functionalities of the application
# Author
Annet Khavere
# User Story
- Comment on the different pitches posted py other users.
- See the pitches posted by other users.
- Vote on pitches they have viwed by giving it a upvote or a downvote.
- Register to be allowed to log in to the application
- View pitches from the different categories.
- Submit a pitch to a specific category of their choice.
# Development Installation
To get the code..

1. Cloning the repository:
https://github.com/anneyk/sixty-seconds-app.git
2. Move to the folder and install requirements
cd sixty-seconds-app
pip install -r requirements.txt
3. Running the application
python3 run.py runserver
4. Open the application on your browser 127.0.0.1:5000.
# Technology Used
- Python3.6
- Heroku
- Flask
- HTML
- CSS
- Bootstrap
- Postgres Database
# BDD
The program lets a user register
- Example input: Submit registration form
- Example output: User receives a welcome email

The program lets the user login
- Example input: Submit login form
- Example output: displays user name on right of navbar

The program lets a user publish a pitch
- Example input: Create a pitch
- Example output: Redirects user to form to create a pitch

# Live Site
https://sixty-seconds-pitch-app.herokuapp.com/
# License
MIT License:
Copyright (c) 2022 <a href='https://github.com/anneyk'>Anneyk</a>
