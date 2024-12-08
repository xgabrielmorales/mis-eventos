import factory

from src.users.models.user import User
from src.users.schemas import Role


class UserFactory(factory.Factory[User]):
    class Meta:
        model = User

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    username = factory.Faker("user_name")
    password = factory.Faker("password")
    role = factory.Iterator(Role)
