# Generated for the initial release of the evaluation system.
import django.core.validators
from decimal import Decimal
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True
    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations = [
        migrations.CreateModel(
            name="StaffMember",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("employee_id", models.CharField(max_length=40, unique=True)),
                ("name", models.CharField(max_length=200)),
                ("email", models.EmailField(blank=True, max_length=254)),
                ("college", models.CharField(default="Ambo University", max_length=180)),
                ("department", models.CharField(blank=True, max_length=180)),
                ("position", models.CharField(blank=True, max_length=180)),
                ("grade", models.CharField(blank=True, max_length=40)),
                ("job_process", models.CharField(blank=True, max_length=180)),
                ("is_active", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("linked_user", models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="staff_record", to=settings.AUTH_USER_MODEL)),
            ],
            options={"verbose_name": "Instructor / staff member", "verbose_name_plural": "Instructors / staff members", "ordering": ["name"]},
        ),
        migrations.CreateModel(
            name="UserProfile",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("role", models.CharField(choices=[("student", "Student evaluator"), ("instructor", "Instructor / self evaluator"), ("peer", "Peer instructor"), ("department_head", "Department head"), ("committee", "Ad-hoc evaluation committee"), ("college_admin", "College / school / institute administration"), ("dean", "Dean / vice dean"), ("academic_vp", "Academic Affairs Vice President / Vice Director")], default="instructor", max_length=32)),
                ("college", models.CharField(blank=True, default="Ambo University", max_length=180)),
                ("department", models.CharField(blank=True, max_length=180)),
                ("phone", models.CharField(blank=True, max_length=40)),
                ("user", models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name="evaluation_profile", to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name="AdministrativeEvaluation",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("period_start", models.DateField()),
                ("period_end", models.DateField()),
                ("plan_title", models.CharField(blank=True, max_length=240)),
                ("planned_outcomes", models.TextField(blank=True)),
                ("actual_achievements", models.TextField(blank=True)),
                ("plan_execution_score", models.DecimalField(decimal_places=2, default=Decimal("0.00"), help_text="Score for results-based plan execution, out of 70.", max_digits=5, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(70)])),
                ("employee_score", models.DecimalField(decimal_places=2, default=Decimal("0.00"), max_digits=4, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)])),
                ("team_score", models.DecimalField(decimal_places=2, default=Decimal("0.00"), max_digits=4, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(15)])),
                ("supervisor_score", models.DecimalField(decimal_places=2, default=Decimal("0.00"), max_digits=4, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10)])),
                ("performance_level", models.CharField(blank=True, choices=[("excellent", "እጅግ በጣም ጥሩ"), ("very_good", "በጣም ጥሩ"), ("good", "ጥሩ"), ("satisfactory", "አጥጋቢ"), ("needs_improvement", "መሻሻል የሚያስፈልገው")], max_length=30)),
                ("strengths", models.TextField(blank=True)),
                ("improvement_gaps", models.TextField(blank=True)),
                ("supervisor_name", models.CharField(blank=True, max_length=180)),
                ("supervisor_signature", models.CharField(blank=True, help_text="Typed name; wet signatures are completed on printed copies.", max_length=180)),
                ("supervisor_date", models.DateField(blank=True, null=True)),
                ("employee_agreed", models.BooleanField(default=True)),
                ("disagreement_reason", models.TextField(blank=True)),
                ("employee_signature", models.CharField(blank=True, help_text="Typed name; wet signatures are completed on printed copies.", max_length=180)),
                ("employee_date", models.DateField(blank=True, null=True)),
                ("status", models.CharField(choices=[("draft", "Draft"), ("submitted", "Submitted")], default="submitted", max_length=12)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("evaluator", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="administrative_evaluations_created", to=settings.AUTH_USER_MODEL)),
                ("staff", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="administrative_evaluations", to="evaluations.staffmember")),
            ],
            options={"ordering": ["-period_end", "-created_at"]},
        ),
        migrations.CreateModel(
            name="EvaluationRecord",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("form_type", models.CharField(choices=[("student", "Form A — Students"), ("department_head", "Form B — Department head"), ("peer", "Form C — Peer"), ("self", "Form D — Self-evaluation")], max_length=24)),
                ("college", models.CharField(blank=True, max_length=180)),
                ("department", models.CharField(blank=True, max_length=180)),
                ("course_title", models.CharField(blank=True, max_length=180)),
                ("course_code", models.CharField(blank=True, max_length=60)),
                ("academic_year", models.CharField(blank=True, max_length=40)),
                ("batch", models.CharField(blank=True, choices=[("1", "Batch 1"), ("2", "Batch 2"), ("3", "Batch 3"), ("4", "Batch 4"), ("5", "Batch 5")], max_length=4)),
                ("semester", models.CharField(blank=True, choices=[("I", "Semester I"), ("II", "Semester II")], max_length=4)),
                ("evaluation_date", models.DateField()),
                ("period_start", models.DateField(blank=True, null=True)),
                ("period_end", models.DateField(blank=True, null=True)),
                ("ratings", models.JSONField(blank=True, default=dict)),
                ("average_score", models.DecimalField(decimal_places=2, default=Decimal("0.00"), max_digits=5)),
                ("strengths", models.TextField(blank=True)),
                ("improvements", models.TextField(blank=True)),
                ("status", models.CharField(choices=[("draft", "Draft"), ("submitted", "Submitted")], default="submitted", max_length=12)),
                ("submitted_at", models.DateTimeField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("evaluator", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="evaluations_created", to=settings.AUTH_USER_MODEL)),
                ("staff", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="evaluations", to="evaluations.staffmember")),
            ],
            options={"ordering": ["-evaluation_date", "-created_at"]},
        ),
        migrations.CreateModel(
            name="FinalEvaluationReview",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("academic_year", models.CharField(max_length=40)),
                ("strengths", models.TextField(blank=True)),
                ("improvements", models.TextField(blank=True)),
                ("final_comment", models.TextField(blank=True)),
                ("reviewed_at", models.DateTimeField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("reviewed_by", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="final_evaluation_reviews", to=settings.AUTH_USER_MODEL)),
                ("staff", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="final_reviews", to="evaluations.staffmember")),
            ],
            options={"ordering": ["-academic_year", "staff__name"], "unique_together": {("staff", "academic_year")}},
        ),
        migrations.AddIndex(model_name="evaluationrecord", index=models.Index(fields=["form_type", "academic_year"], name="eval_form_year_idx")),
        migrations.AddIndex(model_name="evaluationrecord", index=models.Index(fields=["staff", "form_type"], name="eval_staff_form_idx")),
        migrations.AddIndex(model_name="evaluationrecord", index=models.Index(fields=["status", "evaluation_date"], name="eval_status_date_idx")),
    ]
