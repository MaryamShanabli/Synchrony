# Synchrony — Because Chaos Is Expensive

> AI-powered platform that turns study groups into collaborative learning experiences

**[🚀 Live Demo](https://huggingface.co/spaces/maryamshanabli/Synchrony)** • **[📊 Database](https://docs.google.com/spreadsheets/d/1J0lmUpP8aTRmjnvzIYRyvPOIYFumvkTwOMbyv8js_Lg/edit?usp=sharing)** • **[📹 Watch Demo](demo/ui-demo.mp4)**

---

## The Problem

Traditional study groups fail because:
- Everyone studies the *same* topics — redundant effort, zero peer teaching
- Finding compatible study partners is left to chance
- No structure or methodology to make collaboration useful
- TAs are overloaded, students get stuck alone

## Our Solution

Synchrony uses AI to enable real peer teaching:

```
Register → matched by complementary topics → generate challenges → learn by teaching
```

Students are matched with peers studying *different but related* topics, so everyone becomes the expert on their piece and has to teach it to solve challenges together.

---

## What Makes It Special

### AI challenges that require real understanding

Each challenge assigns a specific teaching role to each student based on their topic.

**Example from a Data Structures group:**

> **Challenge:** "Design a university course registration system"
>
> - **Layla (Binary Search Trees):** Implement the course catalog search. Why BST? What's the time complexity?
> - **Omar (Linked Lists):** Implement the waitlist system. Singly or doubly linked? Why?
> - **Khaled (Queues):** Handle concurrent registration requests. Why is a queue the right choice here?
>
> **Group task:** Connect your solutions — how do all three data structures work together in one system?

Each student *must* teach their topic to solve the challenge. No passengers.

### Progressive hints that guide without giving answers

- Level 1 — gentle nudge: "Think about the key property of BSTs..."
- Level 2 — clearer guidance: "Consider how left < parent < right helps with search..."
- Level 3 — almost there: "A BST allows O(log n) search by comparing keys at each node..."

### Smart matching

Groups students studying *different topics within the same subject*. Same course, different focus areas — each person becomes the resident expert on their piece.

### Synco — AI study tutor with shared group memory

Synco is a Groq-powered AI tutor built into the chat tab. It knows the group's topics, each member's confidence level, and the full conversation history across all group members. It asks Socratic questions, never gives away answers directly, and remembers what was discussed even across separate sessions.

---

## Architecture & updates

### Original architecture (as shown in video demo)

```
Google Form → Google Sheets → n8n reads & analyzes → 
matching algorithm → student logs in → Groq generates challenges → 
students collaborate → adaptive hints → learning through teaching
```

The original version used a Google Form for registration and n8n workflows to process and match students. This is what appears in the demo video.

> **Note:** The original Google Form has since been deleted. The n8n workflow is preserved in the demo materials but is no longer the active backend.

### Current architecture (v2 — fully rebuilt)

```
In-app registration → Google Sheets API (gspread) → 
auto-matching on registration → student logs in → 
Groq generates challenges → students collaborate → 
Synco group chat with shared memory → hints → learning
```

The entire registration and matching flow now lives inside the Gradio app itself, connected directly to Google Sheets via the Sheets API using a service account. No external form, no n8n dependency.

**What changed and why:**

The Google Form approach had a hard ceiling — it couldn't handle the 10+ fields with branching logic, validation, timezone selectors, or multi-select topics that a real matching algorithm needs. Rebuilding registration inside the app gave full control over UX, validation, and the data that goes into the sheet.

### Tech stack

| Layer | Tool |
|---|---|
| Frontend | Gradio (Python) |
| AI — challenges & chat | Groq API, Llama 3.3 70B |
| Database | Google Sheets via gspread |
| Hosting | Hugging Face Spaces |
| Original workflow (demo) | n8n |

---

## Registration fields

The in-app registration collects exactly what the matching algorithm needs — nothing more:

| Field | Why it's there |
|---|---|
| Name + university email | Identity, duplicate check, login key |
| University | Auto-detected from email domain |
| Gender | Keeps groups gender-compatible for comfort — not shown publicly |
| Timezone | Critical for scheduling across universities |
| Subject area | Fixed to Information Technology |
| Specific topics | 24 IT topics — the core matching axis |
| Confidence level (1–5) | Adjusts how Synco talks to each student |
| Why are you here? | One sentence fed directly into Synco's context |
| Study style | Discussion / hands-on / quiet — group harmony signal |
| Group preference | Peer teaching (diff topics) vs focused (same topic) |
| Session length | Prevents time-budget mismatches |
| Availability days + time | Scheduling |
| Readiness | Ready to start now vs just setting up |

Fields that were cut from the original plan: university name as a manual field (auto-detected), covered concepts (replaced by confidence slider — nobody fills out concept lists honestly), gender as a demographic tag (kept but repurposed purely for comfort matching).

---

## Google Sheets structure

**Live database:** [View sheet →](https://docs.google.com/spreadsheets/d/1J0lmUpP8aTRmjnvzIYRyvPOIYFumvkTwOMbyv8js_Lg/edit?usp=sharing)

Four tabs, all written by the app in real time:

| Tab | What's in it |
|---|---|
| `Students` | One row per registered student — all profile fields + assigned group_id |
| `Groups` | One row per matched group — member emails, topics, proposed meeting times |
| `Activity` | Timestamped log of every login, challenge generation, hint request |
| `SyncoLog` | Every chat message from every group member — gives Synco its cross-member memory |

Headers are created automatically on first write. The sheet just needs the four tabs to exist.

---

## Group communication model

Gradio is a single-user interface — you can't open a live chat room inside it. Instead of faking real-time messaging, Synchrony uses an **async shared group page** model:

- Every action (login, hint, challenge) logs to the Activity tab — when a teammate opens the app they see what happened since their last visit
- Synco loads the last 20 messages from SyncoLog for the whole group — so it knows what was discussed across all members, not just this session
- Meeting proposals write to the Groups tab and are visible to all members on refresh
- The result feels like a shared notebook, not a chat room — which is actually more useful for async study groups across different timezones

---

## Why this works

- Teaching others → 90% retention rate (Edgar Dale's Cone of Learning)
- Collaborative learning → higher academic performance (Johnson & Johnson, 1989)
- AI-powered tutoring → measurable learning gains (Kulik & Fletcher, 2016)

Students retain 90% of what they teach to others. Synchrony structures the entire experience around peer teaching, not passive reading.

---

## Try it now — test accounts

Three students are already registered and matched into group `G001` so you can experience the full flow without signing up.

| Name | Email | Topics | Confidence |
|---|---|---|---|
| student1 | `student1@test.edu` | Linked Lists, Stacks & Queues | 3/5 |
| student2 | `student2@test.edu` | Trees & Graphs, Algorithm Design | 4/5 |
| student3 | `student3@test.edu` | Databases & SQL, Web Development | 2/5 |

To try the full experience:

1. Go to **home** → enter any email above → log in
2. Go to **my team** → refresh to see the group and activity feed
3. Go to **challenges** → generate challenges built around their three topic sets
4. Go to **hints** → request hints at different levels for any challenge
5. Go to **chat** → talk to Synco — it knows all three members' topics and confidence levels
6. Open a second tab, log in as a different member, send a message in chat — then switch back to the first tab and Synco will already know what was discussed

---

## Run locally

```bash
git clone https://github.com/MaryamShanabli/Synchrony.git
cd Synchrony
pip install -r requirements.txt
python app.py
```

Open `http://localhost:7860` in your browser.

Requires three environment variables (or a `.env` file):
- `GROQ_API_KEY` — your Groq API key
- `GOOGLE_CREDENTIALS` — full JSON from a Google service account key file
- `SHEET_ID` — your Google Sheet ID

---

## Repository structure

```
Synchrony/
├── README.md          — documentation
├── app.py             — full application (registration, matching, challenges, chat)
├── requirements.txt   — dependencies
├── demo/              — video walkthrough and presentation
└── docs/              — additional documentation
```

---

## Future

- Real-time video study sessions
- Gamification — XP, badges, leaderboards
- Mobile apps (iOS / Android)
- LMS integration (Canvas, Moodle, Blackboard)
- Code collaboration tools
- Multi-language support

---

## Built for

**UniAgents Hackathon** — November 2025

*Making education collaborative, one study group at a time*

Built by students, for students.
