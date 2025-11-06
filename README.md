# 🌟 Synchrony - Where Students Teach Students

> AI-powered platform that turns study groups into collaborative learning experiences

**[🚀 Try Live Demo](https://huggingface.co/spaces/Lujainossaily/Synchrony)** • **[📝 Register](https://docs.google.com/forms/d/e/1FAIpQLSfJFGx-yd0FPIuRYLUJut3BOOiQ14x_5DYheWpgrUqcHdQaCA/viewform)** • **[📊 View Database](https://docs.google.com/spreadsheets/d/1rpR-E_RSooDkNDh-Q_1BDIeGw4vfgmusNAfwPqATaW4/edit?gid=746637293#gid=746637293)** • **[📹 Watch Demo](demo/ui-demo.mp4)**

---

## 🎯 The Problem

Traditional study groups fail because:
- Everyone studies the *same* topics (redundant effort)
- Finding compatible study partners is difficult
- No structure or methodology for peer teaching
- TAs are overloaded, students get stuck

## 💡 Our Solution

**Synchrony** uses AI to enable effective peer teaching:

```
Register → AI matches by complementary topics → Generate challenges → Learn by teaching
```

Students are matched with peers studying *different but related* topics, creating natural teaching opportunities.

---

## ✨ What Makes It Special

### 🤖 **AI Challenges That Require Real Understanding**
Each challenge assigns a specific teaching role to each student based on their topic.

**Real example from Data Structures course:**
> **Challenge:** "Design a university course registration system"
> 
> - **Layla (Binary Search Trees):** "Explain how you'd implement the course catalog search. Why use BST? What's the time complexity for finding courses by code or name?"
> 
> - **Omar (Linked Lists):** "Explain how you'd implement the waitlist system. Would you use singly or doubly linked lists? Why?"
> 
> - **Khaled (Queues):** "Explain how you'd handle concurrent registration requests. Why is a queue the right choice here?"
>
> **Group task:** "Now connect your solutions—how do these three data structures work together in one system?"

This way, each student *must* teach their topic to solve the challenge together.

### 💡 **Hints That Guide Without Giving Answers**
Stuck? Request progressive hints:
- **Level 1:** Gentle direction 🤔 "Think about the key property of BSTs..."
- **Level 2:** More specific 💭 "Consider how left < parent < right helps with search..."
- **Level 3:** Nearly complete 🎯 "A BST allows O(log n) search by comparing keys at each node..."

### 👥 **Smart Matching Algorithm**
We group students studying *different topics* within the same subject:
- **Same subject** (e.g., Data Structures)
- **Different focus areas** (e.g., Trees, Lists, Queues)
- **Result:** Each student becomes the "expert" on their topic and teaches it to others

---

## 🚀 Try It Right Now (60 seconds)

### Quick Test:
```
1. Visit: https://huggingface.co/spaces/Lujainossaily/Synchrony
2. Enter: test@university.edu
3. Click "Login"
4. Explore all 5 tabs to see features
```

### Full Experience:
```
1. Fill out the registration form
2. View the database to see your entry
3. Login with your registered email
4. See your AI-matched study group
5. Load personalized challenges for your group
```

---

## 🧠 How It Works

**The Flow:**
```
Form submission → Google Sheets storage → n8n reads and analyzes data → 
Matching algorithm groups by complementary topics → Student logs in → 
Groq AI generates personalized challenges → Students collaborate → 
Adaptive hints available → Learning happens through teaching
```

**The Tech Stack:**
- **Frontend:** Gradio (Python-based UI framework)
- **Backend:** n8n workflows (visual automation)
- **AI:** Groq API with Llama 3.3 70B (fast inference)
- **Database:** Google Sheets (real-time collaboration)
- **Hosting:** Hugging Face Spaces (free deployment)

---

## 🎓 Why This Works

**Research-backed approach:**
- 📊 Teaching others = **90% retention rate** (Edgar Dale's Cone of Learning)
- 📊 Collaborative learning = **higher academic performance** (Johnson & Johnson, 1989)
- 📊 AI-powered tutoring = **measurable learning gains** (Kulik & Fletcher, 2016)

**The principle:** Students retain 90% of what they teach to others. Synchrony structures the entire experience around peer teaching, not passive studying.

---

## 🔗 All Resources

| Resource | Link | Description |
|----------|------|-------------|
| 🌐 **Live Demo** | [Try it →](https://huggingface.co/spaces/Lujainossaily/Synchrony) | Interactive demo |
| 📝 **Register** | [Sign up →](https://docs.google.com/forms/d/e/1FAIpQLSfJFGx-yd0FPIuRYLUJut3BOOiQ14x_5DYheWpgrUqcHdQaCA/viewform) | Join as a student |
| 📊 **Database** | [View data →](https://docs.google.com/spreadsheets/d/1rpR-E_RSooDkNDh-Q_1BDIeGw4vfgmusNAfwPqATaW4/edit?gid=746637293#gid=746637293) | See backend data (read-only) |
| 📹 **Video Demo** | [Watch →](demo/ui-demo.mp4) | 2-minute walkthrough |
| 📊 **Presentation** | [Slides →](demo/presentation.pdf) | Full deck |

All backend workflows and data are transparent—judges can see exactly how the system works.

---

## 🚀 Future Enhancements

- [ ] Real-time video study sessions
- [ ] Gamification system (XP, badges, leaderboards)
- [ ] Mobile applications (iOS/Android)
- [ ] LMS integration (Canvas, Moodle, Blackboard)
- [ ] Code collaboration tools for computer science students
- [ ] Multi-language support for international students

---

## 💻 Run Locally

```bash
# Clone the repository
git clone https://github.com/MaryamShanabli/Synchrony.git
cd Synchrony

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

Open `http://localhost:7860` in your browser.

---

## 📂 Repository Structure

```
Synchrony/
├── README.md              # Documentation
├── app.py                 # Main application
├── requirements.txt       # Python dependencies
├── demo/                  # Video & presentation
└── docs/                  # Additional documentation
```

---

## 🏆 Built For

**UniAgents Hackathon** - November 2025

*Making education collaborative, one study group at a time* ✨

---

**⭐ Star this repo if you believe in collaborative learning**

*Built by students, for students* ❤️
