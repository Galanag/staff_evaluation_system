from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import StaffMember, EvaluationRecord, AdministrativeEvaluation, FinalEvaluationReview, UserProfile, ArchiveEntry


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=150, required=True)
    last_name = forms.CharField(max_length=150, required=True)
    account_type = forms.ChoiceField(
        choices=[("instructor", "Instructor / staff member"), ("student", "Student evaluator")],
        label="I am registering as",
    )

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "account_type", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=commit)
        if commit:
            profile, _ = UserProfile.objects.get_or_create(user=user)
            profile.role = self.cleaned_data["account_type"]
            profile.save(update_fields=["role"])
        return user


class StaffMemberForm(forms.ModelForm):
    class Meta:
        model = StaffMember
        fields = ["employee_id", "name", "email", "college", "department", "position", "grade", "job_process", "linked_user", "is_active"]
        widgets = {
            "employee_id": forms.TextInput(attrs={"placeholder": "e.g. AU-0042"}),
            "name": forms.TextInput(attrs={"placeholder": "Full name"}),
            "college": forms.TextInput(attrs={"placeholder": "College / school / institute"}),
            "department": forms.TextInput(attrs={"placeholder": "Department"}),
        }


class EvaluationRecordForm(forms.ModelForm):
    class Meta:
        model = EvaluationRecord
        fields = [
            "form_type", "staff", "evaluator", "college", "department",
            "course_title", "course_code", "academic_year", "batch",
            "semester", "evaluation_date", "period_start", "period_end",
            "ratings", "average_score", "strengths", "improvements", "status",
        ]
        widgets = {
            "evaluation_date": forms.DateInput(attrs={"type": "date"}),
            "period_start": forms.DateInput(attrs={"type": "date"}),
            "period_end": forms.DateInput(attrs={"type": "date"}),
            "academic_year": forms.TextInput(attrs={"placeholder": "e.g. 2018 E.C."}),
            "batch": forms.Select(choices=[(str(i), f"Batch {i}") for i in range(1, 6)]),
            "semester": forms.Select(choices=[("I", "Semester I"), ("II", "Semester II")]),
        }


class AdministrativeEvaluationForm(forms.ModelForm):
    class Meta:
        model = AdministrativeEvaluation
        fields = [
            "staff", "period_start", "period_end", "plan_title", "planned_outcomes", "actual_achievements",
            "plan_execution_score", "employee_score", "team_score", "supervisor_score", "performance_level",
            "strengths", "improvement_gaps", "supervisor_name", "supervisor_signature", "supervisor_date",
            "employee_agreed", "disagreement_reason", "employee_signature", "employee_date",
        ]
        widgets = {
            "period_start": forms.DateInput(attrs={"type": "date"}),
            "period_end": forms.DateInput(attrs={"type": "date"}),
            "supervisor_date": forms.DateInput(attrs={"type": "date"}),
            "employee_date": forms.DateInput(attrs={"type": "date"}),
            "planned_outcomes": forms.Textarea(attrs={"rows": 3, "placeholder": "Planned results / targets"}),
            "actual_achievements": forms.Textarea(attrs={"rows": 4, "placeholder": "Achievements during the six-month period"}),
            "strengths": forms.Textarea(attrs={"rows": 3}),
            "improvement_gaps": forms.Textarea(attrs={"rows": 3}),
            "disagreement_reason": forms.Textarea(attrs={"rows": 3}),
            "plan_execution_score": forms.NumberInput(attrs={"min": "0", "max": "70", "step": "0.01", "placeholder": "0–70"}),
            "employee_score": forms.NumberInput(attrs={"min": "0", "max": "5", "step": "0.01", "placeholder": "0–5"}),
            "team_score": forms.NumberInput(attrs={"min": "0", "max": "15", "step": "0.01", "placeholder": "0–15"}),
            "supervisor_score": forms.NumberInput(attrs={"min": "0", "max": "10", "step": "0.01", "placeholder": "0–10"}),
        }

    def clean(self):
        cleaned = super().clean()
        start, end = cleaned.get("period_start"), cleaned.get("period_end")
        if start and end and end < start:
            self.add_error("period_end", "The end date must be on or after the start date.")
        if cleaned.get("employee_agreed") and cleaned.get("disagreement_reason"):
            # Keep the explanation if someone typed it, but don't treat it as a validation failure.
            pass
        return cleaned


class FinalReviewForm(forms.ModelForm):
    class Meta:
        model = FinalEvaluationReview
        fields = ["strengths", "improvements", "final_comment"]
        widgets = {
            "strengths": forms.Textarea(attrs={"rows": 3}),
            "improvements": forms.Textarea(attrs={"rows": 3}),
            "final_comment": forms.Textarea(attrs={"rows": 4}),
        }


class ArchiveEntryForm(forms.ModelForm):
    class Meta:
        model = ArchiveEntry
        fields = ["archive_level", "reference_code", "forwarded_to_office", "instructor_copy_sent", "department_copy_sent", "notes"]
        widgets = {
            "reference_code": forms.TextInput(attrs={"placeholder": "Optional archive / registry reference"}),
            "forwarded_to_office": forms.TextInput(attrs={"placeholder": "Office or archive destination"}),
            "notes": forms.Textarea(attrs={"rows": 3, "placeholder": "Optional archive notes"}),
        }
