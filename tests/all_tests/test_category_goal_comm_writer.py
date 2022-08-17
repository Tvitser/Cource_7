from datetime import datetime

from django.utils import timezone

from goals.models import BoardParticipant

import pytest


@pytest.mark.django_db
def test_category_crud_owner(client, get_token, board_factory):
    token = "Token " + get_token[1]
    current_user = get_token[0]
    
    board = board_factory()
    board_participant = BoardParticipant.objects.create(user=current_user,   # noqa F841
                                                        board=board,
                                                        role=BoardParticipant.Role.WRITER)
    
    data = {"title": "test_category_title", "user": current_user, "board": board.id}
    
    create_request = client.post("/goals/goal_category/create", data=data, HTTP_AUTHORIZATION=token)
    
    pk = create_request.data.get("id")
    response = client.get(f"/goals/goal_category/{pk}", HTTP_AUTHORIZATION=token)
    
    update_data = {"title": "updated_title"}
    update_request = client.patch(f"/goals/goal_category/{pk}",
                                  content_type="application/json",
                                  data=update_data, 
                                  HTTP_AUTHORIZATION=token)
                                  
    delete_request = client.delete(f"/goals/goal_category/{pk}", HTTP_AUTHORIZATION=token)
    
    assert create_request.status_code == 201
    assert create_request.data.get("title") == data["title"]
    
    assert response.status_code == 200
    assert response.data.get("title") == data["title"]
    
    assert update_request.status_code == 200
    assert update_request.data.get("title") == update_data["title"]
    
    assert delete_request.status_code == 204

