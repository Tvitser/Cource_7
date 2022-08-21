from datetime import datetime

from django.utils import timezone

from goals.models import BoardParticipant

import pytest
from django.test.client import Client

@pytest.mark.django_db
def test_category_crud_noone(get_login, board_factory):
    current_client=Client()
    current_client.login(username=get_login[0], password=get_login[1])
    current_user = get_login[4]

    owner_client=Client()
    owner_client.login(username=get_login[2], password=get_login[3])
    owner_user = get_login[5]
    
    board = board_factory()
    board_participant = BoardParticipant.objects.create(user=owner_user, board=board, role=BoardParticipant.Role.OWNER)  # noqa F841
    
    data = {"title": "test_category_title", "user": owner_user, "board": board.id}
    reader_data = {"title": "test_category_title", "user": current_user, "board": board.id}
    
    create_request = current_client.post("/goals/goal_category/create", data=reader_data)
    owner_request = owner_client.post("/goals/goal_category/create", data=data)
    
    pk = owner_request.data.get("id")
    response = current_client.get(f"/goals/goal_category/{pk}")
    
    update_data = {"title": "updated_title"}
    update_request = current_client.patch(f"/goals/goal_category/{pk}",
                                  content_type="application/json",
                                  data=update_data)
                                  
    delete_request = current_client.delete(f"/goals/goal_category/{pk}")
    
    assert create_request.status_code == 400
    
    assert response.status_code == 404
    
    assert update_request.status_code == 404
    
    assert delete_request.status_code == 404

  
@pytest.mark.django_db
def test_goal_crud_noone(client, get_login, board_factory, category_factory):
    current_client=Client()
    current_client.login(username=get_login[0], password=get_login[1])
    current_user = get_login[4]


    owner_client=Client()
    owner_client.login(username=get_login[2], password=get_login[3])
    owner_user = get_login[5]
    
    board = board_factory()
    
    board_participant = BoardParticipant.objects.create(user=owner_user, board=board, role=BoardParticipant.Role.OWNER)  # noqa F841
    category = category_factory(user=owner_user, board=board)

    data = {"title": "test_goal_title", 
            "user": owner_user, 
            "category": category.id,
            "description": "some description",
            "due_date": datetime.now(tz=timezone.utc)}
    
    reader_data = {"title": "test_goal_title",   # noqa F841
                   "user": current_user,
                   "category": category.id,
                   "description": "some description",
                   "due_date": datetime.now(tz=timezone.utc)}

    create_request = current_client.post("/goals/goal/create", data=data)
    owner_request = owner_client.post("/goals/goal/create", data=data)
    
    pk = owner_request.data.get("id")
    response = current_client.get(f"/goals/goal/{pk}")
    
    update_data = {"title": "updated_title"}
    update_request = current_client.patch(f"/goals/goal/{pk}",
                                  content_type="application/json",
                                  data=update_data)
                                  
    delete_request = current_client.delete(f"/goals/goal/{pk}")
    
    assert create_request.status_code == 400
    
    assert response.status_code == 404
    
    assert update_request.status_code == 404
    
    assert delete_request.status_code == 404

  
@pytest.mark.django_db
def test_comment_crud_noone(client, get_login, board_factory, category_factory, goal_factory):
    current_client=Client()
    current_client.login(username=get_login[0], password=get_login[1])
    current_user = get_login[4]


    owner_client=Client()
    owner_client.login(username=get_login[2], password=get_login[3])
    owner_user = get_login[5]
    
    board = board_factory()
   
    board_participant = BoardParticipant.objects.create(user=owner_user, board=board, role=BoardParticipant.Role.OWNER)  # noqa F841
    category = category_factory(user=owner_user, board=board)
    goal = goal_factory(user=owner_user, category=category)
    
    data = {"text": "test_text_comment", 
            "user": current_user, 
            "goal": goal.id}
            
    owner_data = {"text": "test_text_comment",   # noqa F841
                  "user": owner_user,
                  "goal": goal.id}
    
    create_request = current_client.post("/goals/goal_comment/create", data=data)
    owner_request = owner_client.post("/goals/goal_comment/create", data=data)
    
    pk = owner_request.data.get("id")
    response = current_client.get(f"/goals/goal_comment/{pk}")
    
    update_data = {"text": "updated_text"}
    update_request = current_client.patch(f"/goals/goal_comment/{pk}",
                                  content_type="application/json",
                                  data=update_data)
                                  
    delete_request = client.delete(f"/goals/goal_comment/{pk}")
    
    assert create_request.status_code == 400
    
    assert response.status_code == 404
    
    assert update_request.status_code == 404
    
    assert delete_request.status_code == 401
