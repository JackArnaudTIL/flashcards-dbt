🧠 Interactive Flashcard Platform
A lightweight, high-performance web application for interactive studying and spaced-repetition testing. Built with vanilla HTML, CSS, and JavaScript, this application supports dynamic filtering, rich media (images and audio), and a seamless "Fast Start" user interface.

This repository operates as a monorepo, containing the static frontend, a serverless Azure feedback API, and a Python automation suite for rapidly scraping, building, and deploying new flashcard decks.

✨ Key Features
Fast Start UI: Users can jump straight into a default 50-card session or expand a custom accordion to filter by Category, Group, and Difficulty.

Hybrid Rich Media: Supports both local assets (stored in /frontend/assets/) and cloud-hosted assets (Azure Blob Storage) for q_image, a_image, q_sound, and a_sound.

Dynamic Grid Layout: Flashcards use CSS Grid stacking to automatically and smoothly resize based on the length of the question, answer, or image height.

Feedback Loop: Includes a flagging system that sends feedback (via an Azure Function API) so deck creators can correct errors.

Automated Deck Compilation: A built-in Python tool scrapes Wikipedia for high-quality images based on your flashcard answers, uploads them directly to Azure Blob Storage, and rewrites your JSON database automatically.

📂 Project Structure
Plaintext
/FLASHCARDS-DBT
│
├── /.github/workflows/          <-- CI/CD Pipelines
│   ├── frontend_pages.yml       <-- Deploys /frontend to GitHub Pages
│   └── main_flashcard-feedback-logging.yml <-- Deploys /api to Azure Functions
│
├── /api/                        <-- Serverless Backend
│   ├── function_app.py          <-- Azure Function for logging card feedback/flags
│   ├── requirements.txt         <-- Python dependencies for the API
│   └── host.json / local.settings.json
│
├── /frontend/                   <-- The Live Web Application
│   ├── index.html               <-- Main application UI
│   ├── style.css                <-- Styling and responsive grid configurations
│   ├── app.js                   <-- Application logic and state management
│   ├── cards.json               <-- The universal deck database
│   └── /assets/                 <-- Local media fallbacks (sounds/images)
│
├── /other-scripts/              <-- Developer Automation Tools
│   ├── image-scrape-and-json-update.py <-- Scrapes Wikipedia & updates JSON
│   ├── requirements.txt         <-- Dependencies for automation scripts
│   └── .env                     <-- (Ignored by Git) Azure Blob credentials
│
└── README.md
🗃️ The cards.json Database
The entire frontend is driven by frontend/cards.json. This file holds all your decks, cards, and configuration settings.

Deck Structure
Decks are organized by their title and optionally grouped into broad sections. You can also define default sounds at the deck level.

JSON
{
  "decks": {
    "Birds of the World": {
      "section": "Biology & Nature",
      "cards": [ ... ]
    },
    "Azure Developer Associate": {
      "section": "Professional Development",
      "a_sound": "success_chime.mp3", 
      "cards": [ ... ]
    }
  }
}
Card Attributes
Each card inside the cards array supports a wide variety of attributes for text, media, and filtering.

JSON
{
  "q": "Name this bird",
  "a": "Peregrine Falcon",
  "q_image": "peregrine_falcon.jpg",
  "a_image": "https://mystorage.blob.core.windows.net/images/peregrine_dive.jpg",
  "q_sound": "falcon_screech.mp3",
  "a_sound_start": 4,
  "category": "Identification",
  "group": ["Raptors", "Birds of Prey"],
  "difficulty": "Medium",
  "certification": "Ornithology 101"
}
Text: q (Question) and a (Answer) are required.

Media: q_image, a_image, q_sound, a_sound. (If the string starts with http, it streams from the cloud; otherwise, it looks in /frontend/assets/).

Audio Control: q_sound_start / a_sound_start skips intro seconds on audio files.

Filters: category, group (can be an array), difficulty (Easy/Medium/Hard), and certification.

🛠️ Developer Setup & Automation
1. Running the Frontend Locally
Because the app fetches cards.json dynamically, you must serve it via a local web server (opening the HTML file directly in a browser will cause a CORS error).

Open a terminal in the /frontend directory.

Run python -m http.server 8000 (or use the VS Code Live Server extension).

Navigate to http://localhost:8000.

2. Running the Deck Compiler (Image Scraper)
To build visual decks quickly, you can use the included Python automation script. It reads your cards.json, searches Wikipedia for the answer text, uploads the best photos to Azure, and updates the JSON file with the new cloud URLs.

Setup:

Navigate to /other-scripts/.

Install dependencies: pip install -r requirements.txt.

Create a .env file in the /other-scripts/ folder (DO NOT commit this file):

Plaintext
AZURE_CONNECTION_STRING="DefaultEndpointsProtocol=https;AccountName=...;"
AZURE_ACCOUNT_NAME="your_account_name"
Add your new cards to /frontend/cards.json using simple local filenames (e.g., "q_image": "toucan.jpg").

Execution:
Run the script:

Bash
python image-scrape-and-json-update.py
The script will generate an updated_cards.json file in the frontend folder. Verify the contents, delete the old cards.json, and rename the new file to replace it.

3. Deployments
This repository utilizes GitHub Actions for continuous deployment:

Frontend: Pushes to the main branch automatically deploy the /frontend directory to GitHub Pages.

Backend: Pushes to the main branch trigger the deployment of the /api directory to your designated Azure Function App.