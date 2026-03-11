from django.db import models
import random
import string

def generate_tracking_code():
    """Generate a unique 8-character tracking code"""
    while True:
        code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        if not Complaint.objects.filter(tracking_code=code).exists():
            return code

class Complaint(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('rejected', 'Rejected'),
    ]
    
    CATEGORY_CHOICES = [
        ('road', 'Road Repair'),
        ('garbage', 'Garbage Collection'),
        ('light', 'Street Light'),
        ('noise', 'Noise Complaint'),
        ('flood', 'Flooding'),
        ('other', 'Other'),
    ]
    
    tracking_code = models.CharField(max_length=8, unique=True, default=generate_tracking_code, editable=False)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.TextField()
    location = models.CharField(max_length=200)
    image = models.ImageField(upload_to='complaints/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # If you want to track which user submitted (optional)
    # submitted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return f"{self.tracking_code} - {self.category}"