# SkillBridge - AI-Powered Career Gap Analyzer 🎯

**SkillBridge** is a production-ready Streamlit application that uses the **Google Gemini 1.5 Flash** model to analyze the gap between a user's current resume and their target career role. It provides a match score, identifies critical skill gaps, and generates a personalized 4-week roadmap to bridge those gaps.

Developed by **Sagar Singh** and team.

## 🚀 Features
* **Multi-Format Upload:** Supports PDF, Images (OCR), and Text files.
* **AI Deep Analysis:** Uses Google Gemini to extract semantic meaning from resumes.
* **Match Scoring:** Get an instant percentage score based on your target role.
* **Critical Gap Identification:** Pinpoints exactly what skills or experiences you are missing.
* **4-Week Action Plan:** A structured, week-by-week roadmap to help you become job-ready.
* **Modern UI:** Sleek, dark-mode interface built with custom CSS in Streamlit.

## 🛠️ Tech Stack
* **LLM:** Google Gemini 1.5 Flash
* **Frontend:** Streamlit
* **OCR & Extraction:** PyTesseract (Images), PyPDF2 (PDFs)
* **Language:** Python 3.9+

## 🏁 Getting Started

### 1. Prerequisites
* You must have **Tesseract OCR** installed on your system.
* You need a **Google Gemini API Key**.

### 2. Installation
```bash
# Clone the repo
git clone [https://github.com/SagarSingh/SkillBridge.git](https://github.com/SagarSingh/SkillBridge.git)
cd SkillBridge

# Install dependencies
pip install streamlit google-generativeai PyPDF2 Pillow pytesseract
3. Run the App
Bash

# Set your API Key (Replace 'your_key' with your actual key)
export GEMINI_API_KEY='your_key_here'

# Start Streamlit
streamlit run app.py
📂 Project Structure
app.py: Main Streamlit application and AI logic.

requirements.txt: List of necessary Python libraries.

.env: (Optional) Local storage for your API key.

🤝 Contributing
Built with passion by Sagar Singh and his teammates. Feel free to fork and improve!

📄 License
Distributed under the MIT License.


---

**One last tiny thing:** To make the "Install dependencies" part work for other people, make a new file in your GitHub called `requirements.txt` and paste these 5 lines into it:
```text
streamlit
google-generativeai
PyPDF2
Pillow
pytesseract
