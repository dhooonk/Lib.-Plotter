# TFT Curve Analyzer (v1.1)

A Python-based GUI tool for analyzing and visualizing SmartSpice TFT simulation data from `.xlsx`, `.xls` and `.csv` files.

## 🚀 Overview
이 프로그램은 SmartSpice로 시뮬레이션한 TFT(박막 트랜지스터) 데이터 또는 측정 데이터 파일을 읽어 다음 두 가지 특성 곡선을 자동으로 시각화하고 분석합니다:
1. **Transfer Curve (Vgs-Id 특성, Vd 파라미터별 도식)**
2. **Output Curve (Vds-Id 특성, Vg 파라미터별 도식)**

## ✨ 주요 기능 (Features)
- **손쉬운 GUI 인터페이스:** 다크 테마 기반의 Tkinter 앱으로 초심자도 직관적으로 사용.
- **강력한 데이터 탐지 (Auto Detection):** 파일 내 헤더 행 위치와 종류와 무관하게 숫자 데이터 배열을 즉시 감지 및 분리.
- **포맷 자유도 향상:** Excel, CSV 등 어떤 형식에서 가져온 값이든 무관하게 파싱 지원.
- **노이즈 및 이상점 자동 마스킹:** 개수가 너무 적은 파라미터(예: 시뮬레이션 에러 발생치)를 자동 검열 후 그래프에서 제외.
- **Reference 플로팅 및 $R^2$ 신뢰도 오버레이:** 기준 데이터 이외에 `비교 데이터`를 추가 업로드하여, 동일 파라미터 곡선 간 일치도 및 오차($R^2$) 판별을 지원.
- **차트 커스터마이징 및 Excel 보고서 변환:** 축 제어(Log Scale 토글) 및 커스텀 한계 범위 지정(X, Y limits) 가능, 또한 `openpyxl` 및 `Agg` 백엔드를 활용하여 고화질 보고서 엑셀 파일을 도출.

## 🛠⚙️ 설치 방법 (Installation)
시스템에 Python 3.8 이상이 설치되어 있는지 확인 후, 가상환경을 구축하고 의존성을 설치하십시오.

```bash
# 가상 환경 생성 및 진입 (권장)
python -m venv venv
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate     # Windows 환경

# 모든 필수 패키지 설치
pip install -r requirements.txt
```

#### 📦 요구 패키지 정보
- `pandas` (데이터 테이블 관리)
- `numpy`
- `openpyxl` (결과 및 차트 엑셀 기록)
- `matplotlib` (GUI 차트 및 그래픽 추출 엔진)
- `scipy` (선형 보간 및 라인 추적, Reference 오버레이용)
- `scikit-learn` ($R^2$ 점수 판별 통계 라이브러리)

## 🖥 사용 방법 (Usage)
```bash
python main.py
```
- 좌측 [입력 파일 카드]에서 분석할 메인 데이터(과 비교 데이터)를 선택합니다.
- 축 범위 제어란에서 원하는 최소, 최대 뷰포트를 입력할 수 있습니다.
- [분석 실행]을 눌러 데이터를 플로팅하고, 이상이 없다면 [엑셀로 저장] 후 앱을 종료합니다. 상세한 규칙과 설명은 동봉된 **`사용설명서.md`**를 참조하십시오.
