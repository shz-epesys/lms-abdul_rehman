from flask import Blueprint

from controllers.ClassController import create_announcements, create_class, delete_announcements, get_announcements, get_classes, get_files, get_student, get_students, get_teacher, store_files, update_announcements, upload_files
class_bp = Blueprint('class_bp', __name__)

class_bp.route('', methods=['POST'])(create_class)
class_bp.route('', methods=['GET'])(get_classes)
class_bp.route('/<class_id>/students', methods=['GET'])(get_students)
class_bp.route('/<class_id>/students/<st_id>', methods=['GET'])(get_student)
class_bp.route('/<class_id>/announcements', methods=['GET'])(get_announcements)
class_bp.route('/<class_id>/announcements', methods=['POST'])(create_announcements)
class_bp.route('/<class_id>/announcements/<a_id>', methods=['PUT'])(update_announcements)
class_bp.route('/<class_id>/announcements/<a_id>', methods=['DELETE'])(delete_announcements)
class_bp.route('/<class_id>/files', methods=['GET'])(get_files)
class_bp.route('/<class_id>/files', methods=['POST'])(store_files)
class_bp.route('/<class_id>/files/upload', methods=['POST'])(upload_files)

class_bp.route('/<class_id>/teacher', methods=['GET'])(get_teacher)
