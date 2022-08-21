def test_no_auth_goal(client):
    response = client.get("/goals/goal/list")
    
    assert response.status_code == 401


def test_no_auth_board(client):
    response = client.get("/goals/board/list")
    
    assert response.status_code == 401


def test_no_auth_category(client):
    response = client.get("/goals/goal_category/list")
    
    assert response.status_code == 401
    

def test_auth_goal_list(client, get_login):
    client.login(username=get_login[0], password=get_login[1])
    response = client.get("/goals/goal/list")
    
    assert response.status_code == 200


def test_auth_goal_board(client, get_login):
    client.login(username=get_login[0], password=get_login[1])
    response = client.get("/goals/board/list")

    assert response.status_code == 200


def test_auth_goal_category(client, get_login):
    client.login(username=get_login[0], password=get_login[1])
    response = client.get("/goals/goal_category/list")

    assert response.status_code == 200


def test_api_swagger(client):
    response = client.get('/schema/swagger-ui/')
    
    assert response.status_code == 200
