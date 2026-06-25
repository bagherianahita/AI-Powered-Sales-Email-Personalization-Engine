# AI-Powered Sales Email Personalization

**Notebook prototype** for B2B sales email personalization using NLP and LLM techniques. Explores RAG-style personalization workflows before production hardening.

![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-F37626?style=flat-square&logo=jupyter&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python&logoColor=white)

---

## Architecture (target production design)

```
┌─────────────┐   enrich    ┌──────────────┐   retrieve   ┌─────────────┐
│ CRM / lead  │ ──────────► │  NLP extract │ ───────────► │ Vector DB   │
│ profile     │             │  (spaCy)     │              │ (Pinecone)  │
└─────────────┘             └──────────────┘              └──────┬──────┘
                                                                 │ RAG
┌─────────────┐   email     ┌──────────────┐ ◄──────────────────┘
│ Sales rep   │ ◄────────── │  GPT-4 draft │
└─────────────┘             └──────────────┘
```

> **Note:** This repo contains **Jupyter notebooks** (`AI_Powered_Sales_Email_Personalization_Engine.ipynb`) as the current implementation. The architecture above reflects the intended production microservice design.

---

## Quick start (employers — no API keys)

```bash
pip install -r requirements.txt
streamlit run app.py --server.port 8503
```

Generates sample personalized B2B emails for two demo leads.

| | URL |
|---|-----|
| **Web UI** | _N/A — terminal demo_ |
| **API** | _N/A_ |

---

## License

MIT — see [LICENSE](LICENSE).
