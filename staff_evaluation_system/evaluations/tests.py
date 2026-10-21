from decimal import Decimal
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.urls import reverse
from .models import StaffMember, EvaluationRecord, AdministrativeEvaluation, UserProfile
from .scoring import average_rating, weighted_score


class ScoringTests(TestCase):
    def test_n_a_is_excluded_and_zero_is_counted(self):
        self.assertEqual(average_rating({"a": "5", "b": "0", "c": "NA"}), Decimal("2.50"))

    def test_weighted_student_result_is_out_of_40(self):
        self.assertEqual(weighted_score("student", {"a": "5", "b": "5"}), Decimal("40.00"))

    def test_weighted_self_result_is_out_of_10(self):
        self.assertEqual(weighted_score("self", {"a": "4"}), Decimal("8.00"))


class EvaluationWorkflowTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.head = User.objects.create_user(username="head", password="StrongPass123!")
        self.instructor = User.objects.create_user(username="instructor", password="StrongPass123!")
        UserProfile.objects.filter(user=self.head).update(role="department_head")
        UserProfile.objects.filter(user=self.head).update(department="Department of Mathematics")
        self.staff = StaffMember.objects.create(
            employee_id="TEST-01", name="Test Instructor",
            linked_user=self.instructor,
            department="Department of Mathematics", college="Ambo University"
        )

    def test_submitted_student_evaluation_stores_average(self):
        record = EvaluationRecord.objects.create(
            form_type="student", staff=self.staff, evaluator=self.head,
            evaluation_date=timezone.localdate(), ratings={"item1": "4", "item2": "5", "item3": "NA"},
            average_score=average_rating({"item1": "4", "item2": "5", "item3": "NA"}),
        )
        self.assertEqual(record.average_score, Decimal("4.50"))
        self.assertEqual(record.weighted_score, Decimal("36.00"))

    def test_admin_total_sums_to_maximum_100(self):
        record = AdministrativeEvaluation.objects.create(
            staff=self.staff, evaluator=self.head,
            period_start=timezone.localdate().replace(month=1, day=1),
            period_end=timezone.localdate(), plan_execution_score=Decimal("70"),
            employee_score=Decimal("5"), team_score=Decimal("15"), supervisor_score=Decimal("10"),
        )
        self.assertEqual(record.total_score, Decimal("100.00"))

    def test_admin_total_is_capped_by_form_fields_not_computed_property(self):
        record = AdministrativeEvaluation(
            staff=self.staff, evaluator=self.head,
            period_start=timezone.localdate(), period_end=timezone.localdate(),
            plan_execution_score=Decimal("70"), employee_score=Decimal("5"),
            team_score=Decimal("15"), supervisor_score=Decimal("10"),
        )
        self.assertEqual(record.total_score, Decimal("100.00"))

    # --- Update tests ---

    def test_can_update_student_evaluation(self):
        record = EvaluationRecord.objects.create(
            form_type="student", staff=self.staff, evaluator=self.head,
            evaluation_date=timezone.localdate(), ratings={"item1": "4", "item2": "5"},
            average_score=average_rating({"item1": "4", "item2": "5"}),
        )
        self.client.login(username="head", password="StrongPass123!")
        updated_ratings = {"item1": "5", "item2": "4"}
        url = reverse("evaluation_update", args=[record.pk])
        response = self.client.post(
            url,
            {
                "staff_id": self.staff.pk,
                "evaluation_date": "2024-03-15",
                "course_title": "Updated Course",
                "course_code": "UPD 101",
                "academic_year": "2024 E.C.",
                "batch": "1",
                "semester": "I",
                "period_start": "2024-01-01",
                "period_end": "2024-03-15",
                "strengths": "Updated strengths",
                "improvements": "Updated improvements",
                **{f"rating_{k}": v for k, v in updated_ratings.items()},
            },
        )
        self.assertRedirects(response, reverse("evaluation_detail", args=[record.pk]))
        record.refresh_from_db()
        self.assertEqual(record.average_score, average_rating(updated_ratings))
        self.assertEqual(record.course_title, "Updated Course")
        self.assertEqual(len(record.ratings), 2)

    def test_can_update_administrative_evaluation(self):
        record = AdministrativeEvaluation.objects.create(
            staff=self.staff, evaluator=self.head,
            period_start=timezone.localdate().replace(month=1, day=1),
            period_end=timezone.localdate().replace(month=6, day=30),
            plan_execution_score=Decimal("35"), employee_score=Decimal("3"),
            team_score=Decimal("10"), supervisor_score=Decimal("8"),
            plan_title="Original Plan",
        )
        self.client.login(username="head", password="StrongPass123!")
        url = reverse("administrative_update", args=[record.pk])
        response = self.client.post(
            url,
            {
                "staff": self.staff.pk,
                "period_start": "2024-01-01",
                "period_end": "2024-06-30",
                "plan_title": "Updated Plan",
                "planned_outcomes": "New outcomes",
                "actual_achievements": "Actual results",
                "plan_execution_score": "50",
                "employee_score": "4",
                "team_score": "12",
                "supervisor_score": "9",
                "performance_level": "good",
                "strengths": "Updated strengths",
                "improvement_gaps": "Need more group work",
                "supervisor_name": "Head Director",
                "supervisor_signature": "HD",
                "supervisor_date": "2024-06-15",
                "employee_agreed": "on",
                "disagreement_reason": "",
                "employee_signature": "Employee",
                "employee_date": "2024-06-20",
            },
        )
        self.assertRedirects(response, reverse("administrative_detail", args=[record.pk]))
        record.refresh_from_db()
        self.assertEqual(record.plan_execution_score, Decimal("50"))
        self.assertEqual(record.total_score, Decimal("75.00"))
        self.assertEqual(record.plan_title, "Updated Plan")

    def test_update_does_not_create_duplicate(self):
        record = EvaluationRecord.objects.create(
            form_type="student", staff=self.staff, evaluator=self.head,
            evaluation_date=timezone.localdate(), ratings={"item1": "4"},
            average_score=average_rating({"item1": "4"}),
        )
        self.client.login(username="head", password="StrongPass123!")
        url = reverse("evaluation_update", args=[record.pk])
        self.client.post(
            url,
            {
                "staff_id": self.staff.pk,
                "evaluation_date": "2024-03-15",
                "course_title": "Updated",
                "course_code": "UPD 101",
                "academic_year": "2024 E.C.",
                "batch": "1",
                "semester": "I",
                "period_start": "2024-01-01",
                "period_end": "2024-03-15",
                "strengths": "Strengths",
                "improvements": "Improvements",
                **{f"rating_{k}": "5" for k in ["instructional_skills__1", "professional_ethics__1"]},
            },
        )
        self.assertEqual(EvaluationRecord.objects.filter(pk=record.pk).count(), 1)
        record.refresh_from_db()
        self.assertEqual(record.course_title, "Updated")

    def test_unauthorized_user_cannot_update_evaluation(self):
        record = EvaluationRecord.objects.create(
            form_type="student", staff=self.staff, evaluator=self.head,
            evaluation_date=timezone.localdate(), ratings={"item1": "4"},
            average_score=average_rating({"item1": "4"}),
        )
        self.client.login(username="instructor", password="StrongPass123!")
        url = reverse("evaluation_update", args=[record.pk])
        response = self.client.post(
            url,
            {
                "staff_id": self.staff.pk,
                "evaluation_date": "2024-03-15",
                "course_title": "Unauthorized",
                "course_code": "UNAUTH 101",
                "academic_year": "2024 E.C.",
                "batch": "1",
                "semester": "I",
                "period_start": "2024-01-01",
                "period_end": "2024-03-15",
                "strengths": "Strengths",
                "improvements": "Improvements",
                **{f"rating_{k}": "5" for k in ["instructional_skills__1", "professional_ethics__1"]},
            },
        )
        self.assertEqual(response.status_code, 404)
        record.refresh_from_db()
        self.assertEqual(record.course_title, "")

    def test_unauthorized_user_cannot_update_administrative(self):
        record = AdministrativeEvaluation.objects.create(
            staff=self.staff, evaluator=self.head,
            period_start=timezone.localdate().replace(month=1, day=1),
            period_end=timezone.localdate().replace(month=6, day=30),
            plan_execution_score=Decimal("35"), employee_score=Decimal("3"),
            team_score=Decimal("10"), supervisor_score=Decimal("8"),
            plan_title="Original Plan",
        )
        self.client.login(username="instructor", password="StrongPass123!")
        url = reverse("administrative_update", args=[record.pk])
        response = self.client.post(
            url,
            {
                "staff": self.staff.pk,
                "period_start": "2024-01-01",
                "period_end": "2024-06-30",
                "plan_title": "Unauthorized",
                "plan_execution_score": "50",
                "employee_score": "4",
                "team_score": "12",
                "supervisor_score": "9",
            },
        )
        self.assertEqual(response.status_code, 404)
        record.refresh_from_db()
        self.assertEqual(record.plan_title, "Original Plan")
