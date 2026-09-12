import os
import django
import json
import urllib.request
import urllib.parse

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'comReporta.settings')
django.setup()

from report.models import Report

def geocode_address(address):
    try:
        url = f"https://nominatim.openstreetmap.org/search?q={urllib.parse.quote(address)}&format=json&limit=1"
        req = urllib.request.Request(url, headers={'User-Agent': 'CommUnityConnect/1.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())
            if data and len(data) > 0:
                return float(data[0]['lat']), float(data[0]['lon'])
    except Exception as e:
        print(f"Error geocoding {address}: {e}")
    return -26.2041, 28.0473  # Default to Johannesburg

# Update all reports without coordinates
reports = Report.objects.filter(latitude__isnull=True)
count = reports.count()
print(f"Found {count} reports to update")

for report in reports:
    print(f"Geocoding: {report.location}")
    lat, lng = geocode_address(report.location)
    report.latitude = lat
    report.longitude = lng
    report.save()
    print(f" Updated {report.reference_number}: {lat}, {lng}")

print(f"\n Done! Updated {count} reports")