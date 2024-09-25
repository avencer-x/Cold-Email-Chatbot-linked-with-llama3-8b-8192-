import streamlit as st
from groq import Groq

# Hardcode your Groq API key here
GROQ_API_KEY = st.secrets["GROQ_API_KEY"]  # Replace with your actual Groq API key

# Initialize the Groq client
client = Groq(api_key=GROQ_API_KEY)

st.set_page_config(page_title="Email Genie", page_icon="✉️")

def generate_email(email_type, industry, recipient_role, company_details, personal_details):
  prompt = f"""
  Generate a personalized {email_type} email for the following context:
  Industry: {industry}
  Recipient Role: {recipient_role}
  Company Details: {company_details}
  Personal Details: {personal_details}

  The email should be professional, engaging, and tailored to the recipient's role and industry.
  """

  completion = client.chat.completions.create(
      model="llama3-8b-8192",
      messages=[
          {
              "role": "user",
              "content": prompt
          }
      ],
      temperature=0.7,
      max_tokens=500,
      top_p=1,
      stream=False,
      stop=None,
  )

  return completion.choices[0].message.content

st.title("Email Genie 🧞‍♂️✉️")
st.subheader("Generate personalized emails")

# Initialize session state variables
if "email_generated" not in st.session_state:
  st.session_state.email_generated = False
if "messages" not in st.session_state:
  st.session_state.messages = []
if "current_email" not in st.session_state:
  st.session_state.current_email = ""

# Step 1: Form to fill out initial details
if not st.session_state.email_generated:
  with st.form(key='email_form'):
      email_type = st.text_input("What kind of email do you need?")
      industry = st.text_input("Industry")
      recipient_role = st.text_input("Recipient Role")
      company_details = st.text_area("Company Details")
      personal_details = st.text_area("Personal Details")
      submit_button = st.form_submit_button(label='Generate Email')

  if submit_button and email_type and industry and recipient_role and company_details and personal_details:
      response = generate_email(email_type, industry, recipient_role, company_details, personal_details)
      st.session_state.current_email = response
      st.session_state.email_generated = True
      st.session_state.messages = [
          {"role": "user", "content": f"Generate a {email_type} email for {industry} industry, recipient role: {recipient_role}"},
          {"role": "assistant", "content": f"I've generated a {email_type} email based on your inputs. Here it is:"},
          {"role": "assistant", "content": response}
      ]
      st.rerun()
  elif submit_button:
      st.error("Please fill in all fields before generating the email.")

# Step 2: Chatbot interface to interact with the generated email
if st.session_state.email_generated:
  # Display chat messages
  for message in st.session_state.messages:
      with st.chat_message(message["role"]):
          st.markdown(message["content"])

  # Chat input for making changes
  if prompt := st.chat_input("How would you like to modify the email?"):
      st.session_state.messages.append({"role": "user", "content": prompt})
      
      response_prompt = f"""
      The current email is:
      {st.session_state.current_email}

      The user wants to make the following changes:
      {prompt}

      Please provide an updated version of the email incorporating these changes.
      """
      
      completion = client.chat.completions.create(
          model="llama3-8b-8192",
          messages=[
              {
                  "role": "user",
                  "content": response_prompt
              }
          ],
          temperature=0.7,
          max_tokens=500,
          top_p=1,
          stream=False,
          stop=None,
      )
      
      response = completion.choices[0].message.content
      st.session_state.current_email = response
      st.session_state.messages.append({"role": "assistant", "content": response})
      st.rerun()

  # Add a button to start over
  if st.button("Start Over"):
      st.session_state.email_generated = False
      st.session_state.messages = []
      st.session_state.current_email = ""
      st.rerun()

# Created/Modified files during execution:
print("app.py")
