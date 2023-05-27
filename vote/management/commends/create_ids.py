from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from vote.models import Profile

User = get_user_model()


class Command(BaseCommand):
    help = 'Create ID numbers in the database for matching'

    def handle(self, *args, **options):
        # Define the range and pattern for the IDs
        start_id = 1000
        end_id = 2000
        id_prefix = 'ID'

        # Get the total number of expected voters (e.g., from a database query)
        total_voters = 5000  # Replace with your actual logic to get the total number

        # Get the total number of registered voters (e.g., from a database query)
        registered_voters = Profile.objects.count()  # Replace with your actual logic to count the registered voters

        while True:
            # Prompt the user to enter a number within the range
            user_input = input(f"Enter a number between {start_id} and {end_id}: ")

            try:
                user_input = int(user_input)

                if start_id <= user_input <= end_id:
                    # Construct the ID by combining the prefix, the number, and '081'
                    user_id = f'{id_prefix}{user_input}081'

                    # Perform the registration using the user ID
                    # ...

                    break  # Exit the loop if the registration is successful
                else:
                    print("Invalid input. Please enter a number within the specified range.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")

        self.stdout.write(self.style.SUCCESS('IDs created successfully'))
        self.stdout.write(f'Total Number of Expected Voters: {total_voters}')
        self.stdout.write(f'Total Number of Registered Voters: {registered_voters}')
