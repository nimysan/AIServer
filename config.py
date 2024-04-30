from flask import render_template, Blueprint

config_bp = Blueprint('config', __name__, url_prefix='/config')


@config_bp.route('/index', methods=('GET', 'POST'))
def save_config():
    return render_template('config/config.html')
