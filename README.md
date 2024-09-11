
# Complaint Classification System with BERT and DialoGPT

This project is a Flask-based complaint classification system that uses BERT for zero-shot classification of complaints and DialoGPT for generating follow-up questions. The system is built to classify complaints based on famous Indian government departments and allows for human-like follow-up interactions if the classification is uncertain.

## Features

- **BERT Model for Complaint Classification**: Classifies complaints into relevant departments using `facebook/bart-large-mnli`.
- **DialoGPT for Follow-up Questions**: If the model is uncertain, it generates follow-up questions to gather additional information.
- **REST API**: Provides endpoints for classifying complaints and submitting additional details.

## Project Structure

├── backend/ # Contains the Node.js backend (if applicable) │ ├── node_modules/ # Node.js dependencies (ignored in git) │ └── ... ├── bertservice/ # Python backend for complaint classification │ ├── venv/ # Python virtual environment (ignored in git) │ └── ... ├── README.md # Project documentation ├── .gitignore # Ignored files and directories └── ...

markdown
Copy code

## Requirements

- **Python 3.7+**
- **Node.js 14+** (if using Node.js backend)
- **Pipenv** (optional, for managing the Python environment)

## Project Setup

### 1. Clone the repository

```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
2. Python Setup
Navigate to the bertservice/ directory and create a virtual environment:

bash
Copy code
cd bertservice
python -m venv venv
Activate the virtual environment:

On Windows:

bash
Copy code
venv\Scripts\activate
On macOS/Linux:

bash
Copy code
source venv/bin/activate
Install the required dependencies:

bash
Copy code
pip install -r requirements.txt
3. Node.js Setup (if applicable)
Navigate to the backend/ directory:

bash
Copy code
cd backend
Install Node.js dependencies:

bash
Copy code
npm install
4. Set Execution Policy on Windows (for Python virtual environment)
If you're on Windows and encounter an error related to script execution when activating the virtual environment, you need to set the execution policy. Follow these steps:

Open PowerShell as Administrator.

Run the following command to set the execution policy:

bash
Copy code
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
This allows PowerShell to execute the necessary scripts to activate your virtual environment.

5. Run the Flask Application
Ensure you're in the bertservice/ directory with the virtual environment activated.

Run the Flask application:

bash
Copy code
flask run --port 5001
The server will be running at http://127.0.0.1:5001.

6. API Endpoints
POST /classify: Classify a complaint.

Request Body: { "complaintText": "Your complaint text here" }
Response: Department classification and follow-up details if needed.
POST /provide-details: Provide additional details if required for classification.

Request Body: { "complaintText": "Your complaint text here", "additionalDetails": "More specific information" }
Example API Request
json
Copy code
{
  "complaintText": "The streetlights on my road are not working."
}
Response:

json
Copy code
{
  "department": "Electricity Board",
  "complaint": "The streetlights on my road are not working.",
  "required_details": "Please provide the exact location and whether the issue is a power outage or streetlight malfunction.",
  "next_steps": "Can you provide the above details to proceed?"
}
License
This project is licensed under the MIT License. See the LICENSE file for details.

markdown
Copy code

### Key Additions:
1. **Project Setup**: Instructions for cloning, setting up the Python virtual environment, and installing dependencies.
2. **Execution Policy**: Instructions for setting the execution policy on Windows, so users can activate the virtual environment without errors.
3. **API Endpoints**: Information about the main API endpoints, including the `/classify` and `/provide-details` endpoints.
4. **Example Request**: An example request and response to illustrate how the API works.
