# External library imports
from flask import Blueprint

bp = Blueprint('web', __name__)

from gameping.web import views
