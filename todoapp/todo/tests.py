from django.test import TestCase
from .models import TodoLists
from django.contrib.auth.models import User
from rest_framework.test import APITestCase


# Create your tests here.


class TodoTests(TestCase):
    fixtures = ['todo']
    def setUp(self):
        self.instance = TodoLists.objects.create(
            user_id = 52,
            title = 'test title',
            description = 'test description',
            scheduled_at = '2023-01-01',
            status = 1
        )


    def test_sampletododata(self):
        with self.subTest('Todo Title Match'):
            self.assertEqual(self.instance.title, 'test title')
        with self.subTest('Todo Description Match'):
            self.assertEqual(self.instance.description, 'test description')
        with self.subTest('Todo User Match'):
            self.assertEqual(self.instance.user.id, 52)
        with self.subTest('Todo Status Match'):
            self.assertEqual(self.instance.status, 1)
        with self.subTest('Todo Scheduled_at Match'):
            self.assertEqual(self.instance.scheduled_at, '2023-01-01')


class TodoCRUDTests(APITestCase):
    fixtures = ['todo']

    def setUp(self):
        self.user = User.objects.create_user(
            username = "sampleuser",
            email = "sampleuser",
            first_name = "fname",
            last_name = "fname",
            password="123"
        )

    def test_listing(self):
        response = self.client.get(f'/todo/todolist/?page=1&limit=5')
        data = response.json()

        with self.subTest(f'=== Todo listing api STATUS CODE TEST =='):
            self.assertEqual(response.status_code, 200)

        with self.subTest(f'=== Todo listing api STATUS CODE TEST from data dict =='):
            self.assertEqual(data["status"], 200)

        with self.subTest(f'=== Todo listing api pagination data count =='):
            self.assertEqual(len(data["data"]["results"]), 5)


    def test_post(self):

        payload = {
                "title": "NEW2 Real protect will model else.",
                "description": "NEW2 Structure necessary public keep most unit say. Every growth behavior here give public law. Memory first surface eye democratic who somebody.",
                "scheduled_at": "2000-04-22T23:30:34+05:30",
                "user" : self.user.id
            }
        response = self.client.post(f'/todo/todolist/', payload)
        data = response.json()
        created_data = {
            "title": data["data"]["title"],
            "description": data["data"]["description"],
            "scheduled_at": data["data"]["scheduled_at"],
            "user" : data["data"]["user"]
        }

        with self.subTest(f'=== test_post(self) status code check =='):
            self.assertEqual(response.status_code, 200)

        with self.subTest(f'=== test_post(self) status code check from data dict=='):
            self.assertEqual(data["status"], 200)
            
        with self.subTest(f'=== test_post(self) created data values check=='):
            self.assertEqual(payload, created_data)
        

        payload_copy = payload.copy()
        payload_copy.pop("title")
        response = self.client.post(f'/todo/todolist/', payload_copy)
        with self.subTest(f'=== test_post(self) status code check without required field title =='):
            self.assertNotEqual(response.status_code, 200)

