# Corelytics - AI Email Generation Engine

An intelligent email generation system that uses structured intent and AI to create natural, context-aware professional emails in seconds.

## 🎯 Features

- ✨ **Hierarchical Taxonomy**: 13 domains spanning academic, professional, legal, healthcare, government, finance, media, and more
- 🧠 **Intelligent Prompting**: Metadata-driven behavioral briefs that prevent generic templates
- 🤖 **AI-Powered**: OpenAI GPT-4 integration for natural language generation
- 🎨 **Beautiful UI**: Vanilla JavaScript + CSS animations with smooth transitions
- ⚡ **Fast & Modular**: Clean separation between backend (Python) and frontend (Vanilla JS)
- 📦 **Optional Scenarios**: Smart handling of both complete and branching communication types
- 🔒 **Error Handling**: Robust logging and error messages throughout

## 📁 Project Structure

```
Corelytics/
│
├── api.py                    # FastAPI application with 4 endpoints ⭐
│
├── core/                     # Backend Logic
│   ├── intent_engine.py      # Orchestrates email generation
│   ├── intent_state.py       # State management model
│   ├── llm_service.py        # OpenAI GPT-4 integration
│   ├── logic_loader.py       # JSON taxonomy loader
│   └── prompt_compiler.py    # Converts intent to behavioral briefs
│
├── data/                     # Data Files
│   └── email_logic_map.json  # 13 domains with hierarchical structure
│
├── ui/                       # Frontend (Vanilla JS)
│   ├── index.html            # Page structure
│   ├── app.js                # API calls & interactivity
│   └── style.css             # Animations & styling
│
├── requirements.txt          # Python dependencies
├── .gitignore                # Files to ignore in Git
├── README.md                 # This file
└── .env                      # ⚠️ NOT TRACKED (create yourself)
```

## 🚀 Installation

### Backend Setup

```bash
# Clone the repository
git clone https://github.com/prince-Sf/Corelytics.git
cd Corelytics

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file with your OpenAI API key
echo OPENAI_API_KEY=sk-your-api-key-here > .env

# Run the server (from root directory)
uvicorn api:app --reload --host 127.0.0.1 --port 8000
```

**Backend API will be at:** `http://127.0.0.1:8000`

### Frontend Setup

Open `ui/index.html` in your browser:

**Option 1: Using VS Code Live Server**
- Right-click `ui/index.html` → **Open with Live Server**

**Option 2: Using Python**
```bash
cd ui
python -m http.server 5500
```

**Frontend will be at:** `http://127.0.0.1:5500`

## 💡 How to Use

1. **Start the backend** (`uvicorn api:app --reload`)
2. **Open the frontend** in your browser
3. **Select** Domain → Recipient → Category → (Optional) Scenario
4. **Click** "Generate Email"
5. **Copy** the generated email and use it!

### Example Flow

```
Sales / Commercial
    → Marketplace
        → Policy & Compliance
            → Marketplace policy clarification
```

## 🔌 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/domains` | GET | Get all available domains |
| `/recipients?domain=<domain>` | GET | Get recipients for a domain |
| `/categories?domain=<domain>&recipient=<recipient>` | GET | Get categories |
| `/scenarios?domain=<domain>&recipient=<recipient>&category=<category>` | GET | Get scenarios |
| `/generate` | POST | Generate email from selection |

### Example Request

```bash
curl -X POST http://127.0.0.1:8000/generate \
  -H "Content-Type: application/json" \
  -d '{
    "domain": "Sales / Commercial",
    "recipient": "Marketplace",
    "category": "Policy & Compliance",
    "scenario": "Marketplace policy clarification"
  }'
```

### Example Response

```json
{
  "status": "success",
  "email": "Subject: Clarification on Marketplace Policies\n\nDear Team,\n\n...",
  "metadata": {
    "domain": "Sales / Commercial",
    "recipient": "Marketplace",
    "category": "Policy & Compliance",
    "scenario": "Marketplace policy clarification",
    "intent_path": "Sales / Commercial → Marketplace → Policy & Compliance → Marketplace policy clarification"
  }
}
```

## 🎓 Architecture Overview

```
┌─────────────────────────────────────┐
│   Frontend (Vanilla JS + CSS)       │
│   - Beautiful interactive UI        │
│   - 4-step wizard interface         │
└──────────────┬──────────────────────┘
               │ JSON Requests
┌──────────────▼──────────────────────┐
│   FastAPI Backend (api.py)          │
│   - 4 main endpoints                │
│   - Dynamic taxonomy navigation     │
└──────────────┬──────────────────────┘
               │
┌──────────────▼─���──────────────────┐
│   Intent Engine + Compiler          │
│   - core/intent_engine.py           │
│   - core/prompt_compiler.py         │
│   - core/logic_loader.py            │
└──────────────┬──────────────────────┘
               │ Behavioral Brief
┌──────────────▼──────────────────────┐
│   LLM Service (core/llm_service.py) │
│   - OpenAI GPT-4 API Integration    │
│   - Natural language generation     │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│   Generated Email (JSON Response)   │
└─────────────────────────────────────┘
```

## 📊 Tech Stack

**Backend:**
- Python 3.8+
- FastAPI
- OpenAI API
- Pydantic
- python-dotenv

**Frontend:**
- HTML5
- CSS3 (with animations)
- Vanilla JavaScript (ES6+)
- No external frameworks!

## 🔑 Environment Variables

Create a `.env` file in the **project root** (same location as `api.py`):

```env
OPENAI_API_KEY=sk-your-openai-api-key-here
```

**⚠️ Important:** Never commit `.env` to GitHub! It's in `.gitignore`

## ✨ Key Innovation: Optional Scenarios

Corelytics intelligently handles two types of scenarios:

1. **Branching Scenarios** - Category has multiple sub-scenarios (shows Step 4)
2. **Leaf Node Scenarios** - Category is complete on its own (skips Step 4)

This design keeps the interface lean while remaining flexible.

## 🛠️ Development

### Running Both Backend & Frontend Locally

**Terminal 1 (Backend):**
```bash
# From project root
source venv/bin/activate
uvicorn api:app --reload
```

**Terminal 2 (Frontend):**
```bash
# From project root
cd ui
python -m http.server 5500
```

Then open `http://127.0.0.1:5500` in your browser.

### Adding New Domains/Scenarios

Edit `data/email_logic_map.json` following this structure:

```json
{
  "id": "unique_id",
  "label": "Human Readable Label",
  "children": [
    {
      "id": "child_id",
      "label": "Child Label",
      "children": [],
      "meta": {
        "intent_focus": "What should the AI focus on?",
        "tone_hint": "What tone to use?",
        "pressure": "high/normal/low",
        "context_hint": "Additional context for the AI"
      }
    }
  ]
}
```

## 📝 Core Components Explained

### 1. **api.py** (Root Directory)
FastAPI application that exposes 4 main endpoints for the taxonomy navigation and email generation.

### 2. **Intent Engine** (`core/intent_engine.py`)
Orchestrates the entire email generation process:
- Takes user selections (domain, recipient, category, scenario)
- Coordinates with PromptCompiler and LLMService
- Returns generated email

### 3. **Prompt Compiler** (`core/prompt_compiler.py`)
Transforms structured intent into a detailed behavioral brief:
- Infers communication archetype
- Applies anti-generic rules (prevents templated language)
- Includes tone guidance
- Sets urgency levels
- Ensures natural, human-like output

### 4. **LLM Service** (`core/llm_service.py`)
Handles OpenAI integration:
- Makes API calls to GPT-4
- Configurable temperature and parameters
- Robust error handling
- Logging for debugging

### 5. **Logic Loader** (`core/logic_loader.py`)
Utility module for loading and parsing the JSON taxonomy:
- Fast hierarchical lookups
- Metadata extraction
- Child node navigation

### 6. **Intent State** (`core/intent_state.py`)
Data model for managing the user's selection state throughout the generation process.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see LICENSE file for details.

## 🙋 Support

For questions or issues:
- Open a [GitHub Issue](https://github.com/prince-Sf/Corelytics/issues)
- Check [GitHub Discussions](https://github.com/prince-Sf/Corelytics/discussions)

## 📈 Roadmap

- [ ] Add 100+ more domains and scenarios
- [ ] User authentication & saved drafts
- [ ] Email templates & custom branding
- [ ] Batch email generation
- [ ] Mobile application
- [ ] Team collaboration features
- [ ] Direct export to Gmail/Outlook
- [ ] API rate limiting & usage analytics

## 👨‍💻 Author

**Safwaan**  
- GitHub: [@prince-Sf](https://github.com/prince-Sf)
- Project: [Corelytics](https://github.com/prince-Sf/Corelytics)

---

Made with ❤️ using Python, FastAPI, and OpenAI GPT-4