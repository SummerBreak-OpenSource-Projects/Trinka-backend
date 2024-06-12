from django.http import JsonResponse
from django.conf import settings
from .models import UploadedFile
from .serializers import UploadedFileSerializer

import PyPDF2
import docx  # Correctly import the python-docx module

ALLOWED_FILE_TYPES = ['pdf', 'docx']

def file_upload(request):
    if request.method == 'POST' and request.FILES.get('file'):
        uploaded_file = request.FILES['file']
        file_extension = uploaded_file.name.split('.')[-1].lower()
        
        if file_extension not in ALLOWED_FILE_TYPES:
            return JsonResponse({'error': 'Unsupported file type'}, status=400)
        
        # Store the uploaded file
        uploaded_file_obj = UploadedFile.objects.create(file=uploaded_file)
        
        # Extract text content from the file
        text_content = ""
        try:
            if file_extension == 'pdf':
                pdf_reader = PyPDF2.PdfReader(uploaded_file_obj.file)
                for page_num in range(len(pdf_reader.pages)):
                    text_content += pdf_reader.pages[page_num].extract_text()
            elif file_extension == 'docx':
                docx_doc = docx.Document(uploaded_file_obj.file)
                for paragraph in docx_doc.paragraphs:
                    text_content += paragraph.text
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
        
        # Update the UploadedFile object with text content
        uploaded_file_obj.text_content = text_content
        uploaded_file_obj.save()
        print(text_content)
        return JsonResponse({'status': 'File uploaded and text content extracted successfully'})
    else:
        return JsonResponse({'error': 'No file found in the request'}, status=400)

def latest_file_detail(request):
    try:
        uploaded_file = UploadedFile.objects.latest('id')
    except UploadedFile.DoesNotExist:
        return JsonResponse({'error': 'No files found'}, status=404)
    
    text_content = uploaded_file.text_content
    word_count = len(text_content.split())
    
    return JsonResponse({
        'text_content': text_content,
        'word_count': word_count
    })
