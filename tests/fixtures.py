import pytest

@pytest.fixture()
@pytest.mark.django_db
def get_login(client, django_user_model):
    """get users and tokens"""

    username = 'igor_'
    password = 'igor_'
    is_staff = True
    
    second_username = 'iigor'
    second_password = 'iiogr'
    
    user1 = django_user_model.objects.create_user(username=username, password=password, is_staff=is_staff)
    user2 = django_user_model.objects.create_user(username=second_username, password=second_password, is_staff=is_staff)

    return username, password, second_username, second_password, user1, user2
