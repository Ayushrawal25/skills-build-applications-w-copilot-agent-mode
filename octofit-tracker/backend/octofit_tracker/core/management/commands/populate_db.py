
from django.core.management.base import BaseCommand
from octofit_tracker.core.models import User, Team, Activity, Leaderboard, Workout
from django.db import transaction

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        with transaction.atomic():
            self.stdout.write(self.style.SUCCESS('Clearing old data...'))
            User.objects.all().delete()
            Team.objects.all().delete()
            Activity.objects.all().delete()
            Leaderboard.objects.all().delete()
            Workout.objects.all().delete()

            self.stdout.write(self.style.SUCCESS('Creating teams...'))
            marvel = Team.objects.create(name='Team Marvel', members=[])
            dc = Team.objects.create(name='Team DC', members=[])

            self.stdout.write(self.style.SUCCESS('Creating users...'))
            spiderman = User.objects.create(name='Spider-Man', email='spiderman@marvel.com', team=marvel.name)
            ironman = User.objects.create(name='Iron Man', email='ironman@marvel.com', team=marvel.name)
            wonderwoman = User.objects.create(name='Wonder Woman', email='wonderwoman@dc.com', team=dc.name)
            batman = User.objects.create(name='Batman', email='batman@dc.com', team=dc.name)

            marvel.members = [spiderman.email, ironman.email]
            dc.members = [wonderwoman.email, batman.email]
            marvel.save()
            dc.save()

            self.stdout.write(self.style.SUCCESS('Creating activities...'))
            Activity.objects.create(user=spiderman.email, activity='Running', duration=30)
            Activity.objects.create(user=ironman.email, activity='Cycling', duration=45)
            Activity.objects.create(user=wonderwoman.email, activity='Swimming', duration=60)
            Activity.objects.create(user=batman.email, activity='Yoga', duration=40)

            self.stdout.write(self.style.SUCCESS('Creating leaderboard...'))
            Leaderboard.objects.create(team=marvel.name, points=150)
            Leaderboard.objects.create(team=dc.name, points=130)

            self.stdout.write(self.style.SUCCESS('Creating workouts...'))
            Workout.objects.create(name='Push-ups', suggested_for=spiderman.team)
            Workout.objects.create(name='Sit-ups', suggested_for=ironman.team)
            Workout.objects.create(name='Squats', suggested_for=wonderwoman.team)
            Workout.objects.create(name='Plank', suggested_for=batman.team)

            self.stdout.write(self.style.SUCCESS('octofit_db database populated with test data!'))
