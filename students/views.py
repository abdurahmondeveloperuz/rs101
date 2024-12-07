from django.shortcuts import render
from django.db.models import Avg
from .storage import JSONStorage
from statistics import mean

def rankings(request):
    class_id = request.GET.get('class_id')
    if not class_id:
        return render(request, 'rankings.html', {'error': 'Class ID is required'})

    storage = JSONStorage()
    class_data = storage.get_class(class_id)
    
    if not class_data:
        return render(request, 'rankings.html', {'error': 'Class not found'})

    students = storage.get_students(class_id)
    
    # Sort students by score in descending order
    students.sort(key=lambda x: x['score'], reverse=True)
    
    # Add rankings
    for idx, student in enumerate(students):
        student['rank'] = idx + 1

    # Calculate average score
    avg_score = mean([s['score'] for s in students]) if students else 0

    context = {
        'class_name': class_data['name'],
        'average_score': round(avg_score, 2),
        'students': students
    }
    
    return render(request, 'rankings.html', context)

def custom_404(request, exception):
    return render(request, '404.html', status=404)