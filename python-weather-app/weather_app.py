#!/usr/bin/env python3
"""
날씨 앱 - OpenWeatherMap API를 사용하여 도시별 날씨 정보를 가져옵니다.
"""

import requests
import os
from typing import Dict, Any, Optional
import json


class WeatherApp:
    """OpenWeatherMap API를 사용한 날씨 정보 조회 클래스"""
    
    def __init__(self, api_key: str):
        """
        WeatherApp 초기화
        
        Args:
            api_key (str): OpenWeatherMap API 키
        """
        self.api_key = api_key
        self.base_url = "http://api.openweathermap.org/data/2.5/weather"
    
    def get_weather(self, city: str) -> Optional[Dict[str, Any]]:
        """
        지정된 도시의 날씨 정보를 가져옵니다.
        
        Args:
            city (str): 도시 이름
            
        Returns:
            Dict[str, Any]: 날씨 정보 딕셔너리 또는 None (오류 시)
        """
        try:
            # API 요청 매개변수 설정
            params = {
                'q': city,
                'appid': self.api_key,
                'units': 'metric',  # 섭씨 온도 사용
                'lang': 'kr'        # 한국어 설명
            }
            
            # API 요청 보내기
            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()  # HTTP 오류 발생 시 예외 발생
            
            return response.json()
            
        except requests.exceptions.Timeout:
            print("❌ 요청 시간이 초과되었습니다.")
            return None
        except requests.exceptions.ConnectionError:
            print("❌ 네트워크 연결 오류가 발생했습니다.")
            return None
        except requests.exceptions.HTTPError as e:
            if response.status_code == 404:
                print(f"❌ 도시를 찾을 수 없습니다: {city}")
            elif response.status_code == 401:
                print("❌ API 키가 유효하지 않습니다.")
            else:
                print(f"❌ HTTP 오류 발생: {e}")
            return None
        except requests.exceptions.RequestException as e:
            print(f"❌ 요청 오류 발생: {e}")
            return None
        except json.JSONDecodeError:
            print("❌ 응답 데이터를 파싱할 수 없습니다.")
            return None

    def format_weather_info(self, weather_data: Dict[str, Any]) -> str:
        """
        날씨 데이터를 보기 좋게 포맷팅합니다.
        
        Args:
            weather_data (Dict[str, Any]): API에서 받은 날씨 데이터
            
        Returns:
            str: 포맷팅된 날씨 정보
        """
        try:
            # 주요 정보 추출
            city = weather_data['name']
            country = weather_data['sys']['country']
            temp = weather_data['main']['temp']
            feels_like = weather_data['main']['feels_like']
            humidity = weather_data['main']['humidity']
            pressure = weather_data['main']['pressure']
            description = weather_data['weather'][0]['description']
            wind_speed = weather_data['wind']['speed']
            
            # 포맷팅된 문자열 생성
            weather_info = f"""
🌍 도시: {city}, {country}
🌡️  온도: {temp}°C (체감 온도: {feels_like}°C)
☁️  날씨: {description}
💧 습도: {humidity}%
🌪️  기압: {pressure} hPa
💨 풍속: {wind_speed} m/s
"""
            return weather_info
            
        except KeyError as e:
            return f"❌ 날씨 정보를 파싱하는 중 오류 발생: {e}"

    def run(self):
        """메인 실행 함수"""
        print("🌤️  날씨 앱에 오신 것을 환영합니다!")
        print("=" * 40)
        
        while True:
            try:
                # 사용자로부터 도시 이름 입력받기
                city = input("\n🏙️  도시 이름을 입력하세요 (종료: 'quit' 또는 'exit'): ").strip()
                
                if city.lower() in ['quit', 'exit', '종료']:
                    print("👋 앱을 종료합니다. 안녕히 가세요!")
                    break
                
                if not city:
                    print("❌ 도시 이름을 입력해주세요.")
                    continue
                
                print(f"🔍 {city}의 날씨 정보를 조회 중...")
                
                # 날씨 정보 가져오기
                weather_data = self.get_weather(city)
                
                if weather_data:
                    # 날씨 정보 출력
                    print(self.format_weather_info(weather_data))
                else:
                    print("날씨 정보를 가져올 수 없습니다.")
                    
            except KeyboardInterrupt:
                print("\n\n👋 앱을 종료합니다. 안녕히 가세요!")
                break
            except Exception as e:
                print(f"❌ 예상치 못한 오류가 발생했습니다: {e}")


def load_api_key() -> Optional[str]:
    """
    환경변수나 .env 파일에서 API 키를 로드합니다.
    
    Returns:
        str: API 키 또는 None
    """
    # 환경변수에서 먼저 확인
    api_key = os.getenv('OPENWEATHER_API_KEY')
    
    if not api_key:
        # .env 파일에서 로드 시도
        try:
            from dotenv import load_dotenv
            load_dotenv()
            api_key = os.getenv('OPENWEATHER_API_KEY')
        except ImportError:
            pass  # python-dotenv가 설치되지 않은 경우
    
    return api_key


def main():
    """메인 실행 함수"""
    # API 키 로드
    api_key = load_api_key()
    
    if not api_key:
        print("❌ OpenWeatherMap API 키를 찾을 수 없습니다.")
        print("다음 중 하나의 방법으로 API 키를 설정해주세요:")
        print("1. 환경변수: export OPENWEATHER_API_KEY='your_api_key'")
        print("2. .env 파일에 OPENWEATHER_API_KEY=your_api_key 추가")
        print("\n🔗 API 키는 https://openweathermap.org/api 에서 무료로 발급받을 수 있습니다.")
        return
    
    # 날씨 앱 실행
    app = WeatherApp(api_key)
    app.run()


if __name__ == "__main__":
    main()