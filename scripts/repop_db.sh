cd ./backend
rm ./db.sqlite3
python manage.py migrate
python manage.py populate_db