from decimal import Decimal, ROUND_HALF_UP
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class UserProfile(models.Model):
    ROLE_CHOICES = [
        ("student", "Student evaluator"),
        ("instructor", "Instructor / self evaluator"),
        ("peer", "Peer instructor"),
        ("department_head", "Department head"),
        ("committee", "Ad-hoc evaluation committee"),
        ("college_admin", "College / school / institute administration"),
        ("dean", "Dean / vice dean"),
        ("academic_vp", "Academic Affairs Vice President / Vice Director"),
        ("archivist", "University / Department Archives"),
        ("office_directorate", "Concerned Office / Directorate"),
    ]
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="evaluation_profile")
    role = models.CharField(max_length=32, choices=ROLE_CHOICES, default="instructor")
    college = models.CharField(max_length=180, default="Ambo University", blank=True)
    department = models.CharField(max_length=180, blank=True)
    phone = models.CharField(max_length=40, blank=True)

    def __str__(self):
        return f"{self.user.get_username()} ({self.get_role_display()})"


class StaffMember(models.Model):
    employee_id = models.CharField(max_length=40, unique=True)
    name = models.CharField(max_length=200)
    email = models.EmailField(blank=True)
    college = models.CharField(max_length=180, default="Ambo University")
    department = models.CharField(max_length=180, blank=True)
    position = models.CharField(max_length=180, blank=True)
    grade = models.CharField(max_length=40, blank=True)
    job_process = models.CharField(max_length=180, blank=True)
    linked_user = models.OneToOneField(
        settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL,
        related_name="staff_record",
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Instructor / staff member"
        verbose_name_plural = "Instructors / staff members"

    def __str__(self):
        return f"{self.name} ({self.employee_id})"


class EvaluationRecord(models.Model):
    FORM_CHOICES = [
        ("student", "Form A — Students"),
        ("department_head", "Form B — Department head"),
        ("peer", "Form C — Peer"),
        ("self", "Form D — Self-evaluation"),
    ]
    STATUS_CHOICES = [("draft", "Draft"), ("submitted", "Submitted")]
    BATCH_CHOICES = [(str(i), f"Batch {i}") for i in range(1, 6)]
    SEMESTER_CHOICES = [("I", "Semester I"), ("II", "Semester II")]

    form_type = models.CharField(max_length=24, choices=FORM_CHOICES)
    staff = models.ForeignKey(StaffMember, on_delete=models.PROTECT, related_name="evaluations")
    evaluator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="evaluations_created")
    college = models.CharField(max_length=180, blank=True)
    department = models.CharField(max_length=180, blank=True)
    course_title = models.CharField(max_length=180, blank=True)
    course_code = models.CharField(max_length=60, blank=True)
    academic_year = models.CharField(max_length=40, blank=True)
    batch = models.CharField(max_length=4, choices=BATCH_CHOICES, blank=True)
    semester = models.CharField(max_length=4, choices=SEMESTER_CHOICES, blank=True)
    evaluation_date = models.DateField()
    period_start = models.DateField(null=True, blank=True)
    period_end = models.DateField(null=True, blank=True)
    ratings = models.JSONField(default=dict, blank=True)
    average_score = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal("0.00"))
    strengths = models.TextField(blank=True)
    improvements = models.TextField(blank=True)
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default="submitted")
    submitted_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-evaluation_date", "-created_at"]
        indexes = [
            models.Index(fields=["form_type", "academic_year"], name="eval_form_year_idx"),
            models.Index(fields=["staff", "form_type"], name="eval_staff_form_idx"),
            models.Index(fields=["status", "evaluation_date"], name="eval_status_date_idx"),
        ]

    def __str__(self):
        return f"{self.get_form_type_display()} — {self.staff.name} — {self.evaluation_date}"

    @property
    def weight(self):
        return {"student": 40, "department_head": 35, "peer": 15, "self": 10}.get(self.form_type, 0)

    @property
    def weighted_score(self):
        return (self.average_score * Decimal(self.weight) / Decimal("5")).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


class AdministrativeEvaluation(models.Model):
    LEVEL_CHOICES = [
        ("excellent", "እጅግ በጣም ጥሩ"),
        ("very_good", "በጣም ጥሩ"),
        ("good", "ጥሩ"),
        ("satisfactory", "አጥጋቢ"),
        ("needs_improvement", "መሻሻል የሚያስፈልገው"),
    ]
    STATUS_CHOICES = [("draft", "Draft"), ("submitted", "Submitted")]

    staff = models.ForeignKey(StaffMember, on_delete=models.PROTECT, related_name="administrative_evaluations")
    evaluator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="administrative_evaluations_created")
    period_start = models.DateField()
    period_end = models.DateField()
    plan_title = models.CharField(max_length=240, blank=True)
    planned_outcomes = models.TextField(blank=True)
    actual_achievements = models.TextField(blank=True)
    plan_execution_score = models.DecimalField(
        max_digits=5, decimal_places=2, default=Decimal("0.00"),
        validators=[MinValueValidator(0), MaxValueValidator(70)],
        help_text="Score for results-based plan execution, out of 70.",
    )
    employee_score = models.DecimalField(
        max_digits=4, decimal_places=2, default=Decimal("0.00"),
        validators=[MinValueValidator(0), MaxValueValidator(5)],
    )
    team_score = models.DecimalField(
        max_digits=4, decimal_places=2, default=Decimal("0.00"),
        validators=[MinValueValidator(0), MaxValueValidator(15)],
    )
    supervisor_score = models.DecimalField(
        max_digits=4, decimal_places=2, default=Decimal("0.00"),
        validators=[MinValueValidator(0), MaxValueValidator(10)],
    )
    performance_level = models.CharField(max_length=30, choices=LEVEL_CHOICES, blank=True)
    strengths = models.TextField(blank=True)
    improvement_gaps = models.TextField(blank=True)
    supervisor_name = models.CharField(max_length=180, blank=True)
    supervisor_signature = models.CharField(max_length=180, blank=True, help_text="Typed name; wet signatures are completed on printed copies.")
    supervisor_date = models.DateField(null=True, blank=True)
    employee_agreed = models.BooleanField(default=True)
    disagreement_reason = models.TextField(blank=True)
    employee_signature = models.CharField(max_length=180, blank=True, help_text="Typed name; wet signatures are completed on printed copies.")
    employee_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default="submitted")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-period_end", "-created_at"]

    def __str__(self):
        return f"የ6 ወር ምዘና — {self.staff.name} ({self.period_start}–{self.period_end})"

    @property
    def total_score(self):
        total = self.plan_execution_score + self.employee_score + self.team_score + self.supervisor_score
        return total.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


class FinalEvaluationReview(models.Model):
    staff = models.ForeignKey(StaffMember, on_delete=models.CASCADE, related_name="final_reviews")
    academic_year = models.CharField(max_length=40)
    strengths = models.TextField(blank=True)
    improvements = models.TextField(blank=True)
    final_comment = models.TextField(blank=True)
    reviewed_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name="final_evaluation_reviews")
    reviewed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [("staff", "academic_year")]
        ordering = ["-academic_year", "staff__name"]

    def __str__(self):
        return f"Final review — {self.staff.name} — {self.academic_year}"


class ArchiveEntry(models.Model):
    SOURCE_CHOICES = [("academic", "Academic evaluation"), ("administrative", "Six-month administrative evaluation")]
    LEVEL_CHOICES = [("department", "Department archive"), ("college", "College / school / institute archive"), ("university", "University archive")]

    source_type = models.CharField(max_length=20, choices=SOURCE_CHOICES)
    academic_record = models.ForeignKey(EvaluationRecord, null=True, blank=True, on_delete=models.PROTECT, related_name="archive_entries")
    administrative_record = models.ForeignKey(AdministrativeEvaluation, null=True, blank=True, on_delete=models.PROTECT, related_name="archive_entries")
    archive_level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default="department")
    reference_code = models.CharField(max_length=100, blank=True)
    forwarded_to_office = models.CharField(max_length=180, default="University / Department Archives")
    instructor_copy_sent = models.BooleanField(default=False)
    department_copy_sent = models.BooleanField(default=False)
    notes = models.TextField(blank=True)
    archived_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="archive_entries_created")
    archived_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-archived_at"]
        verbose_name = "Evaluation archive entry"
        verbose_name_plural = "Evaluation archive entries"

    def clean(self):
        from django.core.exceptions import ValidationError
        # source_type and source record are controlled by the archive-create view,
        # so let ModelForm validate editable fields before those view-only fields exist.
        if not self.source_type:
            return
        if self.source_type == "academic":
            if not self.academic_record or self.administrative_record:
                raise ValidationError("Academic archive entries must reference exactly one academic evaluation.")
        elif self.source_type == "administrative":
            if not self.administrative_record or self.academic_record:
                raise ValidationError("Administrative archive entries must reference exactly one six-month evaluation.")
        else:
            raise ValidationError("Select a valid archive record type.")

    @property
    def staff_member(self):
        if self.source_type == "academic" and self.academic_record_id:
            return self.academic_record.staff
        if self.source_type == "administrative" and self.administrative_record_id:
            return self.administrative_record.staff
        return None

    def __str__(self):
        staff = self.staff_member
        return f"Archive entry — {staff.name if staff else 'unassigned'} — {self.get_source_type_display()}"
