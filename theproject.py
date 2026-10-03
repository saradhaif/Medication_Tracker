import streamlit as st
import pandas as pd
import datetime
from dotenv import load_dotenv
import os
from openai import OpenAI

data= "data.csv"
df = pd.read_csv(data)

st.title("Welcome to your Medication Tracker!💊")
choice = st.selectbox("What would you like to do?",["Add a new medication","Search medications","View all medications","Wellnesstip"],index=None,placeholder="Choose an option")

if choice == "Add a new medication":
    medication_name = st.text_input(" Enter the medication Name ")
    ingredients = st.text_input(" Enter the Active Ingredients or Interacting Substances in the medicine")
    frequency= st.number_input(" Enter Dosage Frequency in hours")
    instructions= st.text_input(" Enter the Usage & Safety Instructions")
    critical_level= st.radio(" What is the Urgency/Critical Level", ["Low", "Medium", "High"])
    category = st.selectbox("What type of medication is this?",["Prescription", "OTC", "Supplement", "First Aid"])
    symptom=st.text_input("What are the current symptoms?")
    start_time = st.time_input("When will you take the first dose?", value= None)
    expiration_date= st.date_input("what is the expiration date?")
    no_pills = st.number_input("what is the available number of pills?")

    
    # to save to the csv file
    if st.button("Save Medication"):
        new_med = pd.DataFrame({"medication_name": [medication_name],"ingredients": [ingredients],"frequency":[frequency],"instructions": [instructions],"critical_level": [critical_level],"category": [category],"symptom": [symptom],"start_time": [start_time],"expiration_date": [expiration_date],"no_pills": [no_pills],})
        df = pd.concat([df, new_med])
        df.to_csv(data, index=False)
        st.success("Medication saved!")


#searching for a medication
if choice == "Search medications":
    search = st.text_input("Search by active ingredient or symptom")

    if st.button("Search"):
        filtered_data = df[(df["symptom"] == search) | (df["ingredients"] == search)]

        if filtered_data.empty:
            st.write("Not available")
        else:
            st.write(filtered_data)
            if search in df["ingredients"].values and len(filtered_data) > 1:
                st.write(f"⚠️ This ingredient is in {len(filtered_data)} medicines, overdose risk.")


if choice == "View all medications":

    st.write("### 💊 All Medications")

    df["start_time"] = pd.to_datetime(df["start_time"])
    df["next_dose"] = df["start_time"] + pd.to_timedelta(df["frequency"].astype(float), unit="h" )
    all_df = df[["medication_name","frequency","next_dose"]]
    all_df.columns = ["Medication","Frequency (hours)","Next Scheduled Intake"]
    st.dataframe(all_df)


    st.write("### 📅 24-Hour Medication Schedule")
    schedule_df = df[["start_time","medication_name","instructions"]]
    schedule_df.columns = ["Time","Medication","Instructions"]
    st.dataframe(schedule_df)


# Random Wellness tip
wellness_df = pd.read_csv("wellnesstips.csv")
if choice == "Wellness tip":
    random = wellness_df["wellness_tip"].sample(n=1).iloc[0]
    st.success(f"💡 {random}")


#Medication Quantity Calculator 
st.write("### 🔢Medication Quantity Calculator") 
frequency = st.number_input("Dosage frequency (hours)",min_value=1) 
days = st.number_input("Number of days",min_value=1) 
pills_needed = int((24 / frequency) * days) 
st.info(f"Estimated pills needed: {pills_needed}")


# Expriration Date
st.write("### ⌛Soon to be expired") 
df["expiration_date"] = pd.to_datetime(df["expiration_date"]).dt.date
today = datetime.date.today()
near_expiration = df[df["expiration_date"] <= today + datetime.timedelta(days=7)]
st.write(near_expiration)


# Select medication
st.write("### 💊Select the medication you took here:")
medication = st.selectbox("Select the medication you took:",df["medication_name"].unique())

# the medication button
if st.button("Take Medication"):
    index = df[df["medication_name"] == medication].index[0]
    df.loc[index, "no_pills"] = df.loc[index, "no_pills"] - 1
    st.write(f"Remaining pills: {df.loc[index, 'no_pills']}")
    df.to_csv(data, index=False)

    # warning, when there is less than 5 pills
    if df.loc[index, "no_pills"] <= 5:
        st.warning("⚠️ Your medication is running low, Time to refill!")


#LLM
load_dotenv('projectkey.env')
openai_api_key = os.getenv('projectkey')

# Initialize the client (API key + Base URL)
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=openai_api_key
)

# Define the LLM function
def get_llm_response(prompt):
    completion = client.chat.completions.create(
        model="cohere/north-mini-code:free",
        messages=[
            {
                "role": "system",
                "content": "You are an empathetic medical communicator. Your job is to translate complex medical jargon, terms, and doctor notes into plain, simple language that anyone without a medical background can easily understand.",
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.0,
    )
    response = completion.choices[0].message.content
    return response

st.write("### 🤖 Ask the Medication Assistant")

prompt = st.text_input("What would you like to know?",placeholder="e.g. What is Omeprazole used for?")

if st.button("Ask AI"):
    if prompt:
        response = get_llm_response(prompt)
        st.write("### 💬 AI Response")
        st.write(response)
    else:
        st.warning("Please enter a question")
