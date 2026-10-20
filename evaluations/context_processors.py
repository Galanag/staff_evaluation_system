def site_context(request):
    role = ""
    role_display = ""
    if request.user.is_authenticated:
        if request.user.is_superuser:
            role = "admin"
            role_display = "System Administrator"
        else:
            try:
                profile = request.user.evaluation_profile
                role = profile.role
                role_display = profile.get_role_display()
            except Exception:
                role = "instructor"
                role_display = "Instructor / self evaluator"
    return {
        "current_role": role,
        "current_role_display": role_display,
        "university_name": "Ambo University",
    }
