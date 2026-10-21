from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from evaluations.models import UserProfile, StaffMember


class Command(BaseCommand):
    help = "Create local demonstration users and sample staff. Demo password: DemoPass2026!"

    def handle(self, *args, **options):
        User = get_user_model()
        people = [
            ("demo_admin", "System", "Administrator", "admin", True),
            ("demo_student", "Sami", "Student", "student", False),
            ("demo_head", "Mekdes", "DepartmentHead", "department_head", False),
            ("demo_peer", "Dawit", "Peer", "peer", False),
            ("demo_instructor", "Lensa", "Instructor", "instructor", False),
            ("demo_committee", "Bontu", "Committee", "committee", False),
        ]
        users = {}
        for username, first, last, role, is_admin in people:
            user, created = User.objects.get_or_create(username=username, defaults={"first_name": first, "last_name": last, "email": f"{username}@example.local"})
            user.first_name = first
            user.last_name = last
            user.email = f"{username}@example.local"
            if created or not user.has_usable_password():
                user.set_password("DemoPass2026!")
            if is_admin:
                user.is_staff = True
                user.is_superuser = True
            user.save()
            profile, _ = UserProfile.objects.get_or_create(user=user)
            profile.role = "instructor" if is_admin else role
            profile.college = "Ambo University"
            profile.department = "Computer Engineering"
            profile.save()
            users[username] = user

        staff_rows = [
            ("AU-0001", "Lensa Bekele", "Institute of Technology", "Computer Engineering", "Lecturer", "XII", "Teaching and Learning", users["demo_instructor"]),
            ("AU-0002", "Tadesse Kumsa", "Natural and Computational Sciences", "Mathematics", "Lecturer", "XI", "Teaching and Learning", None),
            ("AU-0003", "Hana Tolosa", "Social Science and Humanities", "English Language", "Assistant Professor", "XIII", "Teaching and Learning", None),
        ]
        for employee_id, name, college, department, position, grade, job_process, linked_user in staff_rows:
            StaffMember.objects.update_or_create(
                employee_id=employee_id,
                defaults={"name": name, "college": college, "department": department, "position": position, "grade": grade, "job_process": job_process, "linked_user": linked_user, "is_active": True},
            )
        self.stdout.write(self.style.SUCCESS("Demo data is ready."))
        self.stdout.write("Login password for all demo accounts: DemoPass2026!")
        self.stdout.write("Use demo_admin for the Django admin and workbook exports.")
