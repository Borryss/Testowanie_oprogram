import pytest
from django.urls import reverse
from django.contrib.auth.models import User

@pytest.mark.django_db
def test_simple_registration(client):
    url = reverse("registration")  # name=... у urls.py
    response = client.post(url, {
        "username": "uuu",
        "password1": "12345fgh",
        "password2": "12345fgh",
    })

    # print(response.content.decode())

    assert response.status_code == 302
    assert response.url == reverse("home")
    assert User.objects.filter(username="uuu").exists()
@pytest.mark.django_db
def test_password_wrong_registration(client):
    url = reverse("registration")

    response = client.post(url, {
        "username": "uuu",
        "password1": "12345fgh",
        "password2": "22345fgh",
    })

    assert response.status_code == 200
    assert not User.objects.filter(username="uuu").exists()
    assert "The two password fields didn’t match." in response.content.decode()


@pytest.mark.django_db
def test_password_short_registration(client):
    url = reverse("registration")

    response = client.post(url, {
        "username": "uuu",
        "password1": "1234",
        "password2": "1234",
    })

    assert response.status_code == 200
    assert not User.objects.filter(username="uuu").exists()


@pytest.mark.django_db
def test_password_too_common_and_numeric_registration(client):
    url = reverse("registration")

    response = client.post(url, {
        "username": "uuu",
        "password1": "123456789",
        "password2": "123456789",
    })

    assert response.status_code == 200
    assert not User.objects.filter(username="uuu").exists()

@pytest.mark.django_db
def test_invalid_name_registration(client):
    url = reverse("registration")

    response = client.post(url, {
        "username": "$$$",
        "password1": "12345fgh",
        "password2": "12345fgh",
    })

    assert response.status_code == 200
    assert not User.objects.filter(username="uuu").exists()


