from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.http import HttpResponse
from .models import*
from .ml_model import get_predictions
import os
from django.conf import settings
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.contrib import messages

# Create your views here.

def index(request): 
    return render(request , 'index.html', context={'pagetitle' : 'Exam Paper Predictor'})

def about(request): 
    return render(request , 'about.html', context={'pagetitle' : 'About website'})

def browse(request):
    return render(request , 'browse.html', context={'pagetitle' : 'Browse Materials - Exam Paper Predictor'})

# def upload(request):
#     return render(request , 'upload.html', context={'pagetitle' : 'Upload Material - Exam Paper Predictor'})

def result(request):
    subject_id = request.GET.get('subject')
    print("GET DATA:", request.GET)
    subject = Subject.objects.get(id=subject_id)

    csv_path = os.path.join(settings.BASE_DIR, 'myapp', 'datasets', subject.csv_filename)
    print("path:", csv_path)
    print("SUBJECT:", subject.subject_name)
    print("CSV FILENAME:", subject.csv_filename)
    print("CSV PATH:", csv_path)

    predictions = get_predictions(csv_path)

    return render(request , 'result.html', context={'pagetitle' : 'Predicted Paper - Exam Paper Predictor',"predictions": predictions,  "subject": subject.subject_name,   # shown on top
        "semester": subject.semester })


def get_subjects(request):
    sem = request.GET.get('semester')
    subjects = Subject.objects.filter(semester=sem).values('id', 'subject_name')
    return JsonResponse(list(subjects), safe=False)

def download_pdf(request):
    subject_id = request.GET.get("subject")
    semester = request.GET.get("semester")
    college = request.GET.get("college")

    # Fetch the subject object
    subject = Subject.objects.get(id=subject_id)

    # Build correct CSV path
    csv_path = os.path.join(settings.BASE_DIR, "myapp", "datasets", subject.csv_filename)

    # Generate predictions again
    predictions = get_predictions(csv_path)

    # Render template
    template = get_template("pdfresult.html")
    html = template.render({
        "predictions": predictions,
        "subject": subject.subject_name,
        "semester": semester,
        "college": college,
    })

    # Create response
    response = HttpResponse(content_type="application/pdf")
    response['Content-Disposition'] = 'attachment; filename="Predicted_Paper.pdf"'

    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse("PDF generation failed")

    return response

def upload_material(request):
    if request.method == "POST":
        if 'paper' in request.FILES:
            UploadedPaper.objects.create(
            paper=request.FILES['paper']
            )

            messages.success(request, "✅ File uploaded successfully!")
            return redirect('upload')

    return render(request, 'upload.html')
