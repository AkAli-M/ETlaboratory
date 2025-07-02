from scraper import Scraper
from utils import save_to_file
from config import URL, USER_NAME, PASSWORD, Attendence_url

import firebase_admin
from firebase_admin import credentials, firestore

# Firebase setup
cred = credentials.Certificate("firebase-key.json")  # Path to your Firebase private key
firebase_admin.initialize_app(cred)
db = firestore.client()

def push_to_firebase(data):
    for row in data:
        # Assumes row is a dict like {"name": ..., "date": ..., "status": ...}
        db.collection("attendance").add(row)

def main():
    with Scraper(URL) as scraper:
        scraper.login(USER_NAME, PASSWORD)
        scraper.go_to_url(Attendence_url)

        table_data = scraper.get_table_data("items table table-striped table-bordered")
        save_to_file(table_data, "attendance.json")  # Optional local backup

        push_to_firebase(table_data)
    print("✅ Attendance data saved to Firebase and attendance.json")

if __name__ == "__main__":
    main()
