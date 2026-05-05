from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def register():
    user_data = {
        "username": "mock_user",
        "password": "mock_pass",
        "email": "mock@example.com",
        "org": "Mock Org",
    }
    response = client.post("/register", json=user_data)
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["message"] == "New user registered successfully"
    assert json_response["username"] == "mock_user"
    

# class RegisterEndpointTests(unittest.TestCase):
#     def setUp(self):
#         self.client = TestClient(app)

#     def test_register_returns_success_for_mock_payload(self):
#         response = self.client.post(
#             "/register",
#             json={
#                 "username": "mock_user",
#                 "password": "mock_pass",
#                 "email": "mock@example.com",
#                 "org": "Mock Org",
#             },
#         )

#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(
#             response.json(),
#             {
#                 "message": "New user registered successfully",
#                 "username": "mock_user",
#             },
#         )

