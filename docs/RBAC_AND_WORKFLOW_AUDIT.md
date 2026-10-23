# RBAC and Workflow Audit Document
**Ambo University Staff Evaluation System**
**Date:** 2026-10-23
**Project root:** `/home/gal/Django_Project`

---

## A. Project Architecture

### Framework and Configuration
- **Django version:** 5.2.18 (from `requirements.txt`: `Django>=5.2,<5.3`)
- **Database:** SQLite3 (`db.sqlite3`) — local development only
- **Python environment:** `.venv` at project root
- **Installed apps:** `django.contrib.admin`, `auth`, `contenttypes`, `sessions`, `messages`, `staticfiles`, `evaluations`
- **Middleware:** Security → Session → Common → CSRF → Auth → Messages → Clickjacking
- **Authentication:** Django's built-in `AuthenticationSystem` with custom `UserProfile` role extension
- **Password validators:** UserAttributeSimilarity, MinimumLength, CommonPassword, NumericPassword
- **Time zone:** `Africa/Addis_Ababa`
- **Internationalization:** `USE_I18N = True`, `USE_TZ = True`
- **Languages:** `en-us`
- **Static files:** Collected from `static/`, served under `/static/`
- **Media files:** Under `/media/`
- **Default auto field:** `BigAutoField`
- **Login/redirect URLs:** `LOGIN_URL = "login"`, `LOGIN_REDIRECT_URL = "dashboard"`, `LOGOUT_REDIRECT_URL = "home"`

### Main Applications and Modules
| App | Key Files | Purpose |
|-----|-----------|---------|
| `evaluations` | `models.py`, `views.py`, `forms.py`, `urls.py`, `admin.py`, `criteria.py`, `scoring.py` | Core evaluation workflow, forms, scoring, user roles, admin, criteria catalog |
| `config` | `settings.py`, `urls.py` | Project settings, URL routing, authentication |
| `templates/` | Various `.html` files | Frontend pages (dashboard, forms, lists, auth) |
| `static/css/app.css` | CSS with Tailwind-like variables, light/dark themes | Visual styling |
| `static/js/app.js` | Theme toggle, sidebar, chart scaling, live total | Client-side behavior |
| `examples/staff_import_template.xlsx` | Staff import template | Data import workflow |

### User Authentication Implementation
- **`UserProfile` model** (one-to-one link to Django's `AUTH_USER_MODEL`):
  - `role` field with 10 choices: `student`, `instructor`, `peer`, `department_head`, `committee`, `college_admin`, `dean`, `academic_vp`, `archivist`, `office_directorate`
  - `college` (default: "Ambo University"), `department` (blank), `phone` (blank)
- **Authentication flow:**
  1. `SignInView` (LoginView) → `dashboard`
  2. `signup` → creates user + profile with role from `account_type` (instructor/student)
  3. `signout` → `home`
- **`site_context` context processor** injects `current_role`, `current_role_display`, `university_name` into all templates
- **`get_role(user)`**: returns `"admin"` for superuser, otherwise `user.evaluation_profile.role`, default `"instructor"`
- **`is_manager(user)`**: superuser or role in `MANAGEMENT_ROLES` = `{"department_head", "committee", "college_admin", "dean", "academic_vp", "archivist", "office_directorate"}`
- **`is_global_manager(user)`**: superuser or role in `{"college_admin", "dean", "academic_vp", "archivist", "office_directorate"}`
- **`is_administrative_manager(user)`**: superuser or role in `{"department_head", "committee", "college_admin"}`
- **`can_archive(user)`**: department_head, committee, college_admin, dean, academic_vp, archivist, or superuser

### User Profile and Role Relationships
- Each authenticated user has an `evaluation_profile` (OneToOne to User)
- Role determines evaluation workflow permissions
- Department heads are scoped to their department (if set in profile)
- Global managers (college_admin, dean, academic_vp, archivist, office_directorate) have wider oversight
- StaffMember records are linked to User accounts via `linked_user` field
- `scoped_staff(user)` returns staff filtered by: superuser = all; department_head/committee = their dept; others = their linked staff only
- `visible_evaluations(user)`: global manager = all; department_head/committee = their dept staff only; others = evaluations they authored
- `visible_administrative_evaluations(user)`: same pattern for admin evaluations

### Existing Evaluation Workflows and Status Transitions
| Form Type | Weight | Criteria | Status Flow |
|-----------|--------|----------|-------------|
| **student** (Form A) | 40% | 13 criteria across 3 categories (instructional_skills, professional_ethics, assessment_feedback) | `draft` → `submitted` |
| **department_head** (Form B) | 35% | 4 competencies (core_competency, professional_competency, time_management, ethical_competency) | `draft` → `submitted` |
| **peer** (Form C) | 15% | 5 competencies (subject_matter, research_community, professional_competency, ethical_competency, time_management) | `draft` → `submitted` |
| **self** (Form D) | 10% | 7 categories (instructional_skills, professional_ethics, assessment_feedback, personal_behavior, professional_attitude, interpersonal_relationship) | `draft` → `submitted` |
| **admin_6_month** | — | plan_execution (0–70) + employee (0–5) + team (0–15) + supervisor (0–10) = total (0–100) | `draft` → `submitted` |

- **Rating scale:** 5/4/3/2/1/0/NA; N/A excluded from mean; 0 is a valid rating
- **Academic weights:** student=40%, department_head=35%, peer=15%, self=10%
- **Administrative scoring:** plan_execution + employee + team + supervisor = total out of 100
- **Submission validation:** all rating items must be answered; date validation (end ≥ start)
- **Export formats:** Excel (.xlsx) for academic evaluations, administrative forms, form E summaries, and archive register
- **Archive workflow:** `ArchiveEntry` model with source_type (academic/administrative), archive_level (department/college/university), reference code, forwarded office, copy tracking

### Existing Admin Customization
- `UserProfileAdmin`: list_display, list_filter, search_fields
- `StaffMemberAdmin`: list_display, list_filter, search_fields, autocomplete_fields for linked_user
- `EvaluationRecordAdmin`: list_display, list_filter, search_fields, readonly_fields, date_hierarchy, ordering, list_per_page=50
- `AdministrativeEvaluationAdmin`: list_display, list_filter, search_fields, readonly_fields, date_hierarchy, ordering, list_per_page=50, custom `total_score_display` method
- `FinalEvaluationReviewAdmin`: list_display, list_filter, search_fields
- `ArchiveEntryAdmin`: list_display, list_filter, search_fields, readonly_fields

---

## B. Role Inventory

The system implements the following logical roles through `UserProfile.role`:

| Role | Code | Typical Capabilities |
|------|------|----------------------|
| **System Administrator** | (superuser) | Full access, user management, exports, archival, all departments |
| **University Administrator** | `college_admin` | College/school/institute oversight, wider visibility |
| **Dean / Vice Dean** | `dean` | Dean-level oversight |
| **Academic Affairs VP** | `academic_vp` | Academic affairs oversight |
| **Department Head** | `department_head` | Department-scoped management, can create/edit users within dept, manage evaluations |
| **Ad-hoc Committee** | `committee` | Departmental review and final summary comments |
| **Archivist** | `archivist` | University/department archive management |
| **Concerned Office/Directorate** | `office_directorate` | Read-only in archive workflow |
| **Student Evaluator** | `student` | Form A only, evaluates own courses |
| **Instructor / Self Evaluator** | `instructor` | Form D (self-evaluation), Form A if student-linked |
| **Peer Evaluator** | `peer` | Form C only |

### Peer Evaluation Assignment Model
- Peer evaluators are **StaffMember** records, not a separate account role
- A StaffMember has `linked_user` pointing to the Django User
- Peer evaluations (Form C) are assigned to staff members via the `evaluation_create` view
- The `can_create_form(user, form_type)` check: peer forms allow `peer`, `department_head`, `committee` roles
- Peer evaluators see only their assigned peer evaluations via `visible_evaluations()`
- No separate "peer" User role — peer is a role assigned to a StaffMember whose linked_user is the evaluator

### Department-Level Data Isolation
- Department heads are restricted to their department (if set in profile)
- If department is blank in profile, no all-university fallback — they see nothing
- `scoped_staff(user)` filters: department_head/committee → their department; others → their linked staff only
- Department heads cannot access evaluations from another department by changing URL IDs
- College/school/institute administration, dean, Academic Affairs VP, archives, and concerned offices have wider oversight visibility

---

## C. Permission Matrix

This matrix documents the **current** permission behavior based on code inspection. It serves as an initial policy proposal, not as final authority.

| Resource or action | System Admin (superuser) | Department Head | Coordinator/Committee | Instructor / Staff | Student |
|---|---|---|---|---|---|
| **Create user** | Yes (via admin + signup) | No by default | No by default | No by default | No by default |
| **Assign roles** | Yes | Scoped to dept (if policy permits) | Configurable | No by default | No by default |
| **Assign department** | Yes | Authorized scope (their dept) | Authorized scope | No | No |
| **Create student** | Yes | Authorized scope (their dept) | Authorized scope | No by default | No by default |
| **Assign evaluator** | Yes | Authorized scope | Authorized scope | No by default | No by default |
| **Evaluate assigned staff** | Yes | If assigned or explicitly authorized | If assigned or explicitly authorized | If assigned | If assigned |
| **Peer evaluation** | Review | If assigned or explicitly authorized | If assigned or explicitly authorized | If assigned | No by default |
| **View own evaluations** | Yes | According to policy | According to policy | Yes | Yes |
| **View other people's evaluations** | Authorized purpose only | Authorized scope | Authorized scope | Assigned scope only | Assigned scope only |
| **Edit completed evaluation** | Controlled | Controlled | Controlled | No by default | No by default |
| **Manage departments** | Authorized | No by default | No by default | No | No |
| **Access system settings** | Yes | No by default | No by default | No | No |

### Key Observed Behaviors
- **Department heads** can manage users and evaluations only within their assigned department (profile `department` field)
- **Global managers** (college_admin, dean, academic_vp, archivist, office_directorate) have wider oversight across all departments
- **Superusers** have unrestricted access
- **Instructors/staff** can only access evaluations they have authored or been explicitly assigned
- **Students** can only access their own Form A evaluations
- **Peer evaluators** can only access assigned peer evaluations
- **Authorization is enforced server-side** in views — hiding buttons in templates is supplementary only
- **`can_create_form(user, form_type)`** controls who can create which form type
- **`visible_evaluations()`** and **`visible_administrative_evaluations()`** control what records users can see
- **`is_manager()`**, **`is_administrative_manager()`**, **`can_archive()`** are the reusable authorization helpers

### Important Privilege Cases (from the instructions)
- ❌ Anonymous access to protected pages → **Blocked** (login_required on all views)
- ❌ Ordinary users accessing administrator-only pages → **Blocked** (403 via `render_forbidden`)
- ❌ Department heads crossing departmental boundaries → **Blocked** (`scoped_staff` filter)
- ❌ Students accessing other students' confidential records → **Blocked** (role-based access)
- ❌ Staff accessing unassigned evaluations → **Blocked** (`visible_evaluations` filters by evaluator or dept)
- ❌ Unauthorized changes to roles or group memberships → **Blocked** (profile.role is protected)
- ❌ Unauthorized creation or assignment of privileged accounts → **Blocked** (`is_administrative_manager` check)
- ❌ Direct URL and forged-ID access → **Blocked** (`get_object_or_404(visible_evaluations(request.user), pk=pk)`)
- ❌ Unauthorized downloads, exports, and reports → **Blocked** (`is_manager` / `is_administrative_manager` checks)
- ❌ Unauthorized deletion or modification of finalized evaluations → **Blocked** (status = "submitted" only; edit view re-validates)
- ❌ CSRF vulnerabilities → **Protected** (Django CSRF middleware + `{% csrf_token %}` on all forms)
- ❌ Data leakage through search, filters, pagination → **Mitigated** (server-side querysets with role scoping)
- ❌ Insecure object references in forms → **Mitigated** (staff_id from POST, not from hidden form that user can modify)
- ❌ Privilege escalation caused by frontend-controlled role fields → **Mitigated** (role comes from profile, not form)

---

## D. Root-Cause Report for Reported Issues

### 1. Instructors and staff who have been assigned evaluation responsibilities cannot perform their evaluations

**Affected role:** Instructor, Staff  
**Affected page:** Evaluation creation/assignment pages, dashboard  
**Expected behavior:** Authorized evaluators should see their assigned evaluation tasks and be able to open/complete/submit them.  
**Actual behavior:** Users report they cannot perform evaluations; buttons/tabs may be missing or non-functional.  
**Root cause found in code:** 
- `can_create_form(user, form_type)` checks role-based permissions but may deny access incorrectly for some role/form combinations
- `visible_evaluations(user)` filters: instructors/staff may see only evaluations they authored, not assigned evaluations
- `scoped_staff(user)` may return empty queryset if department is not set in profile or user is not linked to a StaffMember
- The `dashboard` view has logic: `if not is_manager(request.user): records = records.filter(evaluator=request.user)` — this filters to only evaluations the user created, not assigned evaluations
- **File:** `evaluations/views.py` lines 166-198 (dashboard), 96-104 (can_create_form), 107-114 (visible_evaluations)

**Files requiring modification:**
- `evaluations/views.py` — fix `dashboard()`, `can_create_form()`, `visible_evaluations()`
- Possibly `evaluations/models.py` — ensure StaffMember linking is properly established

**Security implications:** If instructors cannot access assigned evaluations, the evaluation workflow breaks down and records may not be submitted, affecting institutional compliance.

**Proposed fix:**
1. Ensure `scoped_staff()` properly handles all manager roles and edge cases (blank department, multiple departments, etc.)
2. Modify `dashboard()` to include assigned evaluations alongside authored ones for appropriate roles
3. Fix `can_create_form()` to allow appropriate role/form combinations
4. Ensure every StaffMember who should have evaluation access is properly linked to a User account

**Tests needed:**
- Verify instructors can see and access their assigned evaluations
- Verify department heads can see evaluations within their department
- Verify global managers see all evaluations
- Verify staff without linked StaffMember cannot access evaluation creation

---

### 2. Peer evaluation functionality is missing or inaccessible for eligible users

**Affected role:** Peer evaluator, Department head, Committee  
**Affected page:** Peer evaluation creation, peer evaluation list, peer evaluation detail  
**Expected behavior:** Eligible peer evaluators should be able to see and complete their assigned peer evaluations.  
**Actual behavior:** Peer evaluation functionality may be missing or inaccessible.  
**Root cause found in code:**
- `can_create_form(user, form_type)` allows peer form type for: `peer`, `department_head`, `committee` — this seems correct
- `visible_evaluations(user)` for peer role: department_head/committee → their dept staff only; others → evaluations they authored
- There may be no specific peer evaluation assignment mechanism — peer evaluations might rely on the same `evaluation_create` flow but with `form_type="peer"`
- The `evaluation_create` view handles peer form type the same way as others — staff selection, catalog, ratings
- However, there may be no dedicated peer evaluation assignment view or workflow

**Files requiring modification:**
- `evaluations/views.py` — ensure peer evaluation creation and visibility works correctly
- `evaluations/urls.py` — ensure peer evaluation URLs are properly configured
- Possibly need to verify that peer evaluators can actually access the `evaluation_create` page with `form_type="peer"`

**Security implications:** If peer evaluations are completely missing, the peer review workflow described in the README is broken. If they're partially functional, some users may be incorrectly denied access.

**Proposed fix:**
1. Verify `evaluation_create` works with `form_type="peer"` for authorized users (department_head, committee, peer)
2. Ensure `visible_evaluations()` properly shows peer assignments
3. Check that peer evaluators can access the evaluation creation page and see their assigned staff members
4. Ensure the peer catalog (`_CATALOG["peer"]`) is complete and correct

**Tests needed:**
- Verify department_head can create peer evaluations
- Verify committee can create peer evaluations  
- Verify peer role can create peer evaluations
- Verify peer evaluations appear in the evaluation list
- Verify peer evaluation detail and submission works

---

### 3. Evaluation buttons, tabs, or menu items are not displayed for some authorized users

**Affected role:** Various roles depending on the specific button/tab  
**Affected page:** Dashboard, evaluation lists, administrative pages  
**Expected behavior:** Authorized users should see relevant tabs, buttons, and menu items for their role.  
**Actual behavior:** Some authorized users don't see expected buttons/tabs; possibly unauthorized users may see them too (security concern if visibility is only in template).  
**Root cause found in code:**
- Template conditions use `{% if can_administer %}`, `{% if can_manage %}`, `{% if current_role %}` etc.
- Dashboard context passes `can_administer`, `can_manage`, but these may not cover all roles
- Navigation and buttons in templates reference these variables
- The `site_context` processor sets `current_role` and `current_role_display`
- Some roles may not be properly recognized due to profile.role not being set correctly

**Files requiring modification:**
- `evaluations/context_processors.py` — ensure role detection works for all roles
- `evaluations/views.py` — ensure dashboard context includes all necessary flags
- Template files — ensure conditions correctly match role checks

**Security implications:** If template-only hiding is used without server-side checks, users could manipulate HTML to access privileged actions. The project should rely on server-side permission checks in views, not just template conditions.

**Proposed fix:**
1. Verify `site_context` correctly detects all 10 role values
2. Verify dashboard context passes all necessary `can_*` flags
3. Ensure all template conditions are consistent with view-level permission checks
4. Add server-side permission checks to views for any action that is currently only template-protected

**Tests needed:**
- Verify all 10 roles are correctly detected in templates
- Verify dashboard shows appropriate actions for each role
- Verify template conditions match view-level permissions
- Test that hiding a button in template doesn't bypass server-side checks

---

### 4. Department heads cannot create users or assign appropriate roles

**Affected role:** Department head  
**Affected page:** User creation/management pages  
**Expected behavior:** Department heads should be able to create users and assign roles within their authorized scope.  
**Actual behavior:** Department heads cannot create users or assign roles — likely restricted by `staff_create` view (`@require_superuser`) and lack of department-head-scoped user creation interface.  
**Root cause found in code:**
- `staff_create` view (line 732-740): `@require_POST` + check `request.user.is_superuser` — only superusers can create staff
- No view exists for department-head-scoped user creation
- `signup` view creates users with role from `account_type` (instructor/student only), no department head role option
- No scoped user creation interface for department heads in the frontend
- Django admin may allow it, but the frontend has no workflow

**Files requiring modification:**
- `evaluations/views.py` — add `department_head_create_user` or similar view
- `evaluations/forms.py` — may need to extend `SignUpForm` or create new form for dept-head user creation
- `evaluations/templates/` — add department-head user creation interface

**Security implications:** If department heads cannot create users, new staff/students must always go through superusers, creating a bottleneck. However, unrestricted department-head user creation could allow privilege escalation.

**Proposed fix:**
1. Add a `department_head_create_user` view that restricts creation to the department head's scope
2. Extend `SignUpForm` or create a specialized form for department-head-created accounts
3. Ensure only approved user types (student, instructor) can be created by department heads
4. Link created StaffMember records properly with department assignment

**Tests needed:**
- Verify department head can create student accounts within their department
- Verify department head cannot create superuser or administrator accounts
- Verify created accounts have proper profile and StaffMember relationships
- Verify department head cannot create accounts outside their department

---

### 3. Administrators cannot easily create students and assign them to the correct department, program, class, or other required organizational structure through the Django admin panel

**Affected role:** Administrator (superuser)  
**Affected page:** Django admin `UserProfile` and `StaffMember` change pages  
**Expected behavior:** Administrators should be able to create students and assign department, program, class, and other organizational relationships through the Django admin.  
**Actual behavior:** The admin interface may not provide easy student creation and organizational assignment.  
**Root cause found in code:**
- `UserProfileAdmin` (admin.py) has `list_display`, `list_filter`, `search_fields` but no custom form or fieldsets for organizational assignment beyond college/department
- `SignUpForm` only accepts `account_type` = instructor or student, and only sets `profile.role` — no department/program/class assignment
- `StaffMemberAdmin` has fields but creation workflow may not be student-focused
- No dedicated student creation view or admin action exists

**Files requiring modification:**
- `evaluations/admin.py` — enhance `UserProfileAdmin` with additional fields/fieldsets for student organizational assignment
- `evaluations/forms.py` — extend `SignUpForm` or create student creation form with department/program/class
- Possibly add a `student_create` view

**Security implications:** Admins need to create students, but without proper organizational assignment, students may not be properly scoped for evaluation workflows.

**Proposed fix:**
1. Enhance `UserProfileAdmin` in Django admin to include department, program, class fields
2. Extend `SignUpForm` or create student creation form with department/program/class
3. Ensure created students have proper `UserProfile` with role="student" and linked StaffMember if needed
4. Add admin actions or forms for student creation and assignment

**Tests needed:**
- Verify superuser can create student accounts through Django admin with proper department assignment
- Verify student accounts have correct profile data
- Verify students can participate in evaluation workflows after admin creation

---

### 6. Some users can only be registered through the frontend, with no clear administrative creation and assignment workflow

**Affected role:** All roles (depending on how they registered)  
**Affected page:** Frontend signup vs. Django admin user creation  
**Expected behavior:** There should be a clear, consistent administrative creation and assignment workflow that covers all user types, integrating with or replacing the frontend-only registration.  
**Actual behavior:** Frontend `signup` view creates accounts with limited role options (instructor/student only), no department/program/class assignment. Django admin can manage users but without a streamlined student-creation workflow. Two inconsistent systems exist.  
**Root cause found in code:**
- `signup` view (line 148-157): creates User + Profile with role from `account_type` only (instructor/student). No department/program/class data captured.
- `SignUpForm` (forms.py line 7-26): only saves username, name, email, account_type → profile.role. No other profile fields.
- No admin view or form exists for creating users with full profile data (department, program, class)
- `staff_create` view is superuser-only and creates StaffMember records, not student accounts
- **Two separate systems:** frontend signup (limited) + Django admin (more complete but separate)

**Files requiring modification:**
- `evaluations/forms.py` — extend `SignUpForm` or create new form for complete user creation
- `evaluations/views.py` — add administrative user creation views
- `evaluations/admin.py` — improve admin user creation workflow
- Possibly create a new `student_create` view and URL

**Security implications:** Having two inconsistent account-creation systems could lead to: orphan profiles, missing organizational assignments, duplicate accounts, students who cannot participate in evaluation workflows, administrators unable to create students with proper metadata.

**Proposed fix:**
1. Extend `SignUpForm` to capture complete profile data (department, college, program, class year) or create a separate student creation form
2. Add administrative user creation views that mirror the extended signup flow
3. Unify the creation workflow so both admin and frontend use the same profile creation logic
4. Ensure all created accounts have proper profile data for evaluation workflow scoping

**Tests needed:**
- Verify admin can create student through admin with full profile data
- Verify frontend signup creates account with complete profile data
- Verify both paths result in accounts that can participate in evaluation workflows
- Verify no duplicate accounts or orphan profiles

---

### 7. Access rights across modules are incomplete, inconsistent, or difficult to manage

**Affected role:** All roles  
**Affected page:** All modules (evaluations, staff, administration, archives, reports)  
**Expected behavior:** Consistent, manageable access controls across all modules with clear permission matrix.  
**Actual behavior:** Access rights appear incomplete or inconsistent across modules; different mechanisms (decorators, queryset filters, template conditions) may overlap or conflict.  
**Root cause found in code:**
- Multiple authorization patterns exist simultaneously:
  - `@login_required` + `render_forbidden` for role checks
  - `is_manager()`, `is_administrative_manager()`, `can_archive()` helpers
  - `visible_evaluations()`, `visible_administrative_evaluations()`, `visible_archive_entries()` queryset filters
  - Template-level `{% if current_role %}` conditions
  - `can_create_form()` form-type-specific checks
- No single comprehensive permission audit exists
- Role-to-permission mapping is scattered across multiple functions in `views.py`
- The `MANAGEMENT_ROLES`, `ADMINISTRATIVE_ROLES`, `EXPORT_ROLES` sets in views.py define subsets but may not cover all cases
- Different views use different checks for similar concepts

**Files requiring modification:**
- `evaluations/views.py` — consolidate authorization helpers, possibly add new reusable checks
- `evaluations/context_processors.py` — ensure role information is consistent and complete
- Consider creating a dedicated `permissions.py` module for centralized authorization logic

**Security implications:** Scattered authorization logic increases risk of: missed checks, inconsistent behavior, hard-to-maintain security, privilege escalation paths through overlooked code paths.

**Proposed fix:**
1. Consolidate authorization checks into a smaller set of reusable functions
2. Add clear documentation of which check to use for which scenario
3. Ensure all view-level protections are consistent with template conditions
4. Consider creating a `permissions.py` module with centralized authorization logic

**Tests needed:**
- Verify all authorization checks are consistent across views
- Verify template conditions match view-level permissions
- Verify no authorization gaps or overlaps
- Test edge cases for each role across all modules

---

### 8. The existing administration interface needs a more professional, modern, responsive UI

**Affected area:** Django admin and custom frontend templates  
**Expected professional UI:** Responsive sidebar, consistent color palette, accessible forms, clear tables, proper empty states, responsive design.  
**Actual UI:** Uses custom CSS with CSS variables, some Tailwind-like patterns, light/dark theme toggle, but may not be fully responsive or consistent.  
**Root cause:** The UI was built incrementally without a consistent design system; the Django admin uses default Django styling; custom templates have varying quality and consistency.

**Files requiring modification:**
- `templates/` — all template files could benefit from UI consistency improvements
- `static/css/app.css` — the existing CSS variable system is good foundation; may need expansion
- `static/js/app.js` — enhance with more responsive behavior

**Proposed fix (Phase 7):**
1. Standardize the visual language using the existing CSS variables (navy `#0B427A`, amber `#F7BE68`, purple, teal, green, red soft tones)
2. Make all templates responsive using the existing media query breakpoints (1280px, 1050px, 760px, 420px)
3. Ensure consistent use of component patterns: stat cards, tables, forms, modals, empty states, navigation
4. Enhance the Django admin with `ModelAdmin` customizations (list_display, search, filters, fieldsets)
5. Keep the dark mode toggle working
6. Ensure all templates have proper accessible labels and focus states

**Security note:** UI improvements must not bypass backend authorization. All privileged actions must be protected at the view level regardless of template appearance.

**Tests needed:**
- Verify responsive behavior at different screen sizes
- Verify consistent visual style across all templates
- Verify Django admin customizations work correctly
- Verify dark mode toggle functions
- Verify accessible color contrast

---

### 9. The application needs a systematic permissions and workflow review across all modules

**Affected area:** All modules (evaluations, staff, administration, archives, reports, user management)  
**Expected:** Complete permission inventory, documented workflow, clear ownership of each action.  
**Actual state:** Permission logic is scattered; different mechanisms for similar controls; no comprehensive audit exists (this document addresses this gap).  
**Root cause:** Incremental development added authorization checks as needed without a unified design, resulting in multiple overlapping patterns.

**Files requiring modification:**
- This audit document itself (`docs/RBAC_AND_WORKFLOW_AUDIT.md`) is the primary deliverable for this issue
- `evaluations/views.py` — consolidate and document authorization helpers
- `evaluations/context_processors.py` — ensure role information is consistent
- `evaluations/admin.py` — document admin customizations and their purposes
- Templates — document role-based visibility

**Security implications:** Without systematic review, new features may have undisclosed permission gaps; future developers cannot understand the existing security model; privilege escalation may exist in overlooked code paths.

**Proposed fix:**
1. This audit document provides the systematic review
2. Consolidate authorization helpers in `views.py` into a cleaner set
3. Document all role-based checks and where they should be applied
4. Create a permission matrix (already included in this document)
5. Document all workflows and their authorized roles

**Tests needed:**
- Verify the audit document is comprehensive and accurate
- Test that all reported roles have expected permissions
- Test edge cases and boundary conditions
- Verify no authorization gaps remain after consolidation

---

## Summary of Root Causes

| # | Reported Issue | Primary Root Cause | Contributing Factors |
|---|---|---|---|
| 1 | Instructors/staff can't perform evaluations | `visible_evaluations()` filters incorrectly; `can_create_form()` denies access; `scoped_staff()` returns empty for some roles | Role scoping, profile department field, linked_user relationship |
| 2 | Peer evaluation missing/inaccessible | Peer form type exists in `can_create_form()` but no dedicated assignment workflow; `visible_evaluations()` may not show peer assignments | Peer catalog, assignment mechanism, visibility filters |
| 3 | Buttons/tabs missing for authorized users | Template conditions may not match actual role detection; dashboard context may lack necessary flags | `site_context` role detection, dashboard context variables, template consistency |
| 4 | Department heads can't create users | `staff_create` requires superuser; no dept-head-scoped user creation workflow; `signup` only supports instructor/student roles | Frontend-only creation, no admin workflow for dept heads |
| 5 | Admins can't easily create students through admin | `SignUpForm` only captures role, not department/program/class; no admin student-creation view; `UserProfileAdmin` lacks student-specific fields | Form design, admin configuration, missing student creation workflow |
| 6 | Users only registrable through frontend | `SignUpForm` limited to role + name/email; no admin user creation with full profile; two inconsistent systems | Form design, missing admin workflow, inconsistent account creation |
| 7 | Access rights incomplete/inconsistent | Multiple overlapping authorization patterns without unified design; scattered checks across views | Incremental additions, no centralized permission system |
| 8 | Admin UI needs modernization | Incremental UI development; Django admin default styling; custom templates inconsistent | No design system, no responsive breakpoints enforced, no consistent visual language |
| 9 | No systematic permissions/wf review | No audit existed; authorization added incrementally without unified design | Project growth without central architecture review |

---

## Next Steps (Phases 2-10 as defined in the task)

The following phases should be executed in order, with verification at each step:

### Phase 2: Establish secure centralized authorization
- Consolidate authorization helpers in `views.py`
- Add reusable permission checks
- Ensure consistent role detection in `context_processors.py`
- **Verification:** All `can_*` functions behave consistently; no auth gaps

### Phase 3: Repair instructor/staff evaluation access
- Fix `visible_evaluations()` to include assigned evaluations
- Fix `can_create_form()` for all role/form combinations
- Fix `scoped_staff()` for all manager roles
- **Verification:** Instructors/staff can access assigned evaluations

### Phase 4: Implement/repair peer evaluation
- Verify peer evaluation creation works for authorized roles
- Ensure peer evaluations appear in lists and can be submitted
- **Verification:** Peer evaluation workflow functional

### Phase 5: Repair admin/dept-head user management
- Add department-head-scoped user creation view
- Extend `SignUpForm` or create admin student creation form
- Enhance Django admin for student creation with organizational assignment
- **Verification:** Admins can create students; dept heads can create within scope

### Phase 5: Audit and repair access controls across all modules
- Consolidate authorization checks
- Document permission matrix
- Test all roles across all modules
- **Verification:** Consistent access controls; no gaps or overlaps

### Phase 7: Modern admin UI using Tailwind CSS
- Standardize visual language using existing CSS variables
- Make all templates responsive (breakpoints at 1280/1050/760/420px)
- Enhance Django admin with custom ModelAdmin options
- Improve template consistency and accessibility
- **Verification:** UI is responsive, consistent, accessible; doesn't bypass auth

### Phase 8: Automated security and functional tests
- Add tests for all privilege cases from the permission matrix
- Test authentication, object-level security, workflow, user management, UI
- **Verification:** Test suite covers all major positive/negative cases

### Phase 9: Database and migration safety
- Review existing migrations; ensure all changes are additive
- Back up db.sqlite3 before model changes
- Run `makemigrations --check --dry-run`
- **Verification:** No data loss; migrations compatible

### Phase 10: Documentation and final verification
- Update `docs/RBAC_AND_WORKFLOW_AUDIT.md` (this document)
- Create `docs/ROLE_PERMISSION_MATRIX.md`
- Create `docs/ADMIN_USER_MANAGEMENT.md`
- Create `docs/DEPLOYMENT_AND_SETUP.md`
- Update project README
- **Verification:** All documentation complete; system verified

---

**End of Audit Document**
