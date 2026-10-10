from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Job, Application, Category, Company
from .forms import CompanyRegistrationForm, JobForm, ApplicationForm

def register_company(request):
    if request.method == 'POST':
        form = CompanyRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CompanyRegistrationForm()
    return render(request, 'portal/company_register.html', {'form': form})

def job_list(request):
    jobs = Job.objects.filter(is_active=True).order_by('-created_at')
    categories = Category.objects.all()

    query = request.GET.get('q')
    category_id = request.GET.get('category')
    location = request.GET.get('location')

    if query:
        jobs = jobs.filter(Q(title__icontains=query) | Q(description__icontains=query))
    if category_id:
        jobs = jobs.filter(category_id=category_id)
    if location:
        jobs = jobs.filter(location__icontains=location)

    context = {
        'jobs': jobs,
        'categories': categories,
    }
    return render(request, 'portal/job_list.html', context)

@login_required
def job_detail(request, pk):
    job = get_object_or_404(Job, pk=pk)
    has_applied = Application.objects.filter(job=job, applicant=request.user).exists()
    
    if request.method == 'POST' and not has_applied:
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.applicant = request.user
            application.save()
            return redirect('job_detail', pk=job.pk)
    else:
        form = ApplicationForm()

    return render(request, 'portal/job_detail.html', {
        'job': job, 
        'form': form, 
        'has_applied': has_applied
    })

@login_required
def create_job(request):
    if not hasattr(request.user, 'company'):
        return redirect('job_list')
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.company = request.user.company
            job.save()
            return redirect('job_list')
    else:
        form = JobForm()
    return render(request, 'portal/job_form.html', {'form': form, 'title': 'Post a Job'})

@login_required
def update_job(request, pk):
    job = get_object_or_404(Job, pk=pk, company__user=request.user)
    if request.method == 'POST':
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            return redirect('job_detail', pk=job.pk)
    else:
        form = JobForm(instance=job)
    return render(request, 'portal/job_form.html', {'form': form, 'title': 'Edit Job'})

@login_required
def delete_job(request, pk):
    job = get_object_or_404(Job, pk=pk, company__user=request.user)
    if request.method == 'POST':
        job.delete()
        return redirect('job_list')
    return render(request, 'portal/job_confirm_delete.html', {'job': job})

@login_required
def applicant_list(request, job_id):
    job = get_object_or_404(Job, pk=job_id, company__user=request.user)
    applications = job.applications.all()
    return render(request, 'portal/applicant_list.html', {'job': job, 'applications': applications})

@login_required
def update_application_status(request, app_id, status):
    application = get_object_or_404(Application, pk=app_id, job__company__user=request.user)
    if status in ['Accepted', 'Rejected']:
        application.status = status
        application.save()
    return redirect('applicant_list', job_id=application.job.id)

@login_required
def my_applications(request):
    applications = Application.objects.filter(applicant=request.user).order_by('-applied_at')
    return render(request, 'portal/my_applications.html', {'applications': applications})
