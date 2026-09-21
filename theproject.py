import csv
import streamlit as st
import streamlit as st
import pandas as pd
import datetime

data= "data.csv"

st.title("Welcome to your Medication Tracker!💊")
choice = st.selectbox("What would you like to do?",["Add a new medication","Search medications","View all medications","Wellness tip"],index=None,placeholder="Choose an option...")

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

    if st.button("Save Medication"): 
         with open(data, "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([medication_name,ingredients,frequency,instructions,critical_level,category,symptom,start_time,expiration_date,no_pills])
            st.success("Medication saved!")

#searching medication
#loading the data as a dataframe using pandas for easier haandling
df = pd.read_csv(data)

if choice == "Search medications":
    search = st.text_input("Search by active ingredient or symptom")

    if st.button("Search"):
        filtered_data = df[(df["symptom"] == search) | (df["ingredients"] == search)]

        if filtered_data.empty:
            st.write("Not available")
        else:
            st.write(filtered_data)

            # Warning ONLY if the user searched an ingredient
            if search in df["ingredients"].values and len(filtered_data) > 1:
                st.write(f"⚠️ This ingredient is in {len(filtered_data)} medicines — overdose risk.")


if choice == "View all medications":

    st.write("### 💊 All Medications")

    current_time = datetime.datetime.now()

    all = []

    for index, row in df.iterrows():  
        start_time = datetime.datetime.strptime(row["start_time"],"%H:%M:%S").time()# formating the starttime , from text to 24hour format
        next_dose = datetime.datetime.combine(current_time.date(),start_time) # Create today's starting dose

        # find the next dose after the current time
        while next_dose <= current_time:
            next_dose += datetime.timedelta(hours=float(row["frequency"]))

        all.append({"Medication": row["medication_name"],"Frequency (hours)": row["frequency"],"Next Scheduled Intake": next_dose})

    all_df = pd.DataFrame(all)
    all_df = all_df.sort_values("Next Scheduled Intake") #sorting be the upcoming dose

    # Make the date/time easier to read
    all_df["Next Scheduled Intake"] = all_df["Next Scheduled Intake"].apply(lambda x: x.strftime("%d %b %Y, %I:%M %p"))
    st.dataframe(all_df, use_container_width=True)

    
    #the 24 hour Schedule
    st.write("### 📅 24-Hour Medication Schedule")

    schedule = []

    today = datetime.date.today()

    for index, row in df.iterrows():
        start_time = datetime.datetime.strptime(row["start_time"],"%H:%M:%S").time() # formating the starttime , from text to 24hour format 
        dose_time = datetime.datetime.combine(today,start_time) # Starting dose
        end_time = dose_time + datetime.timedelta(hours=24) # Exactly 24 hours from the starting dose

        # Generate all doses
        while dose_time <= end_time:

            if dose_time.date() == today:
                day = "Today"
            else:
                day = "Tomorrow"

            schedule.append({"DateTime": dose_time,"Day": day,"Time": dose_time.strftime("%I:%M %p"),"Medication": row["medication_name"],
                "Instructions": row["instructions"]})

            dose_time += datetime.timedelta(hours=float(row["frequency"]))

   
    schedule_df = pd.DataFrame(schedule) # Create DataFrame
    schedule_df = schedule_df.sort_values("DateTime")# Sort all medicines
    schedule_df = schedule_df.drop(columns=["DateTime"])# Remove the technical column
    st.dataframe(schedule_df,use_container_width=True)


# Random Wellness tip
wellness_df = pd.read_csv("wellnesstips.csv")
if choice == "Wellness tip":
    random_row = wellness_df["wellness_tip"].sample(n=1).iloc[0]
    st.success(f"💡 {random_row}")


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
    # Find the selected medication
    index = df[df["medication_name"] == medication].index[0]
    df.loc[index, "no_pills"] = df.loc[index, "no_pills"] - 1 # Decrease quantity by 1
    st.write(f"Remaining pills: {df.loc[index, 'no_pills']}")
    df.to_csv(data, index=False)

    # the refill warning
    if df.loc[index, "no_pills"] <= 5:
        st.warning("⚠️ Your medication is running low, Time to refill!")


#LLM
from dotenv import load_dotenv
import os
from openai import OpenAI

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
        st.warning("Please enter a question.")
