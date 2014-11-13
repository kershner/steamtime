from flask import Flask

app = Flask(__name__)  # Creating Flask Object
app.config.from_object('steamtime_config')

from steamtime import routes