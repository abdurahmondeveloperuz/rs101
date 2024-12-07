import json
import os
import base64
from decimal import Decimal
from django.conf import settings

class JSONStorage:
    def __init__(self):
        self.data_dir = os.path.join(settings.BASE_DIR, 'data')
        self.classes_file = os.path.join(self.data_dir, 'classes.json')
        self.students_file = os.path.join(self.data_dir, 'students.json')
        self._ensure_data_files()

    def _ensure_data_files(self):
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
        
        for file_path in [self.classes_file, self.students_file]:
            if not os.path.exists(file_path):
                with open(file_path, 'w') as f:
                    json.dump([], f)

    def _load_data(self, file_path):
        with open(file_path, 'r') as f:
            return json.load(f)

    def _save_data(self, file_path, data):
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)

    def get_class(self, class_id):
        classes = self._load_data(self.classes_file)
        return next((c for c in classes if c['class_id'] == class_id), None)

    def get_students(self, class_id):
        students = self._load_data(self.students_file)
        return [s for s in students if s['class_id'] == class_id]

    def create_or_update_class(self, class_id, class_name, students_data):
        # Update class
        classes = self._load_data(self.classes_file)
        class_data = {'class_id': class_id, 'name': class_name}
        
        existing_class = next((i for i, c in enumerate(classes) if c['class_id'] == class_id), None)
        if existing_class is not None:
            classes[existing_class] = class_data
        else:
            classes.append(class_data)
        
        self._save_data(self.classes_file, classes)

        # Update students
        all_students = self._load_data(self.students_file)
        all_students = [s for s in all_students if s['class_id'] != class_id]  # Remove existing students
        
        new_students = []
        for student in students_data:
            new_student = {
                'class_id': class_id,
                'first_name': student['first_name'],
                'last_name': student['last_name'],
                'score': float(student['score']),
                'image': student.get('image', ''),
                'profile_url': student.get('profile_url', '#')  # Add profile URL field
            }
            new_students.append(new_student)
        
        all_students.extend(new_students)
        self._save_data(self.students_file, all_students)

        return len(new_students)