import os
import base64
import streamlit as st
import google.generativeai as gen_ai
import random
import time
from datetime import datetime
import pytz

# Read the logo image and encode it in base64
def get_base64_image(image_path):
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except Exception as e:
        st.error("Whoops! Something's off. Our team is on it, so please try again shortly.")
        return None

# Path to your image file
image_path = 'NMEIS_Assistant/nmeis.png'

# Get base64 encoding of the image
icon_base64 = get_base64_image(image_path)

# Configure Streamlit page settings
st.set_page_config(
    page_title="NMEIS Assistant",
    page_icon=f"data:image/png;base64,{icon_base64}",
    layout="centered",
)

# Function to read content from a text file
def read_instruction_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

# Function to update the real_time_info.txt file with the current date and time
def get_real_time_info():
    # Define the desired time zone
    desired_timezone = 'Asia/Riyadh'  # Change this to your desired time zone
    
    # Get the current time in the desired time zone
    current_time = datetime.now(pytz.timezone(desired_timezone))
    
    # Format the current time
    formatted_time = current_time.strftime("%Y-%m-%d %I:%M %p")
    
    # Return the formatted time
    return f"Current Time ({desired_timezone}): {formatted_time}"

# Usage
real_time_info = get_real_time_info()

# Path to your instruction file
instruction_file_paths = [
    r'NMEIS_Assistant/system instructions/staff.csv',
    r'NMEIS_Assistant/system instructions/general_instructions.txt',
    r'NMEIS_Assistant/system instructions/shortcut.csv',    
    r'NMEIS_Assistant/system instructions/Ataa Educational Company.txt',
    r'NMEIS_Assistant/system instructions/fee and payment.txt',
    r'NMEIS_Assistant/system instructions/event schedule.csv',
    r'NMEIS_Assistant/system instructions/admission.txt',
    r'NMEIS_Assistant/system instructions/parent.txt',
    r'NMEIS_Assistant/system instructions/behavior.txt',
]

# Read and combine the content of all instruction files
system_instructions = ""
for path in instruction_file_paths:
    system_instructions += read_instruction_file(path) + "\n"

    # Append real-time information to the system instructions
    system_instructions += get_real_time_info()

#GOOGLE_API_KEY = ('AIzaSyDCRGF-WOwm2fNARw6ZQR7WY1ZfOZMr5Go')
GOOGLE_API_KEY = ('AIzaSyDs6j7qFgdinhFJyzLaCGElsKS8UWy9_6w')

# Configure generation settings
generation_config = {
    "temperature": 0.9,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 81290,
    "response_mime_type": "text/plain",
}

safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_NONE",
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_NONE",
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE",
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_NONE",
  },
]

# Set up Google Gemini-Pro AI model
try:
    gen_ai.configure(api_key=GOOGLE_API_KEY)
    model = gen_ai.GenerativeModel(
        model_name="gemini-1.5-pro-latest",
        safety_settings=safety_settings,
        generation_config=generation_config,
        system_instruction=system_instructions,)
except Exception as e:
    st.error("Hang tight! We're sorting out an issue. Please try again soon!")


# Function to translate roles between Gemini-Pro and Streamlit terminology
def translate_role_for_streamlit(user_role):
    if user_role == "model":
        return "assistant"
    else:
        return user_role


# Initialize chat session in Streamlit if not already present
if "chat_session" not in st.session_state:
    try:
        st.session_state.chat_session = model.start_chat(history=[])
    except Exception as e:
        st.error("We're experiencing a hiccup. Don't worry, we're working to fix it. Please try again shortly!")

# Add school logo above the title, centered
school_logo_path = 'NMEIS_Assistant/nmeis.png'
try:
    logo_base64 = get_base64_image(school_logo_path)
except Exception as e:
    st.error("Yikes! Looks like we've hit a snag. Let's give it another go soon!")

st.markdown(
    f"""
    <div style="display: flex; justify-content: center;">
        <img src="data:image/png;base64,{logo_base64}" width="80" height="80" style="margin-right: 10px;">
        <h1 style="margin: 0;">Chat With NMEIS Assistant!</h1>
    </div>
    """,
    unsafe_allow_html=True
)

# Display the chatbot's title on the page
st.write("")
st.write("")

# Define suggestion buttons
suggestions = {
    "School admission process 🏫": "Can you tell me about the school admission process?",
    "Upcoming school events 📅": "What are the upcoming events at the school?",
    "School fee structure details 💰": "Can you provide the details of the school fee structure for cbse curriculum?",
    "Technology Integration 💻": "How does the school integrate technology into the learning process?",
}

# Display suggestion buttons
st.write("**Frequently Asked Questions:**")
columns = st.columns(len(suggestions))
for i, (label, prompt) in enumerate(suggestions.items()):
    if columns[i].button(label):
        st.session_state.user_prompt = prompt

# Display the chat history
try:
    for message in st.session_state.chat_session.history:
        with st.chat_message(translate_role_for_streamlit(message.role)):
            st.markdown(message.parts[0].text)
except Exception as e:
    st.error("Oops! Something went wrong. Our tech wizards are on it. Please try again in a bit!")  


# List of "Thinking..." messages
thinking_messages = [
    "Hold on, gotta check if Siri has the answer first... 🤔📱🤨",
    "The NMEIS Assistant brain trust is on the case! 😎🧠💪",
    "If this takes too long, feel free to blame the slow internet in the metaverse... 🐢🌐",
    "Just making sure this answer is worthy of your awesomeness... ✨👑",
    "Hang tight, gotta find the right meme to go with this answer... 😂🔍",
    "Having a quick chat with Einstein... Back in a jiffy! 🧠⚡",
    "Just making sure my circuits aren't fried before responding... 😅🔌",
    "Let me double-check, I might have gotten distracted by a cat video earlier... 😹⏪",
    "Shhh, I hear the answer approaching on tiny robot roller skates... 🤫🛼🤖",
    "Calculating the meaning of life, the universe, and everything... 🌌💭",
    "Time-traveling to find the best answer... 🕰️🚀",
    "I'm on a mental coffee break... ☕🧠",
    "Asking my pet rock for advice... 🪨💬"
]

# Input field for user's message
user_prompt = st.chat_input("Hey there! I'm NMEIS assistant. Ask me anything about our school!")

# Pre-fill chat input if suggestion button was clicked
if "user_prompt" in st.session_state:
    user_prompt = st.session_state.user_prompt
    del st.session_state.user_prompt

if user_prompt:
    try:
        # Add user's message to chat and display it
        st.chat_message("user").markdown(user_prompt)

        #Writing animation
        ans = random.choice(thinking_messages)

        def stream1():
            for word in ans.split(" "):
                yield word + " "
                time.sleep(0.06)

        #Placeholder for "Thinking..." message
        thinking_message = st.empty()
        with thinking_message.container():
            st.chat_message("assistant").write_stream(stream1)

        # Send user's message to Gemini-Pro and get the response
        gemini_response = st.session_state.chat_session.send_message(user_prompt)

        # Remove "Thinking..." message
        thinking_message.empty()

        #Writing animation
        ans1 = gemini_response.text

        def stream():
            for word in ans1.split(" "):
                yield word + " "
                time.sleep(0.06)

        # Display Gemini-Pro's response
        with st.chat_message("assistant"):
            st.write_stream(stream)

        # Add a reset button to clear chat history
        if st.button("Clear Chat", on_click=lambda: st.session_state.pop("chat_session", None), help="Click to clear chat history."):
            pass

    except Exception as e:
        st.error("Hang tight! We're sorting out an issue. Please try again soon!")
