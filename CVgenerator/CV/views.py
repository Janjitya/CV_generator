from django.shortcuts import render
from .models import Profile
import pdfkit
from django.http import HttpResponse
from django.template import loader
import io
# Create your views here.

def accept_user_date(request):

    if request.method == "POST":

        name = request.POST.get("name","")
        email = request.POST.get("email","")
        phone = request.POST.get("phone","")
        summary = request.POST.get("summary","")
        degree = request.POST.get("degree","")
        school = request.POST.get("school","")
        university = request.POST.get("university","")
        previous_work = request.POST.get("previouswork","")
        skills = request.POST.get("skills","")

        profile_obj = Profile(name=name, email=email, phone=phone, summary=summary, degree=degree, school=school, university=university, previous_work=previous_work, skills=skills)
        profile_obj.save()

    return render(request, "CV/profile-form.html")

def resume(request, id):
    # path_wkthmltopdf = 'C:\wkhtmltopdf\\bin\wkhtmltopdf.exe'
    # config = pdfkit.configuration(wkhtmltopdf=path_wkthmltopdf)
    user_profile = Profile.objects.get(id=id)
    template = loader.get_template("CV/resume.html")
    
    html = template.render({"profile":user_profile})
    options = {
        'page-size':'Letter',
        'encoding':'UTF-8',
    }
    pdf = pdfkit.from_string(html,False,options)
    response = HttpResponse(pdf,content_type='application/pdf')
    response['Content-Disposition']='attachment'
    filename = "resume.pdf"

    return response

def resume_list(request):
    profiles = Profile.objects.all()
    context = {'profiles':profiles}
    return render(request, "CV/list.html",context=context)
