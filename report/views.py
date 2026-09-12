import datetime
import random
import string
import json
import urllib.request
import urllib.parse
from django.shortcuts import render
from django.http import JsonResponse
from .models import Report

def geocode_address(address):
    """Convert address to latitude and longitude using Nominatim API"""
    try:
        url = f"https://nominatim.openstreetmap.org/search?q={urllib.parse.quote(address)}&format=json&limit=1"
        req = urllib.request.Request(url, headers={'User-Agent': 'CommUnityConnect/1.0'})
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            if data and len(data) > 0:
                return float(data[0]['lat']), float(data[0]['lon'])
    except Exception as e:
        print(f"Geocoding error: {e}")
    return -26.2041, 28.0473  # Default to Johannesburg


def get_status_color(status):
    colors = {
        'reported': 'red',
        'verified': 'orange',
        'assigned': 'purple',
        'in_progress': 'blue',
        'resolved': 'green',
        'rejected': 'gray'
    }
    return colors.get(status, 'gray')


def get_reports(request):
    """API endpoint to get all reports for the map"""
    try:
        reports = Report.objects.all().order_by('-created_at')
        
        reports_data = []
        for report in reports:
            reports_data.append({
                'id': report.id,
                'name': report.issue_details,
                'lat': report.latitude or -26.2041,
                'lng': report.longitude or 28.0473,
                'category': report.issue_type,
                'categoryDisplay': dict(Report.ISSUE_TYPE_CHOICES).get(report.issue_type, report.issue_type),
                'status': dict(Report.STATUS_CHOICES).get(report.status, report.status),
                'color': get_status_color(report.status),
                'details': report.description or report.issue_details,
                'reportedDate': report.created_at.strftime('%d %B %Y'),
                'location': report.location,
                'reference_number': report.reference_number
            })
        
        return JsonResponse({'success': True, 'reports': reports_data})
        
    except Exception as e:
        print(f"Error: {e}")
        return JsonResponse({'success': False, 'error': str(e), 'reports': []})


def report_issue(request):
    """Display and process the report issue form"""

    if request.method == 'POST':
        # Get form data
        photo = request.FILES.get('photo')
        location = request.POST.get('location')
        issue_type = request.POST.get('issue_type')
        issue_details = request.POST.get('issue_details')
        description = request.POST.get('description')

        # Validate required fields
        if not location:
            return JsonResponse({
                'success': False,
                'error': 'Please enter the location where the issue is occurring.'
            })

        if not issue_type:
            return JsonResponse({
                'success': False,
                'error': 'Please select the type of issue you are reporting.'
            })

        if not issue_details:
            return JsonResponse({
                'success': False,
                'error': 'Please select the specific issue details.'
            })

        # Prefer exact coordinates if the user picked their location on the client
        client_lat = request.POST.get('latitude')
        client_lng = request.POST.get('longitude')

        if client_lat and client_lng:
            try:
                lat, lng = float(client_lat), float(client_lng)
                print(f"Using client-provided coordinates: {lat}, {lng}")
            except (TypeError, ValueError):
                lat, lng = geocode_address(location)
                print(f"Geocoded (fallback): {lat}, {lng}")
        else:
            print(f"Geocoding address: {location}")
            lat, lng = geocode_address(location)
            print(f"Coordinates: {lat}, {lng}")

        # Generate reference number
        today = datetime.datetime.now()
        date_str = today.strftime('%Y%m%d')

        type_codes = {
            'streetlight': 'STL',
            'water': 'WTR',
            'waste': 'WST',
            'pothole': 'PTH',
            'environment': 'ENV',
            'parks': 'PRK',
            'electricity': 'ELC',
            'infrastructure': 'INF'
        }

        type_code = type_codes.get(issue_type, 'GEN')
        random_num = ''.join(random.choices(string.digits, k=6))
        reference_number = f"{type_code}-{date_str}-{random_num}"

        # Save to database with coordinates
        try:
            report = Report.objects.create(
                reference_number=reference_number,
                issue_type=issue_type,
                issue_details=issue_details,
                location=location,
                description=description or '',
                latitude=lat,
                longitude=lng
            )

            if photo:
                report.photo = photo
                report.save()

            print(f"Report saved: {reference_number} at ({lat}, {lng})")

        except Exception as e:
            print(f"Error saving: {e}")
            return JsonResponse({
                'success': False,
                'error': 'Database error. Please try again.'
            })

        # Return success response
        return JsonResponse({
            'success': True,
            'reference_number': reference_number,
            'issue_type': issue_type,
            'issue_details': issue_details,
            'location': location,
            'description': description or '',
            'date': today.strftime('%d %B %Y, %H:%M'),
            'latitude': lat,
            'longitude': lng
        })

    # GET request - display form
    return render(request, 'report/report_form.html')