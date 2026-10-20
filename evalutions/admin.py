from django.contrib import admin

from .models import (
    EvaluationCycle,
    EvaluationQuestion,
    EvaluationResponse,
    EvaluationSubmission,
    StaffMember,
    UserProfile,
)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "role", "department", "institution")
    list_filter = ("role", "institution")
    search_fields = ("user__username", "user__first_name", "user__last_name")


@admin.register(StaffMember)
class StaffMemberAdmin(admin.ModelAdmin):
    list_display = (
        "employee_id",
        "user",
        "staff_type",
        "job_title",
        "department",
        "is_active",
    )
    list_filter = ("staff_type", "department", "is_active")
    search_fields = (
        "employee_id",
        "user__username",
        "user__first_name",
        "user__last_name",
    )


@admin.register(EvaluationCycle)
class EvaluationCycleAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "evaluation_type",
        "academic_year",
        "start_date",
        "end_date",
        "is_open",
    )
    list_filter = ("evaluation_type", "academic_year", "is_open")
    search_fields = ("name", "academic_year")


@admin.register(EvaluationQuestion)
class EvaluationQuestionAdmin(admin.ModelAdmin):
    list_display = (
        "question_text",
        "evaluation_type",
        "section",
        "order",
        "is_active",
    )
    list_filter = (
        "evaluation_type",
        "section", 
        "is_active",
    )
    search_fields = ("question_text", "section")
    list_editable = ("order", "is_active")


class EvaluationResponseInline(admin.TabularInline):
    model = EvaluationResponse
    extra = 0
    fields = ("question", "score", "not_applicable", "comment")
    readonly_fields = ("question",)

@admin.register(EvaluationSubmission)
class EvaluationSubmissionAdmin(admin.ModelAdmin):
    list_display = (
        "staff_member",
        "cycle",
        "evaluator",
        "evaluator_type",
        "status",
        "created_at",
    )
    list_filter = (
        "evaluator_type",
        "status",
        "cycle",
    )

    search_fields = (
        "staff_member__employee_id",
        "staff_member__user__username",
        "staff_member__user__first_name",
        "staff_member__user__last_name",
        "evaluator__username",
        "cycle__name",
    )
    
    readonly_fields = ("created_at", "submitted_at")
    inlines = [EvaluationResponseInline]
# Register your models here.
