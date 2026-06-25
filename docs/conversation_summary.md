# Perth Data Analyst 포트폴리오 — 대화 정리

> 이 문서는 Cursor 대화 내용을 하나로 모은 요약본입니다.  
> 작성일: 2025-06-25

---

## 목차

1. [분석한 채용 공고 4곳](#1-분석한-채용-공고-4곳)
2. [네 공고가 원하는 기술 스택](#2-네-공고가-원하는-기술-스택)
3. [이력서를 살리는 포트폴리오 프로젝트](#3-이력서를-살리는-포트폴리오-프로젝트)
4. [프로젝트 A 상세 예시 — End-to-End Power BI 운영 대시보드](#4-프로젝트-a-상세-예시--end-to-end-power-bi-운영-대시보드)
5. [포트폴리오에서 “과정”을 증명하는 방법](#5-포트폴리오에서-과정을-증명하는-방법)
6. [실행 플랜 — Python ETL + PostgreSQL + Power BI](#6-실행-플랜--python-etl--postgresql--power-bi)
7. [단계별 학습 진행 방식](#7-단계별-학습-진행-방식)

---

## 1. 분석한 채용 공고 4곳

### 1.1 Crystalise — Graduate/Junior Data Analyst (Perth, Asset Management)

**한 줄 요약:** 퍼스 기반 자산관리 팀에서 엔지니어링·정비 데이터를 SQL·Power BI로 정제·분석하는 **주니어 실무형** 역할.

| 항목 | 내용 |
|------|------|
| 성격 | 데이터 정제, QA/QC, SQL update, 마이그레이션, Power BI |
| 경력 | 신입~3년 |
| 핵심 스킬 | SQL, Excel, Power BI, 데이터 클렌징 |
| 소프트 스킬 | 커뮤니케이션, 세부 정확도 |

**업무 비중 추정:** 데이터 분석 40% + ETL/운영 30% + BI 20% + 커뮤니케이션 10%

---

### 1.2 Curtin University — Data Analyst (Student Services, Insights & Performance)

**한 줄 요약:** Student Services에서 학생·운영 데이터로 **전략적 의사결정·인사이트**를 지원하는 분석가. **기간제(fixed-term).**

| 항목 | 내용 |
|------|------|
| 성격 | 인사이트, 평가, 예측, 거버넌스, Power BI |
| 차별점 | “why” 설명, 이해관계자 영향력, 스토리텔링 |
| Desirable | Higher education, Student One, Oracle |
| 특이 요건 | Working rights, National Police Clearance |

**Crystalise와 비교:** “데이터를 깨끗하게 만든다” → Curtin은 “데이터로 왜 그런지 설명하고 무엇을 할지 권고한다”

---

### 1.3 Communicare — Data Analyst (NFP, Cannington, Permanent)

**한 줄 요약:** NFP 조직에서 **거버넌스 + BI + 통계/모델링 + 프로그램 평가**를 하는 **정규직 올라운더**.

| 항목 | 내용 |
|------|------|
| 연봉 | SCHADS Level 4: $94,696–$97,138 + super |
| 복지 | Salary packaging, Wellbeing leave 5일 등 |
| 핵심 스킬 | Power BI, 클라우드 DB, data governance, 통계·모델링 |
| 특이 요건 | 운전면허, Department of Justice Clearance |

**주의:** JD가 넓음 (거버넌스 + BI + 데이터 사이언스 + 조직 문화). 면접에서 실제 업무 비중 확인 필요.

---

### 1.4 MEDLOG — BI/Data Analyst (IT Team)

**한 줄 요약:** IT 팀에서 **Power BI + SQL Server + SSIS/SSAS**로 리포트 개발·최적화·사용자 지원하는 **기술 중심** 역할.

| 항목 | 내용 |
|------|------|
| Essential | Power BI, Microsoft SQL, **SSIS**, **SSAS**, Dynamics/API |
| Desirable | Power BI cert, Python/R, Power Automate, TMS, L1 desktop support |
| 업무 | 개발 40% + 성능/UX 20% + SQL/연동 20% + 지원·교육 20% |

**네 공고 중 기술 요구 가장 높음.** Power BI만으로는 Essential 미달 가능성 큼.

---

### 1.5 네 공고 비교표

| 구분 | Crystalise | Curtin | Communicare | MEDLOG |
|------|------------|--------|-------------|--------|
| 소속 | Asset Mgmt | Student Services | NFP 전사 | IT Team |
| 고용 | 정규 추정 | Fixed-term | **Permanent** | 미공개 |
| 성격 | 주니어·정제 | 전략·인사이트 | 거버넌스·평가 | BI 개발·지원 |
| 핵심 스택 | SQL, Power BI | Power BI, 인사이트 | BI, 거버넌스, 통계 | Power BI, SQL, SSIS, SSAS |
| 연봉 | 미공개 | 미공개 | **공개** | 미공개 |

---

## 2. 네 공고가 원하는 기술 스택

### 2.1 공통 (거의 전부)

- **Power BI** — 리포트, 대시보드
- **SQL** — 추출, 변환, 분석
- **Excel** — 수식, 데이터 조작
- **관계형 DB** 개념
- **데이터 품질/정확성** (cleansing, QA/QC)
- **이해관계자 커뮤니케이션**

### 2.2 공고별 추가 기술

| 공고 | 추가로 강조되는 기술 |
|------|----------------------|
| **Crystalise** | SQL UPDATE, 마이그레이션, Excel, Power Query |
| **Curtin** | 인사이트·평가·예측, 거버넌스, Student One/Oracle |
| **Communicare** | 클라우드 DB, data architecture, 통계·모델링, 연구 방법론 |
| **MEDLOG** | SQL Server, SSIS, SSAS, Dynamics, API, BI 지원·최적화 |

### 2.3 준비 우선순위

**Tier 1 (네 곳 공통)**  
1. Power BI  
2. SQL  
3. Excel  
4. 데이터 품질 (cleansing, validation)

**Tier 2 (2~3곳)**  
5. 데이터 모델링  
6. Data governance / 지표 정의  
7. 이니셔티브·성과 평가  
8. 예측·수요 분석

**Tier 3 (특정 공고)**  
9. SSIS/SSAS → MEDLOG  
10. 클라우드 DB → Communicare  
11. 통계·모델링 → Communicare  
12. SQL UPDATE, 마이그레이션 → Crystalise

---

## 3. 이력서를 살리는 포트폴리오 프로젝트

### 3.1 가장 먼저 만들 프로젝트 (4곳 공통)

#### 프로젝트 A: End-to-End Power BI 운영 대시보드

더러운 운영 데이터 → SQL/Python 정제 → Power BI 대시보드 → 인사이트·권고

#### 프로젝트 B: SQL 데이터 정제 + 마이그레이션 시뮬레이션

staging → cleansed → production, validation rules, Before/After

#### 프로젝트 C: 인사이트 + 권고 리포트

트렌드 + 원인 + evidence-based recommendation (Curtin·Communicare용)

### 3.2 공고별 각인 프로젝트

| 공고 | 도메인 프로젝트 |
|------|-----------------|
| Crystalise | 산업 자산·정비 데이터 QA |
| Curtin | 학생 서비스·리텐션·피크 예측 |
| Communicare | NFP 프로그램 성과·거버넌스 |
| MEDLOG | Microsoft BI 스택 물류 대시보드 + ETL |

### 3.3 피해야 할 프로젝트

- 튜토리얼 그대로 복붙 (Titanic, Iris만)
- ML만 있고 BI/SQL 없음
- 대시보드만 예쁘고 데이터 품질·정의 없음
- “so what?” 없는 코드만 있는 repo

---

## 4. 프로젝트 A 상세 예시 — End-to-End Power BI 운영 대시보드

### 4.1 시나리오

**가상 회사:** Perth Logistics Co.  
**문제:** 배송·창고 데이터가 Excel/CSV에 분산, KPI 정의 불일치  
**해결:** 정제·검증 후 Power BI 운영 대시보드

### 4.2 데이터 테이블

| 테이블 | 행 수 | 설명 |
|--------|-------|------|
| shipments_raw | ~5,000 | 배송 (의도적 품질 이슈 포함) |
| inventory_raw | ~3,000 | 일별 재고 |
| customers_raw | ~200 | 고객 |
| warehouse_master | 3 | Perth, Fremantle, Kewdale |

### 4.3 의도적 데이터 품질 이슈

- `warehouse_id`: `WH01`, `Perth WH`, `perth wh` 혼재
- `delay_flag`: `Y`, `Yes`, `1`, `true` 혼재
- 중복 shipment_id ~50건
- null warehouse_id ~5%
- 잘못된 날짜 ~2%
- orphan customer_id
- 11~12월 shipment volume spike (피크 분석용)

### 4.4 파이프라인 단계

```
Raw CSV
  → Staging (원본 보존)
  → Cleansing (표준화, quarantine)
  → Validation (12 QA rules)
  → Mart (star schema)
  → Power BI (3 pages)
  → Analysis brief (인사이트 3 + 권고 3)
```

### 4.5 Power BI 대시보드 3페이지

1. **Executive Summary** — KPI cards, 월별 트렌드, 창고별 정시율  
2. **Operations Detail** — slicer, drill-through, heatmap  
3. **Data Quality Monitor** — QA rule pass/fail, quarantine trend

### 4.6 KPI 정의

- **On-Time Delivery %** = `actual_delivery <= scheduled_date + 24h`
- **Avg Delay Hours** = 지연 건의 평균 delay_hours
- **Warehouse Utilization %** = inventory / capacity
- **Shipments YoY %** = 전년 동월 대비

### 4.7 이력서 bullet 예시 (공고별 각도)

**공통:**  
> Built end-to-end logistics operations dashboard: Python ETL pipeline with 12 automated QA rules, PostgreSQL mart, and star-schema Power BI executive reporting.

**Crystalise:**  
> Resolved duplicate and inconsistent warehouse codes via Python cleansing pipeline with automated validation and quarantine workflow.

**Curtin:**  
> Identified peak-season demand drivers and recommended workforce planning actions through trend and cohort analysis.

**Communicare:**  
> Established consistent KPI definitions and curated datasets with data quality monitoring for stakeholder trust.

**MEDLOG:**  
> Designed interactive Power BI dashboards with Python data integration, drill-through, performance tuning, and operational support documentation.

---

## 5. 포트폴리오에서 “과정”을 증명하는 방법

### 5.1 문제 인식

끝난 대시보드 스크린샷만 올리면 채용 담당자는 **정제·분석 과정을 알 수 없다.**

### 5.2 해결 — 검증 가능한 산출물 패키지

```
Raw 데이터 (더러운 것)
+ 정제 스크립트 (Python/SQL)
+ Before/After 수치 (qa_report.json)
+ QA 규칙 12개
+ Cleansed CSV 샘플
+ Power BI 결과
+ 인사이트 brief
+ (선택) 3~5분 walkthrough 영상
```

### 5.3 방법별 설명

| 방법 | 내용 |
|------|------|
| Before/After 데이터 | `data/raw/` + `data/cleansed/` 나란히 공개 |
| SQL/Python 스크립트 | GitHub에 cleansing, validation 로직 |
| qa_report.json | rule별 before/after/passed |
| DQ 대시보드 페이지 | Power BI 안에 품질 모니터링 |
| 프로젝트 스토리 문서 | KPI 정의 선택 이유, quarantine 정책 |
| Loom 영상 | raw 보여주기 → 파이프라인 실행 → 대시보드 |

### 5.4 이력서 작성 팁

**약한 예:**  
> Built Power BI logistics dashboard.

**강한 예:**  
> Built end-to-end ops dashboard: Python cleansing (12 QA rules), star-schema model, executive KPIs.  
> Portfolio: github.com/you/perth-logistics-dashboard (raw/cleansed samples, scripts, walkthrough)

---

## 6. 실행 플랜 — Python ETL + PostgreSQL + Power BI

### 6.1 기술 스택 (사용자 선택)

- **도메인:** 물류·창고·배송 (Perth Logistics Co.)
- **언어:** Python (pandas, SQLAlchemy, psycopg2)
- **DB:** PostgreSQL
- **BI:** Power BI

### 6.2 레포 구조

```
perth-logistics-dashboard/
├── README.md
├── requirements.txt
├── .env.example
├── data/
│   ├── raw/
│   ├── cleansed/
│   ├── reports/qa_report.json
│   └── data_dictionary.md
├── scripts/
│   ├── config.py
│   ├── generate_raw_data.py
│   ├── cleanse.py
│   ├── validate.py
│   ├── load_to_postgres.py
│   ├── export_cleansed.py
│   ├── analyze.py
│   └── run_pipeline.py
├── sql/00_setup.sql
├── docs/
│   ├── kpi_definitions.md
│   └── analysis_brief.md
└── powerbi/
```

### 6.3 Python 파이프라인 흐름

```
generate_raw_data.py
  → cleanse.py
  → validate.py  →  qa_report.json
  → load_to_postgres.py  →  mart tables
  → export_cleansed.py
  → analyze.py  →  analysis_brief.md
```

**한 줄 실행:** `python scripts/run_pipeline.py`

### 6.4 12 QA Rules

1. Duplicate shipment_id  
2. Null warehouse_id  
3. Invalid warehouse_id  
4. Invalid date  
5. Orphan customer_id  
6. is_delayed consistency  
7. Negative delay_hours  
8. Future delivery dates  
9. Row count reconciliation  
10. Referential integrity  
11. KPI sanity (on-time % 0–100)  
12. Quarantine review  

### 6.5 3주 일정

| 주차 | 작업 |
|------|------|
| 1주차 | Raw 생성, cleanse, validate |
| 2주차 | PostgreSQL 적재, Power BI Page 1~2 |
| 3주차 | DQ page, brief, README, GitHub |

### 6.6 백업

이전에 자동으로 진행된 전체 구현은 다음 경로에 백업됨:  
`~/perth-logistics-dashboard-backup-20250625/`

---

## 7. 단계별 학습 진행 방식

사용자 요청에 따라 **처음부터 한 단계씩** 진행하기로 함.

### 7.1 현재 상태 (Step 1만 완료)

새 프로젝트 `~/perth-logistics-dashboard/`:

- [x] **Step 1** — 폴더 구조, requirements.txt, .env.example, .gitignore, README
- [ ] Step 2 — Raw 더미 데이터 (`generate_raw_data.py`)
- [ ] Step 3 — 정제 (`cleanse.py`)
- [ ] Step 4 — QA 검증 (`validate.py`)
- [ ] Step 5 — Cleansed export
- [ ] Step 6 — PostgreSQL 적재
- [ ] Step 7 — 분석 brief
- [ ] Step 8 — Power BI
- [ ] Step 9 — README·GitHub

### 7.2 Step 1 — 직접 실행할 명령

```bash
cd ~/perth-logistics-dashboard
ls -R
python3 -m pip install --user -r requirements.txt
python3 -c "import pandas; print('pandas OK', pandas.__version__)"
```

### 7.3 진행 원칙

- 한 번에 **하나의 Step**만 진행
- 각 Step 완료 후 채팅에 `Step N 완료` 또는 `Step N+1 가자` 요청
- Agent가 여러 단계를 한꺼번에 실행하지 않음

---

## 부록: 공고별 지원 전략 한 줄

| 원하는 것 | 추천 공고 |
|-----------|-----------|
| 신입·SQL·산업 데이터 실무 | Crystalise |
| 스토리텔링·교육·인사이트 | Curtin |
| 정규직·NFP·거버넌스·연봉 명시 | Communicare |
| Power BI + SQL + SSIS 개발 | MEDLOG |

---

*이 문서는 학습·지원 준비용 참고 자료입니다. 공고 내용은 분석 시점 기준이며, 지원 전 공식 채용 페이지에서 최신 정보를 확인하세요.*
