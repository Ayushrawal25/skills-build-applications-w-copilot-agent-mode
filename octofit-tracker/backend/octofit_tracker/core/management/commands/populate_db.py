from django.core.management.base import BaseCommand
from pymongo import MongoClient

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        # Connect to MongoDB directly for index creation
        client = MongoClient('mongodb://localhost:27017')
        db = client['octofit_db']
        db.users.drop()
        db.teams.drop()
        db.activities.drop()
        db.leaderboard.drop()
        db.workouts.drop()
        db.users.create_index([("email", 1)], unique=True)

        # Sample data
        users = [
            {"name": "Superman", "email": "superman@dc.com", "team": "dc"},
            {"name": "Batman", "email": "batman@dc.com", "team": "dc"},
            {"name": "Wonder Woman", "email": "wonderwoman@dc.com", "team": "dc"},
            {"name": "Iron Man", "email": "ironman@marvel.com", "team": "marvel"},
            {"name": "Captain America", "email": "cap@marvel.com", "team": "marvel"},
            {"name": "Black Widow", "email": "widow@marvel.com", "team": "marvel"},
        ]
        teams = [
            {"name": "marvel", "members": ["ironman@marvel.com", "cap@marvel.com", "widow@marvel.com"]},
            {"name": "dc", "members": ["superman@dc.com", "batman@dc.com", "wonderwoman@dc.com"]},
        ]
        activities = [
            {"user": "superman@dc.com", "activity": "flying", "duration": 60},
            {"user": "ironman@marvel.com", "activity": "flying", "duration": 45},
            {"user": "batman@dc.com", "activity": "training", "duration": 30},
            {"user": "cap@marvel.com", "activity": "running", "duration": 50},
        ]
        leaderboard = [
            {"team": "marvel", "points": 120},
            {"team": "dc", "points": 110},
        ]
        workouts = [
            {"name": "Hero HIIT", "suggested_for": "marvel"},
            {"name": "Justice Jog", "suggested_for": "dc"},
        ]
        db.users.insert_many(users)
        db.teams.insert_many(teams)
        db.activities.insert_many(activities)
        db.leaderboard.insert_many(leaderboard)
        db.workouts.insert_many(workouts)
        self.stdout.write(self.style.SUCCESS('octofit_db database populated with test data.'))
