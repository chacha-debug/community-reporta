from django.shortcuts import render
from django.http import JsonResponse
from report.models import Report

def track_issue(request):
    """Track issue by reference number"""
    
    reference = request.GET.get('ref') or request.POST.get('reference_number')
    
    if request.method == 'POST' or reference:
        # Get reference number from POST or GET
        ref_number = request.POST.get('reference_number') or reference
        
        if ref_number:
            try:
                report = Report.objects.get(reference_number=ref_number)
                
                # Prepare report data for display
                report_data = {
                    'reference_number': report.reference_number,
                    'issue_details': report.issue_details,
                    'issue_type': report.get_issue_type_display(),
                    'location': report.location,
                    'description': report.description,
                    'status': report.get_status_display(),
                    'status_code': report.status,
                    'created_at': report.created_at.strftime('%d %B %Y, %H:%M'),
                    'updated_at': report.updated_at.strftime('%d %B %Y, %H:%M'),
                    'photo': report.photo.url if report.photo else None,
                    'latitude': report.latitude,
                    'longitude': report.longitude,
                }
                
                # Calculate days since reported
                from datetime import datetime
                days_ago = (datetime.now().date() - report.created_at.date()).days
                report_data['days_ago'] = days_ago
                
                return render(request, 'track/track_result.html', {
                    'report': report_data,
                    'found': True
                })
                
            except Report.DoesNotExist:
                return render(request, 'track/track_result.html', {
                    'found': False,
                    'error': f'No report found with reference number: {ref_number}'
                })
        else:
            return render(request, 'track/track_result.html', {
                'found': False,
                    'error': 'Please enter a reference number'
            })
    
    # GET request without reference - show search form
    return render(request, 'track/track_result.html', {'show_form': True})