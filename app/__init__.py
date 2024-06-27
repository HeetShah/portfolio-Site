import os
from flask import Flask, render_template, request
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html', title="Heet Shah", url=os.getenv("URL"))

@app.route('/about')
def about():
    education = [
        {
            "school": "University of Waterloo",
            "program": "Software Engineering",
            "link": "https://uwaterloo.ca/future-students/programs/software-engineering",
            "school_link": "https://uwaterloo.ca/",
        }
    ]

    work_experience = [
        {"company": "Okta", "link": "https://www.okta.com/"},
        {"company": "theScore Bet", "link": "https://www.thescore.bet/"},
        {"company": "Dandelion", "link": "https://dandelionnet.io/"},
        {"company": "Postalgia", "link": "https://postalgia.ink/"}
    ]

    places_traveled = ["Banff, Canada", "Vancouver, Canada", "Toronto, Canada", "Victoria, Canada", "Whistler, Canada", "Vadodara, India", "San Francisco, USA", "Miami, USA", "Las Vegas, USA", "Washington, USA", "Philadelphia, USA", "New York, USA", "Cancun, Mexico"]

    return render_template('about.html', education=education, work_experience=work_experience, places_traveled=places_traveled)

@app.route('/hobbies')
def hobbies():
    hobbies_info = {
        "hobbies": [
            {
                "title": "Writing📓",
                "description": "Been using <a href='https://obsidian.md/' target='_blank'>Obsidian</a> to Cmd + F my brain for a few years and it's a great tool to throw ideas, notes, and thoughts into."
            },
            {
                "title": "Basketball🏀",
                "description": "Got the automatic jumper, pick pocket, and dimmer badge. Goat? MJ."
            },
            {
                "title": "Gaming 🎮",
                "games": [
                    "Warzone - Either dropping 20 bombs or getting dropped.",
                    "FIFA - I know how to use R stick.",
                    "League of Legends - Yasuo main, 0/10 powerspike.",
                    "Valorant - Don't play this game, but I'm a Radiant.",
                    "Minecraft - They made survival mode too realistic these days.",
                    "Cup Pong - Absolute demon.",
                    "Chess - Probably grandmaster in my past life.",
                    "Among Us - I'm always sus.",
                    "Rocket League - Just play FIFA...",
                    "Fortnite - I'm a bot."
                ]
            },
            {
                "title": "Photography 📸",
                "description": "Natural tourist. I just use my phone and struggling to afford cloud storage. Please help, thanks."
            },
            {
                "title": "Reading 📚",
                "books": [
                    "Operating Systems: Internals and Design Principles, Global Edition 9th Edition by William Stallings (forced to read this for SE 350 at UW)",
                    "Instagram captions, comments, and DMs",
                    "Messages from my mom",
                    "Random WhatsApp forwards",
                    "Occasional Reddit threads",
                    "Whatever's on my Twitter feed",
                    "ChatGPT generated text"
                ]
            },
            {
                "title": "Music🎧",
                "description": "Top 5 artists:",
                "artists": [
                    "Drake",
                    "Arjit Singh"
                ],
                "playlists": [
                    {"name": "Heat", "link": "https://open.spotify.com/playlist/6U52lhARjejllDrBr34hwN?si=fad1d3f02b164aa2"},
                    {"name": "Bollywood", "link": "https://open.spotify.com/playlist/1ugpVqVkQRQHhcYdn8Efqy?si=a88e26bba1a54501"},
                    {"name": "Welcome to the league", "link": "https://open.spotify.com/playlist/0ceu3j3bZSKm9URaWejJPI?si=18ce33e268b24456"},
                    {"name": "Old Drake", "link": "https://open.spotify.com/playlist/48vfu48BKnFyMPFsG6sPsh?si=0e96491cb3d74c42"}
                ]
            }
        ]
    }
    return render_template('hobbies.html', title="My Hobbies", hobbies_info=hobbies_info)
