from decimal import Decimal
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils import timezone
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
        self.staff = StaffMember.objects.create(employee_id="TEST-01", name="Test Instructor", linked_user=self.instructor)

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
