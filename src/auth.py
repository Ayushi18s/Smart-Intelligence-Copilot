import streamlit as st

# =========================
# INIT STATE
# =========================
def init_auth():

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if "user" not in st.session_state:
        st.session_state.user = None

    if "users" not in st.session_state:
        st.session_state.users = {
            "admin": "admin123"
        }


# =========================
# AUTH UI
# =========================
def auth_ui():

    init_auth()

    # Already logged in
    if st.session_state.logged_in:
        return True

    # Layout
    left, right = st.columns([5, 3], gap="large")

    # =========================
    # LEFT PANEL
    # =========================
    with left:

        st.markdown("""
        # 📊 Smart Business Intelligence Copilot
        ### AI-powered analytics + decision intelligence system
        """)

        st.markdown("---")

        st.markdown("""
        ### 🚀 What you can do

        ✔ Analyze Sales & Profit  
        ✔ Detect weak regions & products  
        ✔ AI-powered insights  
        ✔ Forecast future sales  
        ✔ Generate CEO-level reports  
        ✔ Ask questions in natural language  
        """)

        st.markdown("---")

        st.info(
            "💡 Turn your raw data into business decisions in seconds"
        )

    # =========================
    # RIGHT PANEL
    # =========================
    with right:

        st.markdown(
            """
            <div class="auth-card">
            """,
            unsafe_allow_html=True
        )

        st.markdown("## 🔐 Login")

        tab1, tab2 = st.tabs(
            ["Login", "Create Account"]
        )

        # =====================
        # LOGIN TAB
        # =====================
        with tab1:

            username = st.text_input(
                "Username",
                key="login_user"
            )

            password = st.text_input(
                "Password",
                type="password",
                key="login_pass"
            )

            if st.button(
                "Login",
                key="login_btn",
                use_container_width=True
            ):

                users = st.session_state.users

                if (
                    username in users
                    and users[username] == password
                ):

                    st.session_state.logged_in = True
                    st.session_state.user = username

                    st.success("Welcome 🚀")
                    st.rerun()

                else:
                    st.error("Invalid credentials")

        # =====================
        # SIGNUP TAB
        # =====================
        with tab2:

            new_user = st.text_input(
                "New Username",
                key="signup_user"
            )

            new_pass = st.text_input(
                "New Password",
                type="password",
                key="signup_pass"
            )

            if st.button(
                "Create Account",
                key="signup_btn",
                use_container_width=True
            ):

                users = st.session_state.users

                if not new_user.strip() or not new_pass.strip():

                    st.warning("Fill all fields")

                elif new_user in users:

                    st.error("User already exists")

                else:

                    users[new_user] = new_pass
                    st.session_state.users = users

                    st.success(
                        "Account created successfully. Please login."
                    )

        st.markdown(
            "</div>",
            unsafe_allow_html=True
        )

    return False


# =========================
# LOGIN CHECK
# =========================
def is_logged_in():
    return st.session_state.get(
        "logged_in",
        False
    )


# =========================
# LOGOUT
# =========================
def logout():

    st.session_state.logged_in = False
    st.session_state.user = None

    st.rerun()