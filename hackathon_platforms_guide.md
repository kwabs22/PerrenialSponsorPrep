# Hackathon Platforms Guide

> Comprehensive guide to hackathon platforms, APIs, submission guides, and free credits.

---

## Platform Comparison

| Platform | Focus | API Available | Free Credits | Submission Guide |
|----------|-------|---------------|--------------|------------------|
| **Devpost** | General hackathons | Unofficial only | Via sponsors | Yes |
| **HuggingFace** | AI/ML competitions | Official (huggingface_hub) | Yes ($25+) | Yes |
| **Kaggle** | Data science/ML | Official CLI | Compute credits | Yes |
| **DoraHacks** | Web3/AI/Blockchain | BUIDL platform | Via sponsors | Yes |
| **HackerEarth** | Corporate/Coding | Official API | Via sponsors | Yes |
| **lablab.ai** | AI hackathons | No public API | Yes (extensive) | Yes |
| **MLH** | Student hackathons | No public API | Via sponsors | Comprehensive |
| **Unstop** | India-focused | Limited | Via sponsors | Yes |

---

## 1. Devpost

**Website:** https://devpost.com

### Overview
The most popular hackathon platform globally, hosting thousands of events annually.

### API Access
- **Official API:** None publicly available
- **Unofficial APIs:**
  - [ViRb3/devpost-api](https://github.com/ViRb3/devpost-api) - Scrapes user profiles and projects
  - Lambda-based scrapers for custom solutions

### Submission Guide
- [MLH Guide to Using Devpost](https://guide.mlh.io/general-information/judging-and-submissions/hackathon-submission-portal/using-devpost)
- Required: Project name, description, demo video, GitHub link
- Export: CSV export available for organizers

### Free Credits
Credits come from individual hackathon sponsors, not Devpost itself.

---

## 2. HuggingFace Spaces & Competitions

**Website:** https://huggingface.co

### Overview
Growing platform for AI/ML hackathons with integrated model hosting.

### API Access
```bash
pip install huggingface_hub
```

```python
from huggingface_hub import HfApi
api = HfApi()

# List spaces
api.list_spaces()

# Upload to space
api.upload_file(
    path_or_fileobj="app.py",
    path_in_repo="app.py",
    repo_id="username/my-space",
    repo_type="space"
)
```

### Current Hackathons (2024-2025)
- **Agents-MCP-Hackathon** - $16,500 prizes, 4100+ registrations
- **MCP 1st Birthday** - $21K+ prizes, 7100+ registrations
- **LeRobot Worldwide** - AI robotics focus
- **Gradio Hackathons** - UI/demo focused

### Free Credits
| Provider | Amount | Availability |
|----------|--------|--------------|
| HuggingFace | $25 | All participants |
| Nebius | $25 | First 3300 |
| Anthropic | $25 | First 1000 |
| OpenAI | $25 | First 1000 |

### Submission Guide
- [Competition Space Documentation](https://github.com/huggingface/competitions/blob/main/docs/source/competition_space.mdx)
- Submit via Gradio Space or model upload
- Automatic leaderboard scoring

---

## 3. Kaggle

**Website:** https://kaggle.com

### Overview
Premier platform for data science and ML competitions with robust API.

### API Access
```bash
pip install kaggle
```

**Authentication:**
1. Go to kaggle.com → Account → Create New API Token
2. Save `kaggle.json` to `~/.kaggle/`

**Commands:**
```bash
# List competitions
kaggle competitions list

# Download data
kaggle competitions download -c competition-name

# Submit
kaggle competitions submit -c competition-name -f submission.csv -m "My submission"

# View submissions
kaggle competitions submissions -c competition-name

# Leaderboard
kaggle competitions leaderboard -c competition-name
```

**Python API:**
```python
from kaggle.api.kaggle_api_extended import KaggleApi

api = KaggleApi()
api.authenticate()

# List competitions
api.competitions_list()

# Submit
api.competition_submit(
    file_name='submission.csv',
    message='My submission',
    competition='titanic'
)
```

### Free Credits
- Free GPU/TPU notebooks (30 hrs/week GPU, 20 hrs/week TPU)
- No external API credits

### Resources
- [Official API Documentation](https://www.kaggle.com/docs/api)
- [GitHub Repository](https://github.com/Kaggle/kaggle-api)
- [Competition API Tutorial](https://www.kaggle.com/code/sohier/competition-api-detailed-introduction)

---

## 4. DoraHacks

**Website:** https://dorahacks.io

### Overview
Leading Web3 and frontier-tech hackathon platform with quadratic funding.

### Platform Features
- **BUIDL AI 2.5** - AI-powered evaluation
  - Code review and analysis
  - Plagiarism detection
  - Team background vetting
  - 10+ scoring criteria

### API/Integration
- BUIDL submission platform
- Quadratic funding rounds
- Grant programs integration

### Stats
- 21,000+ startup teams
- $80M+ in funding distributed
- Focus: Blockchain, Web3, Quantum, AI, Space-Tech

### Recent Hackathons
- AWS Global Vibe: $700K+ prize pool
- Cronos x402: $42,000 prizes
- Hack-a-TONx: 230 submissions
- Circle Developer Bounties: 1500 USDC per track

### Submission Guide
- [Hackathon Page](https://dorahacks.io/hackathon)
- Submit via BUIDL platform
- Include: Demo, code repo, documentation

---

## 5. HackerEarth

**Website:** https://hackerearth.com

### Overview
Enterprise hackathon platform popular for corporate challenges.

### API Access
```
POST /challenges/{challenge_id}/submissions
GET /challenges/{challenge_id}/leaderboard
```

**Response format:**
```json
{
  "leaderboard": [
    {"rank": 1, "username": "coder1", "score": 100},
    {"rank": 2, "username": "coder2", "score": 95}
  ]
}
```

### Features
- Automated leaderboards
- Code evaluation
- Filter by country, school, company
- Practice problems

### Active Hackathons
- Shell.ai Hackathon (annual)
- Microsoft Azure Champions League
- EmpowerX Challenge

### Resources
- [HackerEarth API](https://publicapi.dev/hackerearth-api)
- [Challenges Page](https://www.hackerearth.com/challenges/)

---

## 6. lablab.ai

**Website:** https://lablab.ai

### Overview
AI-focused hackathon platform with extensive sponsor credits.

### Free Credits (Examples)
| Hackathon | Credits Available |
|-----------|-------------------|
| AI21 Labs | $9000 API + $3500 cash |
| AI Agents | $3000 Upstage, $2500 Together AI |
| OpenAI Events | $2000 DigitalOcean |
| Llama Events | Up to $100K grants |

### Submission Guide
- [Official Submission Guidelines](https://lablab.ai/delivering-your-hackathon-solution)
- Account required
- Certificate of completion included

### Benefits
- All events free to participate
- No AI experience required
- Domain experts welcome
- Project showcased on blog/newsletter

### Browse Apps
- [Discover AI Applications](https://lablab.ai/apps)

---

## 7. MLH (Major League Hacking)

**Website:** https://mlh.io

### Overview
Student-focused hackathon league with comprehensive organizer resources.

### Submission Requirements
1. **Demo Video:** 2 minutes or less
2. **Code Repository:** Must be public
3. **README:** Detailed explanation
4. **AI Usage:** Credit all tools used

### Judging Style
"Science fair" format - teams at assigned tables, judges rotate.

### Resources
- [Hackathon Organizer Guide](https://guide.mlh.io)
- [Judging and Submissions](https://guide.mlh.io/general-information/judging-and-submissions)
- [GitHub: Organizer Guide](https://github.com/MLH/mlh-hackathon-organizer-guide)
- [Rules for Hackathons](https://guide.mlh.io/general-information/judging-and-submissions/rules-for-your-hackathon)

### Free Credits
Distributed via email to MLH event participants. Check for:
- Google Cloud credits
- AWS credits
- Domain names
- Various sponsor perks

### Contact
league@mlh.io

---

## 8. Other Notable Platforms

### Unstop (formerly Dare2Compete)
- **Website:** https://unstop.com
- **Focus:** India, recruitment hackathons
- **Features:** Skill assessments, gamified hiring

### Agorize
- **Website:** https://agorize.com
- **Focus:** Enterprise innovation
- **Stats:** 10M+ innovators, 7000+ programs

### TAIKAI
- **Website:** https://taikai.network
- **Focus:** Corporate innovation
- **Features:** Connect companies with developers

### Eventornado
- **Website:** https://eventornado.com
- **Focus:** User experience
- **Features:** First-timer friendly

### Hack Club
- **Website:** https://hackathons.hackclub.com
- **Focus:** High school students
- **Features:** Mentorship, workshops

---

## Cloud Provider Free Credits

### Google Cloud
| Program | Amount | Requirements |
|---------|--------|--------------|
| AI Startup Program | Up to $350,000 | AI-first, Seed to Series A |
| Year 1 | $250,000 | Application required |
| Year 2 | $100,000 | + 20% discount |
| MLH Events | Varies | Check MLH email |

**Apply:** [Google Cloud for Startups](https://cloud.google.com/startup)

### AWS
| Program | Amount | Requirements |
|---------|--------|--------------|
| Activate Founders | $1,000 | New startups |
| Activate Portfolio | $5,000-$100,000+ | Via accelerator/VC |
| Hackathon Credits | $100 | First-come basis |

**Apply:** [AWS Activate](https://aws.amazon.com/activate/)

### Microsoft Azure
| Program | Amount | Requirements |
|---------|--------|--------------|
| Founders Hub | $1,000 | New Azure customer |
| Startups | Up to $150,000 | Application required |

**Apply:** [Microsoft for Startups](https://www.microsoft.com/en-us/startups)

### Pro Tip: Stack Credits
You can use multiple programs simultaneously:
- Azure for OpenAI models (GPT-4)
- Google Cloud for Gemini
- AWS Bedrock for Claude

---

## Submission Best Practices

### Video Demo
- **Length:** 2-3 minutes max
- **Content:** Problem → Solution → Demo → Impact
- **Tools:** Loom, OBS, or screen recording

### README Structure
```markdown
# Project Name

## Inspiration
What problem are you solving?

## What it does
Brief description of functionality

## How we built it
Tech stack and architecture

## Challenges we ran into
Honest about difficulties

## Accomplishments
What are you proud of?

## What we learned
Skills gained

## What's next
Future roadmap

## Built With
- technology-1
- technology-2

## Try it out
- [Demo Link](url)
- [Video](url)
```

### Sponsor Integration
- Mention specific sponsor features used
- Link to sponsor documentation
- Show API/SDK integration in code

---

## API Summary Table

| Platform | Auth Method | Rate Limits | Documentation |
|----------|-------------|-------------|---------------|
| Kaggle | API Token (JSON) | Standard | [Docs](https://www.kaggle.com/docs/api) |
| HuggingFace | API Token | Standard | [Docs](https://huggingface.co/docs/huggingface_hub) |
| HackerEarth | API Key | Contact | [PublicAPI](https://publicapi.dev/hackerearth-api) |
| Devpost | N/A (unofficial) | Scraping limits | [Unofficial](https://github.com/ViRb3/devpost-api) |
| DoraHacks | Platform-based | N/A | [BUIDL](https://dorahacks.io/buidl) |

---

## Quick Links

### Find Hackathons
- [Devpost Hackathons](https://devpost.com/hackathons)
- [MLH Season](https://mlh.io/seasons/2025/events)
- [DoraHacks Events](https://dorahacks.io/hackathon)
- [HackerEarth Challenges](https://www.hackerearth.com/challenges/)
- [lablab.ai Events](https://lablab.ai/event)
- [Unstop Hackathons](https://unstop.com/hackathons)

### Submission Platforms
- [Devpost](https://devpost.com)
- [Devfolio](https://devfolio.co)
- [HuggingFace Spaces](https://huggingface.co/spaces)

### Learning Resources
- [MLH Organizer Guide](https://guide.mlh.io)
- [Kaggle Learn](https://www.kaggle.com/learn)
- [HuggingFace Course](https://huggingface.co/learn)

---

*Last Updated: December 2024*
