find . -path "/travelpack/website/migrations/*.py" -not -name "__init__.py" -delete; #deletes all of the .py files in the migrations directory except for the __init__.py file.
find . -path "/travelpack/website/migrations/*.pyc"  -delete; #deletes all of the .pyc files in the migrations directory.
rm db.sqlite3; #deletes the database file.
rm -rf website/migrations; #deletes the migrations folder.
python manage.py migrate; #run the initial django migration to create all the initial tables. need this step because we are killing the database just above
python manage.py makemigrations website; #creates the migration.
python manage.py migrate website; #runs the migration.  This will delete all of the data in your database.
python manage.py loaddata user.json triptype.json trip.json review.json  #loads the data from each .json file in sequential order.