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

```
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
```

🗃️ The cards.json Database
The entire frontend is driven by frontend/cards.json. This file holds all your decks, cards, and configuration settings.

Deck Structure
📝 Configuring Your Data (cards.json)
All flashcards and decks are managed inside the cards.json file. The file is structured as a single decks object, where each key represents the name of a deck.

📂 Deck-Level Properties
These settings apply to the entire deck.

  - cards (Array, Required): The list of flashcard objects that belong to this deck.
  - section (String, Optional): Groups the deck under a specific heading on the main Deck Picker screen (e.g., "Professional Development"). Defaults to "Other" if omitted.
  - q_image / a_image (String, Optional): Sets a default image to display on the front (q_image) or back (a_image) of every card in this deck.
  - q_sound / a_sound (String, Optional): Sets a default audio file to play when viewing the front or flipping to the back of every card.
  - q_sound_start / a_sound_start (Number, Optional): The timestamp (in seconds) where the default deck audio should begin playing.

🃏 Card-Level Properties
These settings are placed inside individual card objects within the cards array.

Core Content

  - q (String, Required): The question text shown on the front of the card. Supports standard text, inline code (`code`), and multi-line code blocks (```code```).
  - a (String, Required): The answer text shown on the back of the card. Supports the same formatting as the question.

Filtering & Meta Tags

  - category (String, Optional): The primary topic of the card. Populates the top row of filter chips.
  - group (String or Array, Optional): A sub-topic (or multiple sub-topics). Populates the second row of filter chips (only appears after a category is selected).
  - difficulty (String, Optional): Generates colored meta-tags on the cards. Must be "Easy", "Medium", or "Hard".
  - certification (String, Optional): If any cards in a deck include this field, the app will automatically generate an intermediate "Choose a certification" screen before the study session.

Media & Interactivity

  - requires_code (Boolean, Optional): Set to true to display a code-editor text area beneath the card, allowing users to draft their answer before flipping.
  - q_image / a_image (String, Optional): A specific image for this card. Overrides the deck-level default.
  - q_sound / a_sound (String, Optional): Specific audio for this card. Overrides the deck-level default.
  - q_sound_start / a_sound_start (Number, Optional): The timestamp (in seconds) to start this card's specific audio.

```
{
  "decks": {
    "Python Basics": {
      "section": "Programming",
      "cards": [
        {
          "q": "Write a Python function to reverse a string.",
          "a": "```python\ndef reverse_string(s):\n    return s[::-1]\n```",
          "category": "Strings",
          "difficulty": "Medium",
          "requires_code": true
        }
      ]
    }
  }
}
```

💡 Note on Media Files: For images and audio, you can provide either a local filename (e.g., "eagle.jpg") which the app will look for in the /assets/ folder, or a full cloud URL (e.g., "https://example.com/audio.mp3").

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