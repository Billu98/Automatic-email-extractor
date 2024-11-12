## Yacht Insurance Inquiry Automation
This project is an automated solution designed to streamline the processing of yacht insurance inquiries. Developed for YachtSicher GmbH, the application leverages advanced technologies, including the GPT-4 language model, to extract information from unstructured PDF documents and present it in a user-friendly, interactive web interface.
![image](https://github.com/user-attachments/assets/d4496167-2841-4033-8424-436abcb26f6c)
![image](https://github.com/user-attachments/assets/304786ee-b542-4f21-a625-8aa229a73fad)
![image](https://github.com/user-attachments/assets/3e6c4f7c-434c-4396-9902-17c2ef70c90c)


## Table of Contents
Project Overview

Features

Technologies Used

Folder Structure

Installation

Usage

Example Workflow


## Project Overview
YachtSicher GmbH receives frequent inquiries about yacht insurance. These inquiries often include details about yacht models, owner information, and insurance history, but in unstructured PDF formats. The goal of this project is to automatically extract relevant information from these PDFs and present it in a structured format, reducing the time and effort required for manual data entry and search.

## The solution includes:

- PDF text extraction.
- Structured data extraction using GPT-4.
- A web interface for users to upload PDF files and view extracted information.
## Features
- PDF Text Extraction: Uses pdfplumber to extract text from PDF files.
- Data Extraction with GPT-4:
Initial Extraction: Extracts specific fields (e.g., Yacht Model, Owner’s Contact Information) from the text.
Missing Data Handling: For missing information, prompts GPT-4 to fill in values based on known information.
- Web Application:
Built using Flask to manage file uploads and routing.
Secure handling of API keys and uploaded files.
- Interactive Front-End:
Styled with Bootstrap and enhanced with DataTables for sorting, searching, and pagination.
- Data Presentation:
Displays extracted data in a transposed table format for easy comparison across multiple inquiries.

## Technologies Used
Flask: Lightweight web framework to build the backend.
pdfplumber: Library to extract text from PDF documents.
OpenAI GPT-4: API for extracting structured information from unstructured text.
Pandas: For data manipulation and table formatting.
Bootstrap: For styling the front-end.
DataTables: jQuery plugin to add sorting, searching, and pagination to HTML tables.

## Folder Structure
YachtInsuranceInquiry/
├── extracted_data/              # Folder to store extracted data (if applicable)
├── static/                      # Folder for static files (CSS, JS)
├── templates/                   # Folder for HTML templates (Jinja2)
├── uploads/                     # Folder where uploaded PDFs are temporarily stored
├── email1.pdf                   # Sample email files for testing
├── email2.pdf
├── email3.pdf
├── Executive Summary.pdf        # Project executive summary
├── main.py                      # Main Flask application file
├── ppt.pptx                     # Project presentation file (optional)
├── requirements.txt             # List of required packages
└── README.md                    # Project documentation (this file)

## Installation
1. Clone the Repository:
git clone https://github.com/yourusername/YachtInsuranceInquiry.git
cd YachtInsuranceInquiry
2. Set Up a Virtual Environment (recommended):
   python -m venv venv
source venv/bin/activate   # On Windows, use venv\Scripts\activate
3. Install Dependencies:
   pip install -r requirements.txt
4. Set Up Environment Variables:
Create a .env file in the project root (or set environment variables directly).
Add your OpenAI API key:
OPENAI_API_KEY=your_openai_api_key

## Usage
Start the Flask Application:
python main.py
By default, the app runs on http://127.0.0.1:5000.

Access the Web Interface:

Open your browser and go to http://127.0.0.1:5000.
Upload one or more PDF files containing yacht insurance inquiries.
The app will process the files and display the extracted data in a table format.
Interact with the Data Table:

The table is interactive, allowing sorting, searching, and pagination.

## Example Workflow
User Interaction:

Users upload PDF files containing yacht insurance inquiries via the web interface.
Backend Processing:

The application saves the uploaded PDFs and extracts text using pdfplumber.
Text is passed to GPT-4 with a prompt to extract structured data.
Missing fields are re-prompted with GPT-4 to ensure completeness.
Data Compilation:

The extracted data is organized into a Pandas DataFrame and transposed for readability.
Front-End Rendering:

The data table is rendered with Bootstrap and enhanced by DataTables for a seamless user experience.
User Review:

Users can view and interact with the extracted data in a clear, organized format.

