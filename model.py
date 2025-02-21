#CONVERT TO JS EVENTUALLY
from transformers import pipeline
from flask import Flask, request, jsonify, send_file
from fpdf import FPDF
import os

# Flask app
app = Flask(__name__)

# Load GPT-J model pipeline
model_pipeline = pipeline("text-generation", model="EleutherAI/gpt-j-6B")  # Ensure you have this model locally or hosted


class PDF(FPDF):
    """Custom PDF class for formatting the resume."""
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'RESUME', align='C', ln=True)
        self.ln(10)

    def add_section(self, title, content):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, title, ln=True)
        self.ln(5)
        self.set_font('Arial', '', 10)
        for line in content.split('\n'):
            self.cell(0, 8, line, ln=True)
        self.ln(10)

    def add_bullet_section(self, title, bullets, role=None, date_range=None):
        """Add a styled bullet-point section similar to the provided example."""
        # Section title
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, title, ln=True)

        # Role and date range
        if role or date_range:
            self.set_font('Arial', 'I', 10)
            role_text = f"{role}" if role else ""
            date_text = f"{date_range}" if date_range else ""
            self.cell(0, 10, f"{role_text} {date_text}".strip(), ln=True)

        self.ln(5)

        # Bullet points
        self.set_font('Arial', '', 10)
        for bullet in bullets:
            self.cell(5)  # Indent bullet
            self.cell(0, 8, f"▪ {bullet}", ln=True)  # Bullet symbol similar to the image
        self.ln(10)

@app.route('/generate-resume', methods=['POST'])
def generate_resume():
    """
    Generate a resume in PDF format based on user inputs.
    """
    try:
        # Get user input from request body
        data = request.json
        name = data.get("name", "Your Name")
        grade = data.get("grade", "Your Grade")
        email = data.get("email", "yourname@example.com")
        gpa = data.get("gpa", "4.0")
        school = data.get("school", "Your School")
        coursework = data.get("coursework", "Relevant Coursework Here")
        clubs = data.get("clubs", "Clubs Here")
        honors = data.get("honors", "Honors Here")
        experiences = data.get("experiences", [])
        skills = data.get("skills", [])
        awards = data.get("awards", [])

        # Generate professional summary using GPT-J
        summary_input = f"Write a professional summary under three sentences for a high school student with a GPA of {gpa}, attending {school}, with {skills} skills. Use buzz words. For example, work ethic, motivated, leverage proven experience.You may use these words but also make sure to use words that are related to their skills."
        summary = model_pipeline(summary_input, max_length=100, num_return_sequences=1, temperature=0.7)[0]["generated_text"]


        experience_bullets = []
        for exp in experiences:
            title = exp.get("title", "Experience Title")
            description = exp.get("description", "Description of your experience.")
            prompt = f"Convert the following experience description into three concise, professional bullet points, making sure to utilize whatever numbers/stats given as well as using buzzwords, if no numbers or stats are given, do not create any. DO NOT UNDER ANY CIRCUMSTANCES add something that was not given(meaning fabricated by you) in the bullet points :\n\nTitle: {title}\nDescription: {description}\nBullet points:"
            generated = model_pipeline(prompt, max_length=150, num_return_sequences=1, temperature=0.7)[0]["generated_text"]
            # Extract the bullet points and add them
            bullets = generated.split("\n")
            bullets = [bullet.strip("• ") for bullet in bullets if bullet.strip()]
            experience_bullets.append({"title": title, "bullets": bullets})

        # Create a PDF
        pdf = PDF()
        pdf.add_page()

        # Add user details
        pdf.set_font('Arial', '', 10)
        pdf.cell(0, 10, f"{name}", ln=True)
        pdf.cell(0, 10, f"{email}", ln=True)
        pdf.cell(0, 10, f"{phone}", ln=True)
        pdf.ln(10)

        # Add sections
        pdf.add_section("Professional Summary", summary)
        pdf.add_section("Education", f"{school}\n{grade}\nGPA: {gpa}\nRelevant Coursework: {coursework}\nClubs: {clubs}\nHonors: {honors}")
        

        # Add experiences
        for exp in experiences:
            pdf.add_bullet_section(
                exp["title"],
                exp["bullets"],
                role=exp.get("role"),
                date_range=exp.get("date_range")
            )

        # Add skills
        skills_content = "\n".join(skills)
        pdf.add_section("Skills", skills_content)

        # Add awards
        awards_content = "\n".join(awards)
        pdf.add_section("Awards, Honors, and Honorary Mentions", awards_content)

        # Save PDF
        output_file = "resume.pdf"
        pdf.output(output_file)

        # Return PDF
        return send_file(output_file, as_attachment=True)

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
