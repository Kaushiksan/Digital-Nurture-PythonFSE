"""
=========================================================
HANDS-ON 1
Web Framework Foundations
=========================================================
"""

# --------------------------------------------------------
# REQUEST RESPONSE CYCLE
# --------------------------------------------------------

"""
Browser

↓

URL Router

↓

View

↓

Model

↓

Database

↓

Model

↓

View

↓

HttpResponse

↓

Browser

"""

# --------------------------------------------------------
# Middleware
# --------------------------------------------------------

"""
Middleware executes between the request and response.

Examples:

1. SecurityMiddleware
   Provides security-related headers.

2. AuthenticationMiddleware
   Associates users with requests.
"""

# --------------------------------------------------------
# WSGI vs ASGI
# --------------------------------------------------------

"""
WSGI

• Synchronous
• Handles one request per worker
• Used by default in Django

ASGI

• Asynchronous
• Supports WebSockets
• Supports long-lived connections
• Better for real-time applications
"""

# --------------------------------------------------------
# MVC vs MVT
# --------------------------------------------------------

"""
MVC

Model
View
Controller

Django MVT

Model → Model

View (MVC)
↓

Template (MVT)

Controller (MVC)
↓

View (Django)

"""
