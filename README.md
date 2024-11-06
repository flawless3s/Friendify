# Friendify

Friendify is a social networking platform designed to help users connect with friends, share posts, and find new friends through recommendations. The platform is built using Flask for the backend, Bootstrap for styling, and JSON for lightweight data persistence. Friendify aims to provide a streamlined experience for social networking in a collaborative environment.

# Table of Contents

-Features

-Installation

-Usage

-Project Structure

-API Endpoints

-Data Structure

-Future Improvements

-Contributing

# Features

User Authentication: Secure registration and login with session management.

Friend Connections: Add friends, view friend requests, and accept or decline requests.

Post Sharing: Users can create posts with captions and share them with friends.

Friend Recommendations: Friend suggestions based on mutual connections.

Profile Dropdown: Easy navigation through profile settings and logout options.

Installation
To set up and run the Friendify project locally:

 ## Clone the Repository:

bash
```
git clone https://github.com/flawless3s/Friendify.git
cd friendify
```
## Set Up a Virtual Environment:

bash

```
python3 -m venv .venv
source .venv/bin/activate   # On Windows, use .venv\Scripts\activate
```
## Run the Application:

bash
```
flask run
```

# Usage

Register: Sign up by providing a username, email, and password.

Login: Log in to access your profile, view posts, and connect with friends.

Post Sharing: Create a new post from your profile, add captions, and view posts from friends.

Manage Connections: Send, receive, and accept friend requests; see friend recommendations based on mutual connections.

# Project Structure
```
Friendify/
├── app/
│   ├── static/                # Static files (CSS, JS, images)
│   ├── templates/             # HTML templates
│   ├── __init__.py            # Initialize Flask app
│   ├── routes.py              # Define all routes
│   ├── models.py              # User and Social Network classes
│   └── utils.py               # Utility functions for JSON read/write
├── data/
│   └── users.json             # JSON file for storing user data
├── .venv/                     # Virtual environment (not included in repo)
├── README.md                  # Project documentation
├── requirements.txt           # Dependencies
└── run.py                     # Main file to start the Flask server
```

**The data for the project is stored in a JSON file (data/users.json).**

## Future Improvements

Enhanced Search: Implement search functionality to find users by username or email.

Comments and Likes: Allow users to like and comment on friends’ posts.

User Analytics: Display activity insights and engagement metrics.

Database Integration: Move from JSON to a more scalable database like SQLite or MongoDB.

# Contributing

Contributions are welcome! Please fork the repository and make a pull request with your improvements.

