from django.http import HttpResponse

def home(request):
    return HttpResponse("""
        <!DOCTYPE html>
        <html>
        <head>
            <meta name="google-site-verification" content="FAkWiYhl3uQijrO-H2lI-NzNY9VoGDrmrqdWKDGZya4" />
        </head>
        <body>
            <p>API está no ar!</p>
        </body>
        </html>
    """)
