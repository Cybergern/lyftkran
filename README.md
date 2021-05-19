# lyftkran

The idea here is to create a more modern version of the swedish powerlifting database. Definitely work in progress.

Install Docker and start with: 

`docker compose up`

`docker compose run web python3 manage.py migrate`

To get some test data, run:

`docker compose run web python3 manage.py generate_test_data`

To remove that same test data, run:

`docker compose run web python3 manage.py clear_test_data`

If you make changes to models, run:

`docker compose run web python3 manage.py makemigrations`

`docker compose run web python3 manage.py migrate`

To view a list of lifters, go to http://localhost:8000/lifter/lifters/

To view a list of clubs, go to http://localhost:8000/lifter/clubs/