# Audio-Speech-To-Sign-Language-Converter

![CI Pipeline](https://github.com/JosephJonathanFernandes/Audio-Speech-To-Sign-Language-Converter/actions/workflows/ci.yml/badge.svg)
![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![Django Version](https://img.shields.io/badge/django-3.0.4%2B-green)

A powerful, accessible tool that bridges the communication gap by converting audio speech and text into visual Indian Sign Language (ISL) animations.

## The Problem

Communication for the hearing impaired is a significant challenge when interacting with individuals who do not know sign language. While text-to-speech exists, speech-to-sign is far more complex due to the grammatical differences and visual nature of sign language. 

## The Solution

SignSpeak provides a seamless interface to capture voice input (or text) and instantly translate it into an animated sign language sequence. It utilizes Natural Language Processing (NLP) to parse English sentences, determine tenses, lemmatize words, and intelligently string together video assets representing ISL gestures.

## Key Features

- **Speech Recognition**: Capture voice input directly from the browser using the Web Speech API.
- **Intelligent NLP Engine**: Processes sentences to handle tenses, stopwords, and lemmatization using NLTK.
- **Smooth Animation Playback**: Dynamically strings together individual sign language videos to form coherent sentences.
- **Enterprise-Grade Architecture**: Built with Django, utilizing a modular service-oriented architecture (SOA).
- **Secure by Default**: Compliant with GitGuardian standards, utilizing environment variables for secrets management.

## Tech Stack

- **Backend**: Python 3.8+, Django 3.0.4+
- **NLP Processing**: NLTK (Natural Language Toolkit)
- **Frontend**: HTML5, CSS3 (Custom Variables, Flexbox), Vanilla JavaScript
- **Testing**: Pytest
- **CI/CD**: GitHub Actions

## Quick Start

### 1. Clone the repository
```bash
git clone https://github.com/JosephJonathanFernandes/Audio-Speech-To-Sign-Language-Converter.git
cd Audio-Speech-To-Sign-Language-Converter
```

### 2. Set up environment variables
```bash
cp .env.example .env
# Edit .env and provide your secret keys
```

### 3. Create a virtual environment and install dependencies
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 4. Run the application
```bash
python manage.py runserver
```
Visit `http://localhost:8000` in your browser.

## Architecture

Please see [ARCHITECTURE.md](docs/ARCHITECTURE.md) for a detailed overview of the system design.

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](docs/CONTRIBUTING.md) for guidelines on how to submit pull requests, report issues, and improve the codebase.

## Security

Please review our [SECURITY.md](SECURITY.md) policy for reporting vulnerabilities.

## License

This project is licensed under the terms of the MIT license.
