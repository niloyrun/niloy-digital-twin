import json
import os
import requests
from dotenv import load_dotenv
import streamlit as st

pushover_user = st.secrets["PUSHOVER_USER"]
pushover_token = st.secrets["PUSHOVER_TOKEN"]

pushover_url = "https://api.pushover.net/1/messages.json"


def push(text):
    requests.post(
        pushover_url,
        data={
            "token": pushover_token,
            "user": pushover_user,
            "message": text,
        },
    )


def record_user_details(
    email=None,
    phone=None,
    name="Name not provided",
    notes="Not provided"
):

    if not email and not phone:
        return "Please provide either an email address or a phone number."

    push(
        f"Recording interest from {name}\n"
        f"Email: {email or 'Not provided'}\n"
        f"Phone: {phone or 'Not provided'}\n"
        f"Notes: {notes}"
    )

    return "Thank you! I've recorded your contact details."


def record_unknown_question(question):
    push(f"Recording {question} asked that I couldn't answer")
    return "OK"


record_user_details_json = {
    "name": "record_user_details",
    "description": (
        "Use this tool when the user wants to get in touch with Niloy. "
        "Record any contact details the user provides, including email, phone number, name, "
        "and any relevant notes from the conversation."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "email": {
                "type": "string",
                "description": "The user's email address, if provided."
            },
            "phone": {
                "type": "string",
                "description": "The user's phone number, if provided."
            },
            "name": {
                "type": "string",
                "description": "The user's name, if provided."
            },
            "notes": {
                "type": "string",
                "description": (
                    "Brief context about why the user wants to get in touch "
                    "or any useful conversation summary."
                )
            },
        },
        "required": [],
        "additionalProperties": False,
    },
}

record_unknown_question_json = {
    "name": "record_unknown_question",
    "description": "Always use this tool to record any question that couldn't be answered as you didn't know the answer",
    "parameters": {
        "type": "object",
        "properties": {
            "question": {"type": "string", "description": "The question that couldn't be answered"},
        },
        "required": ["question"],
        "additionalProperties": False,
    },
}

tools = [
    {"type": "function", "function": record_user_details_json},
    {"type": "function", "function": record_unknown_question_json},
]

tool_map = {
    "record_user_details": record_user_details,
    "record_unknown_question": record_unknown_question,
}


def handle_tool_calls(tool_calls):
    results = []
    for tool_call in tool_calls:
        tool_name = tool_call.function.name
        arguments = json.loads(tool_call.function.arguments)
        print(f"Tool called: {tool_name}", flush=True)
        tool = tool_map.get(tool_name)
        result = tool(**arguments) if tool else "Unknown tool: " + tool_name
        results.append(
            {"role": "tool", "content": json.dumps(result), "tool_call_id": tool_call.id}
        )
    return results
