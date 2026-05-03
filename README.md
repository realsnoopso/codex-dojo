# 🥋 Codex Dojo — 실습 레포지토리

Codex CLI 셀프러닝 스터디그룹 실습용 레포입니다.

## 구조

```
codex-dojo/
├── README.md          # 이 파일
├── app.py             # FastAPI 서버 (버그 내장)
├── utils.py           # 유틸리티 함수들 (리팩토링 대상)
├── tests/             # 테스트 (빠진 테스트 다수)
│   └── test_app.py
└── .codex/
    └── rules.md       # Codex 행동 규칙 (레벨 4)
```

## 레벨별 사용법

각 레벨의 과제를 `codex exec` 명령어로 수행하세요.
모든 과제는 `--dangerously-bypass-approvals-and-sandbox` (yolo) 모드로 실행합니다.
