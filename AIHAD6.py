import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import os
import qrcode
from io import BytesIO


# -------------------------------------------------------------
# Page config
# -------------------------------------------------------------
st.set_page_config(
    page_title="Key Techniques for Communicating Ih Data Decisions",
    layout="wide",
    initial_sidebar_state="expanded"
)
# -------------------------------------------------------------
# Page registry
# -------------------------------------------------------------
PAGES = [
    "Home",
    "Intro",
    "Context",
    "Design to Falsify",
    "Context and Validity",
    "Use Algorithms",
    "Algorithms Help",
    "Example Exposure Decision",
    "Critical Point",
    "ATHENA Searches your Haystack",
    "ATHENA Algorithm",
    "The Choice",
    "Appeal to Data",
    "ATHENA",
    "ATHENA Video Demo",
    "One More Level",
    "The Paradox of Trust",
    "Show it to me in Memes",
    "Questions"
]
# -------------------------------------------------------------
# Session state for page navigation
# -------------------------------------------------------------
if "current_page" not in st.session_state:
    st.session_state.current_page = PAGES[0]

if "page_radio" not in st.session_state:
    st.session_state.page_radio = st.session_state.current_page

def go_to_page(page_name: str) -> None:
    st.session_state.current_page = page_name
    st.session_state.page_radio = page_name

def go_next() -> None:
    idx = PAGES.index(st.session_state.current_page)
    if idx < len(PAGES) - 1:
        next_page = PAGES[idx + 1]
        st.session_state.current_page = next_page
        st.session_state.page_radio = next_page

def go_prev() -> None:
    idx = PAGES.index(st.session_state.current_page)
    if idx > 0:
        prev_page = PAGES[idx - 1]
        st.session_state.current_page = prev_page
        st.session_state.page_radio = prev_page

# -------------------------------------------------------------
# Custom CSS
# -------------------------------------------------------------
st.markdown("""
<style>
    .block-container {
        padding-top: 2rem;
        padding-bottom: 1.2rem;
    }

    /* ---- Home ---- */
    .hero-wrap {
        min-height: 70vh;
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 2rem 1rem;
        background: transparent;
        border: none;
        border-radius: 0;
        box-shadow: none;
    }

    .hero-inner {
        max-width: 980px;
        text-align: center;
    }

    .hero-kicker {
        display: inline-block;
        padding: 0.45rem 0.9rem;
        border-radius: 999px;
        background: rgba(255,255,255,0.06);
        border: 1px solid rgba(255,255,255,0.08);
        font-size: 0.95rem;
        margin-bottom: 1.25rem;
    }

    .hero-title {
        font-size: 3.8rem;
        font-weight: 800;
        line-height: 1.08;
        margin-bottom: 1rem;
        letter-spacing: -0.02em;
    }

    .hero-subtitle {
        font-size: 1.3rem;
        opacity: 0.92;
        max-width: 820px;
        margin: 0 auto 1.8rem auto;
        line-height: 1.55;
    }

    .hero-authors {
        font-size: 1.08rem;
        margin-top: 1rem;
        opacity: 0.98;
    }

    .hero-authors a {
        color: #FF4B4B !important;
        text-decoration: none;
        font-weight: 700;
        margin: 0 0.2rem;
    }

    .hero-authors a:hover {
        text-decoration: underline;
    }

    .hero-footer {
        margin-top: 2rem;
        font-size: 0.96rem;
        opacity: 0.78;
    }

    /* ---- Slide titles ---- */
    .slide-title {
        font-size: 2.4rem;
        font-weight: 700;
        margin-top: 0.15rem;
        margin-bottom: 0.1rem;
    }

    .slide-subtitle {
        font-size: 1.05rem;
        opacity: 0.75;
        margin-bottom: 0.5rem;
    }

    /* ---- Embedded progress under title ---- */
    .slide-progress-track {
        width: 100%;
        height: 1.5px;
        background: rgba(255,255,255,0.10);
        border-radius: 999px;
        overflow: hidden;
        margin-bottom: 1.2rem;
    }

    .slide-progress-fill {
        height: 100%;
        border-radius: 999px;
        background: #FF4B4B;
    }

    /* ---- Bottom nav buttons row spacing ---- */
    .nav-spacer {
        height: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# Helpers
# -------------------------------------------------------------
def section_title(title: str, subtitle: str = "") -> None:
    idx = PAGES.index(st.session_state.current_page) + 1
    total = len(PAGES)
    pct = (idx / total) * 100

    st.markdown(
        f"""
        <div class="slide-title">{title}</div>
        <div class="slide-subtitle">{subtitle}</div>
        <div class="slide-progress-track">
            <div class="slide-progress-fill" style="width:{pct}%"></div>
        </div>
        """,
        unsafe_allow_html=True
    )

def stat_card(col, label: str, value: str, help_text: str = "") -> None:
    col.metric(label, value)
    if help_text:
        col.caption(help_text)


def home_hero(title: str, subtitle: str, authors_html: str) -> None:
    st.markdown(
        f"""
        <div class="hero-wrap">
            <div class="hero-inner">
                <div class="hero-title">{title}</div>
                <div class="hero-subtitle">{subtitle}</div>
                <div class="hero-authors">{authors_html}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

def render_bottom_nav() -> None:
    st.markdown('<div class="nav-spacer"></div>', unsafe_allow_html=True)
    idx = PAGES.index(st.session_state.current_page)

    c1, c2, c3 = st.columns([1, 3, 1])

    with c1:
        if idx > 0:
            st.button("← Previous", on_click=go_prev, use_container_width=True, key=f"prev_{idx}")
        else:
            st.empty()

    with c2:
        st.markdown(
            f"<div style='text-align:center; opacity:0.75'>{idx + 1} / {len(PAGES)}</div>",
            unsafe_allow_html=True
        )

    with c3:
        if idx < len(PAGES) - 1:
            st.button("Next →", on_click=go_next, use_container_width=True, key=f"next_{idx}")
        else:
            st.empty()


def generate_qr(url):
    qr = qrcode.make(url)
    buf = BytesIO()
    qr.save(buf, format="PNG")
    return buf


def centered_image(path, width=300):
    c1, c2, c3 = st.columns([1, 1, 1])
    with c2:
        st.image(path, width=width)

# -------------------------------------------------------------
# Sidebar navigation
# -------------------------------------------------------------
def _sidebar_page_change():
    st.session_state.current_page = st.session_state.page_radio


st.sidebar.title("Navigation")
st.sidebar.radio(
    "Go to section",
    PAGES,
    key="page_radio",
    on_change=_sidebar_page_change
)

page = st.session_state.current_page


# -------------------------------------------------------------
# Page: Home
# -------------------------------------------------------------
if page == "Home":
    authors_html = """
    Presented by
    <a href="https://www.linkedin.com/in/dr-spencer-pizzani-cih-232a7518/" target="_blank">Dr. Spencer Pizzani</a>
    &
    <a href="https://www.linkedin.com/in/caleb-ginorio-gonzález-58b243b4/" target="_blank">Caleb Ginorio González</a>
    """

    home_hero(
        title="Key Techniques for Communicating IH Data Decisions",
        subtitle="Turning exposure data into clear, defensible industrial hygiene decisions",
        authors_html=authors_html
    )

    render_bottom_nav()


# -------------------------------------------------------------
# Page: Intro
# -------------------------------------------------------------
elif page == "Intro":
    section_title("Intro")

    # -------------------------------------------------------------
    # Main Header
    # -------------------------------------------------------------
    st.markdown(
        """
        <div style="
            padding: 1.2rem;
            border-left: 4px solid #FF4B4B;
            background: rgba(255,255,255,0.03);
            margin-bottom: 3rem;
            font-size:3.05rem;
            font-weight:700;
        ">
            Data Tells Stories
        </div>
        """,
        unsafe_allow_html=True
    )


# =============================================================
# 1. FORMULATE A GOOD HYPOTHESIS
# =============================================================
    st.markdown(
    """
    <div style="text-align:center;">
        <h2>1. Formulate a Good Hypothesis</h2>
    </div>
    """,
    unsafe_allow_html=True
    )

    left, center, right = st.columns([1,2,1])

    with center:
        st.image("hypothesis.png", width=800)

    st.markdown("<br><br>", unsafe_allow_html=True)

    # =============================================================
    # 2. USE ALGORITHMS
    # =============================================================
    st.markdown(
        """
        <div style="text-align:center;">
            <h2>2. Use Algorithms</h2>
        </div>
        """,
        unsafe_allow_html=True
    )

    left, center, right = st.columns([1,2,1])

    with center:
        st.image("algorithm.png", width=800)

    st.markdown("<br><br>", unsafe_allow_html=True)

    # =============================================================
    # 3. SIMPLIFY STATISTICS
    # =============================================================
    st.markdown(
        """
        <div style="text-align:center;">
            <h2>3. Simplify Statistics</h2>
        </div>
        """,
        unsafe_allow_html=True
    )

    left, center, right = st.columns([1,2,1])

    with center:
        st.image("statistics.png", width=800)

    st.markdown("<br><br>", unsafe_allow_html=True)

    render_bottom_nav()


# -------------------------------------------------------------
# Page: Context
# -------------------------------------------------------------
elif page == "Context":

    section_title("Context")

    st.markdown("<br><br>", unsafe_allow_html=True)

    # -------------------------------------------------------------
    # Centered Image
    # -------------------------------------------------------------

    
    centered_image("jahn.jpg", width=650)

    st.markdown("<br>", unsafe_allow_html=True)

    # -------------------------------------------------------------
    # Quote
    # -------------------------------------------------------------
    st.markdown(
        """
        <div style="
            text-align:center;
            font-size:2rem;
            font-weight:700;
            line-height:1.5;
            margin-top:1rem;
        ">
            “Industrial hygiene is the practice of putting exposures into context.”
        </div>
        """,
        unsafe_allow_html=True
    )

    render_bottom_nav()

# -------------------------------------------------------------
# Page: Design to Falsify
# -------------------------------------------------------------
elif page == "Design to Falsify":

    section_title("Design to Falsify")

    st.markdown(
        """
        <div style="
            text-align:left;
            font-size:1.5rem;
            font-weight:700;
            margin-top:2rem;
            margin-bottom:3rem;
            line-height:1.5;
        ">
            Remember there is always a fundamentally unknowable difference between the measured and true exposure.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div style="
            padding:1.2rem;
            border-left:4px solid #FF4B4B;
            background: rgba(255,255,255,0.03);
            margin-bottom:2rem;
            font-size:1.25rem;
        ">
            “We believe we are under the OEL for nitric acid.”
        </div>
        """,
        unsafe_allow_html=True
    )

    # -------------------------------------------------------------
    # Reformulated Research Question
    # -------------------------------------------------------------
    st.markdown("### RQ1")

    st.markdown(
        """
        <div style="
            font-size:1.65rem;
            line-height:1.55;
            margin-bottom:3rem;
        ">
        We are at least <strong>70% confident</strong> that the true exposure to nitric acid
        is less than the OEL <strong>95% of the time</strong>.
        </div>
        """,
        unsafe_allow_html=True
    )

    # -------------------------------------------------------------
    # H0 Section
    # -------------------------------------------------------------
    st.markdown(
        """
        <div style="text-align:center; margin-top:1rem;">
            <h2>H₀</h2>
        </div>
        """,
        unsafe_allow_html=True
    )

    centered_image("thumbsup.png", width=500)

    st.markdown(
        """
        <div style="
            text-align:center;
            font-size:1.25rem;
            line-height:1.5;
            margin-top:1rem;
            margin-bottom:3rem;
        ">
            <strong>RQ1 is true.</strong><br>
            We are sufficiently confident that exposure remains below the OEL.
        </div>
        """,
        unsafe_allow_html=True
    )

    # -------------------------------------------------------------
    # Ha Section
    # -------------------------------------------------------------
    st.markdown(
        """
        <div style="text-align:center; margin-top:1rem;">
            <h2>Hₐ</h2>
        </div>
        """,
        unsafe_allow_html=True
    )

    centered_image("warning.png", width=500)

    st.markdown(
        """
        <div style="
            text-align:center;
            font-size:1.25rem;
            line-height:1.5;
            margin-top:1rem;
            margin-bottom:2rem;
        ">
            <strong>RQ1 is false.</strong><br>
            We are not sufficiently confident.
        </div>
        """,
        unsafe_allow_html=True
    )

    render_bottom_nav()



# -------------------------------------------------------------
# Page: Context and Validity
# -------------------------------------------------------------
elif page == "Context and Validity":

    section_title("Context and Validity")

    st.markdown("<br>", unsafe_allow_html=True)

    # -------------------------------------------------------------
    # Two Column Layout
    # -------------------------------------------------------------
    col1, col2 = st.columns(2)

    # =============================================================
    # CONTEXT
    # =============================================================
    with col1:

        st.markdown(
            """
            <div style="
                border-left:4px solid #FF4B4B;
                padding-left:1.2rem;
                margin-bottom:1rem;
            ">
                <h2>Context</h2>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            """
            ### Ensuring data is meaningful and explaining that meaning.
            """
        )

    # =============================================================
    # VALIDITY
    # =============================================================
    with col2:

        st.markdown(
            """
            <div style="
                border-left:4px solid #FF4B4B;
                padding-left:1.2rem;
                margin-bottom:1rem;
            ">
                <h2>Validity</h2>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            """
            ### I can trust this data for that context.
            """
        )

    st.markdown("<br><br>", unsafe_allow_html=True)

    left, center, right = st.columns([1,2,1]) 
    with center: st.image("haystack.png", width=650) 
    st.markdown("<br>", unsafe_allow_html=True)

    

    # -------------------------------------------------------------
    # Haystack Analogy
    # -------------------------------------------------------------
    st.markdown("## Haystack Analogy")

    st.markdown(
        """
        **Context**: I know why this haystack is here.

        **Validity:** It contains only hay, the right kind, it’s baled correctly, and ready for use.
        """
    )

    st.markdown("<br><br>", unsafe_allow_html=True)

    # -------------------------------------------------------------
    # Practical Example
    # -------------------------------------------------------------
    st.markdown("## Practical Example")

    st.markdown(
        """
        **Context:** The data represents worst-case exposure given a specific process configuration.

        **Validity:** Proper calibration, functional testing, good recordkeeping, and no missing, negative, or inappropriate zero data.
        """
    )

    render_bottom_nav()


# -------------------------------------------------------------
# Page: Use Algorithms
# -------------------------------------------------------------
elif page == "Use Algorithms":

    section_title("Use Algorithms")

    st.markdown("<br>", unsafe_allow_html=True)

    # -------------------------------------------------------------
    # Main Statement
    # -------------------------------------------------------------
    st.markdown(
        """
        ## You already know algorithms.
        """
    )

    st.markdown(
        """
        An algorithm is just a structured decision process.

        In IH, algorithms help us move from individual judgment to a repeatable, explainable decision pathway.
        """
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # -------------------------------------------------------------
    # Decision Flow Image
    # -------------------------------------------------------------

    centered_image("algorithm2.png", width=500)

    st.markdown("<br>", unsafe_allow_html=True)

    st.divider()


    centered_image("algorithm3.png", width=500)

    st.markdown("<br>", unsafe_allow_html=True)

    # -------------------------------------------------------------
    # Takeaway
    # -------------------------------------------------------------
    st.markdown(
        """
        ### Why algorithms help

        - They make assumptions visible.
        - They reduce inconsistency.
        - They improve defensibility.
        - They make complex decisions easier to explain.
        """
    )

    render_bottom_nav()

# -------------------------------------------------------------
# Page: Example Exposure Decision
# -------------------------------------------------------------
elif page == "Example Exposure Decision":

    section_title("Example Exposure Decision")

    st.markdown("<br>", unsafe_allow_html=True)

    # -------------------------------------------------------------
    # Scenario
    # -------------------------------------------------------------
    st.markdown(
        """
        ## Worker exposure to inhalable manganese

        **OEL = 0.1 mg/m³**
        """
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # -------------------------------------------------------------
    # Exposure Values
    # -------------------------------------------------------------
    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric("Sample 1", "0.05 mg/m³")

    with c2:
        st.metric("Sample 2", "0.04 mg/m³")

    with c3:
        st.metric("Sample 3", "0.02 mg/m³")

    with c4:
        st.metric("Sample 4", "0.04 mg/m³")

    st.markdown("<br><br>", unsafe_allow_html=True)

    # -------------------------------------------------------------
    # Reveal Session State
    # -------------------------------------------------------------
    if "example_step" not in st.session_state:
        st.session_state.example_step = 0

    def reveal_example():
        st.session_state.example_step = 1

    def reset_example():
        st.session_state.example_step = 0

    # -------------------------------------------------------------
    # Controls
    # -------------------------------------------------------------
    c1, c2, c3 = st.columns([1,1,1])

    with c1:
        st.button(
            "Reset",
            on_click=reset_example,
            use_container_width=True
        )

    with c3:
        st.button(
            "Reveal Analysis",
            on_click=reveal_example,
            use_container_width=True
        )

    st.markdown("<br><br>", unsafe_allow_html=True)

    # -------------------------------------------------------------
    # Revealed Content
    # -------------------------------------------------------------
    if st.session_state.example_step >= 1:

        # centered image
        left, center, right = st.columns([1,2,1])

        with center:
            st.image("BDA.png", width=650)

        st.markdown("<br><br>", unsafe_allow_html=True)

        # -------------------------------------------------------------
        # Main Decision Statement
        # -------------------------------------------------------------
        st.markdown(
            """
            <div style="
                text-align:center;
                font-size:2rem;
                font-weight:700;
                line-height:1.6;
                margin-top:2rem;
                margin-bottom:2rem;
            ">
                We are <span style="color:#FF4B4B;">62.2% confident</span><br>
                that the TRUE exposure is below the OEL<br>
                95% of the time.
            </div>
            """,
            unsafe_allow_html=True
        )

    render_bottom_nav()

# -------------------------------------------------------------
# Page: Algorithms Help
# -------------------------------------------------------------
elif page == "Algorithms Help":

    section_title("Algorithms Help")

    st.markdown("<br>", unsafe_allow_html=True)

    # -------------------------------------------------------------
    # Main Statement
    # -------------------------------------------------------------
    st.markdown(
        """
        ## Algorithms help structure IH decisions.
        """
    )

    st.markdown(
        """
        They do not replace professional judgment.

        They help make decisions:
        - repeatable
        - explainable
        - transparent
        """
    )

    st.markdown("<br><br>", unsafe_allow_html=True)

    # -------------------------------------------------------------
    # Step 1
    # -------------------------------------------------------------
    st.markdown(
        """
        <div style="
            border-left:4px solid #FF4B4B;
            padding-left:1.2rem;
            margin-bottom:2rem;
        ">
            <h2>Step 1 — Determine if SEG</h2>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        Dataset does not reject the lognormal hypothesis.

        Example:
        - Filliben’s Test
        - IHSTAT / AIHA methods
        """
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # -------------------------------------------------------------
    # Step 2
    # -------------------------------------------------------------
    st.markdown(
        """
        <div style="
            border-left:4px solid #FF4B4B;
            padding-left:1.2rem;
            margin-bottom:2rem;
        ">
            <h2>Step 2 — Exposure Decision Analysis</h2>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        Use statistical confidence to determine whether exposure is acceptable.

        The goal is not just:
        - “What was measured?”

        The goal is:
        - “How confident are we in the decision?”
        """
    )

    st.markdown("<br><br>", unsafe_allow_html=True)
# -------------------------------------------------------------
# QR Code Section
# -------------------------------------------------------------
    tool_url = "https://lavoue.shinyapps.io/tool1/_w_a80467c2b0e34ab18e200928e910d3a1/_w_a66b3708481d47d6a2f1c93801aaecb7/?lang=en&mode=extended&color=light"

    tool_qr = generate_qr(tool_url)

    st.markdown("<br><br>", unsafe_allow_html=True)

    st.markdown(
        """
        ## Expostats
        """
    )

    centered_image(tool_qr, width=350)

    render_bottom_nav()


# -------------------------------------------------------------
# Page: Critical Point
# -------------------------------------------------------------

elif page == "Critical Point":
    section_title(
        "Critical Point"
    )

    # vertical spacing
    st.markdown("<br><br>", unsafe_allow_html=True)

    # centered large diagram
    c1, c2, c3 = st.columns([1,6,1])
    with c2:
        st.image("criticalpoint.png", width=1000)

    st.markdown("<br>", unsafe_allow_html=True)


# -------------------------------------------------------------
# Key Takeaways / Content
# -------------------------------------------------------------
    st.markdown("---")

    left_pad, col1, col2, right_pad = st.columns([1, 3, 3, 1])

    with col1:
        st.markdown("### Concept")

        st.markdown(
            """
            The **ATHENA Critical Point** describes the transition from:

            - data-limited analysis  
            → to  
            - practitioner-limited analysis
            """
        )

        st.markdown(
            """
            Systems are constrained by:
            - **Data availability**, or  
            - **Practitioner capability**  
            (capacity + competency)
            """
        )

    with col2:
        st.markdown("### Dynamics")

        st.markdown(
            """
            - **RTDS data size** increases rapidly over time  

            - **Practitioner competency** increases gradually  

            - Step changes occur with:
                - new tools  
                - new methods
            """
        )

    st.markdown("---")

    st.markdown(
        """
        <div style="text-align:center; font-size:1.1rem; opacity:0.85;">
        The constraint shifts from <b>data</b> to <b>analytical capability</b>.
        </div>
        """,
        unsafe_allow_html=True
    )

    render_bottom_nav()

# -------------------------------------------------------------
# Page: The Choice
# -------------------------------------------------------------
elif page == "The Choice":

    section_title("The Choice")

    st.markdown("<br><br>", unsafe_allow_html=True)

    # -------------------------------------------------------------
    # Main Image
    # -------------------------------------------------------------
    left, center, right = st.columns([1,3,1])

    with center:
        st.image("choice.png", width=950)

    st.markdown("<br><br>", unsafe_allow_html=True)

    # -------------------------------------------------------------
    # Main Statement
    # -------------------------------------------------------------
    st.markdown(
        """
        <div style="
            text-align:center;
            font-size:2rem;
            font-weight:700;
            line-height:1.5;
            margin-top:1rem;
            margin-bottom:2rem;
        ">
            Exposure assessment is ultimately a decision problem.
        </div>
        """,
        unsafe_allow_html=True
    )

    render_bottom_nav()

# -------------------------------------------------------------
# Page: Appeal to Data
# -------------------------------------------------------------
elif page == "Appeal to Data":

    section_title("Appeal to Data")

    st.markdown("<br>", unsafe_allow_html=True)

    # -------------------------------------------------------------
    # Scenario
    # -------------------------------------------------------------
    st.markdown(
        """
        ## Worker exposure to citrus peel oil

        **OEL = 3 ppm**
        """
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # -------------------------------------------------------------
    # Exposure Results
    # -------------------------------------------------------------
    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric("Sample 1", "< 1.0 ppm")

    with c2:
        st.metric("Sample 2", "< 1.0 ppm")

    with c3:
        st.metric("Sample 3", "< 1.0 ppm")

    with c4:
        st.metric("Sample 4", "< 1.0 ppm")

    st.markdown("<br><br>", unsafe_allow_html=True)

    # -------------------------------------------------------------
    # First Image
    # -------------------------------------------------------------
    left, center, right = st.columns([1,2,1])

    with center:
        st.image("citrus1.png", width=650)

    st.markdown("<br><br>", unsafe_allow_html=True)

    # -------------------------------------------------------------
    # Main Statement
    # -------------------------------------------------------------
    st.markdown(
        """
        <div style="
            text-align:center;
            font-size:2rem;
            font-weight:700;
            line-height:1.6;
            margin-top:1rem;
            margin-bottom:2rem;
        ">
            We’re confident that this exposure is acceptable,<br>
            and we’d be happy to show you.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<br><br>", unsafe_allow_html=True)

    # -------------------------------------------------------------
    # Reveal Session State
    # -------------------------------------------------------------
    if "appeal_step" not in st.session_state:
        st.session_state.appeal_step = 0

    def reveal_appeal():
        st.session_state.appeal_step = 1

    def reset_appeal():
        st.session_state.appeal_step = 0

    # -------------------------------------------------------------
    # Controls
    # -------------------------------------------------------------
    c1, c2, c3 = st.columns([1,1,1])

    with c1:
        st.button(
            "Reset",
            on_click=reset_appeal,
            use_container_width=True
        )

    with c3:
        st.button(
            "Reveal Data",
            on_click=reveal_appeal,
            use_container_width=True
        )

    st.markdown("<br><br>", unsafe_allow_html=True)

    # -------------------------------------------------------------
    # Revealed Image
    # -------------------------------------------------------------
    if st.session_state.appeal_step >= 1:

        left, center, right = st.columns([1,2,1])

        with center:
            st.image("citrus2.png", width=650)

    render_bottom_nav()

# -------------------------------------------------------------
# Page: The Paradox of Trust
# -------------------------------------------------------------
elif page == "The Paradox of Trust":

    section_title("The Paradox of Trust")

    st.markdown("<br><br>", unsafe_allow_html=True)

    if "trust_step" not in st.session_state:
        st.session_state.trust_step = 1

    def next_trust_step():
        if st.session_state.trust_step < 3:
            st.session_state.trust_step += 1

    def reset_trust_step():
        st.session_state.trust_step = 1

    # -------------------------------------------------------------
    # Reveal controls
    # -------------------------------------------------------------
    c1, c2, c3 = st.columns([1, 1, 1])

    with c1:
        st.button("Reset", on_click=reset_trust_step, use_container_width=True)

    with c3:
        st.button("Reveal Next", on_click=next_trust_step, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # -------------------------------------------------------------
    # Step 1
    # -------------------------------------------------------------
    if st.session_state.trust_step >= 1:
        st.markdown(
            """
            <div style="
                text-align:center;
                font-size:2.2rem;
                font-weight:700;
                padding:1rem;
                border-radius:12px;
                background: rgba(255,255,255,0.03);
                border:1px solid rgba(255,255,255,0.08);
            ">
                👁️ Provide Transparency
            </div>
            """,
            unsafe_allow_html=True
        )

    # -------------------------------------------------------------
    # Step 2
    # -------------------------------------------------------------
    if st.session_state.trust_step >= 2:
        st.markdown(
            """
            <div style="text-align:center; font-size:2rem; margin:1rem;">↓</div>

            <div style="
                text-align:center;
                font-size:2.2rem;
                font-weight:700;
                padding:1rem;
                border-radius:12px;
                background: rgba(255,255,255,0.03);
                border:1px solid rgba(255,255,255,0.08);
            ">
                🤝 Earn Trust
            </div>
            """,
            unsafe_allow_html=True
        )

    # -------------------------------------------------------------
    # Step 3
    # -------------------------------------------------------------
    if st.session_state.trust_step >= 3:
        st.markdown(
            """
            <div style="text-align:center; font-size:2rem; margin:1rem;">↓</div>

            <div style="
                text-align:center;
                font-size:2.2rem;
                font-weight:700;
                padding:1rem;
                border-radius:12px;
                background: rgba(255,255,255,0.03);
                border:1px solid rgba(255,255,255,0.08);
            ">
                💬 Simplify Communications
            </div>
            """,
            unsafe_allow_html=True
        )

    render_bottom_nav()

# -------------------------------------------------------------
# Page: One More Level
# -------------------------------------------------------------
elif page == "One More Level":

    section_title("One More Level")

    st.markdown("<br><br>", unsafe_allow_html=True)

    # -------------------------------------------------------------
    # Session State
    # -------------------------------------------------------------
    if "simple_step" not in st.session_state:
        st.session_state.simple_step = 1

    def next_simple_step():
        if st.session_state.simple_step < 3:
            st.session_state.simple_step += 1

    def reset_simple_step():
        st.session_state.simple_step = 1

    # -------------------------------------------------------------
    # Controls
    # -------------------------------------------------------------
    c1, c2, c3 = st.columns([1,1,1])

    with c1:
        st.button("Reset", on_click=reset_simple_step, use_container_width=True)

    with c3:
        st.button("Reveal Next", on_click=next_simple_step, use_container_width=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    # -------------------------------------------------------------
    # Step 1
    # -------------------------------------------------------------
    if st.session_state.simple_step >= 1:

        st.markdown(
            """
            <div style="
                text-align:center;
                font-size:2rem;
                font-weight:700;
                margin-bottom:2rem;
            ">
            📊 “The red bar is below the black dashed line.”
            </div>
            """,
            unsafe_allow_html=True
        )

        centered_image("redbar.png", width=500) 
        st.markdown("<br><br>", unsafe_allow_html=True)
    # -------------------------------------------------------------
    # Step 2
    # -------------------------------------------------------------
    if st.session_state.simple_step >= 2:

        st.markdown(
            """
            <div style="
                text-align:center;
                font-size:2rem;
                margin-bottom:2rem;
            ">
                ↓
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            """
            <div style="
                text-align:center;
                font-size:2rem;
                font-weight:700;
                margin-bottom:2rem;
            ">
                👍 “The thumbs up means we’re good with this data.”
            </div>
            """,
            unsafe_allow_html=True
        )

      
        centered_image("thumbs.png", width=500) 
        st.markdown("<br><br>", unsafe_allow_html=True)

    render_bottom_nav()

# -------------------------------------------------------------
# Page: ATHENA
# -------------------------------------------------------------
elif page == "ATHENA":
    section_title(
        "ATHENA"
    )

# -------------------------------------------------------------
# ATHENA Links (Launch + Publication + QR Codes)
# -------------------------------------------------------------
    st.markdown("---")

    # URLs
    athena_url = "https://athena-heuristic.streamlit.app/"
    paper_url = "https://docs.google.com/document/d/1GOCPovtH6T6GZzLZpa_twE6ZRIVIG69z/edit?usp=sharing&ouid=116094106714963469191&rtpof=true&sd=true"

    # Generate QR codes
    athena_qr = generate_qr(athena_url)
    paper_qr = generate_qr(paper_url)

    # Layout
    c1, c2 = st.columns(2)

    # -------------------------------------------------------------
    # ATHENA APP
    # -------------------------------------------------------------
    with c1:
        st.markdown(
            f"""
            <div style="
                padding:1.2rem;
                border-radius:12px;
                background: rgba(255,255,255,0.03);
                border: 1px solid rgba(255,255,255,0.08);
                text-align:center;
            ">
                <div style="font-size:0.9rem; opacity:0.7;">Try it yourself</div>
                <div style="font-size:1.2rem; font-weight:700; margin-top:0.3rem;">
                    <a href="{athena_url}" target="_blank" style="color:#FF4B4B; text-decoration:none;">
                        Launch ATHENA
                    </a>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown("<br>", unsafe_allow_html=True)

        # Centered QR
        qr_col1, qr_col2, qr_col3 = st.columns([1, 1.2, 1])
        with qr_col2:
            st.image(athena_qr, width=150)
            st.markdown(
                "<div style='text-align:center; opacity:0.75;'>Scan to open ATHENA</div>",
                unsafe_allow_html=True
            )

    # -------------------------------------------------------------
    # PUBLICATION
    # -------------------------------------------------------------
    with c2:
        st.markdown(
            f"""
            <div style="
                padding:1.2rem;
                border-radius:12px;
                background: rgba(255,255,255,0.03);
                border: 1px solid rgba(255,255,255,0.08);
                text-align:center;
            ">
                <div style="font-size:0.9rem; opacity:0.7;">Read the article</div>
                <div style="font-size:1.2rem; font-weight:700; margin-top:0.3rem;">
                    <a href="{paper_url}" target="_blank" style="color:#FF4B4B; text-decoration:none;">
                        View Publication
                    </a>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown("<br>", unsafe_allow_html=True)

        # Centered QR
        qr_col1, qr_col2, qr_col3 = st.columns([1, 1.2, 1])
        with qr_col2:
            st.image(paper_qr, width=150)
            st.markdown(
                "<div style='text-align:center; opacity:0.75;'>Scan to view paper</div>",
                unsafe_allow_html=True
            )


    render_bottom_nav()


# -------------------------------------------------------------
# Page: ATHENA Searches your Haystack
# -------------------------------------------------------------
elif page == "ATHENA Searches your Haystack":

    section_title("ATHENA Searches your Haystack")

    st.markdown("<br>", unsafe_allow_html=True)

    # -------------------------------------------------------------
    # Main Image
    # -------------------------------------------------------------
    left, center, right = st.columns([1,3,1])

    with center:
        st.image("athena.png", width=900)

    st.markdown("<br><br>", unsafe_allow_html=True)

    # -------------------------------------------------------------
    # What You Bring
    # -------------------------------------------------------------
    st.markdown("## You bring:")

    st.markdown(
        """
        - Context
        - Time-series data log
        - OEL(s)
        - Decisions about cleaning data
        """
    )

    st.markdown("<br><br>", unsafe_allow_html=True)

    # -------------------------------------------------------------
    # Bottom Statement
    # -------------------------------------------------------------
    st.markdown(
        """
        ### ATHENA helps identify meaningful exposure patterns inside large datasets.
        """
    )

    render_bottom_nav()

# -------------------------------------------------------------
# Page: ATHENA Algorithm
# -------------------------------------------------------------
elif page == "ATHENA Algorithm":
    section_title(
        "ATHENA Algorithm"
    )

    left_pad, col1, col2, right_pad = st.columns([0.6, 3.2, 3.2, 0.6])

    # -------------------------------------------------------------
    # LEFT COLUMN — Conjecture / framing
    # -------------------------------------------------------------
    with col1:
        st.markdown("### Conjecture")

        st.markdown(
            """
            The **ATHENA conjecture** states that there exists a set of systematic data processing and calculation rules that allows for a binary exposure decision:

            - **OK**
            - **NOT OK**

            Using **time-series exposure data of arbitrary size**.
            """
        )

        st.markdown("### Heuristic + Algorithm")

        st.markdown(
            """
            These systematic procedures with deterministic results are collectively an **algorithm**.

            The algorithm exists within a **heuristic**, intended to arrive at a context-relevant result with:

            - minimal prerequisite knowledge
            - limited analytical interpolation by the user
            """
        )

        st.markdown(
            """
            The heuristic algorithm is **parametric**, operating within the parameters of:

            - time-series data
            - OELs as limit values
            - statistical confidence
            """
        )

    # -------------------------------------------------------------
    # RIGHT COLUMN — Condensed algorithm
    # -------------------------------------------------------------
    with col2:
        st.markdown("### ATHENA (Condensed)")

        st.markdown(
            """
            1. Identify OEL  
            2. Obtain time-series data  
            3. Clean data and ensure validity  
            4. Calculate moving averages  
            5. Calculate confidence intervals  
            6. Evaluate all moving averages  

            **Decision rule**

            - If all moving TWAs are **less than the 95% UCL of the limit value**  
              → 👍

            - Otherwise  
              → 👎
            """
        )

        st.markdown("---")

        st.markdown(
            """
            <div style="
                padding: 1rem;
                border-left: 4px solid #FF4B4B;
                background: rgba(255,255,255,0.03);
                line-height: 1.5;
            ">
            The goal is a context-relevant exposure decision using transparent, systematic rules.
            </div>
            """,
            unsafe_allow_html=True
        )

    render_bottom_nav()


# -------------------------------------------------------------
# Page: ATHENA Video Demo
# -------------------------------------------------------------
elif page == "ATHENA Video Demo":

    section_title("ATHENA Video Demo")

    st.markdown("<br>", unsafe_allow_html=True)

    # -------------------------------------------------------------
    # Intro Statement
    # -------------------------------------------------------------
    st.markdown(
        """
        <div style="
            text-align:center;
            font-size:2rem;
            font-weight:700;
            line-height:1.6;
            margin-bottom:2rem;
        ">
            Example ATHENA Exposure Decision Workflow
        </div>
        """,
        unsafe_allow_html=True
    )

    # -------------------------------------------------------------
    # Video
    # -------------------------------------------------------------
    left, center, right = st.columns([1,4,1])

    with center:

        video_file = open("videodemo.mp4", "rb")
        video_bytes = video_file.read()

        st.video(video_bytes)

    st.markdown("<br><br>", unsafe_allow_html=True)


    render_bottom_nav()

# -------------------------------------------------------------
# Page: Show it to me in Memes
# -------------------------------------------------------------
elif page == "Show it to me in Memes":

    section_title("Show it to me in Memes")

    st.markdown("<br>", unsafe_allow_html=True)

    # -------------------------------------------------------------
    # Meme List
    # -------------------------------------------------------------
    memes = [
        {
            "image": "meme1.png",
            "caption": "Are you sure their exposures are acceptable… even when you’re not looking?"
        },
        {
            "image": "meme2.png",
            "caption": "My work isn’t the same every day… are you sure I’m protected?"
        },
        {
            "image": "meme3.png",
            "caption": "Please explain to the jury your process to determine you had enough exposure data."
        },
        {
            "image": "meme4.png",
            "caption": "I’m glad we’re under the OEL — but how close is it, really?"
        },
        {
            "image": "meme5.png",
            "caption": "Another sample on the exact same work?"
        }
    ]

    # -------------------------------------------------------------
    # Session State
    # -------------------------------------------------------------
    if "meme_index" not in st.session_state:
        st.session_state.meme_index = 0

    def next_meme():
        if st.session_state.meme_index < len(memes) - 1:
            st.session_state.meme_index += 1

    def prev_meme():
        if st.session_state.meme_index > 0:
            st.session_state.meme_index -= 1

    meme = memes[st.session_state.meme_index]

    # -------------------------------------------------------------
    # Meme Display
    # -------------------------------------------------------------
    left, center, right = st.columns([1,3,1])

    with center:
        st.image(meme["image"], width=850)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(
        f"""
        <div style="
            text-align:center;
            font-size:1.3rem;
            line-height:1.6;
            opacity:0.9;
        ">
            {meme["caption"]}
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<br><br>", unsafe_allow_html=True)

    # -------------------------------------------------------------
    # Navigation
    # -------------------------------------------------------------
    c1, c2, c3 = st.columns([1,2,1])

    with c1:
        st.button("← Previous Meme", on_click=prev_meme, use_container_width=True)

    with c3:
        st.button("Next Meme →", on_click=next_meme, use_container_width=True)

    render_bottom_nav()


# -------------------------------------------------------------
# Page: Questions
# -------------------------------------------------------------
elif page == "Questions":
    st.markdown(
        """
        <div style="
            height:70vh;
            display:flex;
            align-items:center;
            justify-content:center;
            font-size:4.5rem;
            font-weight:700;
            text-align:center;
            letter-spacing:-0.02em;
        ">
            Questions<span style="color:#FF4B4B">?</span>
        </div>
        """,
        unsafe_allow_html=True
    )

    render_bottom_nav()
