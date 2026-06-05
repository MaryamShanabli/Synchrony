# 🔄 Synchrony — Because Chaos Is Expensive

<div align="center">

[![Hugging Face Spaces](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Spaces-FFD21E?style=for-the-badge&logo=huggingface&logoColor=black)](https://huggingface.co/spaces/maryamshanabli/Synchrony)
[![Gradio App](https://img.shields.io/badge/Gradio-Interface-orange?style=for-the-badge&logo=gradio&logoColor=white)](https://huggingface.co/spaces/maryamshanabli/Synchrony)
[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)]()
[![Database](https://img.shields.io/badge/Google_Sheets-Database-34A853?style=for-the-badge&logo=googlesheets&logoColor=white)](https://docs.google.com/spreadsheets/d/1J0lmUpP8aTRmjnvzIYRyvPOIYFumvkTwOMbyv8js_Lg/edit?usp=sharing)

> **AI-powered platform that turns chaotic study groups into collaborative peer-teaching experiences**
> 🚀 **Built for the UniAgents Hackathon — November 2025**

[🕹️ Launch Live Synchrony Space](https://huggingface.co/spaces/maryamshanabli/Synchrony) · [📊 View Live Google Sheet Database](https://docs.google.com/spreadsheets/d/1J0lmUpP8aTRmjnvzIYRyvPOIYFumvkTwOMbyv8js_Lg/edit?usp=sharing)

</div>

---

## 🚀 The Core Dilemma

Traditional study groups frequently collapse due to unstructured environments:

- **Redundant Effort:** Everyone reviews identical topics, leading to zero peer teaching
- **Chance Matching:** Finding compatible, focused study partners is left entirely to random luck
- **Passenger Syndrome:** No clear methodology exists to make collaboration interactive
- **Siloed Blockers:** Teaching assistants are perpetually overloaded, leaving students stuck in isolation

---

## 💡 The Synchrony Engine

Synchrony engineers genuine peer teaching by matching students with counterparts studying *different but interconnected* topics within the same subject area. Every participant instantly becomes the resident expert on their piece, compelling them to teach their peers to solve group challenges together.

```
In-App Onboarding ➔ Complementary Matchmaking ➔ Socratic Challenge Generation ➔ Learn by Teaching
```

---

## 🧠 What Makes It Special

### 1. Socratic AI Challenges

Each challenge assigns distinct teaching roles based on individual focus areas to ensure complete group participation.

> **Data Structures Example:**
> - **Challenge:** "Design a university course registration system"
> - **Layla (Binary Search Trees):** Implement the course catalog search, justify BST selection, calculate time complexity
> - **Omar (Linked Lists):** Architect the student waitlist, choose between singly/doubly linked nodes, present trade-offs
> - **Khaled (Queues):** Handle concurrent registration requests, explain why a queue structure is mandatory here
> - **Group Goal:** Connect all three modules into a single synchronized program

### 2. Progressive Hint Architecture

Rather than giving answers directly, the platform serves adaptive scaffolding:

- **Level 1 (Nudge):** Focus on the core sorting properties of binary nodes
- **Level 2 (Guidance):** Analyze how left < parent < right layouts accelerate search
- **Level 3 (Resolution):** A BST achieves O(log n) lookup by halving search boundaries at each comparison

### 3. Synco — Multi-Agent Shared Memory

Synco is an embedded, Groq-powered AI study tutor with a shared group memory layer. It tracks individual confidence levels, monitors team interactions, poses Socratic questions, and carries conversational context across separate user sessions.

---

## 🗺️ Architecture Evolution

### Original Prototype

```
Google Form ➔ Google Sheets ➔ n8n Cron Workflow ➔ Matching Engine ➔ Groq API ➔ Client App
```

*Initial concept relied on n8n automation and manual forms, creating rigid functional ceilings*

### Current Production (v2)

```
Native App UI ➔ Google Sheets API (gspread) ➔ Auto-Matching Engine ➔ Groq API Llama 3.3 70B ➔ Shared Notebook
```

*Rebuilt entirely inside the app ecosystem for full control over validations, timezone handling, and instant matching without third-party dependencies*

---

## 🛠️ Tech Stack

| Layer | Technology |
| :--- | :--- |
| **Frontend** | Gradio |
| **AI Engine** | Groq API · Llama 3.3 70B |
| **Database** | Google Sheets via `gspread` service accounts |
| **Hosting** | Hugging Face Spaces |
| **Legacy Middleware** | n8n Workflow Automation (archived) |

---

## 📋 Data Management

### Registration Fields

- **Identity:** Names and university email domains filter duplicates and auto-detect campus
- **Safety:** Hidden gender matching ensures secure, comfortable study pairs
- **Matching Inputs:** Topic selection, confidence sliders (1–5), study style tags, and availability grids

### Database Schema

| Tab | Contents |
| :--- | :--- |
| `Students` | Verified profiles with assigned group IDs |
| `Groups` | Team records, member emails, topic splits, calendar slots |
| `Activity` | Timestamps, challenge attempts, hint usage |
| `SyncoLog` | Multi-user chat history for Synco's shared memory |

---

## 🎮 Async Communications Model

Because Gradio uses single-user socket layers, Synchrony implements a **Shared Digital Notebook** model instead of live rooms:

- Activity logs update the `Activity` tab instantly so teammates see a timeline on return
- Synco fetches the last 20 messages from `SyncoLog` to maintain group context across timezones
- Group proposals refresh seamlessly for distributed study networks

---

## 🧪 Test Accounts

Three accounts are pre-staged in group `G001` for full multi-user testing without registration:

| Email | Topic Expertise | Confidence |
| :--- | :--- | :--- |
| `student1@test.edu` | Linked Lists, Stacks & Queues | `3 / 5` |
| `student2@test.edu` | Trees & Graphs, Algorithm Design | `4 / 5` |
| `student3@test.edu` | Databases & SQL, Web Development | `2 / 5` |

**Try the multi-user flow:**

1. Log in with any credential above
2. Go to **My Team** and view your assigned cohort
3. Generate a challenge built around your combined skill sets
4. Switch tabs, log in as a teammate, send a message, and watch Synco maintain context across both users

---

## 💾 Local Setup

```bash
# Clone the repository
git clone https://github.com/MaryamShanabli/Synchrony.git
cd Synchrony

# Install dependencies
pip install -r requirements.txt

# Run locally
python app.py
```

App runs at `http://localhost:7860`

### Environment Variables

Create a `.env` file with:

```env
GROQ_API_KEY=your_groq_api_key_here
GOOGLE_CREDENTIALS=your_full_service_account_json_string
SHEET_ID=your_google_sheet_target_id
```

---

## 📈 Roadmap

- Real-time peer video integration
- Gamification with profile badges and XP leaderboards
- LMS API support for Canvas, Moodle, and Blackboard
- Live collaborative code playgrounds

---

**Synchrony 🔄 Educational Synergy Engine**
*Making learning social, conversational, and highly structured*
Built by students, for students
