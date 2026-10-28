cd ../
python manage.py dumpdata -e=contenttypes -e=auth -e=sessions -o test_db.json
cd bat
pause