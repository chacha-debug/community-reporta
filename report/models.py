from django.db import models

class Report(models.Model):
    # Issue type choices
    ISSUE_TYPE_CHOICES = [
        ('streetlight', 'Streetlight'),
        ('water', 'Water Leak'),
        ('waste', 'Waste & Sanitation'),
        ('pothole', 'Pothole'),
        ('environment', 'Environment & Public Health'),
        ('parks', 'Parks, Trees & Biodiversity'),
        ('electricity', 'Electricity'),
        ('infrastructure', 'Infrastructure Projects'),
    ]
    
    # Status choices
    STATUS_CHOICES = [
        ('reported', 'Reported'),
        ('verified', 'Verified'),
        ('assigned', 'Assigned'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('rejected', 'Rejected'),
    ]
    
    reference_number = models.CharField(max_length=50, unique=True)
    issue_type = models.CharField(max_length=50, choices=ISSUE_TYPE_CHOICES)
    issue_details = models.CharField(max_length=200)
    location = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    photo = models.ImageField(upload_to='reports/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='reported')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # NEW FIELDS for coordinates
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.reference_number} - {self.issue_details}"