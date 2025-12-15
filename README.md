# PerrenialSponsorPrep

A comprehensive hackathon preparation toolkit with 46+ sponsor technology examples, extensive guides, and an interactive planning tool.

## Quick Start

### Run the Documentation Viewer

```bash
cd viewer
npm install
npm run dev
```

Then open http://localhost:5173 in your browser.

### Browse Submissions

Each of the 46 submissions is a standalone project showcasing a sponsor's latest API features:

```bash
cd submissions/01-openai-realtime-voice
cp .env.example .env          # Add your API key
pip install -r requirements.txt
python main.py
```

## What's Included

### Interactive Viewer (`viewer/`)

A Svelte-based web app with two modes:

- **Docs Mode** - Browse 17 comprehensive guides organized by category (Ideas, Guides, AI Agents, Resources, Reference)
- **100 Questions Mode** - A questionnaire to help think through your hackathon project, with auto-save and export

### 46 Sponsor Submissions (`submissions/`)

Ready-to-run examples demonstrating the latest features from major sponsors:

| Category | Sponsors |
|----------|----------|
| LLM Providers | OpenAI, Anthropic, Google Gemini, Meta Llama, Mistral, Cohere, Replicate |
| Vector DBs | Pinecone, Weaviate, Qdrant, Chroma |
| Databases | Supabase, Neon, MongoDB, PlanetScale, Upstash, Firebase |
| Frameworks | LangChain, LlamaIndex, CrewAI, AutoGen, Haystack |
| Platforms | Vercel, Streamlit, Gradio |
| Auth | Clerk, Auth0, Okta |
| Payments | Stripe, Plaid, PayPal |
| Communication | Slack, Discord, Twilio, SendGrid |
| Dev Tools | GitHub, Docker, HuggingFace, GitLab |
| Cloud | AWS, Google Cloud, Azure, Cloudflare |
| E-commerce | Shopify, Algolia, Mapbox |

See [`submissions/README.md`](submissions/README.md) for the full list with status.

### Documentation Guides (Root `.md` files)

| Guide | Description |
|-------|-------------|
| `sponsor_combinations_ideas.md` | 455 sponsor combination ideas |
| `100_local_ai_usecases_4gb.md` | 100 AI use cases for 4GB machines |
| `free_tier_services.md` | Complete list of free services for hackathons |
| `local_ai_guide.md` | Running AI models locally |
| `autonomous_coding_agents.md` | Overview of AI coding assistants |
| `hackathon_platforms_guide.md` | Guide to hackathon platforms |
| `github_free_tools_guide.md` | Leveraging GitHub for hackathons |
| `ai_video_generation_guide.md` | AI video creation techniques |
| And more... | |

## Project Structure

```
PerrenialSponsorPrep/
├── viewer/                    # Svelte + Vite documentation viewer
│   ├── src/
│   │   ├── App.svelte        # Main app with docs browser
│   │   └── Questionnaire.svelte  # 100 Questions tool
│   └── public/docs/          # Markdown files for viewer
├── submissions/              # 46 sponsor example projects
│   ├── 01-openai-realtime-voice/
│   ├── 02-anthropic-computer-use/
│   └── ...
├── *.md                      # Documentation guides
└── README.md                 # This file
```

## Using for Hackathons

1. **Pick your sponsors** - Review `sponsor_combinations_matrix.md` for synergy ratings
2. **Answer the 100 Questions** - Use the questionnaire to plan your project
3. **Start from a template** - Copy a submission as your starting point
4. **Combine technologies** - Mix multiple submissions for multi-sponsor prizes

Example combinations:
- OpenAI + Pinecone + Vercel = RAG Chat App
- Anthropic + Supabase + Clerk = Protected AI Dashboard
- Gemini + Neon + Streamlit = AI Data Explorer

## Requirements

- Node.js 18+ (for viewer)
- Python 3.9+ (for most submissions)
- API keys for sponsors you want to use

## License

MIT 
