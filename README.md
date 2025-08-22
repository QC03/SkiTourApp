
# Step 1 — 프로젝트 골격 & 실행 확인

## 준비
1) Python 3.10+ 설치
2) (권장) 가상환경 생성
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # macOS/Linux
```
3) 의존성 설치
```bash
pip install -r requirements.txt
```

## 실행
```bash
python main.py
```

### 이 단계에서 되는 것
- PyQt6 기반 빈 앱이 실행되며, 상단 탭(예약/강사/스케줄/출력/설정)이 보입니다.
- 이후 단계에서 각 탭의 실제 기능을 채워넣습니다.
