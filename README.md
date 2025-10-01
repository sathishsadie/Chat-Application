# Kitchen Management AI 🧑‍🍳

Welcome to **Kitchen Management AI**, an interactive AI assistant for managing your kitchen! This AI can:

- Check if you have all the ingredients needed for popular recipes.
- Suggest which items are missing and need to be bought.
- Simulate buying missing items and update kitchen stock.
- Guide you to cook 3 supported recipes: **Curd Rice, Lemon Rice, and Tomato Rice**.

---

## Features

- **Ingredient Checker:** Ensures you have all ingredients for a recipe.
- **Buy Items Tool:** Allows you to "buy" missing ingredients and updates stock.
- **Interactive Chat:** Chat interface powered by React + TailwindCSS.
- **AI-Powered Guidance:** Backend powered by FastAPI & LangChain with Gemini LLM.

---

## Project Structure

```

frontend/
│
├─ public/
│  └─ vite.svg
├─ src/
│  ├─ assets/
│  │  └─ react.svg
│  ├─ App.css
│  ├─ App.tsx
│  ├─ index.css
│  └─ main.tsx
├─ package.json
├─ tsconfig.json
└─ tailwind.config.js

backend/
├─ app.py
├─ requirements.txt (optional)
└─ .env

````

---

## Prerequisites

- Node.js & npm
- Python 3.10+
- FastAPI, LangChain, `langchain_google_genai`, `fastapi`, `uvicorn`, `python-dotenv`, `langdetect`
- Gemini API key (from Google Cloud / Gemini AI)

---

## Setup Instructions

### Backend

1. Navigate to the backend folder:

```bash
cd backend
````

2. Install Python dependencies:

```bash
pip install fastapi uvicorn python-dotenv langchain langchain-google-genai langdetect
```

3. Create a `.env` file in the backend folder and add your Gemini API key:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

4. Run the FastAPI server:

```bash
uvicorn app:app --reload
```

Backend will run on `http://127.0.0.1:8000`.

---

### Frontend

1. Navigate to the frontend folder:

```bash
cd frontend
```

2. Install dependencies:

```bash
npm install
```

3. Start the development server:

```bash
npm run dev
```

Frontend will run on `http://localhost:5173` (Vite default port).

---

## How to Use

1. Open the frontend URL in your browser.
2. Type a message to interact with Kitchen AI, such as:

   * `"Check ingredients for Lemon Rice"`
   * `"Buy lemon and green chili"`
   * `"Guide me to cook Curd Rice"`
3. The AI will:

   * Respond with available/missing ingredients.
   * Suggest buying items if missing.
   * Confirm updated stock when items are bought.

---

## Technologies Used

* **Frontend:** React + TypeScript + TailwindCSS
* **Backend:** FastAPI + Python
* **AI/Tools:** LangChain, Gemini AI (via Google Generative AI)
* **State Management:** Local React state
* **Markdown Rendering:** `marked` library

---

## AI Capabilities

* Can check ingredients for 3 recipes: Curd Rice, Lemon Rice, Tomato Rice.
* Can suggest missing items and simulate buying.
* Uses LLM to respond conversationally and provide cooking guidance.
* Detects HTML/Markdown tables in responses to display neatly in chat.

---

## Screenshots

![Kitchen Management AI](./frontend/src/assets/react.svg)

---

## License

This project is licensed under the MIT License.
