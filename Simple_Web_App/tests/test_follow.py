import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from main.models import Follow

@pytest.mark.django_db
def test_simple_registration_and_follow(client):
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
        reverse("toggle_follow", kwargs={"user_id": target.id})
    )

    assert Follow.objects.filter(follower=user, following=target).exists()

    response = client.get(reverse("following"))

    following = response.context["following"]
    assert len(following) == 1





@pytest.mark.django_db
def test_simple_registration_and_follow_and_unfollow(client):
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
        reverse("toggle_follow", kwargs={"user_id": target.id})
    )

    assert Follow.objects.filter(follower=user, following=target).exists()

    response = client.get(reverse("following"))

    following = response.context["following"]
    assert len(following) == 1

    response = client.post(
        reverse("toggle_follow", kwargs={"user_id": target.id})
    )

    assert not Follow.objects.filter(follower=user, following=target).exists()

    response = client.get(reverse("following"))
    following = response.context["following"]
    assert len(following) == 0










