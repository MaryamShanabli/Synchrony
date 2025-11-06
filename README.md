# 🌟 Synchrony - Where Students Teach Students

> AI-powered platform that matches university students into study groups and generates personalized collaborative challenges

**[🚀 Try Live Demo](https://huggingface.co/spaces/Lujainossaily/Synchrony)** • **[📝 Register](https://docs.google.com/forms/d/e/1FAIpQLSfJFGx-yd0FPIuRYLUJut3BOOiQ14x_5DYheWpgrUqcHdQaCA/viewform)** • **[📊 View Database](https://docs.google.com/spreadsheets/d/1rpR-E_RSooDkNDh-Q_1BDIeGw4vfgmusNAfwPqATaW4/edit?gid=746637293#gid=746637293)** • **[📹 Watch Demo](demo/video-demo.mp4)**

---

## 🎯 The Problem

Traditional study groups fail because:
- Everyone studies the same topics (wasted effort)
- Hard to find compatible study partners  
- No structured methodology for peer teaching
- Students need guidance but TAs are overloaded

## 💡 The Solution

**Synchrony** uses AI to unlock the power of peer teaching:

```
1. Students register → 2. AI matches by topics → 3. Generate challenges → 4. Learn by teaching
```

---

## ✨ Features That Matter

### 🤖 **AI Challenge Generation**
Each challenge requires students to **teach their topic** to teammates. No passive learning allowed.

**Example:**
> "Layla, explain Binary Search Trees to the group. Omar and Khaled, compare BST search (O(log n)) with your data structures."

### 💡 **Adaptive Hints** (3 Levels)
- **Level 1:** Gentle nudge 🤔
- **Level 2:** More explicit 💭  
- **Level 3:** Almost there 🎯

### 👥 **Smart Matching**
Matches students with **complementary topics** in the same subject. Creates diversity that drives learning.

---

## 🚀 Try It Now (60 seconds)

### Quick Test:
```
1. Open: https://huggingface.co/spaces/Lujainossaily/Synchrony
2. Enter: test@university.edu
3. Click "Login"
4. Explore all 5 tabs
```

### Full Experience:
```
1. Fill the registration form
2. Check the database to see your entry
3. Login with your email
4. See your matched team
5. Load AI-generated challenges
```

---

## 📊 How It Works

**The Magic:**
1. **Registration Form** → Google Sheets stores student data
2. **n8n Workflow** reads sheets, matches students by complementary topics
3. **Groq AI** generates personalized challenges for each group
4. **Gradio UI** delivers beautiful, interactive experience
5. **Students learn by teaching** their topics to each other

**Data Flow:**
```
Registration → Google Sheets → n8n Matching → Group Creation → Student Login → 
AI Challenge Generation → Collaboration → Adaptive Hints → Learning Success
```

---

## 🎓 Why This Works

**Research-backed:**
- 📊 Peer teaching = **90% retention** (Edgar Dale)
- 📊 Collaborative learning = **higher grades** (Johnson & Johnson)
- 📊 AI tutoring = **significant gains** (Kulik & Fletcher)

**The secret:** Students learn best when they **teach others**. Synchrony forces this through AI-generated challenges that require explanation and collaboration.

---

## 🔗 Important Links

| Resource | Link | Description |
|----------|------|-------------|
| 🌐 **Live Demo** | [Try Now →](https://huggingface.co/spaces/MaryamShanabli/synchrony) | Interactive demo |
| 📝 **Registration** | [Sign Up →](https://docs.google.com/forms/d/e/1FAIpQLSfJFGx-yd0FPIuRYLUJut3BOOiQ14x_5DYheWpgrUqcHdQaCA/viewform) | Join as student |
| 📊 **Database** | [View Data →](https://docs.google.com/spreadsheets/d/1rpR-E_RSooDkNDh-Q_1BDIeGw4vfgmusNAfwPqATaW4/edit?usp=sharing) | Live sheets (read-only) |
| 📹 **Video Demo** | [Watch →](demo/video-demo.mp4) | 2-min walkthrough |
| 📊 **Presentation** | [Slides →](demo/presentation.pdf) | Full deck |

**All backend workflows and data are accessible** - judges can see exactly how it works!

---

## 🚀 Future Vision

- [ ] Real-time video study sessions
- [ ] Gamification (XP, badges, leaderboards)
- [ ] Mobile app (iOS/Android)
- [ ] Integration with Canvas/Moodle
- [ ] Code collaboration for CS students
- [ ] Multi-language support

---

## 💻 Run Locally

```bash
# Clone the repository
git clone https://github.com/MaryamShanabli/Synchrony.git
cd synchrony

# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py
```

Open `http://localhost:7860` in your browser.

---

## 📂 Repository Structure

```
synchrony/
├── README.md              # You are here
├── app.py                 # Main application
├── requirements.txt       # Dependencies
├── demo/                  # Video & presentation
└── docs/                  # Additional docs
```

---

## 🏆 Built For

**[UniAgents]** - November 2025

*Making education collaborative, one study group at a time* ✨

---

**⭐ Star this repo if you believe in better learning!**

*Built with ❤️ for students everywhere*
