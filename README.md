

# **Velosis AI Chatbot**

<p align="center">
  <img src="https://img.shields.io/badge/Streamlit-v1.11.0-blueviolet?style=for-the-badge">
  <img src="https://img.shields.io/badge/PyPDF2-v3.1.0-red?style=for-the-badge">
  <img src="https://img.shields.io/badge/Deep%20Translator-v1.8.2-green?style=for-the-badge">
  <img src="https://img.shields.io/badge/SpeechRecognition-v3.9.0-orange?style=for-the-badge">
</p>

---

## **🌟 Overview**

Velosis AI is an intelligent chatbot designed to assist users with technical queries using **Gemini AI** for real-time answers. The app also supports:

- **Speech Recognition**
- **PDF Documentation Extraction**
- **Language Translation**
- **Text-to-Speech Generation** in multiple languages

It is developed using **Streamlit** and integrates with APIs like **Google Translator** and **Google Gemini AI** for advanced responses. 

---

## **🚀 Features**

- **Multilingual Support**: Translate between languages like Hindi, Spanish, French, and many others.
- **PDF Parsing**: Upload PDF documentation for AI to leverage in its responses.
- **Speech Recognition**: Input your queries using voice in multiple languages.
- **Text-to-Speech (TTS)**: Convert chatbot responses into speech.
- **Custom Complexity Levels**: Choose the complexity of the AI’s responses, ranging from **Easy** to **Expert**.

---

## **🔧 Technologies Used**

- **[Streamlit](https://streamlit.io/)** - Web Framework for real-time data apps.
- **[Google Gemini AI](https://cloud.google.com/)** - AI API for generating responses.
- **[PyPDF2](https://pypdf2.readthedocs.io/)** - Library for PDF parsing.
- **[SpeechRecognition](https://pypi.org/project/SpeechRecognition/)** - Python library for speech-to-text conversion.
- **[Deep Translator](https://pypi.org/project/deep-translator/)** - Language translation API.
- **[gTTS](https://pypi.org/project/gTTS/)** - Google Text-to-Speech library.

---

## **📋 Prerequisites**

Ensure you have the following packages installed:

```bash
pip install -r requirements.txt
```

You will also need:

- **Gemini API Key** from Google to integrate AI responses.

---

## **⚙️ How to Run**

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/velosis-ai.git
    cd velosis-ai
    ```

2. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Set your **Gemini API Key** in the code:
    ```python
    GEMINI_API_KEY = "ENTER YOUR GEMINI KEY"
    ```

4. Run the Streamlit app:
    ```bash
    streamlit run app.py
    ```

---

## **🧠 Usage**

1. **Login**: The default credentials are:
    - **Username**: admin
    - **Password**: admin

2. **Chatbot**: Ask any technical query, upload relevant PDFs, or use speech input for assistance.

3. **Uploaded Files**: View previously uploaded PDFs.

4. **Chat History**: Review past conversations with the bot.

---

## **🌐 Supported Languages**

- Hindi
- Kannada
- Telugu
- Tamil
- Malayalam
- English
- Spanish
- French
- German
- Chinese (Simplified)
- Japanese
- Russian

---

## **👨‍💻 Developer Guide**

Feel free to customize the following:

- **Login credentials**: Update them in the `login` section.
- **Language and Voice options**: Modify or extend the list of languages or voices in the code.
- **CSS Styles**: Customize the UI by changing the styles in the `st.markdown` section.

---

## **📄 License**

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

---

## **💬 Acknowledgments**

Thanks to the open-source libraries and APIs used in this project:

- [Streamlit](https://streamlit.io/)
- [Google Gemini AI](https://cloud.google.com/)
- [gTTS](https://pypi.org/project/gTTS/)
- [Deep Translator](https://pypi.org/project/deep-translator/)

---

Enjoy using **Velosis AI**! Feel free to contribute to this project or suggest new features!
