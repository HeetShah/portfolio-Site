import os
import re
from flask import Flask, render_template, request, Markup
from dotenv import load_dotenv
import folium
from peewee import *
import datetime
from playhouse.shortcuts import model_to_dict
from flask_cors import CORS

load_dotenv()
app = Flask(__name__)
CORS(app)

if os.getenv('TESTING') == 'true':
    print("Running in test mode")
    mydb = SqliteDatabase('file:memory?mode=memory&cache=shared', uri=True)
else:
    mydb = MySQLDatabase(os.getenv("MYSQL_DATABASE"), user=os.getenv("MYSQL_USER"), password=os.getenv("MYSQL_PASSWORD"), host=os.getenv("MYSQL_HOST"), port=3306)
    
class TimelinePost(Model):
    name = CharField()
    email = CharField()
    content = TextField()
    created_at = DateTimeField(default=datetime.datetime.now)
    
    class Meta:
        database = mydb
        

mydb.connect()
mydb.create_tables([TimelinePost])
 
 
@app.route('/api/timeline_post', methods=['POST'])
def post_time_line_post():
    if 'name' not in request.form or not request.form['name']:
        return "Invalid name", 400
    if ('email' not in request.form or 
        not re.search(r"[A-Za-z0-9\._%+\-]+@[A-Za-z0-9\.\-]+\.[A-Za-z]{2,}", request.form['email'])):
        return "Invalid email", 400
    if 'content' not in request.form or not request.form['content']:
        return "Invalid content", 400
    name = request.form['name']
    email = request.form['email']
    content = request.form['content']
    timeline_post = TimelinePost.create(name=name, email=email, content=content)
    return model_to_dict(timeline_post)

@app.route('/api/timeline_post', methods=['GET'])
def get_time_line_post():
    return {
        "timeline_posts": [
            model_to_dict(p) for p in TimelinePost.select().order_by(TimelinePost.created_at.desc())
        ]
    }

@app.route('/api/timeline_post/<int:id>', methods=['DELETE'])
def delete_timeline_post(id):
    try:
        post = TimelinePost.get(TimelinePost.id == id)
        post.delete_instance()
        return {"success": "Post deleted"}, 200
    except TimelinePost.DoesNotExist:
        return {"error": "Post not found"}, 404


@app.route('/')
def index():
    return render_template('index.html', title="Heet Shah", url=os.getenv("URL"))

@app.route('/about')
def about():
    
     # Start with creating a basic map
    folium_map = folium.Map(location=[20, 0], tiles="OpenStreetMap", zoom_start=2)

    # Define your locations
    locations = {
        "Banff, Canada": (51.1784, -115.5708),
        "Vancouver, Canada": (49.2827, -123.1207),
        "Toronto, Canada": (43.65107, -79.347015),
        "Victoria, Canada": (48.4284, -123.3656),
        "Whistler, Canada": (50.1163, -122.9574),
        "Vadodara, India": (22.3072, 73.1812),
        "San Francisco, USA": (37.7749, -122.4194),
        "Miami, USA": (25.7617, -80.1918),
        "Las Vegas, USA": (36.1699, -115.1398),
        "Washington, USA": (38.9072, -77.0369),
        "Philadelphia, USA": (39.9526, -75.1652),
        "New York, USA": (40.7128, -74.0060),
        "Cancun, Mexico": (21.1619, -86.8515)
        
    }

    # Add markers to the map
    for place, coords in locations.items():
        folium.Marker(location=coords, popup=place).add_to(folium_map)
        
    map_html = folium_map._repr_html_()
    
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


    return render_template('about.html', education=education, work_experience=work_experience, map_html=Markup(map_html))


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
                    "Fortnite - I'm a bot.",
                    "GTA V - Can we just get GTA VI already?"
                ]
            },
            {
                "title": "Photography 📸",
                "description": "Natural tourist. I just use my phone and struggling to afford cloud storage. Please help, thanks :)"
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

@app.route('/timeline')
def timeline():
    return render_template('timeline.html', title="Timeline")
