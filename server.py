import os
import fitz
from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
from backend.scripts.recommend import recommend_job
import uuid
from flask import send_file
from reportlab.pdfgen import canvas
from io import BytesIO
import datetime


app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


KEYWORDS_TO_SKILLS = {
    "python": "Python",
    "java": "Java",
    "c++": "C++",
    "javascript": "JavaScript",
    "html": "HTML",
    "css": "CSS",
    "sql": "SQL",
    "react": "React",
    "node": "Node.js",
    "machine learning": "Machine Learning",
    "deep learning": "Deep Learning",
    "data science": "Data Science",
    "flask": "Flask",
    "django": "Django"
}

def extract_keywords_from_pdf(pdf_path):

    doc = fitz.open(pdf_path)
    text = " ".join([page.get_text() for page in doc]).lower()

    detected_skills = [value for key, value in KEYWORDS_TO_SKILLS.items() if key in text]

    return {
        "skills": detected_skills if detected_skills else None
    }
last_user_skills = ["Python", "Django", "SQL"]
last_recommendations = ["Python Developer", "Backend Developer", "Full Stack Developer"]

@app.route("/download")
def download_pdf():
    buffer = BytesIO()
    p = canvas.Canvas(buffer)

    p.setFont("Helvetica-Bold", 16)
    p.drawString(180, 800, "CV Job Recommendation Report")

    p.setFont("Helvetica", 12)
    p.drawString(50, 770, "User Skills:")
    y = 750
    for skill in last_user_skills:
        p.drawString(70, y, f"- {skill}")
        y -= 20

    y -= 10
    p.drawString(50, y, "Recommended Jobs:")
    y -= 20
    for i, job in enumerate(last_recommendations, start=1):
        p.drawString(70, y, f"{i}. {job}")
        y -= 20

    # Add date
    y -= 10
    today = datetime.date.today().strftime("%d %B %Y")
    p.drawString(50, y, f"Date: {today}")

    p.save()
    buffer.seek(0)

    return send_file(buffer, as_attachment=True, download_name="recommendation_report.pdf", mimetype='application/pdf')

@app.route('/')
def home():
    return render_template('upload.html', result=None, sorry_message=None, success_message=None)
@app.route('/upload-cv')
def upload_cv():
    return render_template('upload_cv.html')

@app.route('/view-report')
def view_report():
    return render_template('view_report.html')

@app.route('/settings')
def settings():
    return render_template('settings.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'cv' not in request.files or request.files['cv'].filename == '':
        return render_template('upload.html', result=None, sorry_message="No CV file was uploaded.", success_message=None)

    file = request.files['cv']
    filename = secure_filename(file.filename)
    unique_filename = str(uuid.uuid4()) + "_" + filename  # Add unique prefix
    file_path = os.path.join(UPLOAD_FOLDER, unique_filename)
    file.save(file_path)

    user_input = extract_keywords_from_pdf(file_path)

    if not user_input["skills"]:
        os.remove(file_path)
        return render_template('upload.html', result=None, sorry_message="Sorry, your CV does not match any skills.",
                              success_message=None)



    try:
        recommended_jobs = recommend_job(user_input)
        result_text = recommended_jobs[0] if recommended_jobs else "No job matched."
    except Exception as e:
        return render_template('upload.html', result=None, sorry_message=f"Prediction error: {str(e)}", success_message=None)

    success_message = f"Congratulations! Your CV has been successfully uploaded as {unique_filename}."
    return render_template('upload.html', result=result_text, sorry_message=None, success_message=success_message)

if __name__ == '__main__':
    app.run(debug=True)
