# 🌤️ Python 날씨 앱

OpenWeatherMap API를 사용하여 도시별 날씨 정보를 조회하는 간단한 Python 콘솔 애플리케이션입니다.

## ✨ 기능

- 도시 이름으로 실시간 날씨 정보 조회
- 온도, 습도, 기압, 풍속 정보 표시
- 한국어 날씨 상태 설명
- 사용자 친화적인 콘솔 인터페이스
- 에러 처리 및 예외 상황 대응

## 📋 필요 조건

- Python 3.7 이상
- OpenWeatherMap API 키 (무료)

## 🚀 설치 방법

### 1. 저장소 복제 또는 다운로드

```bash
git clone <repository-url>
cd python-weather-app
```

### 2. 가상환경 생성 (권장)

```bash
# Windows
python -m venv weather_env
weather_env\Scripts\activate

# macOS/Linux
python3 -m venv weather_env
source weather_env/bin/activate
```

### 3. 패키지 설치

```bash
pip install -r requirements.txt
```

## 🔑 API 키 설정

### 1. OpenWeatherMap API 키 발급

1. [OpenWeatherMap](https://openweathermap.org/) 웹사이트 방문
2. 무료 계정 생성
3. [API Keys](https://home.openweathermap.org/api_keys) 페이지에서 API 키 생성

### 2. API 키 설정 방법

#### 방법 1: 환경변수 설정

**Windows:**
```cmd
set OPENWEATHER_API_KEY=your_api_key_here
```

**macOS/Linux:**
```bash
export OPENWEATHER_API_KEY=your_api_key_here
```

#### 방법 2: .env 파일 사용

1. `.env.example` 파일을 `.env`로 복사:
   ```bash
   cp .env.example .env
   ```

2. `.env` 파일을 편집하고 API 키 입력:
   ```
   OPENWEATHER_API_KEY=your_actual_api_key_here
   ```

## 🎯 사용 방법

### 기본 실행

```bash
python weather_app.py
```

### 실행 예시

```
🌤️  날씨 앱에 오신 것을 환영합니다!
========================================

🏙️  도시 이름을 입력하세요 (종료: 'quit' 또는 'exit'): Seoul
🔍 Seoul의 날씨 정보를 조회 중...

🌍 도시: Seoul, KR
🌡️  온도: 15.2°C (체감 온도: 14.8°C)
☁️  날씨: 맑음
💧 습도: 65%
🌪️  기압: 1015 hPa
💨 풍속: 2.1 m/s

🏙️  도시 이름을 입력하세요 (종료: 'quit' 또는 'exit'): quit
👋 앱을 종료합니다. 안녕히 가세요!
```

### 지원되는 도시 이름 형식

- 영문 도시명: `Seoul`, `Tokyo`, `New York`
- 도시명, 국가 코드: `Seoul, KR`, `Paris, FR`
- 도시명, 주/도, 국가 코드: `Austin, TX, US`

## 🧪 테스트 실행

```bash
# 모든 테스트 실행
pytest

# 특정 테스트 파일 실행
pytest test_weather.py

# 상세한 출력과 함께 테스트 실행
pytest -v
```

## 📁 프로젝트 구조

```
python-weather-app/
├── weather_app.py      # 메인 애플리케이션
├── test_weather.py     # 유닛 테스트
├── requirements.txt    # 필요 패키지 목록
├── .env.example       # 환경변수 템플릿
└── README.md          # 프로젝트 문서
```

## 🛠️ 개발

### 코드 포맷팅

```bash
# 코드 포맷팅
black weather_app.py test_weather.py

# 코드 스타일 체크
flake8 weather_app.py test_weather.py
```

### 새로운 기능 추가

1. `WeatherApp` 클래스에 새로운 메서드 추가
2. 해당 메서드에 대한 테스트 작성
3. `README.md` 업데이트

## ❌ 문제 해결

### 일반적인 오류

1. **"API 키가 유효하지 않습니다"**
   - API 키가 올바르게 설정되었는지 확인
   - API 키가 활성화되었는지 확인 (발급 후 몇 분 소요)

2. **"도시를 찾을 수 없습니다"**
   - 도시 이름 철자 확인
   - 영문 도시명 사용 권장
   - 국가 코드와 함께 입력 (예: `Seoul, KR`)

3. **네트워크 연결 오류**
   - 인터넷 연결 상태 확인
   - 방화벽 설정 확인

### 디버깅

상세한 오류 정보가 필요한 경우:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 📜 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.

## 🤝 기여하기

1. Fork 프로젝트
2. Feature 브랜치 생성 (`git checkout -b feature/AmazingFeature`)
3. 변경사항 커밋 (`git commit -m 'Add some AmazingFeature'`)
4. 브랜치에 Push (`git push origin feature/AmazingFeature`)
5. Pull Request 생성

## 📞 지원

문제가 발생하거나 질문이 있으시면 이슈를 생성해 주세요.

---

**즐거운 날씨 확인 되세요! 🌈**