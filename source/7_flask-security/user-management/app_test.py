# pylint: disable=redefined-outer-name
"""파이썬 테스트 라이브러리"""
import pytest
from app import app

admin_token = ''


# 픽스처 기능은 테스트 함수 앞뒤 처리를 담당
@pytest.fixture
def client():
    """app에서 테스트 프로그램 가져오기"""
    with app.test_client() as test_client:
        yield test_client


def test_login_admin(client):
    """admin 유저로 로그인"""
    response = client.post("/login",
                           json={
                            'username': 'admin',
                            'password': 'password'
                           })
    assert response.status == '200 OK'
    print(response.json.keys())
    assert 'access_token' in response.json.keys()
    global admin_token
    admin_token = response.json['access_token']


def test_users_create(client):
    """admin 유저를 사용해 새 유저 생성"""
    global access_token

    response = client.post("/users",
                           headers={
                            'Authorization': f'Bearer {admin_token}'
                           },
                           json={
                            'username': 'test_user',
                            'full_name': 'test_name'
                           })
    assert response.status == '200 OK'
    assert response.json == {'message': 'User created successfully'}


def test_users_get(client):
    """admin 유저를 사용해 새 유저 생성"""
    global access_token

    response = client.get("/users",
                           headers={
                            'Authorization': f'Bearer {admin_token}'
                           })
    assert response.status == '200 OK'
    assert response.json['users'] == [
        {'full_name': 'Bruce Wayne', 'id': 1, 'username': 'batman'},
        {'full_name': 'Ann Takamaki', 'id': 2, 'username': 'panther'},
        {'full_name': 'admin', 'id': 3, 'username': 'admin'},
        {'full_name': 'test_name', 'id': 4, 'username': 'test_user'}]


def test_whoami_test_user(client):
    """test_user 유저로 로그인"""
    response = client.post("/login",
                           json={
                            'username': 'test_user',
                            'password': 'password'
                           })
    assert response.status == '200 OK'
    assert 'access_token' in response.json.keys()
    test_user_jwt = response.json['access_token']
    
    """test_user 유저 확인"""
    response = client.get("/whoami",
                           headers={
                            'Authorization': f'Bearer {test_user_jwt}'
                           })
    assert response.status == '200 OK'
    assert response.json['username'] == 'test_user'