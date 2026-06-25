# Perth Logistics Dashboard — 학습용 포트폴리오

Perth 물류 회사 시나리오로 **Python → PostgreSQL → Power BI** 파이프라인을 단계별로 만듭니다.

## 진행 체크리스트

- [x] **Step 1** — 프로젝트 폴더·설정 파일 만들기 (지금 여기)
- [ ] **Step 2** — Raw 더미 데이터 생성 (`generate_raw_data.py`)
- [ ] **Step 3** — 데이터 정제 (`cleanse.py`)
- [ ] **Step 4** — QA 검증 12 rules (`validate.py`)
- [ ] **Step 5** — Cleansed CSV export (`export_cleansed.py`)
- [ ] **Step 6** — PostgreSQL 적재 (`load_to_postgres.py`)
- [ ] **Step 7** — 분석 brief (`analyze.py`)
- [ ] **Step 8** — Power BI 대시보드
- [ ] **Step 9** — README·GitHub 공개

> 한 번에 하나씩만 진행합니다. Step 2는 준비되면 요청하세요.

## Step 1 — 지금 할 일

### 1) 폴더 확인

```bash
cd ~/perth-logistics-dashboard
ls -R
```

`data/raw/`, `scripts/`, `docs/` 등이 보이면 OK.

### 2) Python 패키지 설치

```bash
python3 -m pip install --user -r requirements.txt
```

에러 없이 끝나면 OK.

### 3) 완료 확인

```bash
python3 -c "import pandas; print('pandas OK', pandas.__version__)"
```

---

**Step 1이 끝나면** 채팅에 `Step 1 완료` 또는 `Step 2 가자`라고 보내주세요.
