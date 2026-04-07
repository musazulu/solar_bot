import json
import re
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Lead

# =========================
# LOAD DATA
# =========================
with open("chatbot/solar_data.json") as f:
    solar_data = json.load(f)

# =========================
# TEMP MEMORY (simple)
# =========================
user_states = {}  # {session_id: state}


# =========================
# HELPERS
# =========================
def check_faq(message):
    for item in solar_data["faq"]:
        if item["question"] in message:
            return item["answer"]
    return None


def recommend_system(message):
    if "fridge" in message or "tv" in message:
        return solar_data["packages"][1]

    elif "business" in message or "everything" in message:
        return solar_data["packages"][2]

    elif "light" in message or "phone" in message:
        return solar_data["packages"][0]

    return None


def detect_phone(message):
    return re.search(r"\d{9,13}", message)


# =========================
# WEB CHAT (SMART)
# =========================
@api_view(['POST'])
def chat(request):
    user_message = request.data.get("message", "").lower()
    session_id = request.META.get('REMOTE_ADDR', 'default')

    state = user_states.get(session_id, "start")

    if not user_message:
        return Response({"reply": "Please type your message."})

    # =========================
    # GREETING
    # =========================
    if "hello" in user_message or "hi" in user_message:
        user_states[session_id] = "start"
        return Response({
            "reply": "Hello 👋 Welcome to SolarBot!\nWhat do you want to power? (TV, fridge, lights, business)"
        })

    # =========================
    # FAQ
    # =========================
    faq = check_faq(user_message)
    if faq:
        return Response({"reply": faq})

    # =========================
    # RECOMMENDATION STEP
    # =========================
    recommendation = recommend_system(user_message)
    if recommendation:
        user_states[session_id] = "waiting_for_confirmation"
        return Response({
            "reply": f"⚡ {recommendation['name']} ({recommendation['price']})\n{recommendation['description']}\n\nWould you like us to contact you? (yes/no)"
        })

    # =========================
    # HANDLE YES
    # =========================
    if state == "waiting_for_confirmation" and user_message in ["yes", "y"]:
        user_states[session_id] = "waiting_for_phone"
        return Response({
            "reply": "Great 👍 Please send your phone number so we can contact you."
        })

    # =========================
    # HANDLE PHONE
    # =========================
    if state == "waiting_for_phone" and detect_phone(user_message):
        Lead.objects.create(
            phone=user_message,
            message="Web Lead"
        )
        user_states[session_id] = "done"
        return Response({
            "reply": "✅ Thank you! Our team will contact you shortly."
        })

    # =========================
    # HANDLE NO
    # =========================
    if state == "waiting_for_confirmation" and user_message in ["no", "n"]:
        user_states[session_id] = "start"
        return Response({
            "reply": "No problem 👍 Tell me what you want to power (TV, fridge, lights, business)."
        })

    # =========================
    # FALLBACK
    # =========================
    return Response({
        "reply": "I can help you choose a solar system.\nTell me what you want to power (TV, fridge, lights, business)."
    })


# =========================
# WHATSAPP (IGNORE FOR NOW)
# =========================
@csrf_exempt
def whatsapp_webhook(request):
    return HttpResponse("OK")