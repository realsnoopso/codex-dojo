# Codex Dojo Rules

## 행동 규칙
- 모든 Python 코드는 타입 힌트를 포함할 것
- 함수에는 docstring을 작성할 것 (Google style)
- 에러 처리는 항상 명시적으로 할 것 (try/except 없이 방치하지 말 것)
- print() 디버깅 대신 logging 모듈 사용할 것
- 커밋 메시지는 Conventional Commits 형식 (feat:, fix:, refactor: 등)

## 코딩 스타일
- Black 포맷터 준수
- 라인 길이 최대 100자
- Pylint 8.0 이상 통과

## 테스트
- pytest 사용
- 모든 public 함수에 단위 테스트 작성
- 최소 커버리지 80%
