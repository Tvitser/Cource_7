from goals.models import BoardParticipant

import pytest


@pytest.mark.django_db
def test_board_create(client, get_login, board_factory):
    client.login(username=get_login[0], password=get_login[0])
    data = {'title': 'test_title'}

    request = client.post('/goals/board/create', data=data, format='json')
    
    pk = request.data.get('id')
    response = client.get(f"/goals/board/{pk}", format='json')
    
    assert request.status_code == 201
    assert request.data.get('title') == data['title']
    
    assert response.status_code == 200
    assert response.data.get('title') == data['title']
  

@pytest.mark.django_db
def test_board_list(client, get_login, board_factory):
    client.login(username=get_login[0], password=get_login[1])
    data_len = 10
    boards = board_factory.create_batch(size=data_len, title='test_title')
    
    for board in boards:
        board_participant = BoardParticipant.objects.create(user=get_login[4], board=board)  # noqa F841
        
    response = client.get('/goals/board/list', format='json')
    
    assert response.status_code == 200
    assert len(response.data) == data_len
    
    for item in response.data:
        assert item.get('title') == 'test_title'
