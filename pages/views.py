from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings


def home(request):
    """Single-page homepage with all sections"""
    return render(request, 'pages/home.html')

def contact_form_submit(request):
    """Handle contact form submission"""
    if request.method == 'POST':
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        subject = request.POST.get('subject', '')
        message = request.POST.get('message', '')
        
        # In a real app, you would send an email here
        # For now, just show a success message
        
        return HttpResponse(f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Message Sent - CommUnity Connect</title>
            <style>
                body {{
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    min-height: 100vh;
                    margin: 0;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                }}
                .container {{
                    max-width: 500px;
                    background: white;
                    border-radius: 20px;
                    padding: 40px;
                    text-align: center;
                    box-shadow: 0 20px 40px rgba(0,0,0,0.2);
                }}
                .success-icon {{
                    font-size: 64px;
                    color: #27ae60;
                    margin-bottom: 20px;
                }}
                h1 {{
                    color: #27ae60;
                    margin-bottom: 15px;
                }}
                p {{
                    color: #666;
                    margin-bottom: 25px;
                }}
                .button {{
                    display: inline-block;
                    background: linear-gradient(135deg, #2c3e50 0%, #1a252f 100%);
                    color: white;
                    text-decoration: none;
                    padding: 12px 30px;
                    border-radius: 8px;
                    font-weight: bold;
                }}
                .button:hover {{
                    transform: translateY(-2px);
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="success-icon">✅</div>
                <h1>Message Sent!</h1>
                <p>Thank you for reaching out, <strong>{name}</strong>!<br>We'll get back to you within 24-48 hours.</p>
                <a href="/" class="button">Back to Home</a>
            </div>
        </body>
        </html>
        """)
    
    return render(request, 'pages/home.html')

@csrf_exempt
def set_language(request, lang_code):
    """Set user's language preference"""
    # Check if language is valid
    valid_langs = [code for code, name in settings.LANGUAGES]
    
    if lang_code in valid_langs:
        # Store in session
        request.session['django_language'] = lang_code
        
        # Store in cookie
        response = JsonResponse({'success': True})
        response.set_cookie('django_language', lang_code, max_age=31536000)  # 1 year
        
        return response
    
    return JsonResponse({'success': False}, status=400)