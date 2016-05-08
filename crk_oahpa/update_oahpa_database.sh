# This script deletes the old sms_oahpa database, creates a new database and fills it with data.
echo "Dropping the old and creating a new database (saving logs)..."
python manage.py sqlclear crk_drill | grep -v '_log' | python manage.py dbshell
echo "Creating the database tables according to crk_drill/models.py..."
python manage.py syncdb
echo "Filling the database with new data..."
INSTALL_SRC=../crk/ sh parafedaba.sh
