import streamlit as st
import gspread
import json
from oauth2client.service_account import ServiceAccountCredentials

# === CONNECT TO GOOGLE SHEET ===
SHEET_NAME = "yes-or-no-game"
CREDENTIALS_PATH = "credentials.json"

@st.cache_resource
def connect_sheet():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_PATH, scope)
    client = gspread.authorize(creds)
    return client.open(SHEET_NAME).sheet1

sheet = connect_sheet()

def read_state():
    records = sheet.get_all_records()
    return {row['key']: json.loads(row['value']) for row in records}

def write_state(state):
    for key, val in state.items():
        cell = sheet.find(key)
        if cell:
            sheet.update_cell(cell.row, 2, json.dumps(val))
        else:
            sheet.append_row([key, json.dumps(val)])

# === INITIAL SETUP ===
st.set_page_config(page_title="ใช่หรือไม่ Game", layout="wide")
st.title("🧠 เกม 'ใช่หรือไม่' - Google Sheet Edition")
state = read_state()

if "phase" not in state:
    state = {
        "phase": "setup",
        "players": [],
        "avatars": {},
        "scores": {},
        "current_owner_idx": 0,
        "current_turn_idx": 0,
        "answer": "",
        "question_history": [],
        "ask_count": {},
        "rounds_left": 0,
    }
    write_state(state)

if state["phase"] == "setup":
    st.header("🎮 ตั้งค่าผู้เล่นและจำนวนรอบ")
    num_players = st.slider("จำนวนผู้เล่น (2-10 คน)", 2, 10, 2)
    total_rounds = st.number_input("จำนวนรอบที่แต่ละคนจะได้ตั้งคำตอบ", min_value=1, value=1)

    avatars_list = ["🐱", "🐶", "🐵", "🐰", "🐼", "🐸", "🦊", "🐯", "🐮", "🐷"]
    names = []
    avatars = {}

    for i in range(num_players):
        col1, col2 = st.columns([2, 1])
        with col1:
            name = st.text_input(f"ชื่อผู้เล่นคนที่ {i+1}", key=f"player_{i}")
        with col2:
            avatar = st.selectbox("Avatar", avatars_list, key=f"avatar_{i}")
        if name:
            names.append(name)
            avatars[name] = avatar

    if st.button("✅ เริ่มเกม") and len(names) == num_players:
        state["players"] = names
        state["avatars"] = avatars
        state["scores"] = {name: 0 for name in names}
        state["rounds_left"] = total_rounds * len(names)
        state["phase"] = "set_answer"
        write_state(state)
        st.rerun()

elif state["phase"] == "set_answer":
    owner = state["players"][state["current_owner_idx"]]
    st.subheader(f"👑 {owner} ({state['avatars'].get(owner, '👤')}) ตั้งคำตอบลับ")
    answer = st.text_input("คำตอบลับของคุณ (จะถูกซ่อนไว้)", type="password")

    if st.button("🔒 ล็อคคำตอบและเริ่มรอบ") and answer:
        state["answer"] = answer
        state["question_history"] = []
        state["ask_count"] = {name: 0 for name in state["players"]}
        state["phase"] = "playing"
        write_state(state)
        st.rerun()

elif state["phase"] == "playing":
    st.subheader("📜 คำถามก่อนหน้า:")
    for q in state["question_history"]:
        color = "green" if "→ ใช่" in q else "red"
        st.markdown(f"<div style='color:{color}; font-size:18px;'>• {q}</div>", unsafe_allow_html=True)

    current_player = state["players"][state["current_turn_idx"]]
    st.markdown(f"### 🧠 ถึงตาของ: {current_player} {state['avatars'].get(current_player, '👤')}")
    action = st.radio("เลือกทำ", ["ถาม", "ตอบ"])

    if action == "ถาม":
        with st.form("ask_form"):
            question = st.text_input("คำถามของคุณ (ลงท้ายด้วย 'ใช่หรือไม่'):")
            submitted = st.form_submit_button("ถาม")
        if submitted and question:
            state["phase"] = "owner_answer"
            state["last_question"] = question + " ใช่หรือไม่"
            write_state(state)
            st.rerun()

    elif action == "ตอบ":
        with st.form("answer_form"):
            guess = st.text_input("คำตอบของคุณ:")
            submitted = st.form_submit_button("ตอบ")
        if submitted:
            if guess.strip().lower() == state["answer"].lower():
                st.success(f"🎉 {current_player} ตอบถูก! ได้ 1 คะแนน")
                state["scores"][current_player] += 1
                state["phase"] = "result"
            else:
                st.warning("❌ ตอบผิด ตกรอบ")
            write_state(state)
            st.rerun()

elif state["phase"] == "owner_answer":
    owner = state["players"][state["current_owner_idx"]]
    st.markdown(f"### 👑 คำถาม: {state['last_question']}")
    ans = st.radio("เลือกคำตอบของคุณ", ["ใช่", "ไม่ใช่"])
    if st.button("✅ ตอบกลับ"):
        full_q = f"{state['last_question']} → {ans}"
        state["question_history"].append(full_q)
        state["phase"] = "playing"
        state["ask_count"][owner] += 1
        write_state(state)
        st.rerun()

elif state["phase"] == "result":
    st.subheader("📊 สรุปคะแนน:")
    for name, score in state["scores"].items():
        avatar = state["avatars"].get(name, "👤")
        st.markdown(f"- {avatar} **{name}**: {score} คะแนน")

    if state["rounds_left"] > 1:
        if st.button("🔁 เริ่มรอบถัดไป"):
            state["rounds_left"] -= 1
            state["current_owner_idx"] = (state["current_owner_idx"] + 1) % len(state["players"])
            state["phase"] = "set_answer"
            write_state(state)
            st.rerun()
    else:
        st.success("🎉 เกมจบแล้ว!")
        funny_titles = ["แชมป์ผู้รู้ใจคำลับ", "เทพตรรกะ 3000", "นักสืบสายฮา"]
        st.markdown(f"## 🏆 ผู้ชนะคือ: {max(state['scores'], key=state['scores'].get'])} 🥳")
        st.caption(f"{funny_titles[state['scores'][max(state['scores'], key=state['scores'].get'])] % 3]}")
        if st.button("🔁 เริ่มใหม่"):
            sheet.clear()
            sheet.append_row(["key", "value"])
            st.rerun()
