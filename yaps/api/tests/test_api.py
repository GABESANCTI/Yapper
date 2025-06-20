
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from yaps.models import Yap, Like, Comment
from django.urls import reverse

class YapsAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.client.login(username="testuser", password="testpass")
        self.yap = Yap.objects.create(autor=self.user, conteudo="Meu primeiro yap")

    def test_list_yaps(self):
        url = reverse("api_yap_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_create_like(self):
        url = reverse("create_like")
        data = {"yap": self.yap.id}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Like.objects.filter(yap=self.yap, user=self.user).exists())

    def test_list_likes(self):
        Like.objects.create(user=self.user, yap=self.yap)
        url = reverse("yap_likes", kwargs={"yap_id": self.yap.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_create_comment(self):
        url = reverse("create_comment")
        data = {"yap": self.yap.id, "conteudo": "Comentário teste"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Comment.objects.filter(yap=self.yap, user=self.user).exists())

    def test_list_comments(self):
        Comment.objects.create(user=self.user, yap=self.yap, conteudo="Comentário existente")
        url = reverse("yap_comments", kwargs={"yap_id": self.yap.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

class YapDeleteTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='teste', password='123456')
        self.client.login(username='teste', password='123456')
        self.yap = Yap.objects.create(autor=self.user, conteudo='Vou deletar isso...')

    def test_user_can_delete_own_yap(self):
        response = self.client.delete(f'/yaps/api/yaps/{self.yap.id}/delete/')
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Yap.objects.filter(id=self.yap.id).exists())