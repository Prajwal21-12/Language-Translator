# 🌍 Talkora – Language Translation Tool

**Breaking language barriers, connecting the world.**

Talkora is a multilingual language translation web application built using Python and Streamlit. It allows users to translate text between 14 different languages through a simple and user-friendly interface.

## ✨ Features

- 🌍 Supports 14 languages.
- 🔄 Quick source and target language swapping.
- ⚡ Instant text translation.
- 📋 Copy-ready translation results.
- 🕘 Recent translation history.
- 📝 Supports text input up to 5,000 characters.
- 🔁 Automatic fallback translation service.
- 💻 Clean and responsive user interface.

## 🛠️ Technologies Used

- Python
- Streamlit
- Requests
- Google Translate web endpoint
- MyMemory Translation API
- HTML and CSS

## 🌐 Supported Languages

1. English
2. Kannada
3. Hindi
4. Telugu
5. Tamil
6. Malayalam
7. French
8. German
9. Spanish
10. Japanese
11. Arabic
12. Chinese (Simplified)
13. Portuguese
14. Italian

## 📂 Project Structure

```text
Language-Translator/
│
├── app.py
├── requirements.txt
└── README.md
```

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/Prajwal21-12/Language-Translator.git
```

### 2. Navigate to the project folder

```bash
cd Language-Translator
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Run the application

```bash
python -m streamlit run app.py
```

The application will open in your browser.

## 🔄 Translation Process

Talkora uses two translation services:

- **Primary:** Google Translate web endpoint.
- **Fallback:** MyMemory Translation API.

The application tries the primary service first and uses the fallback if the primary service fails.

**Note:** These services require an internet connection. The Google web endpoint is unofficial and may be subject to availability or usage restrictions. Translation quality can vary by language and context.

## 🎯 Project Objective

The objective of Talkora is to make multilingual communication easier through a simple, accessible and user-friendly translation application.

## 👨‍💻 Developer

**Prajwal Harihar**

- GitHub: [Prajwal21-12](https://github.com/Prajwal21-12)

## 📜 License

This project is available under the MIT License.

---

**Talkora – Words connect the world. 🌍**