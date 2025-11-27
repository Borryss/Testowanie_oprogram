import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from main.models import Message

@pytest.mark.django_db
def test_simple_registration_and_send_message_in_private_messages(client):
    url = reverse("registration")
    response = client.post(url, {
        "username": "uuu",
        "password1": "12345fgh",
        "password2": "12345fgh",
    })

    assert User.objects.filter(username="uuu").exists()

    url = reverse("registration")
    response = client.post(url, {
        "username": "uuu2",
        "password1": "12345fgh",
        "password2": "12345fgh",
    })

    assert User.objects.filter(username="uuu2").exists()

    target = User.objects.get(username="uuu")
    user = User.objects.get(username="uuu2")

    response = client.post(
        reverse("send_message", kwargs={"user_id": target.id}),
        {"content": "Test_message1"}
    )

    mesage = Message.objects.filter(sender=user, receiver=target).first()
    assert mesage.content == "Test_message1"




@pytest.mark.django_db
def test_simple_registration_and_send_message_and_check_All_dialogs_in_private_messages(client):
    url = reverse("registration")
    response = client.post(url, {
        "username": "uuu",
        "password1": "12345fgh",
        "password2": "12345fgh",
    })

    assert User.objects.filter(username="uuu").exists()

    url = reverse("registration")
    response = client.post(url, {
        "username": "uuu2",
        "password1": "12345fgh",
        "password2": "12345fgh",
    })

    assert User.objects.filter(username="uuu2").exists()

    target = User.objects.get(username="uuu")
    user = User.objects.get(username="uuu2")


    response = client.get(reverse("dialogs"))
    users = response.context["users"]
    assert len(users) == 0

    response = client.post(
        reverse("send_message", kwargs={"user_id": target.id}),
        {"content": "Test_message1"}
    )

    mesage = Message.objects.filter(sender=user, receiver=target).first()
    assert mesage.content == "Test_message1"

    response = client.get(reverse("dialogs"))
    users = response.context["users"]
    assert len(users) == 1

