
from django import forms

from .models import (
    EvaluationCycle,
    EvaluationQuestion,
    EvaluationResponse,
    EvaluationSubmission,
    StaffMember,
)


class EvaluationSubmissionForm(forms.Form):
    staff_member = forms.ModelChoiceField(
        queryset=StaffMember.objects.none(),
        label="Staff member to evaluate",
    )
    cycle = forms.ModelChoiceField(
        queryset=EvaluationCycle.objects.none(),
        label="Evaluation cycle",
    )
    strengths = forms.CharField(
        label="Strengths",
        widget=forms.Textarea(attrs={"rows": 3}),
        required=False,
    )
    improvement_points = forms.CharField(
        label="Points to improve",
        widget=forms.Textarea(attrs={"rows": 3}),
        required=False,
    )
    def __init__(self, *args, evaluator_type=None, user_id=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.evaluator_type = evaluator_type
        self.user_id = user_id

        self.fields["staff_member"].queryset = (
            StaffMember.objects.filter(
                is_active=True,
staff_type=StaffMember.StaffType.ACADEMIC,
            ).select_related("user")
        )

        self.fields["cycle"].queryset = EvaluationCycle.objects.filter(
            is_open=True,
            evaluation_type=EvaluationCycle.EvaluationType.ACADEMIC,
        )

        
        form_type_map = {
            "STUDENT": "STUDENT",
            "HOD": "HOD",
            "PEER": "PEER",
            "SELF": "SELF",
        }

        if evaluator_type == EvaluationSubmission.EvaluatorType.SUPERVISOR:
            selected_form_type = "ADMINISTRATIVE"
        else:
            selected_form_type = form_type_map.get(evaluator_type)

        if selected_form_type is None:
            self.questions = []
        else:
            self.questions = list(
                EvaluationQuestion.objects.filter(
                    evaluation_type=EvaluationQuestion.EvaluationType.ACADEMIC,
                    form_type=selected_form_type,
                    is_active=True,
                ).order_by("section", "order", "id")
            )


        self.questions = list(form_type_map)

        rating_choices = [
            ("5", "5 — Excellent"),
            ("4", "4 — Very Good"),
            ("3", "3 — Good"),
            ("2", "2 — Fair"),
            ("1", "1 — Poor"),
            ("0", "0 — Not demonstrated"),
            ("NA", "Not applicable"),
        ]

        for question in self.questions:
            self.fields[f"question_{question.pk}"] = forms.ChoiceField(
                label=f"{question.section}: {question.question_text}",
                choices=rating_choices,
                widget=forms.RadioSelect,
                required=True,
            )

    def clean(self):
        cleaned_data = super().clean()

        staff_member = cleaned_data.get("staff_member")
        cycle = cleaned_data.get("cycle")

        if (
            staff_member
            and cycle
            and self.evaluator_type == EvaluationSubmission.EvaluatorType.SELF
            and staff_member.user_id != getattr(self, "user_id", None)
        ):
            raise forms.ValidationError(
                "Self-evaluation must be submitted for your own staff record."
            )

        return cleaned_data

    def save_submission(self, *, evaluator):
        if not self.is_valid():
            raise ValueError("Validate the form before saving.")

        staff_member = self.cleaned_data["staff_member"]
        cycle = self.cleaned_data["cycle"]

        if not cycle.is_valid_period:
            raise forms.ValidationError(
                "The evaluation cycle has an invalid date range."
            )

        submission = EvaluationSubmission.objects.create(
            cycle=cycle,
            staff_member=staff_member,
            evaluator=evaluator,
            evaluator_type=self.evaluator_type,
            status=EvaluationSubmission.Status.SUBMITTED,
            strengths=self.cleaned_data["strengths"],
            improvement_points=self.cleaned_data["improvement_points"],
        )

        responses = []

        for question in self.questions:
            answer = self.cleaned_data[f"question_{question.pk}"]

            if answer == "NA":
                responses.append(
                    EvaluationResponse(
                        submission=submission,
                        question=question,
                        score=None,
                        not_applicable=True,
                    )
                )
            else:
                responses.append(
                    EvaluationResponse(
                        submission=submission,
                        question=question,
                        score=int(answer),
                        not_applicable=False,
                    )
                )

        EvaluationResponse.objects.bulk_create(responses)

        return submission
