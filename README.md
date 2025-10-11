AI Study Buddy

An intelligent, on-demand academic assistant designed to make learning more efficient and interactive. Powered by Google's Gemini API and built with Streamlit.

About The Project
 
In today's fast-paced academic environment, students often face challenges in grasping complex topics, condensing vast amounts of notes, and effectively testing their knowledge. The AI Study Buddy is a web application designed to tackle these problems head-on. It provides a suite of AI-powered tools that act as a personal tutor, available 24/7.

This application leverages the power of Large Language Models to provide contextual explanations, generate concise summaries, and create interactive quizzes, transforming a static study process into a dynamic and conversational experience.

 Key Features
 
 Conversational Concept Explainer: Don't just get a definition, have a conversation! Ask about a complex topic and then ask follow-up questions until you fully understand it. The AI maintains context for a natural tutoring experience.

 Interactive Notes Summarizer: Paste your lengthy study notes and receive a well-structured summary. You can then ask the AI to elaborate on specific points, simplify sections, or extract key terms from the original text.

 Dynamic Quiz Generator: Turn any topic into a learning opportunity. Generate a 10-question multiple-choice quiz to test your knowledge, receive your score, and review the correct answers to reinforce learning.

Built With
 
This project was built using the following technologies:

Python: The core programming language.

Streamlit: For creating the interactive web application front-end.

Google Gemini API: The powerful language model that drives all the AI features.

HTML/CSS: For custom styling to create a polished, modern user interface.


Getting Started

To get a local copy up and running, follow these simple steps.

Prerequisites

Make sure you have Python 3.8+ installed on your system.

Installation

Clone the repository:

git clone [https://github.com/Jeevannnn/Ai-Study-Buddy.git](https://github.com/Jeevannnn/Ai-Study-Buddy.git)

cd ai-study-buddy

Install the required packages:

pip install -r requirements.txt

Configure your API Key:

Navigate into the .streamlit folder.

Go to -> secrets.toml.

Add your Google Gemini API key to this file as shown below:

GEMINI_API_KEY = "YOUR_SECRET_API_KEY_HERE"



Run the application:

streamlit run app.py

The application will open in your default web browser.

Deployment

This application is deployed and hosted on Streamlit Community Cloud. The deployment process involves:

Pushing the project code to a public GitHub repository.

Connecting the repository to Streamlit Cloud.

Configuring the GEMINI_API_KEY as a secret variable directly within the Streamlit Cloud dashboard for secure access.

License

This project is licensed under the MIT License. See the LICENSE file for more details.
