from src.schemas.UserSchemas import UserCreateSchema
auth_prefix = f"/api/v1/auth"

def test_user_creation(fake_session, fake_user_service, test_client):
    user_data_dict = {
        "username": "john_doe92",
        "first_name": "John",
        "last_name": "Doe",
        "password": "secret123",
        "email": "john.doe92@gmail.com"
    }

    response = test_client.post(
        url=f"{auth_prefix}/signup",
        json=user_data_dict
    )

    user_data = UserCreateSchema(**user_data_dict)

    assert fake_user_service.user_exists_called_once()
    assert fake_user_service.user_exists_called_once_with(user_data_dict['email'], fake_session)

    assert fake_user_service.create_user_called_once()
    assert fake_user_service.create_user_called_once_with(user_data, fake_session)