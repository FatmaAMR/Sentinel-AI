```
sentinel-ai/
├── backend/                # FastAPI Application
│   ├── app/
│   │   ├── api/            # Route handlers (Endpoints)
│   │   ├── core/           # Config, Security, Constants
│   │   ├── crud/           # Database operations (Create, Read, Update, Delete)
│   │   ├── models/         # SQLAlchemy/Database schemas
│   │   ├── schemas/        # Pydantic models (Data validation)
│   │   ├── services/       # THE AI BRAIN (RAG Logic, LLM Wrappers)
│   │   └── main.py         # Entry point
│   ├── data/               # SQLite DB file & Raw PDFs
│   ├── chromadb/           # Vector Database storage
│   ├── tests/              # Unit tests for the AI pipeline
│   ├── requirements.txt
│   └── .env                # HF_TOKEN, DB_URL
├── frontend/               # React Application (Vite-based)
│   ├── src/
│   │   ├── assets/         # Images, Icons
│   │   ├── components/     # Reusable UI (Charts, Cards, Buttons)
│   │   ├── hooks/          # Custom API fetching hooks
│   │   ├── pages/          # Dashboard, Diagnosis, History
│   │   ├── services/       # API client (Axios/Fetch)
│   │   └── App.jsx
│   ├── package.json
│   └── tailwind.config.js  # Highly recommend Tailwind for styling
├── scripts/                # Utility scripts (Mai's Log Generator)
└── README.md

```