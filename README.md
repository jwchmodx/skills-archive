# skills-archive

자주 쓰는 개발 스킬과 템플릿 모음

## 구조

```
.cursor/           # Cursor AI 설정
├── rules/         # AI 규칙 (.mdc)
└── prompts/       # 자주 쓰는 프롬프트

.skill/            # 개발 스킬/패턴
├── python/        # Python 패턴
├── typescript/    # TypeScript 패턴
└── infra/         # Docker, CI/CD 등
```

## 사용법

새 프로젝트에 필요한 스킬 복사:
```bash
cp -r ~/.../skills-archive/.cursor ./
cp -r ~/.../skills-archive/.skill/python ./
```
