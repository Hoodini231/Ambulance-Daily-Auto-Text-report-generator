# Automated report system for Ambulance sitreps
**Goal of the project:** To output a formatted textual report based on data recieved from ambulance teams

**Context of the project:** For my national service I was tasked to report on the daily situation of a few ambulance bases across Singapore. Feeling that the task was extremely repetitive, I decided to automate the process.

**Brief Outline of Data:** Excel spreadsheet containing responses from a survey done every ambulance shift. Examples of what is to be expected for each entry include: NRIC, Health declearations, Discrepencies and covid-risk questions

**The project should be able to:**
  * Correctly identified which base and shift has submitted their daily sitrep
  * Correctly identify the masked NRIC of those who have not completed their ART SA test
  * Output an accurate report in the form of a text document or string
  * Output the report via Twilio to my whatsapp phone number

**Dependencies:**
  * Serial.txt, acts as a reference for the number in the name of the downloaded data

**Additional features added:**
  * Ability to automatically login in to survey website and mail through the use of Selenium
  * Using MAC OSX and Iphone SMS forwarding feature to acquire SMS otp for login (SQlite3 library used)
  * Download Data for this morning and tonight
  * Sends out report at 10 am to me while I am at camp
