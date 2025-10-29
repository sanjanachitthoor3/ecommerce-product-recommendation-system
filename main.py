from fastapi import FastAPI, Request, Response
from twilio.twiml.messaging_response import MessagingResponse
from db.database import SessionLocal
from models.models import UserPassport

app = FastAPI()

# simple in-memory state tracking
user_state = {}

@app.post("/whatsapp")
async def whatsapp_webhook(request: Request):
    form = await request.form()
    incoming_msg = form.get("Body")
    from_number = form.get("From")  # format: 'whatsapp:+91xxxx'

    resp = MessagingResponse()
    msg = resp.message()

    # Initialize conversation state
    if from_number not in user_state:
        user_state[from_number] = {"step": 0, "data": {}}

    step = user_state[from_number]["step"]
    data = user_state[from_number]["data"]

    if step == 0:
        msg.body("Namaste! I can help you discover Govt schemes. What's your full name?")
        user_state[from_number]["step"] += 1
    elif step == 1:
        data["name"] = incoming_msg
        msg.body("How old are you?")
        user_state[from_number]["step"] += 1
    elif step == 2:
        data["age"] = int(incoming_msg)
        msg.body("Select your gender: Male / Female / Other")
        user_state[from_number]["step"] += 1
    elif step == 3:
        data["gender"] = incoming_msg
        msg.body("Which state do you live in?")
        user_state[from_number]["step"] += 1
    elif step == 4:
        data["state"] = incoming_msg
        msg.body("Approximate annual family income: <2L / 2-5L / 5-10L / >10L")
        user_state[from_number]["step"] += 1
    elif step == 5:
        data["income_range"] = incoming_msg
        msg.body("Preferred language for updates? Hindi / Tamil / Telugu / English")
        user_state[from_number]["step"] += 1
    elif step == 6:
        data["language"] = incoming_msg
        # Save to DB
        db = SessionLocal()
        user = UserPassport(
            whatsapp_number=from_number,
            name=data["name"],
            age=data["age"],
            gender=data["gender"],
            state=data["state"],
            income_range=data["income_range"],
            language=data["language"]
        )
        db.add(user)
        db.commit()
        db.close()

        msg.body("✅ Your Scheme Passport is created! You will now receive eligible scheme updates.")
        user_state.pop(from_number)  # reset conversation

    return Response(content=str(resp), media_type="application/xml")
