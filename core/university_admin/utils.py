import os
from datetime import date
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch

def generate_endorsement_pdf(application, response):
    """
    Generates a PDF endorsement letter and writes it to the provided HTTP response.
    """
    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter
    
    # Title / Header
    p.setFont("Helvetica-Bold", 16)
    p.drawString(1 * inch, height - 1 * inch, "POLYTECHNIC UNIVERSITY OF THE PHILIPPINES")
    p.setFont("Helvetica", 12)
    p.drawString(1 * inch, height - 1.25 * inch, "Office of the Vice President for Student Affairs")
    p.drawString(1 * inch, height - 1.4 * inch, "Student Internship Program")
    
    # Date
    p.drawString(1 * inch, height - 2 * inch, f"Date: {date.today().strftime('%B %d, %Y')}")
    
    # Company Addressee
    p.setFont("Helvetica-Bold", 12)
    p.drawString(1 * inch, height - 2.5 * inch, application.company.name)
    p.setFont("Helvetica", 12)
    p.drawString(1 * inch, height - 2.7 * inch, "Human Resources / Internship Coordinator")
    
    # Subject
    p.setFont("Helvetica-Bold", 12)
    p.drawString(1 * inch, height - 3.2 * inch, "SUBJECT: INTERNSHIP ENDORSEMENT")
    
    # Body
    p.setFont("Helvetica", 12)
    
    # Student Details
    student = application.student
    student_name = student.get_full_name() or student.username
    course = "their academic program"
    if hasattr(student, 'profile') and student.profile.course:
        course = dict(student.profile.COURSE_CHOICES).get(student.profile.course, student.profile.course)

    body_lines = [
        f"Dear Sir/Madam,",
        "",
        f"This is to formally endorse Mr./Ms. {student_name},",
        f"a bonafide student of the Polytechnic University of the Philippines taking up",
        f"{course}, for an internship placement at your esteemed company,",
        f"{application.company.name}.",
        "",
        f"The internship is a requirement for their degree program. We believe that",
        f"the practical experience and exposure your company provides will greatly",
        f"augment their academic learning.",
        "",
        f"Please find attached their resume and necessary credentials for your reference.",
        "",
        f"Thank you for your continued partnership and support in the development of",
        f"our future professionals.",
        "",
        "Sincerely,",
        "",
        "John Doe",
        "Director, Internship Program",
        "Polytechnic University of the Philippines"
    ]
    
    y = height - 3.8 * inch
    for line in body_lines:
        p.drawString(1 * inch, y, line)
        y -= 0.25 * inch

    # Finish page and save
    p.showPage()
    p.save()
