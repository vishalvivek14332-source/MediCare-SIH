"""
Centralized Reusable Navigation Configuration for MediCare.
Provides strict separation between Public Authentication entry points
and Authenticated Application/Dashboard modules to prevent accidental
omission or misplacement during UI updates.
"""

PUBLIC_NAV_ITEMS = [
    {
        "id": "nav_home",
        "title": "Home",
        "url": "/#hero",
        "type": "link"
    },
    {
        "id": "nav_about",
        "title": "About",
        "url": "/#workflow",
        "type": "link"
    },
    {
        "id": "nav_features",
        "title": "Features",
        "url": "/#services",
        "type": "link"
    },
    {
        "id": "nav_resources",
        "title": "Resources",
        "url": "/#security",
        "type": "link"
    },
    {
        "id": "nav_health_id",
        "title": "Health ID",
        "url": "/health-id",
        "type": "link"
    }
]

PUBLIC_AUTH_ACTIONS = [
    {
        "id": "auth_login",
        "title": "Login",
        "url": "/login",
        "type": "button",
        "variant": "outline",
        "role_default": "patient"
    },
    {
        "id": "auth_signup",
        "title": "Sign Up",
        "url": "/signup",
        "type": "button",
        "variant": "primary",
        "role_default": "patient"
    }
]

AUTHENTICATED_NAV_ITEMS = [
    {
        "id": "sidebar_dashboard",
        "title": "Dashboard",
        "url": "/dashboard",
        "icon": "dashboard",
        "roles": ["patient"]
    },
    {
        "id": "sidebar_records",
        "title": "My Health Records",
        "url": "/health-records",
        "icon": "records",
        "roles": ["patient"]
    },
    {
        "id": "sidebar_upload",
        "title": "Upload Documents",
        "url": "/upload-documents",
        "icon": "upload",
        "roles": ["patient"]
    },
    {
        "id": "sidebar_shared",
        "title": "Shared Records",
        "url": "/shared-records",
        "icon": "share",
        "roles": ["patient"]
    },
    {
        "id": "sidebar_facilities",
        "title": "Linked Facilities",
        "url": "/linked-facilities",
        "icon": "facilities",
        "roles": ["patient"]
    },
    {
        "id": "sidebar_appointments",
        "title": "Appointments",
        "url": "/appointments",
        "icon": "calendar",
        "roles": ["patient"]
    },
    {
        "id": "sidebar_booking",
        "title": "Clinic Token / Booking",
        "url": "/booking",
        "icon": "ticket",
        "roles": ["patient"]
    },
    {
        "id": "sidebar_profile",
        "title": "Profile",
        "url": "/profile",
        "icon": "user",
        "roles": ["patient", "doctor", "clinic_admin", "main_admin"]
    },
    {
        "id": "sidebar_settings",
        "title": "Settings",
        "url": "/settings",
        "icon": "settings",
        "roles": ["patient", "doctor", "clinic_admin", "main_admin"]
    }
]

AUTHENTICATED_USER_CONTROLS = [
    {
        "id": "user_profile",
        "title": "Profile",
        "url": "/profile"
    },
    {
        "id": "user_health_id",
        "title": "Health ID",
        "url": "/health-id"
    },
    {
        "id": "user_settings",
        "title": "Settings",
        "url": "/settings"
    },
    {
        "id": "user_logout",
        "title": "Logout",
        "url": "/logout"
    }
]

def get_navigation_context(is_authenticated=False, role='patient'):
    return {
        "public_nav_items": PUBLIC_NAV_ITEMS,
        "public_auth_actions": PUBLIC_AUTH_ACTIONS if not is_authenticated else [],
        "authenticated_nav_items": [item for item in AUTHENTICATED_NAV_ITEMS if role in item.get("roles", [])],
        "authenticated_user_controls": AUTHENTICATED_USER_CONTROLS if is_authenticated else []
    }
