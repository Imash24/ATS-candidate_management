from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from sqlalchemy import text
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Configure PostgreSQL database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:gm5522@localhost/candidatesdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Configure Flask-Mail for sending emails
app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # Replace with actual SMTP server
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'atstesting017@gmail.com'  # Replace with your email
app.config['MAIL_PASSWORD'] = 'xcvrzyzybxdppoxb'  # Replace with your email password

mail = Mail(app)
db = SQLAlchemy(app)

# Define the Candidate model
class Candidate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    status = db.Column(db.String(50), nullable=False, default="pending")

# Route to check database connection
@app.route('/')
def index():
    try:
        # Use text() for raw SQL queries
        result = db.session.execute(text('SELECT 1')).scalar()
        return "Database connected successfully!"
    except Exception as e:
        return f"Database connection failed: {e}"

# Route to list all candidates with their status
@app.route('/candidates', methods=['GET'])
def list_candidates():
    try:
        candidates = Candidate.query.all()
        result = [
            {
                "id": candidate.id,
                "name": candidate.name,
                "email": candidate.email,
                "status": candidate.status
            }
            for candidate in candidates
        ]
        return jsonify({"candidates": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route to add a new candidate (for testing purposes)
@app.route('/add_candidate', methods=['POST'])
def add_candidate():
    try:
        data = request.get_json()
        new_candidate = Candidate(name=data['name'], email=data['email'])
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

    msg = Message(subject, sender="your_email@example.com", recipients=[candidate.email])
    msg.body = body
    mail.send(msg)

if __name__ == '__main__':
    app.run(debug=True)
