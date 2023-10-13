# pylint: disable=redefined-outer-name
"""파이썬 테스트 라이브러리"""
import pytest
from app import app

NS = 'ns_cars'


# 픽스처 기능은 테스트 함수 앞뒤 처리를 담당
@pytest.fixture
def client():
    """app에서 테스트 프로그램 가져오기"""
    with app.test_client() as test_client:
        yield test_client


def test_get_root(client):
    """전체 내용 조회 테스트"""
    response = client.get(f"/{NS}/cars")
    assert response.status == '200 OK'
    assert response.json == {
            'number_of_vehicles': 0,
            'car_info': {}
    }


def test_create_brand(client):
    """bentz 생성 테스트"""
    # 브랜드 생성
    response = client.post(f"/{NS}/cars/bentz", data={})
    assert response.status == '201 CREATED'

    # 생성된 정보 조회
    response = client.get(f"/{NS}/cars")
    assert response.status == '200 OK'
    assert response.json == {'car_info': {'bentz': {}},
                             'number_of_vehicles': 0}


def test_create_model(client):
    """모델 생성 테스트"""
    # 모델 생성
    model = {
        "name": "e-class",
        "price": 1000000,
        "fuel_type": "gasoline",
        "fuel_efficiency": "9.1~13.2km/l",
        "engine_power": "367hp",
        "engine_cylinder": "I6"
    }

    response = client.post(f"/{NS}/cars/bentz/0",
                           json=model)
    assert response.status == '201 CREATED'

    # 생성된 정보 조회
    response = client.get(f"/{NS}/cars")
    assert response.status == '200 OK'
    assert response.json == {'car_info': {'bentz': {'0': model}},
                             'number_of_vehicles': 1}
