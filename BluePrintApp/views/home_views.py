from flask import Blueprint
from infrastructure.view_modifiers import response

blueprint = Blueprint('home', __name__, template_folder='templates')


@blueprint.route('/')
@response(template_file='home/index.html')
def index():
    return{}

