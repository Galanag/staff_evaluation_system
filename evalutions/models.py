
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class UserProfile(models.Model):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "System Administrator"
        STUDENT = "STUDENT", "Student"
        DEPARTMENT_HEAD = "HOD", "Department Head"
        PEER = "PEER", "Peer Instructor"
        ACADEMIC_STAFF = "ACADEMIC", "Academic Staff"
        ADMINISTRATIVE_STAFF = "STAFF", "Administrative Staff"
        COMMITTEE = "COMMITTEE", "Ad-hoc Committee"
        COLLEGE_ADMIN = "COLLEGE", "College Administration"
        DEAN = "DEAN", "Dean / Vice Dean"
        ACADEMIC_AFFAIRS = "AA", "Academic Affairs"

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
    )
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.ACADEMIC_STAFF,
    )
    department = models.CharField(max_length=150, blank=True)
    institution = models.CharField(max_length=200, blank=True)
    employee_id = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.get_role_display()}"


class StaffMember(models.Model):
    class StaffType(models.TextChoices):
        ACADEMIC = "ACADEMIC", "Academic Staff"
        ADMINISTRATIVE = "ADMINISTRATIVE", "Administrative Staff"

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="staff_record",
    )
    staff_type = models.CharField(max_length=20, choices=StaffType.choices)
    job_title = models.CharField(max_length=150)
    department = models.CharField(max_length=150)
    institution = models.CharField(max_length=200)
    employee_id = models.CharField(max_length=50, unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.employee_id} - {self.user.get_full_name() or self.user.username}"


class EvaluationCycle(models.Model):
    class EvaluationType(models.TextChoices):
        ACADEMIC = "ACADEMIC", "Academic Evaluation"
        ADMINISTRATIVE = "ADMINISTRATIVE", "Administrative Evaluation"

    name = models.CharField(max_length=200)
    evaluation_type = models.CharField(
        max_length=20,
        choices=EvaluationType.choices,
    )
    academic_year = models.CharField(max_length=20, blank=True)
    semester = models.CharField(max_length=20, blank=True)
    batch = models.CharField(max_length=20, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    is_open = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-start_date"]

    def __str__(self):
        return self.name

    @property
    def is_valid_period(self):
        return self.start_date <= self.end_date

class EvaluationQuestion(models.Model):
    class EvaluationType(models.TextChoices):
        ACADEMIC = "ACADEMIC", "Academic Evaluation"
        ADMINISTRATIVE = "ADMINISTRATIVE", "Administrative Evaluation"

    class FormType(models.TextChoices):
        STUDENT = "STUDENT", "Student Form"
        HOD = "HOD", "Department Head Form"
        PEER = "PEER", "Peer Form"
        SELF = "SELF", "Self-Evaluation Form"
        ADMINISTRATIVE = "ADMINISTRATIVE", "Administrative Staff Form"

    evaluation_type = models.CharField(
        max_length=20,
        choices=EvaluationType.choices,
    )
    form_type = models.CharField(
        max_length=20,
        choices=FormType.choices,
        default=FormType.SELF,
    )
    section = models.CharField(max_length=150)
    question_text = models.TextField()
    order = models.PositiveIntegerField(default=1)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["evaluation_type", "section", "order"]

    def __str__(self):
        return f"{self.section}: {self.question_text[:70]}"


class EvaluationSubmission(models.Model):
    class EvaluatorType(models.TextChoices):
        STUDENT = "STUDENT", "Student"
        DEPARTMENT_HEAD = "HOD", "Department Head"
        PEER = "PEER", "Peer Instructor"
        SELF = "SELF", "Self Evaluation"
        TEAM = "TEAM", "Evaluation Team"
        SUPERVISOR = "SUPERVISOR", "Immediate Supervisor"

    class Status(models.TextChoices):
        DRAFT = "DRAFT", "Draft"
        SUBMITTED = "SUBMITTED", "Submitted"
        REVIEWED = "REVIEWED", "Reviewed"

    cycle = models.ForeignKey(
        EvaluationCycle,
        on_delete=models.PROTECT,
        related_name="submissions",
    )
    staff_member = models.ForeignKey(
        StaffMember,
        on_delete=models.PROTECT,
        related_name="evaluations",
    )
    evaluator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="submitted_evaluations",
    )
    evaluator_type = models.CharField(
        max_length=20,
        choices=EvaluatorType.choices,
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT,
    )
    strengths = models.TextField(blank=True)
    improvement_points = models.TextField(blank=True)
    submitted_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "cycle",
                    "staff_member",
                    "evaluator",
                    "evaluator_type",
                ],
                name="unique_evaluation_per_evaluator",
            )
        ]

    def __str__(self):
        return f"{self.staff_member} - {self.get_evaluator_type_display()}"


class EvaluationResponse(models.Model):
    submission = models.ForeignKey(
        EvaluationSubmission,
        on_delete=models.CASCADE,
        related_name="responses",
    )
    question = models.ForeignKey(
        EvaluationQuestion,
        on_delete=models.PROTECT,
        related_name="responses",
    )
    score = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(5),
        ],
    )
    not_applicable = models.BooleanField(default=False)
    comment = models.TextField(blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["submission", "question"],
                name="unique_question_per_submission",
            )
        ]

    def __str__(self):
        return f"Response {self.pk}: {self.score}"
