import os
from flask import Flask, render_template, request, redirect, url_for
import pdfplumber
import openai
import json
import pandas as pd

# Ensure your OpenAI API key is set as an environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

# Fields to extract from the pdf documents
fields = [
    'Yacht Model',
    'Yacht Length',
    'Year of Manufacture',
    'Current Value/Purchase Price',
    'Current Location',
    'Intended Cruising Area',
    'Owner\'s Name',
    'Owner\'s Contact Information',
    'Owner\'s Boating Experience',
    'Previous Insurance Claims',
    'Additional Equipment',
    'Current Insurance Coverage',
    'Other'
]
# Extracting the text from the pdf files so that I can feed it to gpt-4 to get the desired data. 
def extract_text_from_pdf(pdf_path):
    text = ''
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + '\n'
    return text

# Here I am extracting the desired data fromm text with the help of gpt-4
def extract_values_with_llm(text):
    prompt = f"""
You are an expert in extracting information from unstructured text documents related to yacht insurance inquiries.

Extract the following fields from the provided text:

{', '.join(fields)}

If a field is not mentioned, leave it empty.

Provide your answers in the following JSON format:

{{
    "Yacht Model": "",
    "Yacht Length": "",
    "Year of Manufacture": "",
    "Current Value/Purchase Price": "",
    "Current Location": "",
    "Intended Cruising Area": "",
    "Owner's Name": "",
    "Owner's Contact Information": "",
    "Owner's Boating Experience": "",
    "Previous Insurance Claims": "",
    "Additional Equipment": "",
    "Current Insurance Coverage": "",
    "Other": ""
}}

Here is the text:

\"\"\"
{text}
\"\"\"
"""

    response = openai.ChatCompletion.create(
        model='gpt-4',
        messages=[
            {'role': 'system', 'content': 'You are a helpful assistant specialized in extracting information from documents.'},
            {'role': 'user', 'content': prompt}
        ],
        max_tokens=1000,
        temperature=0.0
    )

    gpt_output = response['choices'][0]['message']['content']
    try:
        json_start = gpt_output.find('{')
        json_end = gpt_output.rfind('}') + 1
        json_str = gpt_output[json_start:json_end]
        extracted_data = json.loads(json_str)
    except json.JSONDecodeError:
        print("Failed to parse GPT-4's response.")
        extracted_data = {field: '' for field in fields}
    return extracted_data

def find_missing_values_with_llm(extracted_data):
    missing_fields = [k for k, v in extracted_data.items() if not v.strip()]
    if not missing_fields:
        return extracted_data

    prompt = f"""
You are an expert in yacht insurance data.

Based on the provided information, please search reputable sources to find the missing values. Please only fill the values from verified websites and do not make assumptions.

Known information:

{json.dumps(extracted_data, indent=2)}

Fields to fill:

{missing_fields}

Provide your answers in the following JSON format:

{{
    "Field1": "Value1",
    "Field2": "Value2",
    ...
}}
"""

    response = openai.ChatCompletion.create(
        model='gpt-4',
        messages=[
            {'role': 'system', 'content': 'You are a helpful assistant specialized in yacht insurance.'},
            {'role': 'user', 'content': prompt}
        ],
        max_tokens=500,
        temperature=0.7
    )

    gpt_output = response['choices'][0]['message']['content']
    try:
        json_start = gpt_output.find('{')
        json_end = gpt_output.rfind('}') + 1
        json_str = gpt_output[json_start:json_end]
        filled_data = json.loads(json_str)
    except json.JSONDecodeError:
        print("Failed to parse GPT-4's response for missing fields.")
        filled_data = {}
    extracted_data.update({k: v for k, v in filled_data.items() if v.strip()})
    return extracted_data

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        uploaded_files = request.files.getlist('pdf_files')
        all_data = []
        file_names = []
        for file in uploaded_files:
            if file.filename == '':
                continue
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)

            text = extract_text_from_pdf(file_path)

            # Checking here if the text is too long for the LLM's context window. Because the 3rd pdf is very large sized. 
            max_text_length = 6000
            if len(text) > max_text_length:
                text = text[:max_text_length]

            # Extracting values here using LLM
            extracted_data = extract_values_with_llm(text)

            # Filling here the missing values using LLM
            extracted_data = find_missing_values_with_llm(extracted_data)

            all_data.append(extracted_data)
            file_names.append(file.filename)

            # Remove the uploaded file after processing. Just to clean the folder. 
            os.remove(file_path)

        # Creating a DataFrame
        df = pd.DataFrame(all_data, columns=fields)
        df.index = file_names

        # Transpose the DataFrame
        df = df.transpose()
        df.insert(0, 'Fields', df.index)
        df.reset_index(drop=True, inplace=True)

        # Rendering the template with the data
        return render_template('index.html', tables=[df.to_html(classes='data table table-bordered table-hover', header="true", index=False, justify='center')], titles=df.columns.values)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
