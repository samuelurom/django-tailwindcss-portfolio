echo " BUILD START"
pipenv install
python manage.py collectstatic
echo " BUILD END"