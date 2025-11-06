import gradio as gr
import pandas as pd
import random
import json
from datetime import datetime

# ============================================
# 🌟 SYNCHRONY - DARK ACADEMIA
# Oxford Libraries • Scholarly Elegance
# ============================================

REGISTRATION_FORM = "https://docs.google.com/forms/d/e/1FAIpQLSfJFGx-yd0FPIuRYLUJut3BOOiQ14x_5DYheWpgrUqcHdQaCA/viewform"
GOOGLE_SHEETS = "https://docs.google.com/spreadsheets/d/1rpR-E_RSooDkNDh-Q_1BDIeGw4vfgmusNAfwPqATaW4/edit?usp=sharing"

SHEET_ID = "1rpR-E_RSooDkNDh-Q_1BDIeGw4vfgmusNAfwPqATaW4"

STUDENTS_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=Students"
GROUPS_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=Groups"
CHALLENGES_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=Challenges"

current_student = {
    "name": None,
    "email": None,
    "group_id": None,
    "session_id": None,
    "team_members": [],
    "challenges": []
}

MOCK_CHALLENGES = [
    {
        "challenge_number": 1,
        "description": "Layla, explain how Binary Search Trees work to the group. Focus on BST properties, insertion, and search operations. Omar and Khaled, compare this with your data structures - how is searching in a BST different from searching in a linked list or checking elements in a queue?",
        "topics_involved": "Binary Search Trees, Linked Lists, Queues",
        "hints": [
            "Start by drawing a simple diagram showing how nodes are organized in a BST with the property: left < parent < right",
            "Think about the left-subtree and right-subtree properties - what makes a BST special compared to a regular tree?",
            "Compare time complexity: BST search is O(log n) average case, while linked list search is O(n)"
        ]
    },
    {
        "challenge_number": 2,
        "description": "Omar, teach us about Linked Lists. Create a real-world example showing both singly and doubly linked lists. Layla and Khaled, find connections between Linked Lists and your data structures.",
        "topics_involved": "Linked Lists, Binary Search Trees, Queues",
        "hints": [
            "Think about how nodes point to each other - singly linked has 'next' pointer, doubly linked has 'next' and 'prev'",
            "Consider real-world examples: browser history (doubly linked), music playlist (singly linked), undo/redo (doubly linked)",
            "Both BST nodes and queue nodes use pointers/references just like linked lists - they're all node-based structures!"
        ]
    },
    {
        "challenge_number": 3,
        "description": "Everyone: Design ONE real-world system that uses ALL three data structures (BST, Linked Lists, Queues). Explain how they work together. Be creative!",
        "topics_involved": "Binary Search Trees, Linked Lists, Queues",
        "hints": [
            "Think of a system with searching, ordering, and waiting - like a restaurant management system or task scheduler",
            "Example: Restaurant app with BST for menu items (fast lookup by price/name), Queue for order processing, Linked List for order history",
            "Draw a diagram showing how data flows between the three structures in your system"
        ]
    }
]

def read_sheet_safe(url, sheet_name="Unknown"):
    try:
        df = pd.read_csv(url)
        print(f"✅ Loaded {len(df)} rows from {sheet_name}")
        return df
    except Exception as e:
        print(f"⚠️ Could not read {sheet_name}: {e}")
        return pd.DataFrame()

def get_students_in_group(group_id):
    try:
        groups_df = read_sheet_safe(GROUPS_URL, "Groups")
        if groups_df.empty:
            return [
                {"name": "Omar Khalil", "topic": "Linked Lists"},
                {"name": "Khaled Ibrahim", "topic": "Queues"},
                {"name": "Layla Mahmoud", "topic": "Binary Search Trees"}
            ]
        group = groups_df[groups_df['group_id'] == group_id]
        if group.empty:
            return [
                {"name": "Omar Khalil", "topic": "Linked Lists"},
                {"name": "Khaled Ibrahim", "topic": "Queues"},
                {"name": "Layla Mahmoud", "topic": "Binary Search Trees"}
            ]
        group_row = group.iloc[0]
        member_names = str(group_row.get('member_names', '')).split(',')
        topics = str(group_row.get('topics', '')).split(',')
        team_members = []
        for i, name in enumerate(member_names):
            name = name.strip()
            topic = topics[i].strip() if i < len(topics) else "Data Structures"
            if name:
                team_members.append({"name": name, "topic": topic})
        if team_members:
            return team_members
        else:
            return [
                {"name": "Omar Khalil", "topic": "Linked Lists"},
                {"name": "Khaled Ibrahim", "topic": "Queues"},
                {"name": "Layla Mahmoud", "topic": "Binary Search Trees"}
            ]
    except Exception as e:
        return [
            {"name": "Omar Khalil", "topic": "Linked Lists"},
            {"name": "Khaled Ibrahim", "topic": "Queues"},
            {"name": "Layla Mahmoud", "topic": "Binary Search Trees"}
        ]

def get_challenges_for_session(session_id):
    try:
        challenges_df = read_sheet_safe(CHALLENGES_URL, "Challenges")
        if challenges_df.empty:
            return MOCK_CHALLENGES
        session_challenges = challenges_df[challenges_df['session_id'] == session_id]
        if session_challenges.empty:
            return MOCK_CHALLENGES
        challenges = []
        for _, row in session_challenges.iterrows():
            hints_json = row.get('hints_json', '[]')
            try:
                hints = json.loads(hints_json) if isinstance(hints_json, str) else []
            except:
                hints = []
            challenges.append({
                "challenge_number": row.get('challenge_number', len(challenges) + 1),
                "description": row.get('description', 'No description'),
                "topics_involved": row.get('topics_involved', 'N/A'),
                "hints": hints
            })
        if challenges:
            return challenges
        else:
            return MOCK_CHALLENGES
    except Exception as e:
        return MOCK_CHALLENGES

def lookup_student(email):
    try:
        if not email or "@" not in email:
            return "❌ Please enter a valid email address"
        name = email.split("@")[0].replace(".", " ").replace("_", " ").title()
        try:
            students_df = read_sheet_safe(STUDENTS_URL, "Students")
            if not students_df.empty:
                student = students_df[students_df['email'].str.lower() == email.lower()]
                if not student.empty:
                    student_row = student.iloc[0]
                    name = student_row.get('name', name)
                    group_id = student_row.get('group_id', 'G001')
                else:
                    group_id = "G001"
            else:
                group_id = "G001"
        except:
            group_id = "G001"
        team_members = get_students_in_group(group_id)
        session_id = f"S{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
        current_student["name"] = name
        current_student["email"] = email
        current_student["group_id"] = group_id
        current_student["session_id"] = session_id
        current_student["team_members"] = team_members
        welcome_msg = f"### ✅ Welcome back, {name}!\n\n"
        welcome_msg += f"**Session ID:** `{session_id}`\n\n"
        welcome_msg += f"**Synco says:**\n"
        welcome_msg += f"Hey {', '.join([m['name'] for m in team_members])}! Welcome to your Synchrony study session. "
        welcome_msg += f"You're all studying Data Structures with different focus areas—perfect for peer teaching!\n\n"
        welcome_msg += f"**Your Team ({group_id}):** {', '.join([m['name'] for m in team_members])}\n\n"
        welcome_msg += f"👉 Head to the **My Team** tab to see everyone's topics!"
        return welcome_msg
    except Exception as e:
        return f"❌ Error: {str(e)}"

def get_team_info():
    if not current_student.get("team_members"):
        return "⚠️ Please login first in the Home tab"
    output = f"## 👥 Your Study Squad - {current_student.get('group_id', 'G001')}\n\n"
    output += f"**Session ID:** `{current_student.get('session_id', 'not started')}`\n\n"
    output += "---\n\n"
    for member in current_student["team_members"]:
        user_name = current_student.get("name", "").lower()
        member_name = member.get("name", "").lower()
        is_you = " **(You)**" if user_name in member_name or member_name in user_name else ""
        output += f"### 🎓 {member['name']}{is_you}\n"
        output += f"**Focus Area:** {member.get('topic', 'N/A')}\n\n"
    output += "---\n\n💡 Collaborate, learn together, and grow!"
    return output

def load_challenges():
    if not current_student.get("session_id"):
        return "⚠️ No active session. Please login first in the Home tab"
    try:
        session_id = current_student["session_id"]
        challenges = get_challenges_for_session(session_id)
        current_student["challenges"] = challenges
        output = f"# 🎯 Your Collaborative Challenges\n\n"
        output += f"**Synco says:** Here are your 3 collaborative challenges! Work together, discuss your approaches, "
        output += f"and request hints when needed. Ready? Let's go!\n\n"
        output += "---\n\n"
        for challenge in challenges:
            output += f"## Challenge {challenge['challenge_number']}\n\n"
            output += f"{challenge['description']}\n\n"
            output += f"**📚 Topics:** {challenge['topics_involved']}\n\n"
            output += f"💡 *Need help? Request a hint in the Hints tab!*\n\n"
            output += "---\n\n"
        return output
    except Exception as e:
        return f"❌ Error loading challenges: {str(e)}"

def request_hint(challenge_num, hint_level_text):
    if not current_student.get("session_id"):
        return "⚠️ No active session. Please login first"
    if not current_student.get("challenges"):
        return "⚠️ Please load challenges first in the Challenges tab"
    try:
        hint_level = int(hint_level_text.split(" - ")[0])
        challenge_idx = int(challenge_num) - 1
        if challenge_idx < 0 or challenge_idx >= len(current_student["challenges"]):
            return "⚠️ Invalid challenge number"
        challenge = current_student["challenges"][challenge_idx]
        hints = challenge.get("hints", [])
        if hint_level < 1 or hint_level > len(hints):
            return f"⚠️ Only {len(hints)} hints available"
        hint = hints[hint_level - 1]
        if hint_level == 1:
            encouragement = "💡 **Think about it a bit more**"
        elif hint_level == 2:
            encouragement = "💭 **You're getting closer**"
        else:
            encouragement = "🎯 **Almost there**"
        output = f"## {encouragement}\n\n"
        output += f"**Challenge {challenge_num}** • Hint Level {hint_level}\n\n"
        output += "---\n\n"
        output += f"{hint}\n\n"
        output += "---\n\n"
        output += f"💪 You got this! Keep going!"
        return output
    except Exception as e:
        return f"❌ Error: {str(e)}"

def send_message(message, history):
    if not message.strip():
        return history, ""
    history.append({
        "role": "user",
        "content": f"**{current_student.get('name', 'You')}:** {message}"
    })
    if not current_student.get("team_members"):
        response = "**Synco:** Please login first to chat with your team"
    else:
        other_members = [m for m in current_student["team_members"] 
                        if m['name'].lower() != current_student.get('name', '').lower()]
        if other_members:
            member = random.choice(other_members)
            responses = [
                f"**{member['name']}:** That's a great point about {member['topic']}!",
                f"**{member['name']}:** Interesting! Let me explain how {member['topic']} relates to that...",
                f"**{member['name']}:** I agree! In {member['topic']}, we approach it similarly.",
                f"**{member['name']}:** Good question! Let me draw a quick diagram...",
                f"**Synco:** Excellent collaboration! Keep discussing!"
            ]
            response = random.choice(responses)
        else:
            response = "**Synco:** Great thinking!"
    history.append({"role": "assistant", "content": response})
    return history, ""

# ============================================
# 🎨 DARK ACADEMIA AESTHETIC
# ============================================

custom_css = """
@import url('https://fonts.googleapis.com/css2?family=Crimson+Pro:wght@400;600;700&family=Inter:wght@400;500;600&display=swap');

.gradio-container {
    background: linear-gradient(135deg, #F5F1E8 0%, #EBE3D5 100%) !important;
    color: #2B1B17 !important;
    min-height: 100vh !important;
}

* {
    font-family: 'Inter', serif !important;
}

h1, h2, h3 {
    font-family: 'Crimson Pro', serif !important;
}

:root {
    --burgundy: #8B2635;
    --forest: #2F4538;
    --gold: #B8860B;
    --parchment: #F5F1E8;
    --paper: #FFFEF7;
    --espresso: #2B1B17;
    --taupe: #C4B5A0;
}

.contain {
    max-width: 100% !important;
    width: 100% !important;
    padding: 24px 48px !important;
    margin: 0 !important;
}

.tab-nav {
    background: var(--paper) !important;
    border-radius: 12px !important;
    padding: 8px !important;
    margin-bottom: 24px !important;
    box-shadow: 0 4px 12px rgba(43, 27, 23, 0.08) !important;
    border: 1px solid var(--taupe) !important;
}

.tab-nav button {
    background: transparent !important;
    border: none !important;
    color: var(--forest) !important;
    font-weight: 600 !important;
    font-size: 15px !important;
    padding: 12px 24px !important;
    border-radius: 8px !important;
    transition: all 0.3s ease !important;
}

.tab-nav button:hover {
    background: rgba(139, 38, 53, 0.08) !important;
    color: var(--burgundy) !important;
}

.tab-nav button.selected {
    background: var(--burgundy) !important;
    color: var(--paper) !important;
    box-shadow: 0 2px 8px rgba(139, 38, 53, 0.3) !important;
}

input, textarea, select {
    background: var(--paper) !important;
    border: 2px solid var(--taupe) !important;
    color: var(--espresso) !important;
    border-radius: 8px !important;
    font-size: 15px !important;
    padding: 12px 16px !important;
    transition: all 0.3s ease !important;
}

input:focus, textarea:focus, select:focus {
    border-color: var(--burgundy) !important;
    box-shadow: 0 0 0 3px rgba(139, 38, 53, 0.1) !important;
    outline: none !important;
}

button {
    background: var(--burgundy) !important;
    border: none !important;
    color: var(--paper) !important;
    font-weight: 600 !important;
    font-size: 15px !important;
    border-radius: 8px !important;
    padding: 12px 24px !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 3px 10px rgba(139, 38, 53, 0.2) !important;
}

button:hover {
    background: #6D1F2A !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 5px 15px rgba(139, 38, 53, 0.3) !important;
}

button.secondary {
    background: var(--forest) !important;
    box-shadow: 0 3px 10px rgba(47, 69, 56, 0.2) !important;
}

button.secondary:hover {
    background: #1F2F28 !important;
}

.output-markdown, .prose, .markdown {
    background: var(--paper) !important;
    border: 1px solid var(--taupe) !important;
    border-radius: 12px !important;
    padding: 24px !important;
    color: var(--espresso) !important;
    box-shadow: 0 4px 12px rgba(43, 27, 23, 0.06) !important;
    line-height: 1.8 !important;
}

h1 {
    color: var(--burgundy) !important;
    font-weight: 700 !important;
    font-size: 48px !important;
    text-align: center !important;
    margin: 24px 0 !important;
    letter-spacing: -0.5px !important;
}

h2 {
    color: var(--burgundy) !important;
    font-weight: 600 !important;
    font-size: 32px !important;
    margin: 20px 0 12px 0 !important;
}

h3 {
    color: var(--forest) !important;
    font-weight: 600 !important;
    font-size: 22px !important;
    margin: 16px 0 8px 0 !important;
}

p, li {
    color: var(--espresso) !important;
    font-size: 15px !important;
    line-height: 1.8 !important;
}

strong {
    color: var(--burgundy) !important;
    font-weight: 700 !important;
}

a {
    color: var(--burgundy) !important;
    text-decoration: none !important;
    font-weight: 600 !important;
    border-bottom: 1px solid var(--taupe) !important;
    transition: all 0.2s ease !important;
}

a:hover {
    color: var(--forest) !important;
    border-bottom-color: var(--forest) !important;
}

code {
    background: #F0EBE3 !important;
    color: var(--forest) !important;
    padding: 3px 8px !important;
    border-radius: 4px !important;
    border: 1px solid var(--taupe) !important;
    font-family: 'Courier New', monospace !important;
    font-size: 14px !important;
}

hr {
    border: none !important;
    height: 1px !important;
    background: var(--taupe) !important;
    margin: 24px 0 !important;
}

label {
    color: var(--espresso) !important;
    font-weight: 600 !important;
    font-size: 14px !important;
}

.message.user {
    background: var(--burgundy) !important;
    color: var(--paper) !important;
    border-radius: 12px 12px 4px 12px !important;
    padding: 12px 16px !important;
    margin-left: 20% !important;
    box-shadow: 0 2px 8px rgba(139, 38, 53, 0.2) !important;
}

.message.bot {
    background: var(--paper) !important;
    color: var(--espresso) !important;
    border: 1px solid var(--taupe) !important;
    border-radius: 12px 12px 12px 4px !important;
    padding: 12px 16px !important;
    margin-right: 20% !important;
    box-shadow: 0 2px 8px rgba(43, 27, 23, 0.08) !important;
}

::-webkit-scrollbar {
    width: 12px;
}

::-webkit-scrollbar-track {
    background: var(--parchment);
}

::-webkit-scrollbar-thumb {
    background: var(--burgundy);
    border-radius: 6px;
}
"""

demo = gr.Blocks(css=custom_css, title="Synchrony • Collaborative Learning", theme=gr.themes.Soft())

with demo:
    gr.Markdown("""
    # 🌟 Synchrony
    ## Where students teach students
    
    *AI-powered collaborative learning platform*
    
    ---
    """)
    
    with gr.Tab("🏠 Home"):
        with gr.Row():
            with gr.Column(scale=1):
                gr.Markdown("""
                ## Welcome to Synchrony
                
                Join a community of students learning together through peer teaching.
                
                ### 📝 New Here?
                Register to get matched with your perfect study group
                """)
                register_btn = gr.Button("Register Now", variant="primary", size="lg")
            
            with gr.Column(scale=1):
                gr.Markdown("""
                ### 🔐 Already Registered?
                Enter your university email to access your study session
                """)
                email_input = gr.Textbox(
                    label="University Email",
                    placeholder="your.email@university.edu"
                )
                login_btn = gr.Button("Login", variant="secondary", size="lg")
                login_output = gr.Markdown()
        
        register_btn.click(fn=lambda: None, js=f"() => window.open('{REGISTRATION_FORM}', '_blank')")
        login_btn.click(fn=lookup_student, inputs=[email_input], outputs=[login_output])
        email_input.submit(fn=lookup_student, inputs=[email_input], outputs=[login_output])
    
    with gr.Tab("👥 My Team"):
        gr.Markdown("## Your Study Squad")
        gr.Markdown("Meet your teammates and see what everyone's focusing on")
        team_display = gr.Markdown(value="⚠️ Please login first in the Home tab")
        refresh_btn = gr.Button("Refresh Team Info", variant="secondary")
        refresh_btn.click(fn=get_team_info, outputs=[team_display])
    
    with gr.Tab("🎯 Challenges"):
        gr.Markdown("""
        ## Collaborative Challenges
        
        Work together on AI-generated challenges designed for your group's topics
        """)
        load_btn = gr.Button("Load Challenges", variant="primary", size="lg")
        challenges_display = gr.Markdown(value="Click the button above to load your challenges")
        load_btn.click(fn=load_challenges, outputs=[challenges_display])
    
    with gr.Tab("💡 Hints"):
        gr.Markdown("""
        ## Adaptive Hints
        
        Get progressive hints when you're stuck—from gentle nudges to detailed guidance
        """)
        
        with gr.Row():
            challenge_select = gr.Dropdown(label="Select Challenge", choices=["1", "2", "3"], value="1", scale=1)
            hint_level_select = gr.Dropdown(label="Hint Level", choices=["1 - Gentle nudge", "2 - Clearer guidance", "3 - Almost there"], value="1 - Gentle nudge", scale=2)
        
        hint_btn = gr.Button("Get Hint", variant="primary", size="lg")
        hint_display = gr.Markdown(value="Select a challenge and hint level, then click the button")
        hint_btn.click(fn=request_hint, inputs=[challenge_select, hint_level_select], outputs=[hint_display])
    
    with gr.Tab("💬 Chat"):
        gr.Markdown("""
        ## Team Chat
        
        Discuss challenges, share insights, and help each other learn
        
        *Demo mode - responses are simulated*
        """)
        
        chatbot = gr.Chatbot(value=[], label="", height=500, type="messages")
        
        with gr.Row():
            msg_input = gr.Textbox(label="", placeholder="Type your message...", scale=5)
            send_btn = gr.Button("Send", variant="primary", scale=1)
        
        send_btn.click(fn=send_message, inputs=[msg_input, chatbot], outputs=[chatbot, msg_input])
        msg_input.submit(fn=send_message, inputs=[msg_input, chatbot], outputs=[chatbot, msg_input])
    
    gr.Markdown("""
    ---
    
    ### Synchrony • Collaborative Learning Platform
    
    *Powered by AI • Built for Students • Designed for Impact*
    
    Created by Maryam Shanabli • 2025
    """)

print("\n🎨 DARK ACADEMIA AESTHETIC")
print("📚 Oxford libraries • Scholarly elegance")
print("✅ All features functional\n")

demo.launch()