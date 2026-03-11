from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Complaint
from .forms import ComplaintForm

# 🔐 AUTHENTICATION VIEWS
def home(request):
    """Login page - also redirects if already logged in"""
    if request.user.is_authenticated:
        return redirect('admin_dashboard')
    return render(request, 'complaints/index.html')

def login_view(request):
    """Handle login with email"""
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        
        try:
            user_obj = User.objects.get(email=email)
            username = user_obj.username
            
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {user.first_name}!")
                return redirect('admin_dashboard')
            else:
                messages.error(request, "Invalid email or password")
        except User.DoesNotExist:
            messages.error(request, "No account found with this email")
    
    return render(request, 'complaints/index.html')

def register(request):
    """Register new user with email as login"""
    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST.get('confirm_password', '')
        
        # Validation
        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect('register')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered")
            return redirect('register')
        
        # Create username from email
        base_username = email.split('@')[0]
        username = base_username
        counter = 1
        
        while User.objects.filter(username=username).exists():
            username = f"{base_username}{counter}"
            counter += 1
        
        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        
        messages.success(request, "Registration successful! Please login with your email.")
        return redirect('home')
    
    return render(request, 'complaints/register.html')

def logout_view(request):
    """Log out user"""
    logout(request)
    messages.success(request, "Logged out successfully")
    return redirect('home')

# 📝 COMPLAINT VIEWS
def submit_complaint(request):
    """Public page for submitting complaints"""
    if request.method == "POST":
        form = ComplaintForm(request.POST, request.FILES)
        if form.is_valid():
            complaint = form.save()
            messages.success(request, f'Complaint submitted successfully! Your tracking code is: {complaint.tracking_code}')
            return redirect('complaint_success', tracking_code=complaint.tracking_code)
    else:
        form = ComplaintForm()
    
    return render(request, 'complaints/submit_complaint.html', {'form': form})

def complaint_success(request, tracking_code):
    """Show success page with tracking code"""
    complaint = get_object_or_404(Complaint, tracking_code=tracking_code)
    return render(request, 'complaints/complaint_success.html', {'complaint': complaint})

def track_complaint(request):
    """Page to track complaint status"""
    if request.method == "POST":
        tracking_code = request.POST.get('tracking_code', '').upper().strip()
        try:
            complaint = Complaint.objects.get(tracking_code=tracking_code)
            return render(request, 'complaints/track_result.html', {'complaint': complaint})
        except Complaint.DoesNotExist:
            messages.error(request, 'No complaint found with this tracking code.')
    
    return render(request, 'complaints/track_complaint.html')

# 👑 ADMIN VIEWS
def admin_dashboard(request):
    """Admin dashboard to view all complaints"""
    # Check if user is logged in and is staff
    if not request.user.is_authenticated:
        messages.error(request, 'Please login as admin')
        return redirect('home')
    
    # For now, allow any logged-in user to access dashboard
    # You can change this to is_staff later if you want
    
    complaints = Complaint.objects.all().order_by('-created_at')
    
    # Statistics
    total_complaints = complaints.count()
    pending_count = complaints.filter(status='pending').count()
    resolved_count = complaints.filter(status='resolved').count()
    in_progress_count = complaints.filter(status='in_progress').count()
    
    context = {
        'complaints': complaints,
        'total_complaints': total_complaints,
        'pending_count': pending_count,
        'resolved_count': resolved_count,
        'in_progress_count': in_progress_count,
    }
    return render(request, 'complaints/admin_dashboard.html', context)

def update_complaint_status(request, complaint_id):
    """Update complaint status (admin only)"""
    if not request.user.is_authenticated:
        messages.error(request, 'Please login')
        return redirect('home')
    
    complaint = get_object_or_404(Complaint, id=complaint_id)
    
    if request.method == "POST":
        new_status = request.POST.get('status')
        complaint.status = new_status
        complaint.save()
        messages.success(request, f'Complaint {complaint.tracking_code} status updated to {new_status}')
    
    return redirect('admin_dashboard')

def make_admin(request):
    """Create new admin account"""
    if not request.user.is_authenticated:
        messages.error(request, 'Please login first')
        return redirect('home')
    
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
        else:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                is_staff=True  # Makes them staff
            )
            messages.success(request, f'Admin account created for {username}')
            return redirect('admin_dashboard')
    
    return render(request, 'complaints/make_admin.html')