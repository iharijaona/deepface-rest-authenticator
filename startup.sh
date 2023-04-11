# Run the Flask/GraphQL API server
python3 -m gunicorn -c ./gunicorn.config.py wsgi:app

#FLASK_APP=wsgi.py flask run --host=0.0.0.0  --port 8888 --reload --debugger
