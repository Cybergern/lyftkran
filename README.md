# Lyftkran

The idea here is to create a more modern version of the swedish powerlifting database. Definitely work in progress.

Install Docker and start with: 

`docker compose up`

`docker compose run web python3 manage.py migrate`

Also create a file in the root called secrets.json and put this in it:

`{
    "DJANGO_SECRET_KEY":"THIS_IS_A_VERY_SECRET_KEY_BUT_AUTOGENERATE_IT_INSTEAD",
    "DJANGO_DB_PASS":"lyftkran_pass"
}`

To get some example data, run:

`docker compose run web python3 manage.py generate_test_data`

To remove that same example data, run:

`docker compose run web python3 manage.py clear_test_data`

To run all the tests, run:

`docker compose run web pytest`

If you make changes to models, run:

`docker compose run web python3 manage.py makemigrations`

`docker compose run web python3 manage.py migrate`

To view a list of lifters, go to http://localhost:8000/lifter/lifters/

To view a list of clubs, go to http://localhost:8000/lifter/clubs/

This software is licensed under the MIT License.