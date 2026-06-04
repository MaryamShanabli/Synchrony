import gradio as gr
import pandas as pd
import json
import os
import random
import re
from datetime import datetime, timezone

# ══════════════════════════════════════════════════════════════════
#  SYNCHRONY — Collaborative Peer Learning Platform
# ══════════════════════════════════════════════════════════════════

SHEET_ID     = os.environ.get("SHEET_ID", "1J0lmUpP8aTRmjnvzIYRyvPOIYFumvkTwOMbyv8js_Lg")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
GOOGLE_CREDS = os.environ.get("GOOGLE_CREDENTIALS", "")

# ── Sheet tab names ───────────────────────────────────────────────
TAB_STUDENTS  = "Students"
TAB_GROUPS    = "Groups"
TAB_ACTIVITY  = "Activity"
TAB_SYNCO_LOG = "SyncoLog"
TAB_BOARD     = "Board"

# ── Subject areas + common topics ────────────────────────────────
SUBJECT_AREAS = ["Information Technology"]

CS_TOPICS = [
    "Arrays & Strings", "Linked Lists", "Stacks & Queues",
    "Trees & Graphs", "Hash Tables", "Sorting & Searching",
    "Dynamic Programming", "Recursion", "Object-Oriented Programming",
    "Databases & SQL", "Networking & Protocols", "Operating Systems",
    "Algorithm Design & Analysis", "Machine Learning Fundamentals",
    "Web Development", "Software Engineering & Design Patterns",
    "Cloud Computing", "Cybersecurity", "Mobile Development",
    "Compilers & Programming Languages", "Computer Architecture",
    "Discrete Mathematics for CS", "Linear Algebra for ML",
    "Probability & Statistics for CS",
]

TIMEZONES = [
    "UTC-12", "UTC-11", "UTC-10", "UTC-9", "UTC-8", "UTC-7",
    "UTC-6", "UTC-5", "UTC-4", "UTC-3", "UTC-2", "UTC-1",
    "UTC+0: London, Lisbon",
    "UTC+1: Paris, Berlin, Lagos",
    "UTC+2: Cairo, Amman, Beirut, Damascus, Jerusalem",
    "UTC+3: Riyadh, Kuwait, Baghdad, Doha, Nairobi",
    "UTC+4: Dubai, Abu Dhabi, Muscat",
    "UTC+5: Karachi, Tashkent",
    "UTC+5:30: Mumbai, Delhi",
    "UTC+6: Dhaka",
    "UTC+7: Bangkok, Jakarta",
    "UTC+8: Beijing, Singapore, Perth",
    "UTC+9: Tokyo, Seoul",
    "UTC+9:30: Adelaide",
    "UTC+10: Sydney, Melbourne",
    "UTC+11", "UTC+12: Auckland, Fiji",
]

# University domain → name map (auto-detect from email)
UNI_DOMAINS = {
    "uj.ac.za": "University of Johannesburg",
    "wits.ac.za": "University of the Witwatersrand",
    "uct.ac.za": "University of Cape Town",
    "sun.ac.za": "Stellenbosch University",
    "up.ac.za": "University of Pretoria",
    "mit.edu": "MIT", "stanford.edu": "Stanford University",
    "harvard.edu": "Harvard University", "ox.ac.uk": "University of Oxford",
    "cam.ac.uk": "University of Cambridge",
}


# ══════════════════════════════════════════════════════════════════
#  GOOGLE SHEETS — gspread connection
# ══════════════════════════════════════════════════════════════════

_gc = None

def _get_gc():
    global _gc
    if _gc:
        return _gc
    if not GOOGLE_CREDS:
        return None
    try:
        import gspread
        from google.oauth2.service_account import Credentials
        scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive",
        ]
        creds_dict = json.loads(GOOGLE_CREDS)
        creds = Credentials.from_service_account_info(creds_dict, scopes=scopes)
        _gc = gspread.authorize(creds)
        return _gc
    except Exception as e:
        print(f"gspread init error: {e}")
        return None


def _get_sheet(tab_name: str):
    gc = _get_gc()
    if not gc:
        return None
    try:
        sh = gc.open_by_key(SHEET_ID)
        try:
            return sh.worksheet(tab_name)
        except Exception:
            ws = sh.add_worksheet(title=tab_name, rows=1000, cols=26)
            return ws
    except Exception as e:
        print(f"Sheet open error ({tab_name}): {e}")
        return None


def _ensure_headers(ws, headers: list):
    try:
        first = ws.row_values(1)
        if not first or first != headers:
            ws.insert_row(headers, 1)
    except Exception as e:
        print(f"Header ensure error: {e}")


def sheet_append(tab_name: str, headers: list, row: list):
    ws = _get_sheet(tab_name)
    if not ws:
        return False
    try:
        _ensure_headers(ws, headers)
        ws.append_row(row, value_input_option="USER_ENTERED")
        return True
    except Exception as e:
        print(f"sheet_append error ({tab_name}): {e}")
        return False


def sheet_read_all(tab_name: str) -> pd.DataFrame:
    ws = _get_sheet(tab_name)
    if not ws:
        return pd.DataFrame()
    try:
        data = ws.get_all_records()
        return pd.DataFrame(data) if data else pd.DataFrame()
    except Exception as e:
        print(f"sheet_read error ({tab_name}): {e}")
        return pd.DataFrame()


def sheet_update_cell(tab_name: str, match_col: str, match_val: str,
                       update_col: str, update_val: str):
    ws = _get_sheet(tab_name)
    if not ws:
        return
    try:
        data = ws.get_all_records()
        headers = ws.row_values(1)
        for i, row in enumerate(data, start=2):
            if str(row.get(match_col, "")).lower() == str(match_val).lower():
                col_idx = headers.index(update_col) + 1
                ws.update_cell(i, col_idx, update_val)
                return
    except Exception as e:
        print(f"sheet_update error: {e}")


def log_activity(group_id: str, email: str, action: str, detail: str = ""):
    headers = ["timestamp", "group_id", "member_email", "action_type", "detail"]
    row = [datetime.now(timezone.utc).isoformat(), group_id, email, action, detail]
    sheet_append(TAB_ACTIVITY, headers, row)


def log_synco(group_id: str, email: str, role: str, message: str):
    headers = ["timestamp", "group_id", "sender_email", "role", "message"]
    row = [datetime.now(timezone.utc).isoformat(), group_id, email, role, message]
    sheet_append(TAB_SYNCO_LOG, headers, row)


# ══════════════════════════════════════════════════════════════════
#  REGISTRATION
# ══════════════════════════════════════════════════════════════════

STUDENTS_HEADERS = [
    "email", "name", "university", "timezone", "gender",
    "subject_area", "topics", "confidence", "why_here",
    "study_style", "group_preference", "session_length",
    "availability_days", "availability_time", "readiness",
    "group_id", "registered_at", "last_seen"
]


def uni_from_email(email: str) -> str:
    domain = email.split("@")[-1].lower()
    if domain in UNI_DOMAINS:
        return UNI_DOMAINS[domain]
    parts = domain.split(".")
    if len(parts) >= 2:
        return parts[-2].replace("-", " ").title() + " University"
    return "Unknown University"


def email_exists(email: str) -> bool:
    df = sheet_read_all(TAB_STUDENTS)
    if df.empty or "email" not in df.columns:
        return False
    return email.lower() in df["email"].str.lower().values


def register_student(reg_state: dict) -> tuple[bool, str]:
    email = reg_state.get("email", "").strip().lower()
    if not email or "@" not in email:
        return False, "please enter a valid university email"
    if email_exists(email):
        return False, "that email is already registered: head to the log in tab"

    row = [
        email,
        reg_state.get("name", "").strip(),
        uni_from_email(email),
        reg_state.get("timezone", "UTC"),
        reg_state.get("gender", "prefer not to say"),
        reg_state.get("subject_area", ""),
        reg_state.get("topics", ""),
        str(reg_state.get("confidence", 3)),
        reg_state.get("why_here", ""),
        reg_state.get("study_style", ""),
        reg_state.get("group_preference", ""),
        reg_state.get("session_length", ""),
        reg_state.get("availability_days", ""),
        reg_state.get("availability_time", ""),
        reg_state.get("readiness", "just setting up"),
        "",  # group_id: assigned by matching
        datetime.now(timezone.utc).isoformat(),
        datetime.now(timezone.utc).isoformat(),
    ]
    ok = sheet_append(TAB_STUDENTS, STUDENTS_HEADERS, row)
    if ok:
        assign_group(email)
        return True, "registered!"
    return False, "could not save: check your GOOGLE_CREDENTIALS secret"


def assign_group(email: str):
    try:
        students_df = sheet_read_all(TAB_STUDENTS)
        if students_df.empty:
            return
        me = students_df[students_df["email"].str.lower() == email.lower()]
        if me.empty:
            return
        me_row = me.iloc[0]

        # Find unmatched students with compatible preference
        unmatched = students_df[
            (students_df["group_id"].isna() | (students_df["group_id"] == "")) &
            (students_df["email"].str.lower() != email.lower())
        ]
        if len(unmatched) < 2:  # need 2 others so total group = 3
            return

        my_pref   = str(me_row.get("group_preference", "")).lower()
        my_gender = str(me_row.get("gender", "")).lower()

        # Gender filter — same gender groups when possible
        same_gender = unmatched[unmatched["gender"].str.lower() == my_gender]
        pool = same_gender if len(same_gender) >= 2 else unmatched

        # Prefer peer-teaching (different topics)
        if "peer" in my_pref or "diff" in my_pref:
            my_topics = set(str(me_row.get("topics", "")).lower().split(","))
            def topic_score(r):
                their = set(str(r.get("topics", "")).lower().split(","))
                return len(my_topics & their)
            pool = pool.copy()
            pool["_score"] = pool.apply(topic_score, axis=1)
            pool = pool.sort_values("_score")

        partners = pool.head(2)
        if len(partners) < 2:  # must have exactly 2 partners for a group of 3
            return

        groups_df = sheet_read_all(TAB_GROUPS)
        existing_ids = list(groups_df["group_id"].dropna()) if not groups_df.empty and "group_id" in groups_df.columns else []
        num = len(existing_ids) + 1
        group_id = f"G{num:03d}"

        member_emails = [email] + list(partners["email"])
        # Use | to separate per-member topic strings so commas within topics are safe
        topics_list   = [str(me_row.get("topics","")), ] + [str(r.get("topics","")) for _, r in partners.iterrows()]

        g_headers = ["group_id", "member_emails", "topics", "created_at",
                     "proposed_time", "confirmed_members", "status"]
        g_row = [
            group_id,
            ",".join(member_emails),
            " | ".join(topics_list),
            datetime.now(timezone.utc).isoformat(),
            "", "", "active"
        ]
        sheet_append(TAB_GROUPS, g_headers, g_row)

        for em in member_emails:
            sheet_update_cell(TAB_STUDENTS, "email", em, "group_id", group_id)

    except Exception as e:
        print(f"assign_group error: {e}")


# ══════════════════════════════════════════════════════════════════
#  LOGIN + SESSION
# ══════════════════════════════════════════════════════════════════

def login(email: str, state: dict):
    if not email or "@" not in email:
        return state, "please enter a valid email"

    email = email.strip().lower()
    df = sheet_read_all(TAB_STUDENTS)

    if df.empty or "email" not in df.columns:
        return state, "no students registered yet: create an account first"

    match = df[df["email"].str.lower() == email]
    if match.empty:
        return state, "email not found: did you register? create an account on the register tab"

    row = match.iloc[0]
    name       = str(row.get("name", email.split("@")[0].title()))
    group_id   = str(row.get("group_id", ""))
    university = str(row.get("university", uni_from_email(email)))
    subject    = str(row.get("subject_area", ""))
    topics     = str(row.get("topics", ""))
    why        = str(row.get("why_here", ""))
    confidence = str(row.get("confidence", "3"))

    team_members = _get_group_members(group_id, email)

    sheet_update_cell(TAB_STUDENTS, "email", email, "last_seen",
                      datetime.now(timezone.utc).isoformat())
    if group_id:
        log_activity(group_id, email, "login", "")

    new_state = {
        "email":        email,
        "name":         name,
        "university":   university,
        "group_id":     group_id,
        "subject":      subject,
        "topics":       topics,
        "why":          why,
        "confidence":   confidence,
        "team_members": team_members,
        "challenges":   [],
        "session_id":   f"S{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}",
    }

    # If no group yet but readiness is "ready", attempt matching now
    readiness = str(row.get("readiness", "")).strip().lower()
    if not group_id and readiness == "ready":
        assign_group(email)
        # Re-read after attempted match
        df2 = sheet_read_all(TAB_STUDENTS)
        if not df2.empty and "email" in df2.columns:
            match2 = df2[df2["email"].str.lower() == email]
            if not match2.empty:
                group_id = str(match2.iloc[0].get("group_id", ""))
                if group_id:
                    team_members = _get_group_members(group_id, email)
                    new_state["group_id"]     = group_id
                    new_state["team_members"] = team_members
                    if group_id:
                        log_activity(group_id, email, "login", "")

    if not group_id:
        msg = (f"### welcome back, {name}\n\n"
               f"you are registered but not in a group yet. "
               f"matching happens once more students with compatible topics join.")
    else:
        members_md = "\n".join(
            f"- **{m['name']}**: {m['topic']}" for m in team_members
        )
        msg = (f"### hey {name} 👋\n\n"
               f"**group** `{group_id}` · **{university}**\n\n"
               f"your squad:\n{members_md}\n\n"
               f"head to the my team tab to see what has been happening.")
    return new_state, msg


def _get_group_members(group_id: str, my_email: str) -> list:
    if not group_id:
        return []
    try:
        groups_df = sheet_read_all(TAB_GROUPS)
        if groups_df.empty:
            return []
        g = groups_df[groups_df["group_id"] == group_id]
        if g.empty:
            return []

        # Email list from group row — these are the only members
        raw_emails = [e.strip().lower() for e in
                      str(g.iloc[0]["member_emails"]).split(",") if e.strip()]

        # Load students and only keep emails that actually exist there
        students_df = sheet_read_all(TAB_STUDENTS)
        if students_df.empty or "email" not in students_df.columns:
            return []

        verified = students_df["email"].str.lower().tolist()
        members = []
        for em in raw_emails:
            if em not in verified:
                continue  # skip ghost entries
            row = students_df[students_df["email"].str.lower() == em].iloc[0]
            name  = str(row.get("name", em.split("@")[0].title()))
            # Pull topic from Students row, not the Groups blob
            topic = str(row.get("topics", "various")).split(",")[0].strip()
            members.append({
                "name":  name,
                "email": em,
                "topic": topic,
                "is_me": em == my_email.strip().lower(),
            })
        return members
    except Exception as e:
        print(f"get_group_members error: {e}")
        return []


# ══════════════════════════════════════════════════════════════════
#  TEAM / GROUP PAGE
# ══════════════════════════════════════════════════════════════════

def get_team_info(state: dict) -> str:
    if not state.get("email"):
        return "log in first →"
    if not state.get("group_id"):
        return ("## waiting for your group\n\n"
                "matching runs automatically when enough students with compatible "
                "topics have registered. check back soon.")

    group_id = state["group_id"]
    members  = state.get("team_members", [])

    lines = [f"## group `{group_id}`\n"]

    for m in members:
        you = " · *you*" if m.get("is_me") else ""
        lines.append(f"### {m['name']}{you}\n{m['topic']}\n")

    lines.append("\n---\n")

    # Activity feed from sheet
    try:
        act_df = sheet_read_all(TAB_ACTIVITY)
        if not act_df.empty and "group_id" in act_df.columns:
            group_act = act_df[act_df["group_id"] == group_id].tail(10)
            if not group_act.empty:
                lines.append("## recent activity\n")
                for _, row in group_act.iloc[::-1].iterrows():
                    ts  = str(row.get("timestamp", ""))[:16].replace("T", " ")
                    who = str(row.get("member_email", "")).split("@")[0]
                    act = str(row.get("action_type", ""))
                    det = str(row.get("detail", ""))
                    lines.append(f"- `{ts}` **{who}**: {act} {det}\n")
    except Exception:
        pass

    return "\n".join(lines)


def propose_meeting(time_str: str, state: dict) -> str:
    if not state.get("group_id"):
        return "log in first"
    if not time_str.strip():
        return "enter a time suggestion first"
    group_id = state["group_id"]
    email    = state["email"]
    sheet_update_cell(TAB_GROUPS, "group_id", group_id, "proposed_time", time_str.strip())
    log_activity(group_id, email, "proposed_meeting", time_str.strip())
    return f"meeting time **{time_str}** proposed: your group will see this when they open the app"


def get_proposed_meeting(state: dict) -> str:
    if not state.get("group_id"):
        return ""
    try:
        groups_df = sheet_read_all(TAB_GROUPS)
        if groups_df.empty:
            return ""
        g = groups_df[groups_df["group_id"] == state["group_id"]]
        if g.empty:
            return ""
        t = str(g.iloc[0].get("proposed_time", "")).strip()
        return f"proposed time: **{t}**" if t else "no meeting proposed yet"
    except Exception:
        return ""


# ══════════════════════════════════════════════════════════════════
#  CHALLENGES
# ══════════════════════════════════════════════════════════════════

def generate_challenges_ai(team_members: list) -> list:
    topics = [m["topic"] for m in team_members]
    names  = [m["name"]  for m in team_members]

    if GROQ_API_KEY:
        system = (
            "You are an expert CS educator. Generate exactly 3 collaborative peer-teaching challenges "
            "for a study group. Each challenge must assign a teaching role to each student based on their topic. "
            "Return ONLY valid JSON: an array of 3 objects with keys: "
            "challenge_number (int), description (string), topics_involved (string), hints (array of 3 strings). "
            "No markdown, no backticks, no preamble."
        )
        user = (
            "Study group members:\n"
            + "\n".join(f"- {n}: {t}" for n, t in zip(names, topics))
            + "\n\nCreate 3 challenges requiring each student to teach their topic."
        )
        try:
            from groq import Groq
            client = Groq(api_key=GROQ_API_KEY)
            resp = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "system", "content": system},
                          {"role": "user",   "content": user}],
                max_tokens=1200, temperature=0.7,
            )
            raw = resp.choices[0].message.content.strip()
            raw = re.sub(r"^```[a-z]*|```$", "", raw, flags=re.MULTILINE).strip()
            data = json.loads(raw)
            if isinstance(data, list) and len(data) >= 3:
                return data[:3]
        except Exception as e:
            print(f"Challenge AI error: {e}")

    n = len(names)
    def role(i): return f"{names[i%n]} ({topics[i%n]})"
    return [
        {
            "challenge_number": 1,
            "description": (
                f"**Teaching round.** {role(0)}: explain your topic with a real-world example. "
                + " ".join(f"{role(i)}: ask one clarifying question." for i in range(1, n))
            ),
            "topics_involved": ", ".join(topics),
            "hints": [
                "start with why this concept exists before explaining how it works",
                "use an everyday analogy: queues are like checkout lines, trees are like org charts",
                "show the time complexity difference concretely with a small example",
            ],
        },
        {
            "challenge_number": 2,
            "description": (
                "**Cross-topic connections.** Each member finds one similarity and one difference "
                "between their topic and a teammate's. Then together: build a concept map showing how they relate."
            ),
            "topics_involved": ", ".join(topics),
            "hints": [
                "look at internal structure: do both use nodes, pointers, or contiguous memory?",
                "compare operations: which are fast or slow in each and why?",
                "think use cases: when would you reach for one over the other?",
            ],
        },
        {
            "challenge_number": 3,
            "description": (
                f"**System design.** Design one real-world system that uses ALL of: {', '.join(topics)}. "
                "Each member explains exactly how their concept is used. "
                "Group task: trace the data flow between all the concepts."
            ),
            "topics_involved": ", ".join(topics),
            "hints": [
                "think of a system with search + ordering + waiting: like a hospital or ride-share",
                "map each concept to a specific operation with a reason",
                "draw arrows showing where data enters, transforms, and exits each concept",
            ],
        },
    ]


def load_challenges(state: dict):
    if not state.get("email"):
        return state, "log in first"
    if not state.get("team_members"):
        return state, "you need to be in a group first: check the my team tab"

    challenges = generate_challenges_ai(state["team_members"])
    state = dict(state)
    state["challenges"] = challenges

    if state.get("group_id"):
        log_activity(state["group_id"], state["email"], "generated_challenges", "")

    lines = ["# challenges\n\n"]
    for c in challenges:
        lines.append(f"## {c['challenge_number']}. {c.get('topics_involved','')}\n\n")
        lines.append(f"{c['description']}\n\n---\n\n")
    return state, "\n".join(lines)


def request_hint(challenge_num: str, hint_level_text: str, state: dict):
    if not state.get("challenges"):
        return "generate challenges first"
    try:
        level = int(hint_level_text.split(" ")[0])
        idx   = int(challenge_num) - 1
        c     = state["challenges"][idx]
        hints = c.get("hints", [])
        hint  = hints[min(level - 1, len(hints) - 1)]
        labels = {1: "gentle nudge", 2: "clearer guidance", 3: "almost there"}
        if state.get("group_id"):
            log_activity(state["group_id"], state.get("email",""),
                         "hint_requested", f"challenge {challenge_num} level {level}")
        return f"**{labels.get(level, 'hint')}**\n\n{hint}\n\n---\n\n*challenge {challenge_num}:* {c.get('description','')}"
    except Exception as e:
        return f"error: {e}"


# ══════════════════════════════════════════════════════════════════
#  SYNCO CHAT
# ══════════════════════════════════════════════════════════════════

def _fallback(message: str, history: list, team: list) -> str:
    """
    Context-aware fallback when Groq is unavailable.
    Reads the actual message and responds meaningfully instead of cycling pools.
    """
    msg  = message.lower().strip()
    turn = len(history) // 2

    # Cheatsheet / resource request
    if any(w in msg for w in ["cheatsheet", "cheat sheet", "cheat-sheet", "notes", "summary", "reference"]):
        topic_hint = ""
        for w in ["web", "database", "sql", "linked list", "tree", "graph", "algorithm", "oop", "network"]:
            if w in msg:
                topic_hint = w
                break
        if topic_hint:
            return f"**synco** nice, a cheatsheet for {topic_hint} is a great study tool 📝 what concepts do you want it to cover? start listing and i will help you build it out"
        return "**synco** good idea 📝 what topic is the cheatsheet for, and what level? like beginner syntax or deeper concepts?"

    # Code request
    if any(w in msg for w in ["code", "example", "snippet", "syntax", "implementation", "write", "show me"]):
        return "**synco** i cannot run code here but i can walk you through it 👀 what specifically are you trying to implement? describe the logic and we will figure it out together"

    # Help / stuck
    if any(w in msg for w in ["help", "stuck", "lost", "confused", "dont get", "don't get", "not sure"]):
        return "**synco** yeah okay, let's slow down 🤔 what's the last thing that made sense before it got confusing? start from there"

    # Greeting
    if any(w in msg for w in ["hi", "hello", "hey", "yo", "sup", "hiya", "how are", "how r"]):
        return "**synco** hey! 👋 what are we working on today?"

    # Agreement / got it
    if any(w in msg for w in ["yes", "yeah", "yep", "right", "exactly", "true", "got it", "makes sense", "okay", "ok"]):
        return "**synco** nice! now push it further 🎯 can you explain that same idea to one of your teammates without looking at your notes?"

    # Why / how / what question
    if any(w in msg for w in ["why", "how", "what", "explain", "difference", "between", "when to use"]):
        return "**synco** good question, what is your current understanding before i add anything? even a rough guess helps 🧩"

    # Want / need / request
    if any(w in msg for w in ["want", "need", "can you", "could you", "give me", "make", "create", "generate"]):
        return "**synco** on it, tell me more about what you need 👀 what is the context, what challenge are you working on?"

    # Default
    resp = "**synco** interesting, say more 👂 what is the specific part you are working through?"
    if team and turn > 1 and turn % 4 == 0:
        m = team[turn % len(team)]
        resp = f"**synco** what does {m['name']} think? connecting this to {m['topic']} might unlock something 🔗"
    return resp


def _load_group_history(group_id: str, limit: int = 20) -> list:
    try:
        df = sheet_read_all(TAB_SYNCO_LOG)
        if df.empty or "group_id" not in df.columns:
            return []
        gdf = df[df["group_id"] == group_id].tail(limit)
        history = []
        for _, row in gdf.iterrows():
            role = str(row.get("role", "user"))
            msg  = str(row.get("message", ""))
            if role in ("user", "assistant") and msg:
                history.append({"role": role, "content": msg})
        return history
    except Exception:
        return []


def chat_with_synco(message: str, history: list, state: dict):
    if not message.strip():
        return history, "", state

    history = list(history or [])
    group_id = state.get("group_id", "")
    email    = state.get("email", "")
    team     = state.get("team_members", [])
    topics   = ", ".join(m["topic"] for m in team) if team else "various topics"
    why      = state.get("why", "")
    conf     = state.get("confidence", "3")

    history = history + [{"role": "user", "content": message}]

    if email and group_id:
        log_synco(group_id, email, "user", message)

    ai_response = None
    if GROQ_API_KEY:
        # Seed with shared group history so Synco remembers cross-member context
        group_hist = _load_group_history(group_id) if group_id else []
        ctx_msgs = (group_hist + history)[-12:]

        system = (
            "You are Synco: a chill, knowledgeable friend who knows a lot about CS. "
            "You chat like you're over coffee, not lecturing. "
            "You never give the answer directly: you ask the right question so the student figures it out. "
            f"This group is studying: {topics}. "
            f"This student's confidence is {conf}/5: adjust depth accordingly. "
            + (f"They joined because: {why}. " if why else "")
            + "Style: use 1-2 emojis per message, max 3 sentences, "
            "sound like a smart friend not a textbook. "
            "If they're confused, validate first ('yeah that part trips everyone up') then guide. "
            "If they get it right, hype briefly then push further. "
            "No bullet points or headers ever."
        )
        try:
            from groq import Groq
            client = Groq(api_key=GROQ_API_KEY)
            resp = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "system", "content": system}] + ctx_msgs,
                max_tokens=150, temperature=0.85,
            )
            ai_response = "**synco** · " + resp.choices[0].message.content.strip()
        except Exception as e:
            print(f"Chat AI error: {e}")

    if not ai_response:
        ai_response = _fallback(message, history, team)

    if email and group_id:
        log_synco(group_id, email, "assistant", ai_response)

    history = history + [{"role": "assistant", "content": ai_response}]
    return history, "", state



# ══════════════════════════════════════════════════════════════════
#  GROUP BOARD (student-to-student messaging)
# ══════════════════════════════════════════════════════════════════

BOARD_HEADERS = ["timestamp", "group_id", "author_email", "author_name", "message"]


def board_post(message: str, state: dict) -> tuple:
    """Post a message to the group board. Returns (updated_display, cleared_input)."""
    if not state.get("group_id"):
        return _board_display(state), ""
    if not message.strip():
        return _board_display(state), ""

    row = [
        datetime.now(timezone.utc).isoformat(),
        state["group_id"],
        state.get("email", ""),
        state.get("name", "someone"),
        message.strip(),
    ]
    sheet_append(TAB_BOARD, BOARD_HEADERS, row)
    log_activity(state["group_id"], state.get("email", ""), "board_post", message.strip()[:60])
    return _board_display(state), ""


def _board_display(state: dict) -> str:
    if not state.get("group_id"):
        return "log in first to see your group board"

    try:
        df = sheet_read_all(TAB_BOARD)
        if df.empty or "group_id" not in df.columns:
            return "no messages yet. say something to your group 👋"

        gdf = df[df["group_id"] == state["group_id"]].tail(50)
        if gdf.empty:
            return "no messages yet. say something to your group 👋"

        my_email = state.get("email", "").lower()
        lines = []
        for _, row in gdf.iterrows():
            ts      = str(row.get("timestamp", ""))[:16].replace("T", " ")
            author  = str(row.get("author_name", "someone"))
            email   = str(row.get("author_email", "")).lower()
            msg     = str(row.get("message", ""))
            you     = " *(you)*" if email == my_email else ""
            lines.append(f"**{author}**{you} `{ts}`\n{msg}\n")

        return "\n---\n".join(lines)
    except Exception as e:
        print(f"board_display error: {e}")
        return "could not load messages"


def board_refresh(state: dict) -> str:
    return _board_display(state)

# ══════════════════════════════════════════════════════════════════
#  CSS
# ══════════════════════════════════════════════════════════════════

custom_css = """
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&display=swap');

:root {
    --page:     #0C0A09;
    --surf:     #131110;
    --card:     #1C1917;
    --input:    #242120;
    --bd:       #2E2A27;
    --bd-hi:    #4A4540;
    --t1:       #F2EDE8;
    --t2:       #A89F97;
    --t3:       #6B6460;
    --accent:   #D4374A;
    --acc-dim:  #7D1F2B;
    --acc-glo:  rgba(212,55,74,.15);
}

*, *::before, *::after { box-sizing: border-box; }
html, body { background: var(--page) !important; color: var(--t1) !important; }

.gradio-container, .gradio-container > div, .contain, .wrap, .app, main {
    background: var(--page) !important;
    color: var(--t1) !important;
    font-family: 'DM Sans', sans-serif !important;
    max-width: 900px !important;
    margin: 0 auto !important;
    padding: 0 28px !important;
}

#sync-header { text-align: center; padding: 52px 0 24px; background: transparent; }
#sync-header h1 {
    font-family: 'Syne', sans-serif !important;
    font-size: 58px !important; font-weight: 800 !important;
    color: var(--accent) !important; letter-spacing: -2px;
    margin: 0 0 8px; line-height: 1;
}
#sync-header p { color: var(--t3) !important; font-size: 13px; letter-spacing: .08em; text-transform: uppercase; margin: 0; }

.tabs > .tab-nav {
    background: var(--surf) !important; border: 1px solid var(--bd) !important;
    border-radius: 14px !important; padding: 5px !important; margin-bottom: 24px !important;
}
.tabs > .tab-nav button {
    background: transparent !important; color: var(--t3) !important; border: none !important;
    border-radius: 10px !important; font-family: 'DM Sans', sans-serif !important;
    font-weight: 500 !important; font-size: 13px !important; padding: 9px 16px !important;
    transition: all .15s ease !important;
}
.tabs > .tab-nav button:hover { background: rgba(212,55,74,.08) !important; color: var(--t1) !important; }
.tabs > .tab-nav button.selected { background: var(--accent) !important; color: #fff !important; font-weight: 600 !important; }

.tabitem, .tabitem > .block, .tab-content {
    background: transparent !important; border: none !important; padding: 0 !important;
}

.block {
    background: var(--card) !important; border: 1px solid var(--bd) !important;
    border-radius: 16px !important; padding: 28px 32px !important;
    margin-bottom: 14px !important; color: var(--t1) !important;
}
.gap { gap: 14px !important; background: transparent !important; }
.form { background: transparent !important; border: none !important; padding: 0 !important; }

.prose *, .md-prose *, [data-testid="markdown"] *,
.output-markdown *, .wrap *, p, li, span, strong, em, blockquote {
    color: var(--t1) !important; font-family: 'DM Sans', sans-serif !important; line-height: 1.75 !important;
}
h1, h2 { font-family: 'Syne', sans-serif !important; color: var(--t1) !important; font-weight: 700 !important; margin: 0 0 10px !important; }
h3, h4 { font-family: 'DM Sans', sans-serif !important; color: var(--t2) !important; font-weight: 500 !important; margin: 0 0 8px !important; }
hr  { border-color: var(--bd) !important; margin: 20px 0 !important; }
code { background: var(--input) !important; border: 1px solid var(--bd) !important; border-radius: 5px !important; padding: 2px 7px !important; color: var(--accent) !important; font-size: 13px !important; }

label, .label-wrap span {
    color: var(--t3) !important; font-size: 12px !important; font-weight: 500 !important;
    text-transform: uppercase !important; letter-spacing: .06em !important;
}

input[type=text], input[type=email], input[type=search],
input[type=number], input[type=password], textarea, select {
    background: var(--input) !important; border: 1px solid var(--bd) !important;
    border-radius: 10px !important; color: var(--t1) !important;
    font-family: 'DM Sans', sans-serif !important; font-size: 15px !important;
    padding: 12px 16px !important; transition: border-color .18s !important;
}
input[type=text]:focus, input[type=email]:focus, textarea:focus, select:focus {
    border-color: var(--accent) !important; outline: none !important;
    box-shadow: 0 0 0 3px var(--acc-glo) !important;
}
input::placeholder, textarea::placeholder { color: var(--t3) !important; }

/* ── range slider ── */
input[type=range] {
    -webkit-appearance: none !important; appearance: none !important;
    width: 100% !important; height: 6px !important;
    background: var(--bd) !important; border: none !important;
    border-radius: 3px !important; padding: 0 !important;
    accent-color: var(--accent) !important;
    margin: 10px 0 6px !important;
    box-shadow: none !important;
}
input[type=range]::-webkit-slider-thumb {
    -webkit-appearance: none !important; appearance: none !important;
    width: 18px !important; height: 18px !important;
    border-radius: 50% !important; background: var(--accent) !important;
    cursor: pointer !important; border: none !important;
}
input[type=range]::-moz-range-thumb {
    width: 18px !important; height: 18px !important;
    border-radius: 50% !important; background: var(--accent) !important;
    cursor: pointer !important; border: none !important;
}
.gradio-slider .block,
[data-testid="slider"] {
    padding: 20px 24px !important;
    background: var(--card) !important;
    border-radius: 12px !important;
    border: 1px solid var(--bd) !important;
    margin-bottom: 14px !important;
}
.gradio-slider span,
[data-testid="slider"] span,
[data-testid="slider"] .output-class {
    color: var(--t2) !important; font-size: 14px !important; display: block !important;
    margin-bottom: 8px !important;
}
.gradio-slider .value-text,
[data-testid="slider"] input[type=number] {
    color: var(--accent) !important; font-size: 22px !important;
    font-weight: 600 !important; font-family: 'Syne', sans-serif !important;
    background: transparent !important; border: none !important;
    padding: 0 !important; width: 48px !important;
}

/* ── checkboxes: explicit fix so blanket input rule doesn't break them ── */
input[type=checkbox] {
    width: 18px !important; height: 18px !important;
    padding: 0 !important; margin: 0 2px 0 0 !important;
    border-radius: 4px !important; border: 1.5px solid var(--bd-hi) !important;
    background: var(--input) !important; cursor: pointer !important;
    accent-color: var(--accent) !important;
    appearance: auto !important; -webkit-appearance: auto !important;
    flex-shrink: 0 !important;
}
input[type=checkbox]:checked {
    background: var(--accent) !important;
    border-color: var(--accent) !important;
}
.gradio-checkbox, .gradio-checkboxgroup {
    padding: 4px 0 !important;
}
.gradio-checkboxgroup .wrap {
    display: flex !important; flex-wrap: wrap !important;
    gap: 10px !important; padding: 10px 0 !important;
}
.gradio-checkboxgroup label {
    display: flex !important; align-items: center !important;
    gap: 8px !important; cursor: pointer !important;
    background: var(--input) !important; border: 1px solid var(--bd) !important;
    border-radius: 8px !important; padding: 8px 14px !important;
    font-size: 14px !important; color: var(--t1) !important;
    text-transform: none !important; letter-spacing: 0 !important;
    transition: border-color .15s, background .15s !important;
}
.gradio-checkboxgroup label:hover {
    border-color: var(--bd-hi) !important; background: var(--card) !important;
}
.gradio-checkboxgroup label:has(input:checked) {
    border-color: var(--accent) !important;
    background: rgba(212,55,74,.12) !important;
    color: var(--t1) !important;
}

button.primary {
    background: var(--accent) !important; color: #fff !important; border: none !important;
    border-radius: 10px !important; font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important; font-size: 14px !important; padding: 12px 26px !important;
    transition: background .15s, transform .1s !important;
}
button.primary:hover { background: #bf2d3e !important; transform: translateY(-1px) !important; }
button.primary:active { transform: translateY(0) !important; }

button.secondary {
    background: transparent !important; color: var(--t2) !important;
    border: 1px solid var(--bd-hi) !important; border-radius: 10px !important;
    font-family: 'DM Sans', sans-serif !important; font-weight: 400 !important;
    font-size: 13px !important; padding: 10px 20px !important;
    transition: border-color .15s, color .15s !important;
}
button.secondary:hover { border-color: var(--accent) !important; color: var(--t1) !important; }

.chatbot, [data-testid="chatbot"] {
    background: var(--surf) !important; border: 1px solid var(--bd) !important;
    border-radius: 16px !important; padding: 8px !important;
}
.message-wrap { padding: 12px 16px !important; }
.message.user-message, .message.user {
    background: var(--acc-dim) !important; border-radius: 14px 14px 4px 14px !important;
    padding: 12px 18px !important; margin: 6px 0 6px 22% !important; border: none !important;
}
.message.user-message *, .message.user * { color: #fff !important; }
.message.bot-message, .message.bot {
    background: var(--card) !important; border: 1px solid var(--bd) !important;
    border-radius: 14px 14px 14px 4px !important;
    padding: 12px 18px !important; margin: 6px 22% 6px 0 !important;
}
.message.bot-message *, .message.bot * { color: var(--t1) !important; }

::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: var(--bd-hi); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: var(--acc-dim); }

footer { display: none !important; }
"""


# ══════════════════════════════════════════════════════════════════
#  UI
# ══════════════════════════════════════════════════════════════════

with gr.Blocks(title="Synchrony") as demo:

    session  = gr.State({})
    reg_data = gr.State({})   # accumulates registration fields across steps

    gr.HTML("""
    <div id="sync-header">
        <h1>Synchrony</h1>
        <p>peer learning  |  ai-powered  |  built different</p>
    </div>
    """)

    # ── TAB: home ────────────────────────────────────────────────
    with gr.Tab("home"):
        with gr.Row():
            with gr.Column(scale=1):
                gr.Markdown("""
## what is this

Synchrony pairs you with peers studying **different but related** topics,
then drops AI-generated challenges that force everyone to teach what they know.

No passive reading. You learn by explaining.
                """)
            with gr.Column(scale=1):
                gr.Markdown("## log in")
                login_email  = gr.Textbox(label="university email", placeholder="you@university.edu")
                login_btn    = gr.Button("log in →", variant="primary", size="lg")
                login_output = gr.Markdown(value="")

        login_btn.click(fn=login, inputs=[login_email, session], outputs=[session, login_output])
        login_email.submit(fn=login, inputs=[login_email, session], outputs=[session, login_output])

    # ── TAB: register ────────────────────────────────────────────
    with gr.Tab("register"):
        gr.Markdown("## create your profile\n\nfour quick sections: takes about 2 minutes.")

        gr.Markdown("### 1 · who you are")
        with gr.Row():
            reg_name  = gr.Textbox(label="full name", placeholder="Sara Ahmed")
            reg_email = gr.Textbox(label="university email", placeholder="sara@university.edu")
        with gr.Row():
            reg_gender = gr.Dropdown(
                label="gender",
                choices=["female", "male", "non-binary / other", "prefer not to say"],
                value="prefer not to say",
                info="used only to keep groups gender-compatible for comfort: never shown publicly",
            )
            reg_tz = gr.Dropdown(
                label="your timezone",
                choices=TIMEZONES,
                value="UTC+2: Cairo, Amman, Beirut, Damascus, Jerusalem",
                info="so your group can find a meeting time that works",
            )

        gr.Markdown("---\n### 2 · what you study")
        reg_subject = gr.Dropdown(
            label="subject area",
            choices=SUBJECT_AREAS,
            value="Information Technology",
        )
        reg_topics = gr.Dropdown(
            label="topics you are currently working on",
            choices=CS_TOPICS,
            multiselect=True,
            info="pick everything on your plate right now: you can always update later",
        )
        gr.Markdown("**how solid is your grasp right now?** &nbsp; 1 = just started &nbsp;·&nbsp; 3 = getting there &nbsp;·&nbsp; 5 = pretty solid")
        reg_confidence = gr.Slider(
            label="confidence level",
            minimum=1, maximum=5, step=1, value=3,
        )
        reg_why = gr.Textbox(
            label="one sentence: why are you here?",
            placeholder="I keep getting lost when topics connect and want people to think with",
            max_lines=2,
            info="helps Synco understand how to talk to you",
        )

        gr.Markdown("---\n### 3 · how you work")
        reg_style = gr.Dropdown(
            label="study style",
            choices=[
                "discussion: talking through ideas out loud",
                "hands-on: solving problems together",
                "quiet: parallel work, check in occasionally",
            ],
            value=None,
            info="pick the one that sounds most like you",
        )
        reg_group_pref = gr.Dropdown(
            label="what kind of group do you want",
            choices=[
                "peer teaching: different topics, teach each other",
                "focused: same topic, go deep together",
                "no preference",
            ],
            value="peer teaching: different topics, teach each other",
        )
        reg_session_len = gr.Dropdown(
            label="preferred session length",
            choices=["30 min", "1 hour", "2 hours", "flexible"],
            value="1 hour",
        )
        reg_days = gr.CheckboxGroup(
            label="available days",
            choices=["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
        )
        reg_time = gr.Dropdown(
            label="preferred time of day",
            choices=["morning (8–12)", "afternoon (12–17)", "evening (17–22)", "flexible"],
            value="flexible",
        )

        gr.Markdown("---\n### 4 · readiness")
        reg_readiness = gr.Dropdown(
            label="where are you at right now",
            choices=[
                "ready to start: match me with a group",
                "just setting up my profile: not ready yet",
            ],
            value="ready to start: match me with a group",
        )

        reg_submit_btn = gr.Button("create account →", variant="primary", size="lg")
        reg_output     = gr.Markdown(value="")

        def do_register(name, email, gender, tz, subject, topics,
                        confidence, why, style, group_pref,
                        session_len, days, time_pref, readiness):
            if not name.strip():
                return "please enter your full name"
            if not email.strip() or "@" not in email:
                return "please enter a valid university email"
            if not topics:
                return "please select at least one topic you are studying"
            if not style:
                return "please pick a study style"
            rd = {
                "name":              name.strip(),
                "email":             email.strip().lower(),
                "gender":            gender or "prefer not to say",
                "timezone":          tz or "UTC+0",
                "subject_area":      subject or "Information Technology",
                "topics":            ", ".join(topics) if isinstance(topics, list) else str(topics),
                "confidence":        int(confidence),
                "why_here":          why.strip(),
                "study_style":       (style or "").split(":")[0].strip(),
                "group_preference":  (group_pref or "").split(":")[0].strip(),
                "session_length":    session_len or "flexible",
                "availability_days": ", ".join(days) if days else "",
                "availability_time": time_pref or "flexible",
                "readiness":         "ready" if "ready" in (readiness or "") else "setting up",
            }
            ok, msg = register_student(rd)
            if ok:
                suffix = ("your group will be assigned automatically: head to **log in** ✅"
                          if rd["readiness"] == "ready"
                          else "profile saved: come back when you are ready 👍")
                return f"### welcome, {name}!\n\n{suffix}"
            return f"### something went wrong\n\n{msg}"

        reg_submit_btn.click(
            fn=do_register,
            inputs=[reg_name, reg_email, reg_gender, reg_tz, reg_subject, reg_topics,
                    reg_confidence, reg_why, reg_style, reg_group_pref,
                    reg_session_len, reg_days, reg_time, reg_readiness],
            outputs=[reg_output],
        )

    # ── TAB: my team ─────────────────────────────────────────────
    with gr.Tab("my team"):
        gr.Markdown("## your group")
        team_display    = gr.Markdown(value="log in first →")
        team_refresh    = gr.Button("refresh", variant="secondary")

        gr.Markdown("---\n### propose a meeting time")
        with gr.Row():
            meeting_input  = gr.Textbox(label="suggest a time", placeholder="Saturday 3pm UTC+2", scale=4)
            meeting_btn    = gr.Button("propose →", variant="primary", scale=1)
        meeting_output   = gr.Markdown(value="")
        meeting_proposed = gr.Markdown(value="")

        def refresh_team(state):
            team_md    = get_team_info(state)
            proposed   = get_proposed_meeting(state)
            return team_md, proposed

        team_refresh.click(fn=refresh_team, inputs=[session], outputs=[team_display, meeting_proposed])
        meeting_btn.click(fn=propose_meeting, inputs=[meeting_input, session], outputs=[meeting_output])

    # ── TAB: group board ─────────────────────────────────────────
    with gr.Tab("group board"):
        gr.Markdown("""
## group board

your space to talk without Synco. leave notes, ask teammates, coordinate.
hit refresh to see new messages.
        """)
        board_display_md = gr.Markdown(value="log in first to see your group board")
        board_refresh_btn = gr.Button("refresh", variant="secondary")

        gr.Markdown("---")
        with gr.Row():
            board_input = gr.Textbox(
                label="",
                placeholder="write something to your group...",
                scale=5,
            )
            board_post_btn = gr.Button("post", variant="primary", scale=1)

        board_post_btn.click(
            fn=board_post,
            inputs=[board_input, session],
            outputs=[board_display_md, board_input],
        )
        board_input.submit(
            fn=board_post,
            inputs=[board_input, session],
            outputs=[board_display_md, board_input],
        )
        board_refresh_btn.click(
            fn=board_refresh,
            inputs=[session],
            outputs=[board_display_md],
        )

    # ── TAB: challenges ──────────────────────────────────────────
    with gr.Tab("challenges"):
        gr.Markdown("""
## challenges

ai-generated around your group's exact topics.
every member has a teaching role — no passengers.
        """)
        load_btn           = gr.Button("generate challenges →", variant="primary", size="lg")
        challenges_display = gr.Markdown(value="log in and hit the button ↑")
        load_btn.click(fn=load_challenges, inputs=[session], outputs=[session, challenges_display])

    # ── TAB: hints ───────────────────────────────────────────────
    with gr.Tab("hints"):
        gr.Markdown("## stuck? get a hint")
        with gr.Row():
            challenge_select   = gr.Dropdown(label="challenge", choices=["1","2","3"], value="1", scale=1)
            hint_level_select  = gr.Dropdown(
                label="how much help",
                choices=["1 - gentle nudge", "2 - clearer guidance", "3 - almost there"],
                value="1 - gentle nudge", scale=2,
            )
        hint_btn     = gr.Button("get hint →", variant="primary", size="lg")
        hint_display = gr.Markdown(value="generate challenges first, then come here")
        hint_btn.click(fn=request_hint,
                       inputs=[challenge_select, hint_level_select, session],
                       outputs=[hint_display])

    # ── TAB: chat ────────────────────────────────────────────────
    with gr.Tab("chat"):
        gr.Markdown("""
## synco

your group's ai tutor. shared memory: everyone's questions feed the same context.
        """)
        chatbot   = gr.Chatbot(value=[], label="", height=440)
        with gr.Row():
            msg_input = gr.Textbox(label="", placeholder="what are you working through?", scale=5)
            send_btn  = gr.Button("send", variant="primary", scale=1)

        send_btn.click(
            fn=chat_with_synco,
            inputs=[msg_input, chatbot, session],
            outputs=[chatbot, msg_input, session],
        )
        msg_input.submit(
            fn=chat_with_synco,
            inputs=[msg_input, chatbot, session],
            outputs=[chatbot, msg_input, session],
        )

demo.launch(server_name="0.0.0.0", css=custom_css, ssr_mode=False)
