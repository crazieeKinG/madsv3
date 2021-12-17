from flask import Flask 

mads_app = Flask(__name__)
mads_app.secret_key = b'j193j[.-12l=!727'

from mads import views