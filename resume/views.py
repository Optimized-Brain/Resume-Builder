from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from xhtml2pdf import pisa  # Import xhtml2pdf's pisa module
from django.contrib.auth.models import User
from .models import Resume
from .forms import ResumeForm  # we’ll define this form next

def home(request):
    # Redirect to dashboard if logged in; otherwise, show home page
    if request.user.is_authenticated:
        return redirect('resume:dashboard')
    return render(request, 'resume/base.html')

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username').strip()
        email = request.POST.get('email').strip()
        password = request.POST.get('password')
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            messages.success(request, "Registration successful. Please log in.")
            return redirect('resume:login')
    return render(request, 'resume/register.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username').strip()
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('resume:dashboard')
        else:
            messages.error(request, "Invalid credentials. Please try again.")
    return render(request, 'resume/login.html')

@login_required
def dashboard(request):
    try:
        resume = Resume.objects.get(user=request.user)
    except Resume.DoesNotExist:
        resume = None
    return render(request, 'resume/dashboard.html', {'resume': resume})

@login_required
def create_resume(request):
    try:
        instance = Resume.objects.get(user=request.user)
    except Resume.DoesNotExist:
        instance = None
    if request.method == 'POST':
        form = ResumeForm(request.POST, instance=instance)
        if form.is_valid():
            resume = form.save(commit=False)
            resume.user = request.user
            resume.save()
            messages.success(request, "Resume saved successfully.")
            return redirect('resume:view_resume')
    else:
        form = ResumeForm(instance=instance)
    return render(request, 'resume/create_resume.html', {'form': form})

@login_required
def view_resume(request):
    try:
        resume = Resume.objects.get(user=request.user)
    except Resume.DoesNotExist:
        messages.error(request, "Please create your resume first.")
        return redirect('resume:create_resume')
    return render(request, 'resume/view_resume.html', {'resume': resume})

@login_required
def download_pdf(request):
    try:
        resume = Resume.objects.get(user=request.user)
    except Resume.DoesNotExist:
        messages.error(request, "Please create your resume first.")
        return redirect('resume:create_resume')

    # Render the résumé template to an HTML string.
    # You can use the same template as your view_resume page or create a dedicated PDF template.
    html = render_to_string('resume/view_resume.html', {
        'resume': resume,
        'pdf': True,  # Flag to hide buttons
    })
    
    # Create a HttpResponse object with PDF headers.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="resume.pdf"'

    # Create PDF using xhtml2pdf and write to the response.
    pisa_status = pisa.CreatePDF(html, dest=response)
    
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

def logout_view(request):
    logout(request)
    return redirect('resume:home')
