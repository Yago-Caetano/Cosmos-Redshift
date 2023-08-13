from flask import Blueprint
from controllers.web_controller import WebController

common_blueprint = Blueprint('common_blueprint', __name__)


@common_blueprint.route('/version', methods=['GET'])
def get_version():
    return WebController().get_version()

@common_blueprint.route('/last_dataset_sync', methods=['GET'])
def get_last_dataset_sync():
    return WebController().get_last_dataset_sync()

