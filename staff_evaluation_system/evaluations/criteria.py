"""Criterion catalog transcribed from the evaluation materials supplied by the user.

A criterion that was only named in Form E but whose detailed items were not present
in the supplied Form D excerpt is listed in SUMMARY_ONLY_CATEGORIES below; no new
criterion text has been invented for it.
"""

RATING_OPTIONS = [("5", "5"), ("4", "4"), ("3", "3"), ("2", "2"), ("1", "1"), ("0", "0"), ("NA", "N/A")]
WEIGHTS = {"student": 40, "department_head": 35, "peer": 15, "self": 10}
FORM_TITLES = {
    "student": "Form A · Student evaluation",
    "department_head": "Form B · Department head evaluation",
    "peer": "Form C · Peer evaluation",
    "self": "Form D · Self-evaluation",
    "admin_6_month": "Six-month administrative evaluation",
}
SUMMARY_ONLY_CATEGORIES = ["Performing non-instructional duties"]

_CATALOG = {
    "student": [
        ("instructional_skills", "Instructional Skills", [
            "Presents the course objective clearly.",
            "Specifies the activities to be done during the lesson clearly.",
            "Explains the content of each units/chapters clearly.",
            "Covers the course content according to time table given.",
            "Presents the course clearly using the language of instruction.",
            "Responds students’ question positively.",
            "Links the lesson clearly to the previous and future lessons.",
            "Adapt knowledge to the level of the learners.",
            "Makes students active participant during teaching and learning.",
            "Tries to support students’ attempt in solving problems.",
            "Gives time for students during lessons.",
            "Use a variety of teaching techniques to accommodate different student learning styles.",
            "Make the class thought provoking and interesting.",
            "Gives make up classes properly if classes are missed.",
            "Gives tutorial classes properly when assigned.",
        ]),
        ("professional_ethics", "Professional Ethics and Attitude Towards Students", [
            "Begins and ends class on time.",
            "Make effective use of class time (time on task).",
            "Gives consultation service for students in arranged hours.",
            "Show genuine concern for student’s learning/problems.",
            "Encourages students to freely express feelings/opinion/ideas in classes.",
            "Encourages students’ peer/cooperative learning.",
            "Acts in a professionally acceptable manner.",
            "Able to handle classroom atmosphere conducive.",
        ]),
        ("assessment_feedback", "Assessment Methods & Feedback", [
            "Checks if students have understood the topic.",
            "Assesses students’ learning with various techniques.",
            "Shows timely students results in every assessment.",
            "Gives subsequent feedback on time.",
            "Constructs tests that represent the course content.",
            "Allots appropriate time to complete exams.",
            "Assesses student performance continually to improve instruction.",
        ]),
    ],
    "department_head": [
        ("core_competency", "Core Competency", [
            "Efforts of self development in his/her specialization.",
            "Adequacy of subject matter knowledge.",
            "Willingness to accept additional teaching assignments when compelling situation arises in the department.",
            "Willingness to accept related assignments other than regular teaching in the department (mentorship…).",
            "Effectiveness as a mentor in educational development army, internship etc.",
            "Active participation in improvement of teaching-learning process.",
            "Participation in community service affairs.",
            "Participating actively in seminars/workshop/symposia.",
            "Identifying priority areas in one’s discipline and pursuing research in that area.",
            "Participation in research project and project proposal development.",
            "Performance as an academic advisor.",
        ]),
        ("professional_competency", "Professional Competency", [
            "Participation in problem identification and solving at department/college/institution.",
            "Continuous assessment implementation.",
            "Participating actively in departmental/College/institution affairs.",
            "Providing and reporting tutorial activities designed for the students.",
            "Participation in preparation and reviewing of teaching materials.",
            "Updating teaching materials.",
            "Willingness to share University resources with other colleagues.",
        ]),
        ("time_management", "Time Management", [
            "Executing assigned classes/invigilation on time.",
            "Notifying and implementing consultation timely.",
            "Giving timely feedback to students.",
            "Meeting deadlines (in reporting, SIMS result feeding, submission of grade/documents, etc.).",
        ]),
        ("ethical_competency", "Ethical Competence", [
            "Having positive attitude to work with others.",
            "Showing concern for the use of resources of the department and the University.",
            "Willingness and participation in committee works at department/University level.",
            "Willingness to take assignments outside the University in his area of specialization.",
            "His/her professional ethics (dressing, hair style, personality…).",
        ]),
    ],
    "peer": [
        ("subject_matter", "Subject Matter Competency", [
            "Contribution in preparing and searching for teaching materials.",
            "Continuous update of the subject matter.",
            "Attending seminars organized by the department/college/school/institute.",
            "Level of his/her subject matter knowledge and skill.",
        ]),
        ("research_community", "Research and Community Services", [
            "Willingness and level of engagement in community service activities.",
            "Participation on seminars/workshops at department/college/school/institute level during the year.",
            "Identifying priority areas in one’s discipline and pursuing research in that area.",
            "Willingness to prepare research projects with other colleagues.",
            "Willingness to help colleagues in identifying areas of research and proposal development.",
        ]),
        ("professional_competency", "Professional Competency", [
            "Guidance and counseling role to students.",
            "Contributing ideas and activities that improve the teaching-learning process.",
            "Participation in problem identification and solving at department/college/institution.",
            "Willingness and preparedness to implement change tools.",
            "Willing to actively participate in 1-5 grouping (Education development army) activities.",
            "Implementation of different teaching methods in his/her discipline.",
            "Properly invigilate exams and tests to ensure academic integrity.",
        ]),
        ("ethical_competency", "Ethical Competence", [
            "Willingness to participate and level of commitment in committee works.",
            "Participating actively in departmental/college/institute meetings.",
            "Willingness to share university resources with other colleagues.",
            "Showing cordiality to others.",
            "Having positive attitude to work with others.",
            "Respecting ideas of others.",
            "Level of respect to rules and guidelines of the institution.",
            "His/her discipline (dressing, addictions, personality etc.).",
        ]),
        ("time_management", "Time Management", [
            "Time management in department affairs.",
            "Time utilization for consultation hours.",
        ]),
    ],
    "self": [
        ("instructional_skills", "Instructional Skills", [
            "Presents the course objective clearly.",
            "Specifies the activities to be done during the lesson clearly.",
            "Explains the content of each units/chapters clearly.",
            "Covers the course content according to time table given.",
            "Presents the course clearly using the language of instruction.",
            "Responds students’ question positively.",
            "Links the lesson clearly to the previous and future lessons.",
            "Adapt knowledge to the level of the learners.",
            "Makes students active participant during teaching and learning.",
            "Tries to support students’ attempt in solving problems.",
            "Gives time for students during lessons.",
            "Use a variety of teaching techniques to accommodate different student learning styles.",
            "Make the class thought provoking and interesting.",
            "Gives make up classes properly if classes are missed.",
            "Gives tutorial classes properly when assigned.",
        ]),
        ("professional_ethics", "Professional Ethics and Attitude Towards Students", [
            "Begins and ends class on time.",
            "Make effective use of class time (time on task).",
            "Gives consultation service for students in arranged hours.",
            "Show genuine concern for student’s learning/problems.",
            "Encourages students to freely express feelings/opinion/ideas in classes.",
            "Encourages students’ peer/cooperative learning.",
            "Acts in a professionally acceptable manner.",
            "Able to handle classroom atmosphere conducive.",
        ]),
        ("assessment_feedback", "Assessment Methods & Feedback", [
            "Provides students with appropriate assignments.",
            "Checks if students have understood the topic.",
            "Assesses students’ learning with various techniques.",
            "Shows timely students results in every assessment.",
            "Gives subsequent feedback on time.",
            "Constructs tests that represent the course content.",
            "Allots appropriate time to complete exams.",
            "Assesses student performance continually to improve instruction.",
            "Using continuous assessment during instruction.",
        ]),
        ("personal_behavior", "Overall Personal Behavior", [
            "Offer appropriate respect for his/her colleagues and heads.",
            "Keeps dignity of his/her job and professional ethics.",
            "Free from alcohol and any drug addiction.",
            "Arrives on time for appointments/meetings with colleagues for institutional activities.",
            "Role model for students and surrounding society.",
            "Take appropriate care for materials borrowed from the institution for teaching-learning process.",
            "Free from considering others’ work or findings as if it is his/her own.",
            "Raise his/her complaints in the right way to the appropriate body.",
            "Propose ideas on how teaching-learning activities could be improved in the department.",
        ]),
        ("professional_attitude", "Professional Attitude", [
            "Attending in professional meetings and seminars.",
            "Participates in activities to improve personal knowledge.",
            "Participates in solving the problem arising in the department.",
            "Engage Professional researches in his/her field.",
            "Lets the concerned college community know the outcome of his/her research.",
            "Gets him/her self ready to share his/her knowledge and experience to colleagues.",
            "Accept constructive comments of evaluation and attempts to put them into practice for improvement.",
            "Show willingness to help less experienced colleagues in identifying areas of research and developing proposals.",
            "Perform additional mandates/responsibilities given to him/her.",
            "Participate in the instructor’s performance efficiency evaluation in the department.",
            "Participate with the college and department head in curriculum development and accomplishing the instructional mission.",
            "Adheres to established laws, policies, rules and regulations important for teaching and learning effectiveness.",
            "Service, especially in a leadership role, on major university and college committees.",
            "Handling resources and materials carefully and wisely.",
        ]),
        ("interpersonal_relationship", "Interpersonal Relationship Capability", [
            "Participates in the development of a broad vision of the university.",
            "Foster relationships with institutions, colleagues, department and communities to support students’ learning and well-being.",
            "Is aware of, and acts in accordance with, university policies and practices.",
            "Holds meetings with students to discuss their learning problems.",
            "Communicates with students and instructors positively.",
            "Works cooperatively with the department head.",
            "Works collegially with other college and staff in the department.",
        ]),
    ],
}


def get_catalog(form_type):
    """Return categories and stable criterion keys for one academic form."""
    result = []
    for category_key, title, questions in _CATALOG.get(form_type, []):
        items = []
        for idx, question in enumerate(questions, start=1):
            items.append({
                "key": f"{category_key}__{idx}",
                "number": idx,
                "text": question,
            })
        result.append({"key": category_key, "title": title, "items": items})
    return result


def all_items(form_type):
    return [item for category in get_catalog(form_type) for item in category["items"]]


def form_type_label(form_type):
    return FORM_TITLES.get(form_type, form_type.replace("_", " ").title())
