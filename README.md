# AI-Powered Sales Email Personalization

**Notebook prototype** for B2B sales email personalization using NLP and LLM techniques. Explores RAG-style personalization workflows before production hardening.
<img width="1764" height="548" alt="image" src="https://github.com/user-attachments/assets/f049ae1a-5701-4cb8-801f-4b64157e4516" />

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
streamlit run app.py
```

Opens a **browser demo** with three sample leads. Click **Generate email** — works instantly without API keys. Optional: set `OPENAI_API_KEY` and enable **Use OpenAI** in the sidebar.

| | URL |
|---|-----|
| **Web UI (demo)** | http://localhost:8504 |
| **Terminal demo** | `python demo.py` |

> Default port is **8504** (configured in `.streamlit/config.toml`). Use `--server.port 8502` if another app is using 8504.

---

## License

MIT — see [LICENSE](LICENSE).
