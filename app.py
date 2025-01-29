from flask import Flask, request, jsonify, render_template
import os
from mistralai import Mistral

app = Flask(__name__)

# Predefined questions and answers mapped to keywords
predefined_answers = {
    ("your name", "who are you"): "I am Khagendra Neupane's AI clone!",
    ("how are you", "how's it going"): "I'm just a bot, but I'm here to help!",
    ("what can you do", "your abilities"): "I can answer questions about Khagendra Neupane. Try asking about his skills, projects, or background!",
    ("who is khagendra", "about khagendra", "khagendra neupane"): "Khagendra Neupane is an aspiring Cybersecurity, Networking, and AI/ML Professional, currently studying at Tribhuvan University, IOE, Pulchowk Campus.",
    ("khagendra's skills", "his skills", "what skills does he have"): "Khagendra is skilled in C Programming (95%), HTML (90%), Java (60%), Python (65%), C++ (85%), Linux (85%), and Microcontrollers (50%).",
    ("khagendra's projects", "his projects", "what projects has he done"): "You can check out Khagendra's projects on his GitHub profile.",
    ("contact khagendra", "how to reach khagendra", "his contact info"): "You can contact Khagendra through the contact section on his website.",
    ("where does khagendra study", "his university", "his education"): "Khagendra studies at Tribhuvan University, IOE, Pulchowk Campus.",
    ("khagendra's passion", "what is he passionate about"): "Khagendra is passionate about securing digital systems, optimizing networks, and leveraging AI/ML technologies.",
    ("khagendra's experience", "his work experience", "professional background"): "Khagendra has worked at Grand Hyatt Doha and Hyatt Regency Kathmandu.",
    ("khagendra's education", "his academic background", "where did he study"): "Khagendra studied MBS at Shankar Dev College, Kathmandu, and attended Chure Secondary School in Bardia, Nepal.",
    ("khagendra's social media", "his online profiles", "where to find him online"): "You can find Khagendra on Facebook, Instagram, and Twitter.",
    ("khagendra's hobbies", "his interests", "what does he do for fun"): "Information about Khagendra's hobbies is not specified in the available sources.",
    ("khagendra's achievements", "his awards", "what has he accomplished"): "Specific achievements and awards are not detailed in the available sources.",
    ("khagendra's publications", "his articles", "has he written any papers"): "There are no publications or articles listed in the available sources.",
    ("khagendra's certifications", "his credentials", "what certifications does he have"): "Specific certifications are not mentioned in the available sources.",
    ("khagendra's languages", "what languages does he speak", "his language proficiency"): "Information about Khagendra's language proficiency is not provided in the available sources.",
    ("khagendra's location", "where is he based", "his current city"): "Khagendra is currently based in Kathmandu, Nepal.",
    ("khagendra's contact methods", "how to get in touch with him", "his email address"): "You can contact Khagendra through the contact section on his website.",
    ("khagendra's recent activities", "what is he currently working on", "his latest projects"): "For the latest updates on Khagendra's activities and projects, please visit his GitHub profile and social media accounts.",
    ("khagendra's future goals", "his aspirations", "what are his plans"): "Khagendra aims to bridge academic learning with practical applications in the fields of cybersecurity, networking, and AI/ML technologies.",
    ("khagendra's collaborations", "who has he worked with", "his partners"): "Information about Khagendra's collaborations is not specified in the available sources.",
    ("khagendra's testimonials", "what do others say about him", "his reviews"): "Testimonials or reviews about Khagendra are not provided in the available sources.",
    ("khagendra's blog", "does he write a blog", "his blogging activities"): "There is no mention of a blog in the available sources.",
    ("khagendra's favorite technologies", "what tech does he prefer", "his preferred tools"): "Specific preferences for technologies or tools are not detailed in the available sources.",
    ("khagendra's volunteering", "his community work", "does he volunteer"): "Information about Khagendra's volunteering activities is not provided in the available sources.",
    ("khagendra's memberships", "organizations he belongs to", "his affiliations"): "Khagendra is associated with the Non-Resident Nepali Association.",
    ("khagendra's publications", "has he been featured in any media", "his media appearances"): "There are no media features or publications listed in the available sources.",
    ("khagendra's favorite projects", "which projects is he most proud of", "his notable work"): "For details on Khagendra's notable projects, please visit his GitHub profile.",
    ("khagendra's learning", "what is he currently studying", "his ongoing education"): "Khagendra is currently pursuing his studies at Tribhuvan University, IOE, Pulchowk Campus.",
    ("khagendra's speaking engagements", "has he given any talks", "his presentations"): "There is no information about speaking engagements or presentations in the available sources.",
    ("khagendra's mentorship", "does he mentor others", "his mentoring activities"): "Information about Khagendra's mentorship activities is not provided in the available sources.",
    ("khagendra's favorite books", "what does he read", "his reading list"): "There is no information about Khagendra's reading preferences in the available sources.",
    ("khagendra's favorite programming language", "which language does he prefer", "his coding preferences"): "Khagendra has expertise in Python, Java, C, and C++ for building efficient applications.",
    ("khagendra's open source contributions", "has he contributed to open source", "his open source work"): "For information on Khagendra's open source contributions, please visit his GitHub profile.",
    ("khagendra's travel", "where has he traveled", "his travel experiences"): "There is no detailed information about Khagendra's travel experiences in the available sources.",
    ("khagendra's photography", "does he do photography", "his photos"): "There is no information about Khagendra's involvement in photography in the available sources.",
    ("khagendra's design work", "is he a designer", "his design projects"): "There is no information about Khagendra's design work in the available sources.",

}

# Mistral AI API Key (Set this as an environment variable for security)
api_key = os.getenv("MISTRAL_API_KEY")
if not api_key:
    raise ValueError("API key not found! Set MISTRAL_API_KEY in the environment variables.")

model = "mistral-large-latest"
client = Mistral(api_key=api_key)

def match_predefined_answer(question):
    """Find the best predefined answer based on keywords in the question."""
    question = question.lower()
    for keywords, answer in predefined_answers.items():
        if any(keyword in question for keyword in keywords):
            return answer
    return None  # Return None if no match is found

def ask_mistral(question):
    """Call Mistral AI API if question is out of predefined scope."""
    chat_response = client.chat.complete(
        model=model,
        messages=[{"role": "user", "content": question}]
    )
    return chat_response.choices[0].message.content.strip()

@app.route("/")
def index():
    return render_template("chat.html")  # This will serve your frontend

@app.route("/ask", methods=["POST"])
def ask():
    data = request.json
    question = data.get("question", "").strip().lower().rstrip('?')

    answer = match_predefined_answer(question)
    
    if not answer:
        answer = ask_mistral(question)  # Fallback to AI

    return jsonify({"answer": answer})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)  # Port 10000 (Render default)
