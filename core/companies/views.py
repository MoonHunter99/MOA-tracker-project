from django.shortcuts import render, get_object_or_404
from .models import Company, Tag
from documents.models import RequirementDocument

# Create your views here.

def dashboard(request):
    # Get all tags to display in the filter sidebar
    tags = Tag.objects.all()
    
    # Check if the user clicked a specific tag filter
    selected_tag = request.GET.get('tag')
    
    # Check if the user entered a search query
    search_query = request.GET.get('q', '')
    
    # Start with all active companies
    companies = Company.objects.filter(is_active=True)
    
    if selected_tag:
        # Filter companies by the selected tag
        companies = companies.filter(tags__name=selected_tag)
        
    if search_query:
        # Filter companies where the name contains the search query (case-insensitive)
        companies = companies.filter(name__icontains=search_query)
        
    # Ensure distinct results just in case 'tags__name' creates duplicates
    companies = companies.distinct()
        
    context = {
        'companies': companies,
        'tags': tags,
        'selected_tag': selected_tag,
        'search_query': search_query,
    }
    
    return render(request, 'companies/dashboard.html', context)

def company_detail(request, pk):
    # Fetch the specific company or return a 404 error if it doesn't exist
    company = get_object_or_404(Company, pk=pk, is_active=True)
    
    # Fetch documents specific to this company
    specific_docs = RequirementDocument.objects.filter(specific_company=company)
    
    # Fetch general requirements (where specific_company is null)
    general_docs = RequirementDocument.objects.filter(specific_company__isnull=True)
    
    context = {
        'company': company,
        'specific_docs': specific_docs,
        'general_docs': general_docs,
    }
    
    return render(request, 'companies/company_detail.html', context)