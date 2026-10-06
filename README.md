#  Digital Medication Tracker & Personal Health Record

## Problem Statement

Managing medications can be challenging when users need to keep track of dosage frequency, medication quantities, expiration dates, and usage instructions. This project provides a simple, interactive application that helps users organize their medication records, monitor their supplies, and access easy-to-understand medication information.

## Executive Summary

The Digital Medication Tracker is a Python-based application developed using Streamlit to simplify medication record management. It allows users to add medication details, search records by active ingredients or symptoms, view medication schedules, and access random wellness tips.

The application also includes a medication quantity calculator, expiration-date monitoring, and a feature for recording when a medication has been taken. When medication quantities become low, the application displays a refill warning. These features help users organize their medication information in one place.

An AI-powered medication assistant is integrated using the OpenRouter API to help explain medical terminology in simpler language. Medication records and wellness tips are stored in CSV files, while Pandas is used to process and manage the data.

## Features

### 1. Medication Management

* Add new medication records.
* Store medication names, active ingredients, dosage frequency, usage instructions, urgency level, category, symptoms, start time, expiration date, and available pill quantity.
* Save medication records in a CSV file.

### 2. Medication Search

* Search for medications using active ingredients or symptoms.
* Display matching medication records.
* Warn users when multiple records match a search, helping them identify potential ingredient overlap.

*Note: The current search uses exact matching. The warning is a basic record-matching alert and does not determine whether taking medicines together is unsafe.*

### 3. Medication Schedule

* View saved medications and their dosage frequency.
* Calculate the next scheduled intake based on the recorded start time and dosage interval.
* Display medication instructions alongside scheduled times.

### 4. Wellness Tips

* Display a randomly selected wellness tip from a separate CSV file.

### 5. Medication Quantity Calculator

* Estimate the number of pills needed based on dosage frequency and the number of days.

### 6. Expiration-Date Monitoring

* Identify medications that are approaching their expiration dates within the next seven days, including those that have already expired.

### 7. Medication Intake and Refill Alerts

* Select a medication when recording an intake.
* Decrease the stored pill quantity by one.
* Save the updated quantity to the CSV file.
* Display a refill warning when the remaining quantity is five pills or fewer.

### 8. AI Medication Assistant

* Accept user questions about medications and medical terminology.
* Use a language model accessed through the OpenRouter API to provide explanations in simple language.

AI-generated information may be inaccurate and should not be used to make medication or dosage decisions.

## Technologies Used

* **Python** — application logic and data processing.
* **Streamlit** — interactive web application interface.
* **Pandas** — reading, filtering, updating, and saving tabular data.
* **CSV** — local storage for medication records and wellness tips.
* **Python-dotenv** — loading API credentials from an environment file.
* **OpenAI Python library** — connecting to the OpenRouter API.
* **OpenRouter API** — accessing the language model used by the medication assistant.

## Installation and Setup

## Data Storage

The application uses CSV files for simple, local data storage.

| File               | Purpose                                                 |
| ------------------ | ------------------------------------------------------- |
| `data.csv`         | Stores medication information and available quantities. |
| `wellnesstips.csv` | Stores wellness tips displayed by the application.      |
| `projectkey.env`   | Stores the API key used by the AI assistant.            |

Medication changes are saved to `data.csv`. This approach is suitable for a beginner project, although it does not provide the access controls, encryption, or multi-user data management expected of a production healthcare application.

## Limitations and Future Improvements

Potential improvements include:

* Add more flexible, case-insensitive ingredient and symptom searches.
* Validate user inputs, including dosage frequency, medication quantity, and expiration dates.
* Prevent medication quantities from becoming negative.
* Store medication intake history with timestamps.
* Improve the schedule to calculate upcoming doses accurately and refresh it as time passes.
* Add user authentication and more secure storage.
* Improve error handling for missing CSV files, invalid data, and API failures.
* Add clear warnings that AI responses may be inaccurate and require professional verification.

## Author
Sara Dahif

Developed as part of a Data Science learning project to apply Python programming, data manipulation, application development, and AI integration to a practical use case.
