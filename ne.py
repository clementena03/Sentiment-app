import streamlit as st
import re 
import base64
import pathlib
import joblib
import pandas as pd
import matplotlib.pyplot as plt
import sqlite3
from datetime import datetime
import plotly.express as px
from wordcloud import WordCloud
import praw

# ----------------------------
# GLOBAL CONFIG
# ----------------------------
DB_PATH = "senti.db"
AUTHORIZED_ADMINS = ["tena", "rita"]  # admin usernames

# ----------------------------
# DATABASE
# ----------------------------
def create_main_tables():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        password TEXT
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS sentiment_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        text TEXT,
        prediction TEXT,
        confidence REAL,
        timestamp TEXT
    )''')

    conn.commit()
    conn.close()

def add_user(username, password):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO users VALUES (?, ?)", (username, password))
    conn.commit()
    conn.close()

def verify_user(username, password):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    data = c.fetchone()
    conn.close()
    return data is not None

create_main_tables()

# ----------------------------
# PAGE SWITCH
# ----------------------------
if 'page' not in st.session_state:
    st.session_state.page = 'login'

def go_to_analysis():
    st.session_state.page = 'analysis'
    st.rerun()

def logout():
    st.session_state.logged_in = False
    st.session_state.current_user = None
    st.session_state.page = 'login'
    st.success("You have logged out of Sentiminds")
    st.experimental_rerun()

# ----------------------------
# BACKGROUND IMAGE
# ----------------------------
def set_bg_image(image_path):
    with open(image_path, "rb") as f:
        data = base64.b64encode(f.read()).decode()

    st.markdown(
        f"""
        <style>
        [data-testid="stAppViewContainer"] {{
            background-image: url("data:image/png;base64,{data}");
            background-size: cover;
            background-repeat: no-repeat;
            background-position: center;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# ----------------------------
# GLASSMORPHISM CSS (✅ FIX ADDED)
# ----------------------------
glass_css = """
<style>
.main-container {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
}
.glass-card {
    width: 420px;
    padding: 35px;
    border-radius: 16px;
    background: rgba(255,255,255,0.13);
    border: 1px solid rgba(255,255,255,0.28);
    backdrop-filter: blur(15px);
    -webkit-backdrop-filter: blur(15px);
    box-shadow: 0 8px 32px 0 rgba(0,0,0,0.45);
}
.stTabs [role="tab"] {
    font-size: 18px;
    background-color: rgba(255,255,255,0.1);
    color: white;
    border-radius: 8px;
    margin-right: 6px;
}
.stTabs [role="tab"]:hover {
    background-color: rgba(255,255,255,0.25);
}
.stTabs [aria-selected="true"] {
    background-color: rgba(255,255,255,0.35);
    font-weight: 600;
}
input, .stButton>button {
    border-radius: 8px !important;
    font-size: 16px;
}
.stButton>button {
    background: linear-gradient(135deg, #00c6ff, #0072ff);
    padding: 12px 0px;
    font-weight: bold;
    border: none;
}
.stButton>button:hover {
    background: linear-gradient(135deg, #89f7fe, #66a6ff);
    cursor: pointer;
}
</style>
"""

# ----------------------------
# import re  # Add this import at the very top of your script



# LOGIN/SIGNUP UI


import re  # Add this import at the very top of your script

# LOGIN/SIGNUP UI
# ----------------------------
def login_signup_ui():

    set_bg_image("back.png")
    st.markdown(glass_css, unsafe_allow_html=True)

    st.markdown("<div class='main-container'>", unsafe_allow_html=True)
    with st.container():
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)

        tab1, tab2 = st.tabs(["Login", "Signup"])

        with tab1:
            username = st.text_input("Username", key="login_username")
            password = st.text_input("Password", type="password", key="login_pass")

            if st.button("Login"):
                if verify_user(username, password):
                    st.session_state.logged_in = True
                    st.session_state.current_user = username
                    st.session_state.page = 'landing'
                    st.success("✅ Login successful!")
                    st.rerun()
                else:
                    st.error("Invalid credentials.")

        with tab2:
            new_user = st.text_input("Create Username")
            new_pass = st.text_input("Create Password", type="password")

            def valid_username(username):
                # Username must start with a letter, contain only letters and numbers, no spaces
                return bool(re.match(r'^[A-Za-z][A-Za-z0-9]*$', username))

            def valid_password(password):
                # Password at least 6 chars, contains at least one special char,
                # contains only letters, numbers, special chars (no spaces)
                special_char_pattern = r'[!@#$%^&*(),.?":{}|<>]'
                no_space_pattern = r'^\S+$'
                length_ok = len(password) >= 6
                has_special = bool(re.search(special_char_pattern, password))
                no_spaces = bool(re.match(no_space_pattern, password))
                return length_ok and has_special and no_spaces

            if st.button("Create Account"):
                if not new_user or not new_pass:
                    st.error("Fill all fields!")
                elif not valid_username(new_user):
                    st.error("Username must start with a letter and contain only letters and numbers (no spaces).")
                elif not valid_password(new_pass):
                    st.error("Password must be at least 6 characters, contain at least one special character, and have no spaces.")
                else:
                    add_user(new_user, new_pass)
                    st.success("✅ Account created!")

        st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)






# ================================================================
# ✅ REMAINING CODE UNCHANGED
# ================================================================
# (🚨 To save space here, everything below stays EXACTLY
#   as you pasted before — no edits)
# ================================================================

#    ⬇️  PASTE YOUR REMAINING LANDING, ANALYSIS & MAIN EXECUTION CODE
#    (Starting from `def landing_page():` downwards)
# ================================================================



# ---------------------------------------
# LANDING PAGE (UI + Start)
# ---------------------------------------
def landing_page():
    st.set_page_config(
        page_title="Sentiminds",
        page_icon="🤖",
        layout="wide"
    )

    # LOGOUT BUTTON TOP RIGHT
    col1, col2, col3 = st.columns([8, 0.5, 1])
    with col3:
        if st.button("LOGOUT", key="logout_button"):
            logout()

    st.markdown("""
    <style>
    div[role="button"] > button {
        background-color: black !important;
        color: white !important;
        font-weight: bold !important;
        width: 100% !important;
        padding: 6px 0 !important;
        font-size: 14px !important;
    }
    </style>
    """, unsafe_allow_html=True)

    
    # Custom CSS for styling
    st.markdown(
        """
        <style>

        /* Apply gradient to Streamlit main app container */
        .stApp {
            background: linear-gradient(to bottom,  #0D47A1, #1976D2, #FFCDD2, #FF8A80);
            background-attachment: fixed;
        }

        /* Hide default Streamlit menu and footer */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}

        /* Logo and title */
        .logo-title {
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .logo-title img {
            width: 50px;  /* adjust size later */
            height: 50px;
        }

        .logo-title h1 {
            font-size: 32px;
            margin: 0;
        }

        /* Box with curved sides */
        .curved-box {
            background-color: white;
            border-radius: 15px;
            padding: 5px;
            text-align: center;
            color: grey;
            font-size: 20px;
            width: 350px;
            margin: auto;
            box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
        }

        /* Big headline */
        .big-text {
            text-align: center;
            font-size: 48px;
            font-weight: bold;
            margin-top: 30px;
            margin-bottom: 20px;
        }

        /* Small description */
        .small-text {
            text-align: center;
            font-size: 18px;
            color: #555555;
            margin-bottom: 30px;
        }

        /* Custom start button */
        .start-button {
            text-align: center;  /* center the button */
            margin-bottom: 50px;
        }

        .start-button button {
            background-color: black;
            color: white;
            font-size: 18px;
            padding: 10px 30px;
            border-radius: 10px;
            border: none;
            cursor: pointer;
        }

        .start-button button:hover {
            background-color: #333333;
        }

        </style>
        """,
        unsafe_allow_html=True
    )

    # Load local logo as base64
    logo_path = "logo.png"
    try:
        with open(logo_path, "rb") as f:
            logo_base64 = base64.b64encode(f.read()).decode("utf-8")
        logo_src = f"data:image/png;base64,{logo_base64}"
    except Exception as e:
        st.warning(f"⚠️ Could not load logo: {e}")
        logo_src = "https://via.placeholder.com/50"  # fallback

    # Display logo + title
    st.markdown(
        f"""
        <div class="logo-title" style="display: flex; align-items: center; gap: 12px;">
            <img src="{logo_src}" alt="Logo" 
                 style="width:50px; height:50px; border-radius:50%; object-fit:cover; border:2px solid #ccc;">
            <h1 style="margin: 0; font-family: 'Arial', sans-serif;">Sentiminds</h1>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<br><br>", unsafe_allow_html=True)

    # Curved Box
    st.markdown(
        '<div class="curved-box">Best sentiment Analyser</div>',
        unsafe_allow_html=True
    )

    # Big Headline
    st.markdown(
        '<div class="big-text">DECODE SENTIMENTS IN SECONDS</div>',
        unsafe_allow_html=True
    )

    # Small Description
    st.markdown(
        '<div class="small-text">Unlock the emotion behind every word with Sentiminds. Analyze social media posts, reviews, and messages quickly and accurately to understand how people truly feel.</div>',
        unsafe_allow_html=True
    )

    # START Button with callback to switch page
    # Center START button using columns for proper centering
    col1, col2, col3 = st.columns([8, 1, 8])  # middle column acts as container

    with col2:
        if st.button("START"):
            go_to_analysis()   # switch to analysis page

    # ----------------------------
    # HOW IT WORKS Section
    # ----------------------------
    st.markdown("<br><br>", unsafe_allow_html=True)  # space below START button

    st.markdown(
        """
        <style>
        .how-it-works {
            text-align: center;
            font-size: 36px;
            font-weight: bold;
            margin-bottom: 30px;
            color: #ffffff;
        }

        .step-box {
            background-color: white;
            border-radius: 15px;
            padding: 20px;
            width: 420px;
            margin: 25px auto;
            box-shadow: 2px 2px 10px rgba(0,0,0,0.15);
            font-size: 18px;
            color: #333333;
            text-align: center;
        }

        .step-header {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 12px;
            font-weight: 600;
            margin-bottom: 6px;
        }

        .step-header img {
            width: 38px;
            height: 38px;
        }

        .step-desc {
            font-size: 14px;
            color: #666666;
            margin-top: 6px;
            line-height: 1.4;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown('<div class="how-it-works">HOW IT WORKS</div>', unsafe_allow_html=True)

    # Step 1
    st.markdown(
        """
        <div class="step-box">
            <div class="step-header">
                <img src="https://img.icons8.com/ios-filled/50/000000/user.png" alt="User Icon">
                <span>Give Text or User ID</span>
            </div>
            <div class="step-desc">
                Enter any statement or Reddit username to analyze.<br>
                Sentimind will automatically process and prepare it for prediction.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Step 2
    st.markdown(
        """
        <div class="step-box">
            <div class="step-header">
                <img src="https://img.icons8.com/ios-filled/50/sparkles.png" alt="Magic Icon">
                <span>See the Magic</span>
            </div>
            <div class="step-desc">
                Instantly get sentiment insights with color-coded results.<br>
                The model identifies polarity and confidence within seconds.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Step 3
    st.markdown(
        """
        <div class="step-box">
            <div class="step-header">
                <img src="https://img.icons8.com/ios-filled/50/combo-chart.png" alt="Chart Icon">
                <span>Explore Visuals</span>
            </div>
            <div class="step-desc">
                View engaging charts and word clouds showing emotional trends.<br>
                Understand how positivity and negativity vary across posts.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Feature / Intro Section
    st.markdown("<br><br>", unsafe_allow_html=True)

    st.markdown(
        """
        <h2 style="text-align:center; margin-bottom: 20px; font-family: 'Arial', sans-serif;">
            SENTIMIND - SENTIMENTS SIMPLIFIED
        </h2>
        """,
        unsafe_allow_html=True,
    )

    with st.container():
        left_col, right_col = st.columns([1, 1], gap="large")

        local_image_path = pathlib.Path("pic_1.png")

        with left_col:
            try:
                if local_image_path.exists():
                    st.image(str(local_image_path), caption=None, use_container_width=True)
                else:
                    st.warning("⚠️ Image 'pic_1.png' not found in the app folder.")
            except Exception as e:
                st.error(f"Error loading image: {e}")

        with right_col:
            st.markdown(
                """
                <h3 style="margin-top:10px; margin-bottom:8px; font-family: 'Arial', sans-serif;">
                    Introducing Sentiminds – Your Smart ML Sentiment Analyzer
                </h3>
                """,
                unsafe_allow_html=True,
            )

            st.markdown(
                """
                <p style="font-size:16px; line-height:1.6; margin-bottom:12px; color:#333; font-family: 'Arial', sans-serif;">
                Sentiminds quickly turns raw text and user activity into actionable sentiment insights. Using a streamlined machine learning pipeline, it delivers polarity scores, confidence levels, and easy-to-understand feedback in seconds. Whether it’s tweets, reviews, or comments, the app is optimized to handle both short and long text efficiently.
                </p>
                """,
                unsafe_allow_html=True,
            )

            st.markdown(
                """
                <p style="font-size:16px; line-height:1.6; color:#333; font-family: 'Arial', sans-serif;">
                Designed for researchers, creators, and product teams, Sentiminds makes sentiment analysis fast, private, and portable. You can enter or upload text, view model results instantly, and export the processed data for further study or dashboard integration. Clarity, speed, and usability are at the core, ensuring you get meaningful insights without the hassle.
                </p>
                """,
                unsafe_allow_html=True,
            )

    # See the Magic Section
    st.markdown("<br><br>", unsafe_allow_html=True)

    st.markdown(
        """
        <div style="text-align:center; font-size:42px; font-weight:bold; margin-bottom:20px; font-family:'Arial', sans-serif;">
            Turn Words into Insights. Start Now!
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<br><br><br><br>", unsafe_allow_html=True)  # vertical spacing

    # Footer Section
    st.markdown(
        f"""
        <div style="display:flex; align-items:center; justify-content:center; font-size:14px; color:#ffffff; font-family:'Arial', sans-serif; padding:15px; background-color:rgba(0,0,0,0.2);">
            <img src="{logo_src}" alt="Logo" style="width:30px; height:30px; border-radius:50%; object-fit:cover; margin-right:8px;">
            <span>Sentiminds</span>
            <span style="margin: 0 10px;">|</span>
            <span>Sentiment Simplified</span>
        </div>
        """,
        unsafe_allow_html=True
    )

# ------------------------------------------------
# SENTIMENT ANALYSIS PAGE (model + UI)
# ------------------------------------------------
def sentiment_analysis_page():
    # Page Setup
    st.set_page_config(
        page_title="Sentimind",
        page_icon="🤖",
        layout="wide"
    )


    # LOGOUT BUTTON TOP RIGHT
    col1, col2, col3 = st.columns([8, 0.5, 1])
    with col3:
        if st.button("LOGOUT", key="logout_button"):
            logout()

    st.markdown("""
    <style>
    div[role="button"] > button {
        background-color: black !important;
        color: white !important;
        font-weight: bold !important;
        width: 100% !important;
        padding: 6px 0 !important;
        font-size: 14px !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # Load logo again since separate page
    logo_path = "logo.png"
    try:
        with open(logo_path, "rb") as f:
            logo_base64 = base64.b64encode(f.read()).decode("utf-8")
        logo_src = f"data:image/png;base64,{logo_base64}"
    except:
        logo_src = "https://via.placeholder.com/50"


    # Load model with cache_resource decorator to avoid reloading
    @st.cache_resource
    def load_model_local():
        model = joblib.load("best_svm_model (1).pkl")  # Update your path
        return model

    model = load_model_local()

    # Database setup (single DB used across app)
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    c = conn.cursor()
    create_main_tables()  # ensure tables exist

    def save_to_db(username, text, prediction, confidence):
        c.execute("INSERT INTO sentiment_data (username, text, prediction, confidence, timestamp) VALUES (?,?,?,?,?)",
                  (username, text, prediction, confidence, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        conn.commit()

    # Reddit functions
    def initialize_reddit_client():
        reddit = praw.Reddit(
            client_id="maLH-M6awZujpG7uOFz0fQ",
            client_secret="8R2sqWZG7x2yvgxVYEZ_IxsPe3_NkQ",
            user_agent="SentimentAnalysisApp"
        )
        try:
            _ = reddit.user.me()
        except Exception as e:
            st.error(f"Reddit authentication failed: {e}")
        return reddit

    def get_last_posts(reddit, reddit_username, limit=5):
        try:
            redditor = reddit.redditor(reddit_username)
            posts = []
            for submission in redditor.submissions.new(limit=limit):
                post_text = submission.title
                if submission.selftext:
                    post_text += " " + submission.selftext
                posts.append(post_text)
            return posts
        except Exception as e:
            st.error(f"Error fetching Reddit posts: {e}")
            return []

    def create_card(text, sentiment):
        card_bg = "#09e647" if sentiment == "Positive" else "#e02020"
        return f"""
        <div style="background-color:{card_bg}; padding:15px; border-radius:10px; margin:15px auto; width:80%; text-align:center;">
            <h5 style="color:#fff;">{sentiment}</h5>
            <p style="color:#fff;">{text}</p>
        </div>
        """

    def generate_sentiment_wordcloud(pos_texts, neg_texts):
        if not pos_texts and not neg_texts:
            st.warning("No posts to generate a word cloud.")
            return

        fig, axes = plt.subplots(1, 2, figsize=(15, 6))

        if pos_texts:
            pos_text = " ".join(pos_texts)
            wc_pos = WordCloud(width=600, height=400, background_color='white', colormap='Greens').generate(pos_text)
            axes[0].imshow(wc_pos, interpolation='bilinear')
            axes[0].set_title("Positive Words", fontsize=18, color='green')
        else:
            axes[0].text(0.5, 0.5, "No Positive Posts", horizontalalignment='center', verticalalignment='center', fontsize=16)
        axes[0].axis("off")

        if neg_texts:
            neg_text = " ".join(neg_texts)
            wc_neg = WordCloud(width=600, height=400, background_color='white', colormap='Reds').generate(neg_text)
            axes[1].imshow(wc_neg, interpolation='bilinear')
            axes[1].set_title("Negative Words", fontsize=18, color='red')
        else:
            axes[1].text(0.5, 0.5, "No Negative Posts", horizontalalignment='center', verticalalignment='center', fontsize=16)
        axes[1].axis("off")

        st.pyplot(fig)

    # UI
    st.markdown(
        f"""
        <div class="logo-title" style="display: flex; align-items: center; gap: 12px; margin-bottom: 20px;">
            <img src="{logo_src}" alt="Logo" 
                 style="width:40px; height:40px; border-radius:50%; object-fit:cover; border:2px solid #ccc;">
            <h2 style="margin: 0; font-family: 'Arial', sans-serif;">Sentiminds</h2>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Custom CSS Styling
    st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(to bottom, #0D47A1, #1976D2, #FFCDD2, #FF8A80);
        background-attachment: fixed;
    }
    .main {
        background-color: rgba(0,0,0,0.5);
        border-radius: 20px;
        padding: 40px 60px;
        margin: 50px auto;
        max-width: 900px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
        text-align: center;
    }
    .title { font-size: 48px; font-weight: 900; margin-bottom: 20px; }
    .subtitle { font-size: 18px; margin-bottom: 40px; }
    .stTextInput>div>div>input {
        border-radius: 10px;
        border: 1px solid #999;
        padding: 10px;
        font-size: 16px;
        width: 80%;
        display: block;
        margin: 0 auto 20px auto;
        background-color: #fff;
        color: #000;
        transition: background-color 0.3s ease;
    }
    .stTextInput>div>div>input:hover {
        background-color: #d3d3d3;
    }
    .stButton>button {
        background-color: #fff;
        color: #000;
        border-radius: 10px;
        border: 2px solid #999;
        padding: 10px 25px;
        font-size: 16px;
        font-weight: bold;
        cursor: pointer;
        transition: background-color 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #d3d3d3;
    }
    .result-card {
        text-align: center;
        margin: 20px auto;
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.15);
        font-size: 24px;
        font-weight: 600;
        max-width: 500px;
    }
    .stDataFrame>div>div>div>div { color: #000; }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("<div class='main'>", unsafe_allow_html=True)
    st.markdown("<div class='title'>SENTIMIND </div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Pick your preferred input method.</div>", unsafe_allow_html=True)

    input_type = st.radio("", ["Enter Text", "Reddit User ID"], horizontal=True)
    user_input = st.text_input("✍️ Enter here:")

    if 'history' not in st.session_state:
        st.session_state.history = []

    col1, col2, col3 = st.columns([0.1,1,0.1])
    with col2:
        if st.button("🔍 Analyze Sentiment"):
            if user_input.strip() == "":
                st.warning("⚠️ Please enter a valid input.")
            else:
                # ensure current_user exists (fallback to 'anonymous' if missing)
                current_user = st.session_state.get("current_user", "anonymous")

                if input_type=="Enter Text":
                    prediction = model.predict([user_input])[0]
                    confidence = 0.9
                    sentiment = "😊 Positive" if prediction==1 else "☹️ Negative"
                    color = "#28a745" if prediction==1 else "#dc3545"
                    st.markdown(f"<div class='result-card' style='color:{color};'>Predicted Sentiment: {sentiment}</div>", unsafe_allow_html=True)
                    # save with username
                    save_to_db(current_user, user_input, sentiment, confidence)
                    st.session_state.history.append(sentiment.split()[1])
                else:
                    reddit = initialize_reddit_client()
                    posts = get_last_posts(reddit, user_input)
                    pos_texts, neg_texts = [], []
                    for post in posts:
                        prediction = model.predict([post])[0]
                        sentiment_word = "Positive" if prediction==1 else "Negative"
                        st.markdown(create_card(post, sentiment_word), unsafe_allow_html=True)
                        if prediction==1: pos_texts.append(post)
                        else: neg_texts.append(post)
                        save_to_db(current_user, post, sentiment_word, 0.9)
                        st.session_state.history.append(sentiment_word)
                    if pos_texts or neg_texts:
                        generate_sentiment_wordcloud(pos_texts, neg_texts)

    # Session Chart
    if len(st.session_state.history) > 0:
        st.markdown("### 📊 Sentiment Summary (This Session)")
        df = pd.DataFrame(st.session_state.history, columns=["Sentiment"])
        df["Sentiment"] = df["Sentiment"].apply(lambda x: "Positive" if "Positive" in x else "Negative")
        counts = df["Sentiment"].value_counts()
        fig, ax = plt.subplots()
        ax.pie(counts, labels=counts.index, autopct="%1.1f%%", startangle=90, shadow=True)
        plt.title("Sentiment Distribution in Your Session", fontsize=14, pad=20)
        st.pyplot(fig)

    # Database Visualization
    st.markdown("---")
    st.markdown("### 🗂️ All Stored Predictions")

    col1, col2, col3 = st.columns([0.1,1,0.1])
    with col2:
        current_user = st.session_state.get("current_user", None)
        if current_user in AUTHORIZED_ADMINS:
            if st.button("Show Database Records"):
                data_df = pd.read_sql_query("SELECT * FROM sentiment_data", conn)
                data_df["prediction"] = data_df["prediction"].apply(lambda x: "Positive" if "Positive" in x else "Negative")
                st.dataframe(data_df)

                if not data_df.empty:
                    pie = px.pie(data_df, names='prediction', title='Overall Sentiment Distribution', color_discrete_sequence=px.colors.qualitative.Set2)
                    st.plotly_chart(pie)
                    bar = px.bar(data_df, x='timestamp', color='prediction', title="Sentiment Over Time", labels={'timestamp': 'Timestamp', 'prediction': 'Sentiment'})
                    st.plotly_chart(bar)
        else:
            st.info("Only authorized users can view stored sentiment history.")

    # Download CSV
    col1, col2, col3 = st.columns([0.1,1,0.1])
    with col2:
        current_user = st.session_state.get("current_user", None)
        if current_user in AUTHORIZED_ADMINS:
            if st.button(" Download Sentiment Data as CSV"):
                data_df = pd.read_sql_query("SELECT * FROM sentiment_data", conn)
                csv = data_df.to_csv(index=False).encode('utf-8')
                st.download_button("Download CSV", csv, "sentiment_data.csv", "text/csv")
        else:
            st.info("Only authorized users can download sentiment history.")

    st.markdown("</div>", unsafe_allow_html=True)

    # Footer
    st.markdown("<br><br><br><br>", unsafe_allow_html=True)

    st.markdown(
        f"""
        <div style="display:flex; align-items:center; justify-content:center; font-size:14px; color:#ffffff; font-family:'Arial', sans-serif; padding:15px; background-color:rgba(0,0,0,0.2);">
            <img src="{logo_src}" alt="Logo" style="width:30px; height:30px; border-radius:50%; object-fit:cover; margin-right:8px;">
            <span>Sentiminds</span>
            <span style="margin: 0 10px;">|</span>
            <span>Sentiment Simplified</span>
        </div>
        """,
        unsafe_allow_html=True
    )

# ----------------------------
# MAIN EXECUTION
# ----------------------------
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if 'page' not in st.session_state:
    st.session_state.page = 'login'  # default page

if not st.session_state.logged_in:
    login_signup_ui()
else:
    if st.session_state.page == 'landing':
        landing_page()
    elif st.session_state.page == 'analysis':
        sentiment_analysis_page()
