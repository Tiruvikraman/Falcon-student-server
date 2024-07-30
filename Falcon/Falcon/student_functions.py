import easyocr
from pypdf import PdfReader
from ai71 import AI71
AI71_API_KEY = "api71-api-df260d58-62e0-46c9-b549-62daa9c409be"

def extract_text_from_pdf(pdf_path):
    text = ""
    reader = PdfReader(pdf_path)
    for page in reader.pages:
        text += page.extract_text() + "\n"
    print(text)
    return text

def generate_response_from_pdf(query, pdf_text):
    response = ''
    for chunk in AI71(AI71_API_KEY).chat.completions.create(
        model="tiiuae/falcon-180b-chat",
        messages=[
            {"role": "system", "content": "You are a project building assistant."},
            {"role": "user", "content": f'''Answer the querry based on the given content.Content:{pdf_text},query:{query}'''},
        ],
        stream=True,
    ):
        if chunk.choices[0].delta.content:
            response += chunk.choices[0].delta.content
    return response[:-6]

def generate_quiz(subject, topic, count, difficult):
    quiz_output = ""
    
    for chunk in AI71(AI71_API_KEY).chat.completions.create(
        model="tiiuae/falcon-180b-chat",
        messages=[
            {"role": "system", "content": "You are a teaching assistant."},
            {"role": "user", "content": f'''Generate {count} multiple-choice questions in the subject of {subject} for the topic {topic} for students at a {difficult} level. Ensure the questions are well-diversified and cover various aspects of the topic. Format the questions as follows:
Question: [Question text] [specific concept in a question] 
<<o>> [Option1] 
<<o>> [Option2] 
<<o>> [Option3] 
<<o>> [Option4], 
Answer: [Option number]'''},
        ],
        stream=True,
    ):
        if chunk.choices[0].delta.content:
            quiz_output += chunk.choices[0].delta.content
    print("Quiz generated")
    return quiz_output

def perform_ocr(image_path):
    reader = easyocr.Reader(['en'])
    try:
        result = reader.readtext(image_path)
        extracted_text = ''
        for (bbox, text, prob) in result:
            extracted_text += text + ' '
        return extracted_text.strip()
    except Exception as e:
        print(f"Error during OCR: {e}")
        return ''

def generate_ai_response(query):
    ai_response = ''
    for chunk in AI71(AI71_API_KEY).chat.completions.create(
        model="tiiuae/falcon-180b-chat",
        messages=[
            {"role": "system", "content": "You are a teaching assistant."},
            {"role": "user", "content": f'Assist the user clearly for his questions: {query}.'},
        ],
        stream=True,
    ):
        if chunk.choices[0].delta.content:
            ai_response += chunk.choices[0].delta.content
    return ai_response


def generate_project_idea(subject, topic, overview):
    string = ''
    for chunk in AI71(AI71_API_KEY).chat.completions.create(
        model="tiiuae/falcon-180b-chat",
        messages=[
            {"role": "system", "content": "You are a project building assistant."},
            {"role": "user", "content": f'''Give the different project ideas to build project in {subject} specifically in {topic} for school students. {overview}.'''},
        ],
        stream=True,
    ):
        if chunk.choices[0].delta.content:
            string += chunk.choices[0].delta.content
    return string

def generate_project_idea_questions(project_idea, query):
    project_idea_answer = ''
    for chunk in AI71(AI71_API_KEY).chat.completions.create(
        model="tiiuae/falcon-180b-chat",
        messages=[
            {"role": "system", "content": "You are a project building assistant."},
            {"role": "user", "content": f'''Assist me clearly for the following question for the given idea. Idea: {project_idea}. Question: {query}'''},
        ],
        stream=True,
    ):
        if chunk.choices[0].delta.content:
            project_idea_answer += chunk.choices[0].delta.content
    return project_idea_answer
def generate_step_by_step_explanation(query):
    explanation = ''
    for chunk in AI71(AI71_API_KEY).chat.completions.create(
        model="tiiuae/falcon-180b-chat",
        messages=[
            {"role": "system", "content": "You are the best teaching assistant."},
            {"role": "user", "content": f'''Provide me the clear step by step explanation answer for the following question. Question: {query}'''},
        ],
        stream=True,
    ):
        if chunk.choices[0].delta.content:
            explanation += chunk.choices[0].delta.content
    return explanation


def study_plan(subjects,hours,arealag,goal):
  plan=''
  for chunk in AI71(AI71_API_KEY).chat.completions.create(
      model="tiiuae/falcon-180b-chat",
      messages=[
          {"role": "system", "content": "You are the best teaching assistant."},
          {"role": "user", "content":f'''Provide me the clear personalised study plan for the subjects {subjects} i lag in areas like {arealag}, im available for {hours} hours per day and my study goal is to {goal}.Provide me like a timetable like day1,day2 for 5 days with concepts,also suggest some books'''},
      ],
      stream=True,
          ):
      if chunk.choices[0].delta.content:
                   plan+= chunk.choices[0].delta.content
  return plan.replace('\n','<br>')
