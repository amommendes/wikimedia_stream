#Start Flask
echo $(date) [INFO] Starting Flask
cd /app
export FLASK_APP=dashboard
export FLASK_ENV=development
nohup gunicorn -w 1 -b 0.0.0.0:5000 "dashboard:create_app()" --access-logfile guinicorn_access.log --error-logfile guinicorn_error.log &


rc=$?

if [ "${rc}" -eq "0" ]; then
    echo $(date) [INFO] Flask Started
else
    echo $(date) [Error] Error while starting flask
    exit 1
fi

echo $(date) [INFO] Starting WikimediaStreams App

python3.6 wikimedia_app.py --mode=persist 