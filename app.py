import google.generativeai as genai
from flask import Flask, render_template, request
import os
import PyPDF2

app = Flask('name')

# Configure Google Generative AI API
genai.configure(api_key="AIzaSyC2BF1XFfiyvIMIaj2MuaEMGqCB2J3v4og")

# Set up the model
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 0,
    "max_output_tokens": 8192,
}

safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
]

model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

# Function to process PDF files and add their contents to the conversation history
def process_pdf_documents(directory_path):
    conversation_history = []
    for file_name in os.listdir(directory_path):
        file_path = os.path.join(directory_path, file_name)
        if os.path.isfile(file_path) and file_name.lower().endswith('.pdf'):
            with open(file_path, "rb") as file_obj:
                pdf_reader = PyPDF2.PdfReader(file_obj)
                for page in pdf_reader.pages:
                    page_text = page.extract_text()
                    conversation_history.append({"role": "user", "parts": [page_text]})
    return conversation_history

# Function to start a conversation and generate a response based on user input
def generate_response(user_input, conversation_history):
    convo = model.start_chat(history=conversation_history)
    convo.send_message(user_input)
    response = convo.last.text
    return response

# Route for homepage
@app.route('/')
def index():
    return render_template('index1.html', answer=None)
# Route for processing user queries
@app.route('/process', methods=['POST'])
def process():
    user_question = request.form.get('question')
    if user_question:
        # Process PDF documents and add their contents to the conversation history
        directory_path = r"D:\app45\Scholarships"
        conversation_history = process_pdf_documents(directory_path)

        # Generate a response using the model and conversation history
        response = generate_response(user_question, conversation_history)

        # Render the result template with the answer
        return render_template('index1.html', answer=response)

    # If no question was provided
    return "Please enter a question."

if __name__ == '__main__':
    app.run(debug=True)
app = Flask(__name__)
