# Hackathon Platforms Guide

> Comprehensive guide to 40+ hackathon platforms, APIs, submission guides, scrapers, and free credits worldwide.

---

## Platform Comparison (Major Platforms)

| Platform | Focus | API Available | Free Credits | Region |
|----------|-------|---------------|--------------|--------|
| **Devpost** | General hackathons | Unofficial scrapers | Via sponsors | Global |
| **HuggingFace** | AI/ML competitions | Official (`huggingface_hub`) | Yes ($25+) | Global |
| **Kaggle** | Data science/ML | Official CLI + Python | Compute credits | Global |
| **DoraHacks** | Web3/AI/Blockchain | BUIDL platform | Via sponsors | Global |
| **HackerEarth** | Corporate/Coding | Official REST API | Via sponsors | Global |
| **lablab.ai** | AI hackathons | No public API | Yes (extensive) | Global |
| **MLH** | Student hackathons | No public API | Via sponsors | Global |
| **ETHGlobal** | Ethereum/Web3 | Showcase platform | Via sponsors | Global |
| **Devfolio** | Web3/General | Platform-based | Via sponsors | India |
| **AngelHack** | Corporate/Enterprise | StackUp platform | Via sponsors | Asia/Global |
| **Unstop** | Recruitment | Limited | Via sponsors | India |
| **Product Hunt** | Maker launches | No API | Via sponsors | Global |

---

## Devpost Scrapers & Data Extraction

Since Devpost has no official API, here are community tools:

### GitHub Scrapers

| Repository | Description | Language |
|------------|-------------|----------|
| [lasamson/devpost-scraper](https://github.com/lasamson/devpost-scraper) | Collects submission data from any hackathon page → CSV | Python |
| [jayrav13/devpost-scraper](https://github.com/jayrav13/devpost-scraper) | Scrapes all project submissions (65,000+ projects) | Python |
| [HackNC/DevGET](https://github.com/HackNC/DevGET) | Chrome extension for organizers to export judging CSVs | JavaScript |
| [ViRb3/devpost-api](https://github.com/ViRb3/devpost-api) | REST API wrapper via Docker | Go |

### Usage Example (lasamson/devpost-scraper)
```bash
git clone https://github.com/lasamson/devpost-scraper
cd devpost-scraper
pip install -r requirements.txt
python scraper.py https://hackathon-name.devpost.com
# Outputs: submissions.csv
```

### Key Insight from jayrav13
> "DevPost scans the client's User Agent and recognizes that this request is NOT coming from a browser, thus returning a JSON object of all of the projects on that given page."

---

## Platform Deep Dives

### 1. Devpost
**Website:** https://devpost.com

- **Founded:** 2009 (as ChallengePost)
- **Stats:** Thousands of hackathons hosted annually
- **API:** None official - use scrapers above
- **Export:** CSV export for organizers only
- **Submission:** Project name, description, video, GitHub link

---

### 2. HuggingFace
**Website:** https://huggingface.co

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

**Current Hackathons:**
- Agents-MCP-Hackathon - $16,500 prizes
- MCP 1st Birthday - $21K+ prizes, 7100+ registrations
- LeRobot Worldwide - AI robotics

**Free Credits per Event:**
| Provider | Amount | Availability |
|----------|--------|--------------|
| HuggingFace | $25 | All participants |
| Nebius | $25 | First 3300 |
| Anthropic | $25 | First 1000 |
| OpenAI | $25 | First 1000 |

---

### 3. Kaggle
**Website:** https://kaggle.com

**Full API Access:**
```bash
pip install kaggle

# Authentication: Save kaggle.json to ~/.kaggle/

kaggle competitions list
kaggle competitions download -c competition-name
kaggle competitions submit -c name -f file.csv -m "message"
kaggle competitions submissions -c name
kaggle competitions leaderboard -c name
```

**Free Resources:**
- 30 hrs/week GPU notebooks
- 20 hrs/week TPU notebooks

**Documentation:**
- [Official API Docs](https://www.kaggle.com/docs/api)
- [GitHub: kaggle-api](https://github.com/Kaggle/kaggle-api)

---

### 4. DoraHacks
**Website:** https://dorahacks.io

**Stats:**
- 21,000+ startup teams
- $80M+ funding distributed
- Focus: Web3, Quantum, AI, Space-Tech

**BUIDL AI 2.5 Features:**
- Code review and analysis
- Plagiarism detection
- Team background vetting
- 10+ scoring criteria

**Recent Prize Pools:**
- AWS Global Vibe: $700K+
- Cronos x402: $42,000
- Circle Bounties: 1500 USDC/track

---

### 5. ETHGlobal
**Website:** https://ethglobal.com

**Stats (ETHGlobal New York):**
- 1400 attendees, 950 hackers
- 49 countries represented
- 33% new to Web3
- 303 submissions, $500K+ prizes

**Submission Requirements:**
- 2-4 minute demo video
- Public repository
- All work must start after hackathon begins
- Evaluated on: creativity, functionality, technical difficulty, impact

**Upcoming:**
- ETHGlobal Buenos Aires (Nov 2025): $500K prizes

---

### 6. lablab.ai
**Website:** https://lablab.ai

**All events FREE to participate**

**Credit Examples:**
| Event | Credits |
|-------|---------|
| AI21 Labs | $9000 API + $3500 cash |
| AI Agents | $3000 Upstage + $2500 Together AI |
| Llama Events | Up to $100K grants |

**Resources:**
- [Submission Guidelines](https://lablab.ai/delivering-your-hackathon-solution)
- [Browse Apps](https://lablab.ai/apps)

---

### 7. MLH (Major League Hacking)
**Website:** https://mlh.io

**Submission Requirements:**
1. Demo Video: ≤2 minutes
2. Public code repository
3. Detailed README
4. Credit all AI tools used

**Resources:**
- [Organizer Guide](https://guide.mlh.io)
- [GitHub: mlh-hackathon-organizer-guide](https://github.com/MLH/mlh-hackathon-organizer-guide)
- [Judging Plan](https://guide.mlh.io/general-information/judging-and-submissions/judging-plan)

---

### 8. HackerEarth
**Website:** https://hackerearth.com

**API Endpoints:**
```
POST /challenges/{challenge_id}/submissions
GET /challenges/{challenge_id}/leaderboard
```

**Documentation:** [PublicAPI.dev](https://publicapi.dev/hackerearth-api)

---

## Regional & Specialized Platforms

### India
| Platform | Website | Focus |
|----------|---------|-------|
| **Devfolio** | devfolio.co | India's largest builder community, ETHIndia host |
| **Unstop** | unstop.com | Recruitment hackathons, skill assessments |
| **Hack2Skill** | hack2skill.com | Corporate challenges |

### Europe
| Platform | Website | Focus |
|----------|---------|-------|
| **Junction** | hackjunction.com | Europe's leading hackathon (Finland) |
| **JunctionApp** | github.com/hackjunction | Open source organizer platform |
| **HackZurich** | hackzurich.com | Switzerland's largest |

### Asia
| Platform | Website | Focus |
|----------|---------|-------|
| **AngelHack** | angelhack.com | 250+ events in 100+ cities, StackUp platform |
| **TAIKAI** | taikai.network | Corporate innovation |

### Web3/Blockchain
| Platform | Website | Focus |
|----------|---------|-------|
| **ETHGlobal** | ethglobal.com | Ethereum hackathons worldwide |
| **Gitcoin** | gitcoin.co | Grants + bounties |
| **DoraHacks** | dorahacks.io | Quadratic funding |

### Hardware/Maker
| Platform | Website | Focus |
|----------|---------|-------|
| **Hackaday.io** | hackaday.io | World's largest hardware community |
| **Hackster.io** | hackster.io | Hardware learning community |
| **Instructables** | instructables.com | DIY projects |

### Enterprise/Corporate
| Platform | Website | Focus |
|----------|---------|-------|
| **Agorize** | agorize.com | 10M+ innovators, 7000+ programs |
| **HackHQ** | hackhq.co | Internal corporate hackathons |
| **Mettl Xathon** | mettl.com | Recruitment + team building |

---

## Event Discovery Platforms

| Platform | Website | Description |
|----------|---------|-------------|
| **Luma** | lu.ma/hackathons | Event discovery + hosting for tech |
| **Hackalist** | hackalist.org | Curated upcoming hackathons |
| **Hack Club** | hackathons.hackclub.com | High school focused |
| **Devpost** | devpost.com/hackathons | Largest directory |
| **MLH** | mlh.io/seasons/2025/events | Student events |

---

## AI-Powered Builder Platforms

### Bolt.new (World's Largest Hackathon)
**Website:** https://bolt.new

- **Prize Pool:** $1,000,000+
- **Powered by:** Claude Sonnet 3.5
- **Requirement:** Build NEW app primarily with Bolt.new
- **Awards Ceremony:** [bolt.new/awards](https://bolt.new/awards)

### Replit
**Website:** https://replit.com

- Browser-based IDE
- Real-time collaboration
- Built-in deployment
- Great for hackathon teams

### Buildspace (Closed)
**Website:** buildspace.so (archived)

- Was "largest accelerator in the world"
- 30,000+ participants in Nights & Weekends
- $100K grand prize
- Backed by a16z and YC
- **Status:** Closed after Season 5

---

## Product Hunt Hackathons
**Website:** https://producthunt.com

**Global Hackathon Stats:**
- 4,500+ makers
- 124 countries
- $250,000 in prizes

**Judging:** 50% product/idea, 50% technical

**Tools:**
- [Hackathon Match](https://www.producthunt.com/products/hackathon-match) - Team matching for PH hackathons

---

## Kiroween 2025 (Case Study)

> From [kiro.dev/blog/kiroween-2025](https://kiro.dev/blog/kiroween-2025/)

**Event:** Kiro's inaugural annual hackathon
**Dates:** Oct 31 - Dec 5, 2025
**Prize Pool:** $100,000 across 12 categories (66 winners)
**Top Prize:** $30,000

### Challenge Categories
1. **Resurrection** - Bring dead technology back to life
2. **Frankenstein** - Combine incompatible technologies
3. **Skeleton Crew** - Build reusable code templates
4. **Costume Contest** - Polished interfaces with spooky design

### Submission Requirements
- Public repo with `.kiro` directory
- Functional application URL
- 3-minute demo video
- Documentation showing: specs, hooks, steering, MCP usage

### Judging Criteria
- **Potential Value** - Usefulness and impact
- **Implementation** - Effective Kiro capability leverage
- **Quality and Design** - Creativity and polish

### Perks
- Kiro Pro+ tier access during competition
- Discord support with bi-weekly office hours

---

## Winning Strategies (from Serial Winners)

### Focus on ONE Feature
> "What you need is a single feature that your application focuses on and does extremely well. The winning submissions are the projects that have a single idea that is coherent, defined, and well-implemented."

### Pitch > Perfect Code
> "Judges care more about your business proposition than the technical functionality. The only parts of the software that need to work are the parts used in your pitch."

### Preparation Tips
1. **Install libraries beforehand** - Biggest time waster
2. **Create a faux deadline** - Finish early for buffer
3. **Research judges and sponsors** - Tailor your project
4. **Meet the API Evangelist** - Get validation + help

### Presentation Tips
- Perform a skit demonstrating the pain point
- Do an interactive demo
- Involve the audience
- Keep it under 3 minutes

### Team Composition
> "Team chemistry and makeup is one of the most important factors not only in winning, but also in making sure that you don't burn out."

Ideal team: Programmers + Designers + Project Managers + Visionaries

---

## Cloud Credits Summary

### Google Cloud
| Program | Amount |
|---------|--------|
| AI Startup Program | Up to $350,000 |
| Year 1 | $250,000 |
| Year 2 | $100,000 + 20% discount |

### AWS
| Program | Amount |
|---------|--------|
| Activate Founders | $1,000 |
| Activate Portfolio | $5,000-$100,000+ |
| Hackathon Credits | $100 (first-come) |

### Microsoft Azure
| Program | Amount |
|---------|--------|
| Founders Hub | $1,000 |
| Startups Program | Up to $150,000 |

### Pro Tip: Stack Credits
Use multiple providers simultaneously:
- Azure for GPT-4
- Google Cloud for Gemini
- AWS Bedrock for Claude

---

## Awesome Lists & Resources

### GitHub Awesome Lists
- [dribdat/awesome-hackathon](https://github.com/dribdat/awesome-hackathon) - Platforms, tools, guides
- [mbiesiad/awesome-hackathons](https://github.com/mbiesiad/awesome-hackathon) - Global hackathon list
- [HappyHackingSpace/awesome-hackathon](https://github.com/HappyHackingSpace/awesome-hackathon) - Tools to win

### Open Source Platforms
| Platform | Tech | Description |
|----------|------|-------------|
| **Dribdat** | Python/JS | Hackathons for impact |
| **Hibiscus** | - | Turnkey platform by HackSC |
| **JunctionApp** | - | All-in-one by Junction |
| **OpenHackathon** | Next.js | Cloud dev environments |
| **Hackerspace3** | Ruby | For GovHack events |

### Tools
| Tool | Purpose |
|------|---------|
| **HELPq** | Mentor queue management |
| **Hangar** | Slack bot for judging |
| **Gavel** | Mathematical judging system |
| **Hackathon Starter** | Node.js boilerplate |

---

## API Summary Table

| Platform | Auth Method | Rate Limits | Docs |
|----------|-------------|-------------|------|
| Kaggle | API Token (JSON) | Standard | [Docs](https://www.kaggle.com/docs/api) |
| HuggingFace | API Token | Standard | [Docs](https://huggingface.co/docs/huggingface_hub) |
| HackerEarth | API Key | Contact | [PublicAPI](https://publicapi.dev/hackerearth-api) |
| Devpost | N/A (scraping) | Rate-limited | [Scrapers](#devpost-scrapers--data-extraction) |
| DoraHacks | Platform-based | N/A | [BUIDL](https://dorahacks.io/buidl) |

---

## Quick Links

### Find Hackathons
- [Devpost](https://devpost.com/hackathons)
- [MLH Season](https://mlh.io/seasons/2025/events)
- [DoraHacks](https://dorahacks.io/hackathon)
- [HackerEarth](https://www.hackerearth.com/challenges/)
- [lablab.ai](https://lablab.ai/event)
- [Luma Hackathons](https://lu.ma/hackathons)
- [ETHGlobal](https://ethglobal.com/events)
- [Devfolio](https://devfolio.co/hackathons)
- [Unstop](https://unstop.com/hackathons)

### Learning Resources
- [MLH Organizer Guide](https://guide.mlh.io)
- [Kaggle Learn](https://www.kaggle.com/learn)
- [HuggingFace Course](https://huggingface.co/learn)

### Blog Posts & Tips
- [How I Win Most Hackathons](https://szeyusim.medium.com/how-i-win-most-hackathons-stories-pro-tips-from-a-serial-hacker-1969c6470f92)
- [Ultimate 8 Step Guide](https://medium.com/garyyauchan/ultimate-8-step-guide-to-winning-hackathons-84c9dacbe8e)
- [10+ Projects to Win in 2024](https://dev.to/lokesh_singh/10-projects-to-win-hackathons-in-2024-5596)
- [Tips for Devpost Wins](https://medium.com/developer-circles-lusaka/tips-on-how-to-win-an-online-hackathon-on-devpost-c548027e0eae)

---

*Last Updated: December 2024*
*Platforms Covered: 40+*
