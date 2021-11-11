from flask import Blueprint

from controllers.StudentController import get_classes, get_class
student_bp = Blueprint('student_bp', __name__)

student_bp.route('/classes', methods=['GET'])(get_classes)
student_bp.route('/classes/<class_id>', methods=['GET'])(get_class)

