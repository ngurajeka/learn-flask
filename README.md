# Learn Flask, a Python MicroFramework

## How to start
- Clone this repo (or fork)
- Create virtual environment and install Flask
```bash
virtualenv env
source env/bin/activate
pip install Flask
```
- Open Python prompt shell inside repo directory and then execute:
```python
from app import db
db.create_all()
```
- Start the built-in web server
```bash
python app.py
```
- Open the web browser and go to http://0.0.0.0:9001 or http://localhost:9001
- Open http://flask.pocoo.org/docs to see the full documentation

## Happy Hacking
