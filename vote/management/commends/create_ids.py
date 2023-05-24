from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from yourapp.models import Profile

User = get_user_model()


class Command(BaseCommand):
    help = 'Create ID numbers in the database for matching'


def handle(self, *args, **options):
    # Define the range and pattern for the IDs
    start_id = 1000
    end_id = 2000
    id_prefix = 'ID'

    while True:
        # Prompt the user to enter a number within the range
        user_input = input(f"Enter a number between {start_id} and {end_id}: ")

        try:
            user_input = int(user_input)

            if start_id <= user_input <= end_id:
                # Construct the ID by combining the prefix and the number
                user_id = f'{id_prefix}{user_input}'

                # Perform the registration using the user ID
                # ...

                break  # Exit the loop if the registration is successful
            else:
                print("Invalid input. Please enter a number within the specified range.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

            # Create a corresponding profile for each user
            profile = Profile.objects.create(user=user, district='Your District', county='Your County',
                                             national_id=user_id, citizenship=False, age=18,
                                             residency_proof='path/to/residency_proof')

        self.stdout.write(self.style.SUCCESS('IDs created successfully'))
