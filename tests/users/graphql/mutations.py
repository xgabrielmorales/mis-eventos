from httpx import Client

from tests.users.factories.user import UserFactory


class TestUserMutations:
    def test_create_user(self, client: Client) -> None:
        new_user = UserFactory()

        mutation = """
        mutation CreateUser($userData: UserInput!) {
            createUser(userData: $userData) {
                id
                firstName
                lastName
                username
                role
            }
        }
        """

        variables = {
            "userData": {
                "firstName": new_user.first_name,
                "lastName": new_user.last_name,
                "username": new_user.username,
                "password": new_user.password,
                "role": new_user.role.value.upper(),
            },
        }

        response = client.post(
            url="/graphql",
            json={"query": mutation, "variables": variables},
        )

        assert response.status_code == 200
        data = response.json()

        assert "errors" not in data

        user = data["data"]["createUser"]
        assert user["username"] == new_user.username
        assert user["role"] == new_user.role.value.upper()
