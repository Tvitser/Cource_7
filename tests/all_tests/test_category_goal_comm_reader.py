from goals.models import BoardParticipant

from django.test.client import Client

import pytest


@pytest.mark.django_db
def test_category_crud_reader(client, get_login, board_factory):
    current_client = Client()
    current_client.login(username=get_login[0], password=get_login[1])
    current_user = get_login[4]

    owner_client = Client()
    owner_client.login(username=get_login[2], password=get_login[3])
    owner_user = get_login[5]
    
    board = board_factory()
    board_participant = BoardParticipant.objects.create(user=current_user,  # noqa F841
                                                        board=board,
                                                        role=BoardParticipant.Role.READER)
    board_participant = BoardParticipant.objects.create(user=owner_user,  # noqa F841
                                                        board=board,
                                                        role=BoardParticipant.Role.OWNER)
    
    data = {"title": "test_category_title", "user": owner_user, "board": board.id}
    reader_data = {"title": "test_category_title", "user": current_user, "board": board.id}
    
    create_request = current_client.post("/goals/goal_category/create", data=reader_data, HTTP_AUTHORIZATION=token)
    owner_request = owner_client.post("/goals/goal_category/create", data=data, HTTP_AUTHORIZATION=owner_token)
    
    pk = owner_request.data.get("id")
    response = current_client.get(f"/goals/goal_category/{pk}", HTTP_AUTHORIZATION=token)
    
    update_data = {"title": "updated_title"}
    update_request = current_client.patch(f"/goals/goal_category/{pk}",
                                  content_type="application/json",
                                  data=update_data, 
                                  HTTP_AUTHORIZATION=token)
                                  
    delete_request = current_client.delete(f"/goals/goal_category/{pk}", HTTP_AUTHORIZATION=token)
    
    assert create_request.status_code == 400
    
    assert response.status_code == 200
    assert response.data.get("title") == data["title"]
    
    assert update_request.status_code == 403
    
    assert delete_request.status_code == 403

  
@pytest.mark.django_db
def test_comment_crud_reader(client, get_token, board_factory, category_factory, goal_factory):
    token = "Token " + get_token[1]
    current_user = get_token[0]
    
    owner_token = "Token " + get_token[3]
    owner_user = get_token[2]
    
    board = board_factory()
    board_participant = BoardParticipant.objects.create(user=current_user,  # noqa F841
                                                        board=board,
                                                        role=BoardParticipant.Role.READER)
    board_participant = BoardParticipant.objects.create(user=owner_user,  # noqa F841
                                                        board=board,
                                                        role=BoardParticipant.Role.OWNER)
    category = category_factory(user=owner_user, board=board)
    goal = goal_factory(user=owner_user, category=category)
    
    data = {"text": "test_text_comment", 
            "user": current_user, 
            "goal": goal.id}
            
    owner_data = {"text": "test_text_comment", # noqa F841
                  "user": owner_user,
                  "goal": goal.id}
    
    create_request = client.post("/goals/goal_comment/create", data=data, HTTP_AUTHORIZATION=token)
    owner_request = client.post("/goals/goal_comment/create", data=data, HTTP_AUTHORIZATION=owner_token)
    
    pk = owner_request.data.get("id")
    response = client.get(f"/goals/goal_comment/{pk}", HTTP_AUTHORIZATION=token)
    
    update_data = {"text": "updated_text"}
    update_request = client.patch(f"/goals/goal_comment/{pk}",
                                  content_type="application/json",
                                  data=update_data, 
                                  HTTP_AUTHORIZATION=token)
                                  
    delete_request = client.delete(f"/goals/goal_comment/{pk}", HTTP_AUTHORIZATION=token)
    
    assert create_request.status_code == 400
    
    assert response.status_code == 200
    assert response.data.get("text") == data["text"]
    
    assert update_request.status_code == 403
    
    assert delete_request.status_code == 403
