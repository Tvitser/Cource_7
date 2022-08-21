from goals.models import BoardParticipant

import pytest

from django.test.client import Client

@pytest.mark.django_db
def test_category_crud_owner(client, get_login, board_factory):
    current_client=Client()
    current_client.login(username=get_login[0], password=get_login[1])
    current_user = get_login[4]

    board = board_factory()
    board_participant = BoardParticipant.objects.create(user=current_user, board=board, role=BoardParticipant.Role.OWNER) # noqa F841
    
    data = {"title": "test_category_title", "user": current_user, "board": board.id}
    
    create_request = current_client.post("/goals/goal_category/create", data=data, HTTP_AUTHORIZATION=token)
    
    pk = create_request.data.get("id")
    response = current_client.get(f"/goals/goal_category/{pk}", HTTP_AUTHORIZATION=token)
    
    update_data = {"title": "updated_title"}
    update_request = current_client.patch(f"/goals/goal_category/{pk}",
                                  content_type="application/json",
                                  data=update_data,
                                  HTTP_AUTHORIZATION=token)
                                  
    delete_request = current_client.delete(f"/goals/goal_category/{pk}", HTTP_AUTHORIZATION=token)
    
    assert create_request.status_code == 201
    assert create_request.data.get("title") == data["title"]
    
    assert response.status_code == 200
    assert response.data.get("title") == data["title"]
    
    assert update_request.status_code == 200
    assert update_request.data.get("title") == update_data["title"]
    
    assert delete_request.status_code == 204

@pytest.mark.django_db
def test_comment_crud_owner(client, get_login, board_factory, category_factory, goal_factory):
    current_client = Client()
    current_client.login(username=get_login[0], password=get_login[1])
    current_user = get_login[4]
    
    board = board_factory()
    board_participant = BoardParticipant.objects.create(user=current_user, board=board, role=BoardParticipant.Role.OWNER)  # noqa F841
    category = category_factory(user=current_user, board=board)
    goal = goal_factory(user=current_user, category=category)
    
    data = {"text": "test_text_comment", 
            "user": current_user, 
            "goal": goal.id}
    
    create_request = current_client.post("/goals/goal_comment/create", data=data)
    
    pk = create_request.data.get("id")
    response = current_client.get(f"/goals/goal_comment/{pk}")
    
    update_data = {"text": "updated_text"}
    update_request = current_client.patch(f"/goals/goal_comment/{pk}",
                                  content_type="application/json",
                                  data=update_data, 
                                  HTTP_AUTHORIZATION=token)
                                  
    delete_request = current_client.delete(f"/goals/goal_comment/{pk}")
    
    assert create_request.status_code == 201
    assert create_request.data.get("text") == data["text"]
    
    assert response.status_code == 200
    assert response.data.get("text") == data["text"]
    
    assert update_request.status_code == 200
    assert update_request.data.get("text") == update_data["text"]
    
    assert delete_request.status_code == 204
