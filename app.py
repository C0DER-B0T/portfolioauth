import streamlit as st
import os
import requests
import urllib.parse
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# --- CONFIGURATION ---
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
GITHUB_PAT = os.getenv("GITHUB_PAT")
PUBLIC_REPO = os.getenv("PUBLIC_REPO")
PRIVATE_REPO = os.getenv("PRIVATE_REPO")
# --- HELPER FUNCTIONS ---
def get_access_token(code):
    url = "https://github.com/login/oauth/access_token"
    payload = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "code": code
    }
    headers = {"Accept": "application/json"}
    response = requests.post(url, json=payload, headers=headers)
    return response.json().get("access_token")

def get_user_info(access_token):
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get("https://api.github.com/user", headers=headers)
    return response.json()

def check_if_starred(user_oauth_token):
    headers = {
        "Authorization": f"Bearer {user_oauth_token}",
        "Accept": "application/vnd.github.v3+json"
    }
    url = f"https://api.github.com/user/starred/{PUBLIC_REPO}"
    
    try:
        # Added timeout=10 (wait max 10 seconds before giving up)
        response = requests.get(url, headers=headers, timeout=10)
        return response.status_code == 204
    except requests.exceptions.RequestException as e:
        # If the internet drops or times out, show an error in Streamlit instead of crashing
        st.error(f"Network error while connecting to GitHub: {e}")
        return False

def invite_to_repo(username):
    headers = {
        "Authorization": f"Bearer {GITHUB_PAT}",
        "Accept": "application/vnd.github.v3+json"
    }
    url = f"https://api.github.com/repos/{PRIVATE_REPO}/collaborators/{username}"
    response = requests.put(url, headers=headers)
    return response.status_code in [201, 204] # 201 Created, 204 Already a collaborator

# --- UI & LOGIC ---

video_file = open("lv_0_20260318165655.mp4", "rb")
video_bytes = video_file.read()
st.subheader("Portfolio Preview")
st.video(video_bytes)




st.set_page_config(page_title="Unlock Assignments", page_icon="⭐")

st.title("Unlock the Portfolio Source Code")
st.write(f"To get access to the Source Code, you must star the public repository: **{PUBLIC_REPO}**")


# 1. Check if we have a "code" in the URL (meaning the user just logged in)
query_params = st.query_params
if "code" in query_params:
    code = query_params["code"]
    
    with st.spinner("Authenticating with GitHub..."):
        # Clear the code from the URL so it doesn't run twice
        st.query_params.clear() 
        
        token = get_access_token(code)
        if token:
            user_info = get_user_info(token)
            username = user_info.get("login")
            
            if username:
                st.success(f"Logged in as **{username}**!")
                
                with st.spinner("Checking your stars..."):
                    if check_if_starred(token):
                        st.success("Awesome! You starred the repo. 🌟")
                        
                        with st.spinner("Inviting you to the private vault..."):
                            if invite_to_repo(username):
                                st.balloons()
                                st.success("🎉 **Success!** You have been invited to the private repository.")
                            
                                st.markdown(f'<a href="https://github.com/{PRIVATE_REPO}"><button style="background-color:#FF0000;  color:white; padding:10px 20px; border:none; border-radius:5px; cursor:pointer; font-weight:bold;">Click here to Access the Source Code</button></a>', unsafe_allow_html=True)

                                st.info("Check your email or your GitHub notifications to accept the invitation.")
                            else:
                                st.error("Something went wrong while sending the invite. Make sure the PAT has the right permissions.")
                    else:
                        st.error(f"❌ It looks like you haven't starred [{PUBLIC_REPO}](https://github.com/{PUBLIC_REPO}) yet.")
                        st.warning("Go star it, then come back and try logging in again!")
                        st.link_button("Star the Repo", f"https://github.com/{PUBLIC_REPO}")

                        
        else:
            st.error("Authentication failed. Please try again.")


else:
    
    st.write(f"If You didn't star the repo then first [Star it](https://github.com/{PUBLIC_REPO})")
    # Generate the GitHub Login URL
    login_url = f"https://github.com/login/oauth/authorize?client_id={CLIENT_ID}&scope=read:user"
    st.markdown(f'<a href="{login_url}"><button style="background-color:#2ea043; color:white; padding:10px 20px; border:none; border-radius:5px; cursor:pointer; font-weight:bold;">Login with GitHub to Verify Star</button></a>', unsafe_allow_html=True)