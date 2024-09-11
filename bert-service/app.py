from flask import Flask, request, jsonify
from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer
import torch

app = Flask(__name__)

# Load BERT model for text classification
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

# Expanded list of famous Indian government departments
labels = [
    "Public Works Department (PWD)", "Electricity Board", 
    "Municipal Corporation", "Ministry of Health", 
    "Ministry of Education", "Road Transport Department", 
    "Ministry of Environment and Forests", "Police Department", 
    "Income Tax Department", "Telecom Regulatory Authority of India (TRAI)", 
    "Ministry of Agriculture", "Ministry of Railways", "Postal Department", 
    "Ministry of Finance"
]

# Load DialoGPT model and tokenizer for follow-up questions
tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
dialog_model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")

# Function to identify compulsory details based on the department
def required_details_for_department(department):
    detail_requirements = {
        "Electricity Board": "Please provide the exact location and whether the issue is a power outage or streetlight malfunction.",
        "Public Works Department (PWD)": "Please specify the nature of the road issue (e.g., potholes, broken pavement).",
        "Municipal Corporation": "Please provide the area and describe the civic issue (e.g., garbage, drainage).",
        "Ministry of Health": "Please mention the hospital or clinic and describe the health-related issue.",
        "Ministry of Environment and Forests": "Please describe the environmental concern (e.g., pollution, deforestation) and its location."
    }
    return detail_requirements.get(department, "No additional details required.")

# Function to generate follow-up questions using DialoGPT
def generate_followup_question(input_text):
    input_ids = tokenizer.encode(input_text + tokenizer.eos_token, return_tensors='pt')
    response_ids = dialog_model.generate(input_ids, max_length=1000, pad_token_id=tokenizer.eos_token_id)
    response = tokenizer.decode(response_ids[:, input_ids.shape[-1]:][0], skip_special_tokens=True)
    return response

@app.route('/classify', methods=['POST'])
def classify_text():
    data = request.get_json()
    complaint_text = data.get('complaintText')

    # Perform classification using the BERT model
    result = classifier(complaint_text, labels)
    
    # Get the top 2 departments and their scores
    top_departments = result['labels'][:2]
    scores = result['scores'][:2]
    
    # If the top 2 scores are close (e.g., within 10% confidence), ask for more information using DialoGPT
    if abs(scores[0] - scores[1]) < 0.1:
        additional_info_1 = required_details_for_department(top_departments[0])
        additional_info_2 = required_details_for_department(top_departments[1])
        
        follow_up_question = generate_followup_question(
            f"The complaint could be related to either of these departments: {top_departments[0]} or {top_departments[1]}. "
            "Can you provide additional details to clarify?"
        )
        
        return jsonify({
            'message': follow_up_question,
            'required_details': {
                top_departments[0]: additional_info_1,
                top_departments[1]: additional_info_2
            }
        })
    
    # Fallback: if no department has a confidence score greater than 0.5, request clarification using DialoGPT
    if scores[0] < 0.3:
        follow_up_question = generate_followup_question(
            f"We couldn’t confidently classify the complaint. The complaint could be related to: {', '.join(top_departments)}. "
            "Could you provide more specific information?"
        )
        
        return jsonify({
            'message': follow_up_question
        })

    # Return the most confident department and ask for compulsory information if needed
    department = top_departments[0]
    required_info = required_details_for_department(department)

    follow_up_question = generate_followup_question(
        f"Your complaint seems related to {department}. Please provide more details: {required_info}"
    )

    return jsonify({
        'department': department,
        'complaint': complaint_text,
        'required_details': required_info,
        'next_steps': follow_up_question
    })

@app.route('/provide-details', methods=['POST'])
def provide_details():
    # Endpoint to handle additional user details after clarification is requested
    data = request.get_json()
    complaint_text = data.get('complaintText')
    additional_details = data.get('additionalDetails')

    # Simulate confirmation and return a final response after gathering additional information
    return jsonify({
        'message': f'Thank you for the additional details. Your complaint about "{complaint_text}" has been successfully classified under "{additional_details}".',
        'status': 'Complaint lodged successfully'
    })

if __name__ == '__main__':
    app.run(debug=True, port=5001)
