import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from datetime import datetime
from dateutil.relativedelta import relativedelta
from datetime import timezone

cred = credentials.Certificate("credentials/serviceAccountCred.json")
firebase_admin.initialize_app(cred)

def get_people_signed_in():
    db = firestore.client()
    ref = db.collection("active_sessions")
    docs = ref.stream()
    people_signed_in = []
    for doc in docs:
        data = doc.to_dict()
        start_date = data["start_date"]
        now = datetime.now(timezone.utc)
        delta = relativedelta(now, start_date)

        if delta.years > 0:
            relative = f"{delta.years} year(s) ago"
        elif delta.months > 0:
            relative = f"{delta.months} month(s) ago"
        elif delta.days > 0:
            relative = f"{delta.days} day(s) ago"
        elif delta.hours > 0:
            relative = f"{delta.hours} hour(s) ago"
        elif delta.minutes > 0:
            relative = f"{delta.minutes} minute(s) ago"
        else:
            relative = "just now"

        people_signed_in.append({"name": data["name"], "start_date": relative})
    return people_signed_in