

from django.core.management.base import BaseCommand
from django.conf import settings
from pymongo import MongoClient, ASCENDING
from django.contrib.auth import get_user_model
from django.apps import apps

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Connecting to MongoDB...'))
        client = MongoClient('localhost', 27017)
        db = client[settings.DATABASES['default']['NAME']]

        # Drop collections if they exist
        db.users.drop()
        db.teams.drop()
        db.activities.drop()
        db.leaderboard.drop()
        db.workouts.drop()

        # Create unique index on email for users
        db.users.create_index([('email', ASCENDING)], unique=True)

        # Teams
        teams = [
            {'name': 'Team Marvel'},
            {'name': 'Team DC'}
        ]
        team_ids = db.teams.insert_many(teams).inserted_ids

        # Users (superheroes)
        users = [
            {'name': 'Spider-Man', 'email': 'spiderman@marvel.com', 'team': 'Team Marvel'},
            {'name': 'Iron Man', 'email': 'ironman@marvel.com', 'team': 'Team Marvel'},
            {'name': 'Wonder Woman', 'email': 'wonderwoman@dc.com', 'team': 'Team DC'},
            {'name': 'Batman', 'email': 'batman@dc.com', 'team': 'Team DC'},
        ]
        db.users.insert_many(users)

        # Activities
        activities = [
            {'user': 'spiderman@marvel.com', 'activity': 'Running', 'duration': 30},
            {'user': 'ironman@marvel.com', 'activity': 'Cycling', 'duration': 45},
            {'user': 'wonderwoman@dc.com', 'activity': 'Swimming', 'duration': 60},
            {'user': 'batman@dc.com', 'activity': 'Yoga', 'duration': 40},
        ]
        db.activities.insert_many(activities)

        # Leaderboard
        leaderboard = [
            {'team': 'Team Marvel', 'points': 150},
            {'team': 'Team DC', 'points': 130},
        ]
        db.leaderboard.insert_many(leaderboard)

        # Workouts
        workouts = [
            {'user': 'spiderman@marvel.com', 'workout': 'Push-ups', 'reps': 50},
            {'user': 'ironman@marvel.com', 'workout': 'Sit-ups', 'reps': 40},
            {'user': 'wonderwoman@dc.com', 'workout': 'Squats', 'reps': 60},
            {'user': 'batman@dc.com', 'workout': 'Plank', 'duration': 5},
        ]
        db.workouts.insert_many(workouts)

        self.stdout.write(self.style.SUCCESS('octofit_db database populated with test data!'))
