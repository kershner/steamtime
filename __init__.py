from flask import Flask

app = Flask(__name__)  # Creating Flask Object
app.config.from_object('steamtime_config')

# This line is necessary for my local server to run
from steamtime import routes