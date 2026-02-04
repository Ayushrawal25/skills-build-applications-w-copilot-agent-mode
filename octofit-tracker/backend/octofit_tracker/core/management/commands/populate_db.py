
from django.core.management.base import BaseCommand
from octofit_tracker.core.models import User, Team, Activity, Leaderboard, Workout
from django.db import transaction

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        with transaction.atomic():
            User.objects.all().delete()
            Team.objects.all().delete()
            Activity.objects.all().delete()
            Leaderboard.objects.all().delete()
            Workout.objects.all().delete()

            users = [
                User(name="Superman", email="superman@dc.com", team="dc"),
                User(name="Batman", email="batman@dc.com", team="dc"),
                User(name="Wonder Woman", email="wonderwoman@dc.com", team="dc"),
                User(name="Iron Man", email="ironman@marvel.com", team="marvel"),
                User(name="Captain America", email="cap@marvel.com", team="marvel"),
                User(name="Black Widow", email="widow@marvel.com", team="marvel"),
            ]
            User.objects.bulk_create(users)

            teams = [
                Team(name="marvel", members=["ironman@marvel.com", "cap@marvel.com", "widow@marvel.com"]),
                Team(name="dc", members=["superman@dc.com", "batman@dc.com", "wonderwoman@dc.com"]),
            ]
            Team.objects.bulk_create(teams)

            activities = [
                Activity(user="superman@dc.com", activity="flying", duration=60),
                Activity(user="ironman@marvel.com", activity="flying", duration=45),
                Activity(user="batman@dc.com", activity="training", duration=30),
                Activity(user="cap@marvel.com", activity="running", duration=50),
            ]
            Activity.objects.bulk_create(activities)

            leaderboard = [
                Leaderboard(team="marvel", points=120),
                Leaderboard(team="dc", points=110),
            ]
            Leaderboard.objects.bulk_create(leaderboard)

            workouts = [
                Workout(name="Hero HIIT", suggested_for="marvel"),
                Workout(name="Justice Jog", suggested_for="dc"),
            ]
            Workout.objects.bulk_create(workouts)

        self.stdout.write(self.style.SUCCESS('octofit_db database populated with test data using Django ORM.'))
