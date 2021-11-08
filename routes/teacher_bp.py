from flask import Blueprint

from controllers.TeacherController import get_classes, get_class, is_teacher
teacher_bp = Blueprint('teacher_bp', __name__)

teacher_bp.route('/classes', methods=['GET'])(is_teacher)
# teacher_bp.route('/classes', methods=['GET'])(get_classes)
teacher_bp.route('/classes/<class_id>', methods=['GET'])(get_class)

