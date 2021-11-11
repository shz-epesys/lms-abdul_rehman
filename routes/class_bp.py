from flask import Blueprint

from controllers.ClassController import create_class, get_classes, get_students
class_bp = Blueprint('class_bp', __name__)

class_bp.route('', methods=['POST'])(create_class)
class_bp.route('', methods=['GET'])(get_classes)
class_bp.route('/<class_id>/students', methods=['GET'])(get_students)
