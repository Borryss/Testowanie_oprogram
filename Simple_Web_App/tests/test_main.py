import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from main.models import Post

@pytest.mark.django_db
def test_simple_registration_and_post_in_main(client):
    reg_url = reverse("registration")
    reg_response = client.post(reg_url, {
        "username": "uuu",
        "password1": "12345fgh",
        "password2": "12345fgh",
    })

    assert User.objects.filter(username="uuu").exists()

    home_url = reverse("home")
    response = client.post(home_url, {
        "content": "Test_message1"
    })

    assert Post.objects.filter(content="Test_message1").exists()

@pytest.mark.django_db
def test_simple_registration_and_post_and_delete_in_main(client):
    reg_url = reverse("registration")
    reg_response = client.post(reg_url, {
        "username": "uuu",
        "password1": "12345fgh",
        "password2": "12345fgh",
    })

    assert User.objects.filter(username="uuu").exists()

    home_url = reverse("home")
    response = client.post(home_url, {
        "content": "Test_message1"
    })

    assert Post.objects.filter(content="Test_message1").exists()

    post = Post.objects.get(content="Test_message1")


    response = client.post(
        reverse("delete_post", kwargs={"post_id": post.id})
    )

    assert response.status_code == 302

    assert not Post.objects.filter(id=post.id).exists()

@pytest.mark.django_db
def test_simple_registration_and_post_and_edit_in_main(client):
    reg_url = reverse("registration")
    reg_response = client.post(reg_url, {
        "username": "uuu",
        "password1": "12345fgh",
        "password2": "12345fgh",
    })

    assert User.objects.filter(username="uuu").exists()

    home_url = reverse("home")
    response = client.post(home_url, {
        "content": "Test_message1"
    })

    assert Post.objects.filter(content="Test_message1").exists()

    post = Post.objects.get(content="Test_message1")

    response = client.post(
        reverse("edit_post", kwargs={"post_id": post.id}),
        {"content": "Test_message1(Test-edit)"}
    )

    post.refresh_from_db()
    assert post.content == "Test_message1(Test-edit)"


