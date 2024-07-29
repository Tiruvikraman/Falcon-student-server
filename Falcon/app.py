from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import os
from student_functions import extract_text_from_pdf,generate_ai_response,generate_project_idea,generate_project_idea_questions,generate_quiz,generate_response_from_pdf,generate_step_by_step_explanation,perform_ocr,study_plan

AI71_API_KEY = "api71-api-df260d58-62e0-46c9-b549-62daa9c409be"
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS =  {'pdf', 'jpg', 'jpeg', 'png'}
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/student')
def student():
    return render_template('student.html')

@app.route('/teacher')
def teacher():
    return render_template('teacher.html')

@app.route('/student_pdfqa', methods=['GET', 'POST'])
def student_pdfqa():
    if request.method == 'POST':
        file = request.files.get('pdf-file')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            
            pdf_text = extract_text_from_pdf(file_path)
            return jsonify({'message': f'PDF uploaded and processed. You can now ask questions.', 'pdf_text': pdf_text})
        else:
            return jsonify({'message': 'Invalid file type. Please upload a PDF.'}), 400

    return render_template('student_pdfqa.html')

@app.route('/ask_pdf_question', methods=['POST'])
def ask_pdf_question():
    data = request.json
    query = data['query']
    pdf_text = data['pdf_text']
    
    response = generate_response_from_pdf(query, pdf_text)[:-6]
    return jsonify({'response': response})

@app.route('/student_aitutor')
def student_aitutor():
    return render_template('student_aitutor.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    query = data['message']
    response = generate_ai_response(query)
    return jsonify({'response': response})

@app.route('/upload_image_for_ocr', methods=['POST'])
def upload_image_for_ocr():
    if 'image-file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['image-file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        extracted_text = perform_ocr(file_path)
        ai_response = generate_ai_response(extracted_text)
        
        return jsonify({'ai_response': ai_response})
    return jsonify({'error': 'Invalid file type'}), 400


@app.route('/student_projectideas')
def student_projectideas():
    return render_template('student_projectideas.html')

@app.route('/student_quiz')
def student_quiz():
    return render_template('student_quiz.html')

@app.route('/generate_quiz', methods=['POST'])
def generate_quiz_route():
    data = request.json
    subject = data['subject']
    topic = data['topic']
    count = int(data['num-questions'])
    difficulty = data['difficulty']
    
    quiz = generate_quiz(subject, topic, count, difficulty)
    return jsonify({'quiz': quiz})

@app.route('/generate_project_idea', methods=['POST'])
def generate_project_idea_route():
    data = request.json
    subject = data['subject']
    topic = data['topic']
    plan = data['plan']
    
    project_idea = generate_project_idea(subject, topic, plan)
    return jsonify({'project_idea': project_idea})

@app.route('/ask_followup', methods=['POST'])
def ask_followup_route():
    data = request.json
    project_idea = data['project_idea']
    query = data['query']
    
    response = generate_project_idea_questions(project_idea, query)
    return jsonify({'response': response})

@app.route('/student_studyplans')
def student_studyplans():
    return render_template('student_studyplans.html')

@app.route('/generate_study_plan', methods=['POST'])
def generate_study_plan_route():
    data = request.json
    subjects = data['subjects']
    hours = data['hours']
    area_lag = data['areaLag']  # Ensure the key matches
    goal = data['goal']
    learning_style = data['learningStyle']

    study_plan_text = study_plan(subjects, hours, area_lag, goal)
    return jsonify({'study_plan': study_plan_text})


@app.route('/student_stepexplanation')
def student_stepexplanation():
    return render_template('student_stepexplanation.html')


@app.route('/generate_step_by_step_explanation', methods=['POST'])
def generate_step_by_step_explanation_route():
    data = request.get_json()
    question = data['question']
    answer = generate_step_by_step_explanation(question)
    return jsonify({'answer': answer})

if __name__ == '__main__':
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.run(debug=True)
