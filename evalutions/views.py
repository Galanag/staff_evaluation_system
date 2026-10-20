from datetime import date
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import EvaluationCycle, EvaluationSubmission, StaffMember


@login_required
def dashboard(request):
    user = request.user

    try:
        profile = user.profile
        role = profile.role
    except Exception:
        profile = None
        role = "UNASSIGNED"

    context = {
        "profile": profile,
        "role": role,
        "staff_count": StaffMember.objects.filter(is_active=True).count(),
        "open_cycles": EvaluationCycle.objects.filter(is_open=True).count(),
        "submission_count": EvaluationSubmission.objects.count(),
        "my_submissions": EvaluationSubmission.objects.filter(
            evaluator=user
        ).select_related("cycle", "staff_member")[:10],
    }

    return render(request, "evaluations/dashboard.html", context)

# Create your views here.

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db import IntegrityError, transaction
from django.shortcuts import redirect, render

from .forms import EvaluationSubmissionForm
from .models import EvaluationSubmission
from .permessions import get_user_role


@login_required
def create_academic_evaluation(request):
    role = get_user_role(request.user)

    role_mapping = {
        "STUDENT": EvaluationSubmission.EvaluatorType.STUDENT,
        "HOD": EvaluationSubmission.EvaluatorType.DEPARTMENT_HEAD,
        "PEER": EvaluationSubmission.EvaluatorType.PEER,
        "ACADEMIC": EvaluationSubmission.EvaluatorType.SELF,
    }

    evaluator_type = role_mapping.get(role)

    if evaluator_type is None:
        raise PermissionDenied(
            "Your role is not authorized to submit academic evaluations."
        )

    if request.method == "POST":
        form = EvaluationSubmissionForm(
            request.POST,
            evaluator_type=evaluator_type,
            user_id=request.user.id,
        )

        if form.is_valid():
            staff_member = form.cleaned_data["staff_member"]
            cycle = form.cleaned_data["cycle"]

            if not cycle.start_date <= cycle.end_date:
                form.add_error("cycle", "Invalid evaluation cycle dates.")

            elif not cycle.start_date <= date.today() <= cycle.end_date:
                form.add_error(
                    "cycle",
                    "This evaluation cycle is not currently within its date range.",
                )

            elif (
                evaluator_type == EvaluationSubmission.EvaluatorType.SELF
                and staff_member.user_id != request.user.id
            ):
                form.add_error(
                    "staff_member",
                    "You can only evaluate your own staff record.",
                )

            else:
                try:
                    with transaction.atomic():
                        submission = form.save_submission(
                            evaluator=request.user
                        )
                    messages.success(
                        request,
                        "Your evaluation has been submitted successfully.",
                    )
                    return redirect("evaluations:dashboard")

                except IntegrityError:
                    form.add_error(
                        None,
                        "You have already submitted this evaluation for this cycle.",
                    )

    else:
        form = EvaluationSubmissionForm(
            evaluator_type=evaluator_type,
            user_id=request.user.id,
        )

    return render(
        request,
        "evaluations/evaluation_form.html",
        {
            "form": form,
            "evaluator_type": evaluator_type,
        },
    )

