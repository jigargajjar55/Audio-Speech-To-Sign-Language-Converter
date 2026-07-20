# Architecture Overview

## Introduction
The Audio-Speech-To-Sign-Language-Converter (SignSpeak) utilizes a Service-Oriented Architecture (SOA) within the Django framework to ensure maintainability, scalability, and clean code principles (SOLID).

## Components

### 1. Presentation Layer (Frontend)
- **HTML/CSS/JS**: Clean, modular vanilla JS and custom CSS properties.
- **Web Speech API**: Handles audio-to-text conversion directly in the user's browser, ensuring low latency.
- **Video Renderer**: JavaScript dynamically queues and plays HTML5 `<video>` tags based on the words processed by the backend.

### 2. Controller Layer (Django Views)
- Located in `src/core/views/`.
- **Auth Views**: Handles user registration, login, and sessions using standard Django authentication.
- **Animation View**: Acts as the API endpoint for form submissions. It receives the transcribed text, delegates processing to the `NLPService`, and returns the rendering context.

### 3. Service Layer (NLPService)
- Located in `src/core/services/nlp_service.py`.
- Responsible for all business logic:
  - **Tokenization**: Breaking sentences into words.
  - **POS Tagging**: Identifying verbs, nouns, adjectives using NLTK.
  - **Stop-word Removal**: Filtering out unnecessary words to streamline the sign language translation.
  - **Lemmatization**: Converting words to their root forms (e.g., "running" -> "run") so they map correctly to the video asset dictionary.
  - **Tense Adjustments**: Inferring context (Past/Future) and injecting indicator words (e.g., "Before", "Will").

### 4. Data Layer
- **SQLite Database**: Used currently for User models and authentication sessions.
- **Static Assets (`assets/`)**: Contains the MP4 files representing the sign language vocabulary. The `finders` utility maps lemmatized words to these physical files.

## Request Flow
1. User speaks into the microphone (Frontend -> Web Speech API).
2. The browser translates speech to text and submits it via POST to `/animation/`.
3. `animation_view` receives the text and calls `nlp_service.process_text(text)`.
4. `NLPService` returns a sanitized list of word tokens.
5. Django renders `animation.html` with the token list.
6. The frontend JavaScript (`animation.js`) matches tokens to static video URLs and plays them sequentially.
