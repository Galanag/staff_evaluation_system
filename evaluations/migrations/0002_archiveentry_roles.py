import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("evaluations", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]
    operations = [
        migrations.AlterField(
            model_name="userprofile",
            name="role",
            field=models.CharField(
                choices=[
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
                ],
                default="instructor",
                max_length=32,
            ),
        ),
        migrations.CreateModel(
            name="ArchiveEntry",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("source_type", models.CharField(choices=[("academic", "Academic evaluation"), ("administrative", "Six-month administrative evaluation")], max_length=20)),
                ("archive_level", models.CharField(choices=[("department", "Department archive"), ("college", "College / school / institute archive"), ("university", "University archive")], default="department", max_length=20)),
                ("reference_code", models.CharField(blank=True, max_length=100)),
                ("forwarded_to_office", models.CharField(default="University / Department Archives", max_length=180)),
                ("instructor_copy_sent", models.BooleanField(default=False)),
                ("department_copy_sent", models.BooleanField(default=False)),
                ("notes", models.TextField(blank=True)),
                ("archived_at", models.DateTimeField(auto_now_add=True)),
                ("academic_record", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name="archive_entries", to="evaluations.evaluationrecord")),
                ("administrative_record", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name="archive_entries", to="evaluations.administrativeevaluation")),
                ("archived_by", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="archive_entries_created", to=settings.AUTH_USER_MODEL)),
            ],
            options={"verbose_name": "Evaluation archive entry", "verbose_name_plural": "Evaluation archive entries", "ordering": ["-archived_at"]},
        ),
    ]
