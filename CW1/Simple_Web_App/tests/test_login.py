import pytest
from django.urls import reverse
from django.contrib.auth.models import User

@pytest.mark.django_db
def test_simple_registration_and_login(client):
    reg_url = reverse("registration")
    reg_response = client.post(reg_url, {
        "username": "uuu",
        "password1": "12345fgh",
        "password2": "12345fgh",
    })

    assert User.objects.filter(username="uuu").exists()

    login_url = reverse("login")
    login_response = client.post(login_url, {
        "username": "uuu",
        "password": "12345fgh"
    })

    assert login_response.status_code == 302
    assert "_auth_user_id" in client.session
    assert client.session["_auth_user_id"] == str(User.objects.get(username="uuu").id)


@pytest.mark.django_db
def test_wrong_password_login(client):
    reg_url = reverse("registration")
    reg_response = client.post(reg_url, {
        "username": "uuu",
        "password1": "12345fgh",
        "password2": "12345fgh",
    })

    assert User.objects.filter(username="uuu").exists()

    client.logout()

    login_url = reverse("login")
    login_response = client.post(login_url, {
        "username": "uuu",
        "password": "112345fgh"
    })

    assert login_response.status_code == 200
    assert "_auth_user_id" not in client.session

@pytest.mark.django_db
def test_wrong_username_login(client):
    reg_url = reverse("registration")
    reg_response = client.post(reg_url, {
        "username": "uuu",
        "password1": "12345fgh",
        "password2": "12345fgh",
    })

    assert User.objects.filter(username="uuu").exists()

    client.logout()

    login_url = reverse("login")
    login_response = client.post(login_url, {
        "username": "uuu1",
        "password": "12345fgh"
    })

    assert login_response.status_code == 200
    assert "_auth_user_id" not in client.session







