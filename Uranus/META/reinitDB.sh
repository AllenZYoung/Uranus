URANUS="`pwd`/.."
PY3="/usr/bin/env python3"

echo "[Step:0] Shell: Switching pwd to $URANUS"
cd $URANUS
echo "DONE!"

echo "[Step:1] MySQL: DROP DATABASE"
mysql -uuranus -puranus -e "DROP DATABASE uranus;"
echo "DONE!"

echo "[Step:2] MySQL: RE-CREATE DATABASE"
mysql -uuranus -puranus -e "CREATE DATABASE IF NOT EXISTS uranus CHARSET utf8mb4;"
echo "DONE!"

echo "[Step:3] Shell: rm -r /app/migrations"
rm -r $URANUS/app/migrations
echo "DONE!"

echo "[Step:4] Django: makemigrations app"
$PY3 ./manage.py makemigrations app
echo "DONE!"

echo "[Step:5] Django: migrate"
$PY3 ./manage.py migrate
echo "DONE!"
