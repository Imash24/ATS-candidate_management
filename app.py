from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from sqlalchemy import text
from flask_cors import CORS
from flask_migrate import Migrate

app = Flask(__name__)
CORS(app)

# Configure PostgreSQL database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:gm5522@localhost/candidatesdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Configure Flask-Mail for sending emails
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'atstesting017@gmail.com'
app.config['MAIL_PASSWORD'] = 'xcvrzyzybxdppoxb'  # Consider using environment variables for security

mail = Mail(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Define the Candidate model
class Candidate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    status = db.Column(db.String(50), nullable=False, default="pending")
    year = db.Column(db.Integer, nullable=False)  # Year of graduation
    round = db.Column(db.String(50), nullable=False)  # Interview round (e.g., level1, level2)

# Create tables if they don't exist
with app.app_context():
    db.create_all()

# Route to check database connection
@app.route('/')
def index():
    try:
        result = db.session.execute(text('SELECT 1')).scalar()
        return "Database connected successfully!"
    except Exception as e:
        return f"Database connection failed: {e}"

# Route to list all candidates with their status
@app.route('/candidates', methods=['GET'])
def list_candidates():
    try:
        year = request.args.get('year')  # Filter by year
        round_filter = request.args.get('round')  # Filter by interview round

        # Filter based on query params
        query = Candidate.query
        if year:
            query = query.filter_by(year=year)
        if round_filter:
            query = query.filter_by(round=round_filter)

        candidates = query.all()
        result = [
            {
                "id": candidate.id,
                "name": candidate.name,
                "email": candidate.email,
                "status": candidate.status,
                "year": candidate.year,
                "round": candidate.round
            }
            for candidate in candidates
        ]
        return jsonify({"candidates": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route to add a new candidate
@app.route('/add_candidate', methods=['POST'])
def add_candidate():
    try:
        data = request.get_json()
        new_candidate = Candidate(
            name=data['name'],
            email=data['email'],
            year=data['year'],
            round=data['round']
        )
        db.session.add(new_candidate)
        db.session.commit()
        return jsonify({"message": "Candidate added successfully!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route to update the status of a candidate and send an email
@app.route('/update_status/<int:id>', methods=['POST'])
def update_status(id):
    try:
        candidate = Candidate.query.get(id)
        if not candidate:
            return jsonify({"error": "Candidate not found"}), 404

        data = request.get_json()
        new_status = data.get('status')

        if new_status not in ['selected', 'rejected']:
            return jsonify({"error": "Invalid status"}), 400

        # Update the candidate's status
        candidate.status = new_status
        db.session.commit()

        # Send status update email
        send_status_email(candidate)

        return jsonify({"message": f"Candidate status updated to {new_status}"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Function to send email based on the candidate's status
def send_status_email(candidate):
    if candidate.status == 'selected':
        subject = "Congratulations! You've been selected"
        body = f"Dear {candidate.name},\n\nWe are pleased to inform you that you have been selected for the position."
    else:
        subject = "Thank you for applying"
        body = f"Dear {candidate.name},\n\nWe regret to inform you that you have not been selected at this time."

    msg = Message(subject, sender=app.config['MAIL_USERNAME'], recipients=[candidate.email])
    msg.body = body
    mail.send(msg)

# Updated Email templates mapped to interview rounds with multiple templates
email_templates = {
    "level1": [
        {
            "id": "level1_template1",
            "subject": "Level 1 Interview Task Assignment",
            "body": (
                "Dear {name},\n\n"
                "Congratulations on advancing to the Level 1 interview stage at Hash Agile Technologies! We are excited to have you progress further in our selection process.\n\n"
                "Please find below the instructions for your next task:\n\n"
                "### **Installation Instructions**\n\n"
                "1. **Read about Apache Solr:** Familiarize yourself with Solr by visiting the [Solr Tutorial](https://solr.apache.org/guide/).\n"
                "2. **Install Apache Solr:** Install Apache Solr on your local machine following the official [installation guide](https://solr.apache.org/guide/installing-solr.html).\n"
                "3. **Configure Solr Port:** Start the Solr service on port **8989** instead of the default port.\n"
                "4. **Download Employee Dataset:** Obtain the Employee Dataset from [Kaggle](https://www.kaggle.com/datasets/williamlucas0/employee-sample-data).\n\n"
                "### **Function Definitions**\n\n"
                "Using any programming language of your choice, implement the following functions:\n\n"
                "a) `createCollection(p_collection_name)`\n\n"
                "b) `indexData(p_collection_name, p_exclude_column)`: Index the given employee data into the specified collection, excluding the column provided in `p_exclude_column`.\n\n"
                "c) `searchByColumn(p_collection_name, p_column_name, p_column_value)`: Search within the specified collection for records where the column `p_column_name` matches the value `p_column_value`.\n\n"
                "d) `getEmpCount(p_collection_name)`\n\n"
                "e) `delEmpById(p_collection_name, p_employee_id)`\n\n"
                "f) `getDepFacet(p_collection_name)`: Retrieve the count of employees grouped by department from the specified collection.\n\n"
                "### **Function Executions**\n\n"
                "Once the functions are implemented, execute them in the following order with the specified parameters. Capture separate full-screen screenshots for each step:\n\n"
                "a) `v_nameCollection = 'Hash_<Your Name>'`\n"
                "b) `v_phoneCollection = 'Hash_<Your Phone Last Four Digits>'`\n"
                "c) `createCollection(v_nameCollection)`\n"
                "d) `createCollection(v_phoneCollection)`\n"
                "e) `getEmpCount(v_nameCollection)`\n"
                "f) `indexData(v_nameCollection, 'Department')`\n"
                "g) `indexData(v_phoneCollection, 'Gender')`\n"
                "h) `getEmpCount(v_nameCollection)`\n"
                "i) `delEmpById(v_nameCollection, 'E02003')`\n"
                "j) `getEmpCount(v_nameCollection)`\n"
                "k) `searchByColumn(v_nameCollection, 'Department', 'IT')`\n"
                "l) `searchByColumn(v_nameCollection, 'Gender', 'Male')`\n"
                "m) `searchByColumn(v_phoneCollection, 'Department', 'IT')`\n"
                "n) `getDepFacet(v_nameCollection)`\n"
                "o) `getDepFacet(v_phoneCollection)`\n\n"
                "### **Submission Requirements**\n\n"
                "Please submit your completed task in **PDF format** within **12 hours** of receiving this email using the following link:\n\n"
                "[Submit Your Task](https://forms.gle/9eKUSfg23JZngR4z8)\n\n"
                "Your submission should include:\n\n"
                "a) **Full Name:** Include your name.\n"
                "b) **Selfie Pic:** Add a selfie taken during the test right after your name.\n"
                "c) **First Task Email Screenshot:** Insert the screenshot of the first task email.\n"
                "d) **Second Task Email Screenshot:** Insert the screenshot of the second task email.\n"
                "e) **GitHub URL for Round 1:** Add the link to your GitHub repository for Round 1.\n"
                "f) **GitHub URL for Assignment:** Add the link to your GitHub repository for the assignment code.\n"
                "g) **Screenshot Proof of Service Running on Port 8989:** Provide a screenshot showing the service is running on port 8989.\n"
                "h) **Function Execution Results:** For each step (a-n), provide input, output, and screenshots of the execution.\n"
                "i) **Submit the PDF:** Once completed, export it as a PDF and submit within the 12-hour deadline.\n\n"
                "**Note:**\n\n"
                "- Please use all 1000+ records from the dataset to index and not just the sample.\n"
                "- Host the code on GitHub, and ensure the PDF contains only the function execution commands and results—pasting the code in the PDF will result in disqualification.\n"
                "- Follow the same bullet points as outlined in the Submission Requirements and attach the corresponding supporting links/documents.\n"
                "- All screenshots must be full-screen, showing the time and date.\n"
                "- Additional features like a custom UI to search by name, visualizations, Dockerizing the steps, or any other out-of-the-box implementations will provide an added advantage.\n"
                "- Do not rely on AI tools for function definitions. In the face-to-face round, you will be required to redefine and modify functions without access to Google. The GitHub links will be checked using ZeroGPT for AI-generated content and will factor into the selection criteria.\n\n"
                "We look forward to your participation and wish you the best of luck!\n\n"
                "Regards,\n\n"
                "Recruitment Team\n\n"
                "Hash Agile Technologies"
            )
        }
        # You can add more templates for other rounds here
    ]
    # You can add more rounds and their templates here
}

# Route to get available templates based on the selected round
@app.route('/get_templates', methods=['GET'])
def get_templates():
    try:
        round_filter = request.args.get('round')
        if not round_filter or round_filter not in email_templates:
            return jsonify({"error": "Invalid or missing round"}), 400

        templates = email_templates[round_filter]
        return jsonify({"templates": templates})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route to send emails based on subject, body, and filters provided
@app.route('/send_emails_by_filter', methods=['POST'])
def send_emails_by_filter():
    try:
        data = request.get_json()
        year = data.get('year')
        round_filter = data.get('round')
        status_filter = data.get('status')  # New: Get the status filter from the request
        subject = data.get('subject')
        body = data.get('body')

        if not round_filter:
            return jsonify({"error": "Missing round"}), 400

        if not subject or not body:
            return jsonify({"error": "Subject and body are required"}), 400

        # Build the query based on filters
        query = Candidate.query.filter_by(round=round_filter)
        if year:
            query = query.filter_by(year=year)
        if status_filter:
            query = query.filter_by(status=status_filter)  # New: Filter by status

        candidates = query.all()
        if not candidates:
            return jsonify({"error": "No candidates found with the given filters"}), 404

        for candidate in candidates:
            # Replace placeholders in subject and body
            formatted_subject = subject.format(name=candidate.name)
            formatted_body = body.format(name=candidate.name)

            # Send email
            msg = Message(formatted_subject, sender=app.config['MAIL_USERNAME'], recipients=[candidate.email])
            msg.body = formatted_body
            mail.send(msg)

        return jsonify({"message": f"Emails sent successfully to {len(candidates)} candidates!"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route to delete a candidate by id
@app.route('/delete_candidate/<int:id>', methods=['DELETE'])
def delete_candidate(id):
    try:
        candidate = Candidate.query.get(id)
        if not candidate:
            return jsonify({"error": "Candidate not found"}), 404

        db.session.delete(candidate)
        db.session.commit()
        return jsonify({"message": "Candidate deleted successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
