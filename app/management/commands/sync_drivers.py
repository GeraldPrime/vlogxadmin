from django.core.management.base import BaseCommand
from app.models import Driver

class Command(BaseCommand):
    help = 'Sync only drivers between Django and Firebase'

    def add_arguments(self, parser):
        parser.add_argument(
            '--from-firebase', 
            action='store_true',
            help='Sync drivers from Firebase to Django'
        )
        parser.add_argument(
            '--to-firebase', 
            action='store_true',
            help='Sync drivers from Django to Firebase'
        )

    def handle(self, *args, **options):
        if options['from_firebase']:
            Driver.sync_from_firebase()
            self.stdout.write(
                self.style.SUCCESS('Successfully synced drivers from Firebase')
            )
        
        if options['to_firebase']:
            drivers = Driver.objects.all()
            for driver in drivers:
                driver.save_to_firebase()
            self.stdout.write(
                self.style.SUCCESS(f'Successfully synced {drivers.count()} drivers to Firebase')
            )
        
        if not options['from_firebase'] and not options['to_firebase']:
            self.stdout.write(
                self.style.ERROR('Please specify --from-firebase or --to-firebase')
            )