from rest_framework.decorators import api_view
from rest_framework.response import Response
from ..storage import JSONStorage
from .serializers import ClassInputSerializer, StudentSerializer
from .auth import require_api_key

@api_view(['GET', 'POST'])
@require_api_key
def set_class(request):
    class_id = request.GET.get('class_id')
    if not class_id:
        return Response({'error': 'class_id is required'}, status=400)

    storage = JSONStorage()

    if request.method == 'GET':
        # Get class data
        class_data = storage.get_class(class_id)
        if not class_data:
            return Response({'error': 'Class not found'}, status=404)
        
        students = storage.get_students(class_id)
        # Sort students by score in descending order
        students.sort(key=lambda x: x['score'], reverse=True)
        
        # Add rankings
        for idx, student in enumerate(students):
            student['rank'] = idx + 1

        return Response({
            'class_id': class_id,
            'class_name': class_data['name'],
            'students': students
        })

    elif request.method == 'POST':
        serializer = ClassInputSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        try:
            student_count = storage.create_or_update_class(
                class_id=class_id,
                class_name=serializer.validated_data['class_name'],
                students_data=serializer.validated_data['students']
            )

            return Response({
                'status': 'success',
                'message': 'Data saved successfully',
                'class_id': class_id,
                'student_count': student_count
            })
        except Exception as e:
            return Response({'error': str(e)}, status=400)