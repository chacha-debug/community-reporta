from django.shortcuts import render


def home(request):
    """Single-page homepage with all sections"""
    return render(request, 'pages/home.html')


def contact_form_submit(request):
    """Handle contact form submission"""
    if request.method == 'POST':
        name = request.POST.get('name', 'Guest')
        # In a real app, you'd send an email here.
        # For now, just render a success page.
        return render(request, 'pages/contact_success.html', {'name': name})

    # If someone hits this URL with GET, send them home
    return render(request, 'pages/home.html')