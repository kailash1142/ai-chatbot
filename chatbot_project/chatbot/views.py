


from django.shortcuts import render, redirect
from .models import ChatMessage
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def chatbot_view(request):

    if request.method == "POST":

        question = request.POST.get("message")

        try:
            response = client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a flower shop assistant."
                    },
                    {
                        "role": "user",
                        "content": question
                    }
                ]
            )

            answer = response.choices[0].message.content


        except Exception:
            answer = "OpenAI API quota exceeded. Please add credits to your API account."


        user = User.objects.get(username="admin")

        ChatMessage.objects.create(
            user=user,
            question=question,
            answer=answer
        )

    messages = ChatMessage.objects.all().order_by("-created_at")

    return render(
        request,
        "chatbot/chat.html",
        {"messages": messages}
    )


def register_view(request):

    if request.method == "POST":

        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("/admin/login/")

    else:
        form = UserCreationForm()

    return render(
        request,
        "chatbot/register.html",
        {"form": form}
    )