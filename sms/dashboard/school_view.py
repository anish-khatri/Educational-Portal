from django.shortcuts import render, get_object_or_404, redirect
from models.models import School
from .forms import SchoolForm

def school_list(request):
    """Read: List all schools"""
    schools = School.objects.all()
    return render(request, 'admin/schools/school_list.html', {'schools': schools})

def school_create(request):
    """Create a new school"""
    if request.method == "POST":
        form = SchoolForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('school_list')
    else:
        form = SchoolForm()
    return render(request, 'admin/schools/school_form.html', {'form': form, 'title': 'Add School'})

def school_update(request, pk):
    """Update an existing school"""
    school = get_object_or_404(School, pk=pk)
    if request.method == "POST":
        form = SchoolForm(request.POST, request.FILES, instance=school) 
        if form.is_valid():
            form.save()
            return redirect('school_list')
    else:
        form = SchoolForm(instance=school)
    return render(request, 'admin/schools/school_form.html', {'form': form, 'title': 'Edit School'})

def school_delete(request, pk):
    """Delete a school"""
    school = get_object_or_404(School, pk=pk)
    if request.method == "POST":
        school.delete()
        return redirect('school_list')
    return render(request, 'admin/schools/school_confirm_delete.html', {'school': school})
