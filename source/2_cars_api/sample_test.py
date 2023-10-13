"""pytest의 기본 사용 방법 샘플 코드
pytest나 pytest <파일명> 을 사용하여 동작시킴
test로 시작하는 함수를 테스트함"""


def test_func1():
    '''데이터가 같으므로 passed가 나타남'''
    assert 0 == 0


def test_func2():
    '''데이터가 다르므로 failed가 나타남'''
    assert 0 == 1
