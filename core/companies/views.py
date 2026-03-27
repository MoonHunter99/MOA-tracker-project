from django.shortcuts import render
from .models import Company, Tag

# Create your views here.

def dashboard(request):
    # Get all tags to display in the filter sidebar
    tags = Tag.objects.all()
    
    # Check if the user clicked a specific tag filter
    selected_tag = request.GET.get('tag')
    
    if selected_tag:
        # Filter companies by the selected tag and ensure they are active
        companies = Company.objects.filter(tags__name=selected_tag, is_active=True).distinct()
    else:
        # If no filter is applied, show all active companies
        companies = Company.objects.filter(is_active=True)
        
    context = {
        'companies': companies,
        'tags': tags,
        'selected_tag': selected_tag,
    }
    
    return render(request, 'companies/dashboard.html', context)