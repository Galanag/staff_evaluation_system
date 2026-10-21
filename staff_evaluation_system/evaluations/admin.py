from django.contrib import admin
from .models import UserProfile, StaffMember, EvaluationRecord, AdministrativeEvaluation, FinalEvaluationReview, ArchiveEntry

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "role", "college", "department")
    list_filter = ("role", "college")
    search_fields = ("user__username", "user__first_name", "user__last_name", "department")

@admin.register(StaffMember)
class StaffMemberAdmin(admin.ModelAdmin):
    list_display = ("employee_id", "name", "department", "position", "linked_user", "is_active")
    list_filter = ("college", "department", "is_active")
    search_fields = ("employee_id", "name", "email", "department")
    autocomplete_fields = ("linked_user",)

@admin.register(EvaluationRecord)
class EvaluationRecordAdmin(admin.ModelAdmin):
    list_display = ("staff", "form_type", "evaluator", "academic_year", "evaluation_date", "average_score", "status")
    list_display_links = ("staff",)
    list_filter = ("form_type", "academic_year", "semester", "status", "college", "department")
    search_fields = ("staff__name", "staff__employee_id", "evaluator__username", "course_title", "course_code")
    readonly_fields = ("average_score", "submitted_at", "created_at")
    date_hierarchy = "evaluation_date"
    ordering = ["-evaluation_date", "-created_at"]
    list_per_page = 50


@admin.register(AdministrativeEvaluation)
class AdministrativeEvaluationAdmin(admin.ModelAdmin):
    list_display = ("staff", "period_start", "period_end", "plan_execution_score", "total_score_display", "evaluator", "status")
    list_display_links = ("staff",)
    list_filter = ("performance_level", "status", "staff__college", "staff__department")
    search_fields = ("staff__name", "staff__employee_id", "supervisor_name")
    readonly_fields = ("created_at",)
    date_hierarchy = "period_start"
    ordering = ["-period_end", "-created_at"]
    list_per_page = 50

    @admin.display(description="Total / 100")
    def total_score_display(self, obj):
        return obj.total_score

@admin.register(FinalEvaluationReview)
class FinalEvaluationReviewAdmin(admin.ModelAdmin):
    list_display = ("staff", "academic_year", "reviewed_by", "reviewed_at")
    list_filter = ("academic_year",)
    search_fields = ("staff__name", "staff__employee_id", "final_comment")


@admin.register(ArchiveEntry)
class ArchiveEntryAdmin(admin.ModelAdmin):
    list_display = ("archived_at", "source_type", "archive_level", "reference_code", "archived_by", "forwarded_to_office", "instructor_copy_sent", "department_copy_sent")
    list_filter = ("source_type", "archive_level", "instructor_copy_sent", "department_copy_sent", "archived_at")
    search_fields = ("reference_code", "forwarded_to_office", "academic_record__staff__name", "administrative_record__staff__name", "notes")
    readonly_fields = ("archived_at",)
