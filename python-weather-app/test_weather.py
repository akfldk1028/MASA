#!/usr/bin/env python3
"""
날씨 앱 유닛 테스트
"""

import pytest
import json
from unittest.mock import Mock, patch, MagicMock
import requests
from weather_app import WeatherApp, load_api_key


class TestWeatherApp:
    """WeatherApp 클래스에 대한 테스트"""
    
    def setup_method(self):
        """각 테스트 메서드 실행 전 설정"""
        self.api_key = "test_api_key"
        self.app = WeatherApp(self.api_key)
        
        # 샘플 날씨 데이터
        self.sample_weather_data = {
            "name": "Seoul",
            "sys": {"country": "KR"},
            "main": {
                "temp": 15.2,
                "feels_like": 14.8,
                "humidity": 65,
                "pressure": 1015
            },
            "weather": [{"description": "맑음"}],
            "wind": {"speed": 2.1}
        }
    
    def test_weather_app_initialization(self):
        """WeatherApp 초기화 테스트"""
        app = WeatherApp("test_key")
        assert app.api_key == "test_key"
        assert app.base_url == "http://api.openweathermap.org/data/2.5/weather"
    
    @patch('weather_app.requests.get')
    def test_get_weather_success(self, mock_get):
        """성공적인 날씨 정보 조회 테스트"""
        # Mock 응답 설정
        mock_response = Mock()
        mock_response.json.return_value = self.sample_weather_data
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        
        # 날씨 정보 조회
        result = self.app.get_weather("Seoul")
        
        # 검증
        assert result == self.sample_weather_data
        mock_get.assert_called_once()
        
        # API 호출 매개변수 검증
        call_args = mock_get.call_args
        assert call_args[0][0] == self.app.base_url
        params = call_args[1]['params']
        assert params['q'] == "Seoul"
        assert params['appid'] == self.api_key
        assert params['units'] == 'metric'
        assert params['lang'] == 'kr'
    
    @patch('weather_app.requests.get')
    def test_get_weather_city_not_found(self, mock_get):
        """도시를 찾을 수 없는 경우 테스트"""
        # Mock 404 응답 설정
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError()
        mock_get.return_value = mock_response
        
        # 날씨 정보 조회
        with patch('builtins.print') as mock_print:
            result = self.app.get_weather("NonExistentCity")
        
        # 검증
        assert result is None
        mock_print.assert_called_with("❌ 도시를 찾을 수 없습니다: NonExistentCity")
    
    @patch('weather_app.requests.get')
    def test_get_weather_invalid_api_key(self, mock_get):
        """잘못된 API 키 테스트"""
        # Mock 401 응답 설정
        mock_response = Mock()
        mock_response.status_code = 401
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError()
        mock_get.return_value = mock_response
        
        # 날씨 정보 조회
        with patch('builtins.print') as mock_print:
            result = self.app.get_weather("Seoul")
        
        # 검증
        assert result is None
        mock_print.assert_called_with("❌ API 키가 유효하지 않습니다.")
    
    @patch('weather_app.requests.get')
    def test_get_weather_timeout(self, mock_get):
        """요청 시간 초과 테스트"""
        # Mock 시간 초과 예외 설정
        mock_get.side_effect = requests.exceptions.Timeout()
        
        # 날씨 정보 조회
        with patch('builtins.print') as mock_print:
            result = self.app.get_weather("Seoul")
        
        # 검증
        assert result is None
        mock_print.assert_called_with("❌ 요청 시간이 초과되었습니다.")
    
    @patch('weather_app.requests.get')
    def test_get_weather_connection_error(self, mock_get):
        """네트워크 연결 오류 테스트"""
        # Mock 연결 오류 예외 설정
        mock_get.side_effect = requests.exceptions.ConnectionError()
        
        # 날씨 정보 조회
        with patch('builtins.print') as mock_print:
            result = self.app.get_weather("Seoul")
        
        # 검증
        assert result is None
        mock_print.assert_called_with("❌ 네트워크 연결 오류가 발생했습니다.")
    
    @patch('weather_app.requests.get')
    def test_get_weather_json_decode_error(self, mock_get):
        """JSON 파싱 오류 테스트"""
        # Mock 응답 설정 (잘못된 JSON)
        mock_response = Mock()
        mock_response.json.side_effect = json.JSONDecodeError("test", "test", 0)
        mock_response.status_code = 200
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        # 날씨 정보 조회
        with patch('builtins.print') as mock_print:
            result = self.app.get_weather("Seoul")
        
        # 검증
        assert result is None
        mock_print.assert_called_with("❌ 응답 데이터를 파싱할 수 없습니다.")
    
    def test_format_weather_info_success(self):
        """날씨 정보 포맷팅 성공 테스트"""
        formatted_info = self.app.format_weather_info(self.sample_weather_data)
        
        # 검증 - 주요 정보들이 포함되어 있는지 확인
        assert "Seoul" in formatted_info
        assert "KR" in formatted_info
        assert "15.2°C" in formatted_info
        assert "14.8°C" in formatted_info
        assert "65%" in formatted_info
        assert "1015" in formatted_info
        assert "맑음" in formatted_info
        assert "2.1" in formatted_info
    
    def test_format_weather_info_missing_key(self):
        """날씨 정보에 필수 키가 없는 경우 테스트"""
        incomplete_data = {"name": "Seoul"}  # 필수 정보 누락
        
        formatted_info = self.app.format_weather_info(incomplete_data)
        
        # 검증
        assert "오류 발생" in formatted_info
    
    @patch('weather_app.input')
    @patch('weather_app.print')
    @patch.object(WeatherApp, 'get_weather')
    @patch.object(WeatherApp, 'format_weather_info')
    def test_run_successful_query(self, mock_format, mock_get_weather, mock_print, mock_input):
        """성공적인 날씨 조회 실행 테스트"""
        # Mock 입력 설정 (Seoul 입력 후 quit)
        mock_input.side_effect = ["Seoul", "quit"]
        
        # Mock 메서드 반환값 설정
        mock_get_weather.return_value = self.sample_weather_data
        mock_format.return_value = "Formatted weather info"
        
        # 앱 실행
        self.app.run()
        
        # 검증
        mock_get_weather.assert_called_with("Seoul")
        mock_format.assert_called_with(self.sample_weather_data)
    
    @patch('weather_app.input')
    @patch('weather_app.print')
    @patch.object(WeatherApp, 'get_weather')
    def test_run_failed_query(self, mock_get_weather, mock_print, mock_input):
        """실패한 날씨 조회 실행 테스트"""
        # Mock 입력 설정
        mock_input.side_effect = ["InvalidCity", "exit"]
        
        # Mock 메서드 반환값 설정 (실패)
        mock_get_weather.return_value = None
        
        # 앱 실행
        self.app.run()
        
        # 검증
        mock_get_weather.assert_called_with("InvalidCity")
    
    @patch('weather_app.input')
    @patch('weather_app.print')
    def test_run_empty_input(self, mock_print, mock_input):
        """빈 입력 테스트"""
        # Mock 입력 설정 (빈 문자열 입력 후 quit)
        mock_input.side_effect = ["", "quit"]
        
        # 앱 실행
        self.app.run()
        
        # 빈 입력에 대한 오류 메시지 확인
        mock_print.assert_any_call("❌ 도시 이름을 입력해주세요.")
    
    @patch('weather_app.input')
    @patch('weather_app.print')
    def test_run_keyboard_interrupt(self, mock_print, mock_input):
        """키보드 인터럽트(Ctrl+C) 테스트"""
        # Mock 키보드 인터럽트 설정
        mock_input.side_effect = KeyboardInterrupt()
        
        # 앱 실행
        self.app.run()
        
        # 종료 메시지 확인
        mock_print.assert_any_call("\n\n👋 앱을 종료합니다. 안녕히 가세요!")


class TestLoadApiKey:
    """load_api_key 함수 테스트"""
    
    @patch.dict('os.environ', {'OPENWEATHER_API_KEY': 'env_api_key'})
    def test_load_api_key_from_environment(self):
        """환경변수에서 API 키 로드 테스트"""
        api_key = load_api_key()
        assert api_key == 'env_api_key'
    
    @patch.dict('os.environ', {}, clear=True)
    @patch('weather_app.load_dotenv')
    @patch.dict('os.environ', {'OPENWEATHER_API_KEY': 'dotenv_api_key'})
    def test_load_api_key_from_dotenv(self, mock_load_dotenv):
        """dotenv 파일에서 API 키 로드 테스트"""
        # 환경변수를 비운 상태에서 시작
        with patch.dict('os.environ', {}, clear=True):
            # dotenv 로드 후 환경변수에 키가 설정되도록 시뮬레이션
            def mock_load_dotenv_func():
                os.environ['OPENWEATHER_API_KEY'] = 'dotenv_api_key'
            
            mock_load_dotenv.side_effect = mock_load_dotenv_func
            
            with patch('os.getenv') as mock_getenv:
                # 첫 번째 호출: None (dotenv 로드 전)
                # 두 번째 호출: 'dotenv_api_key' (dotenv 로드 후)
                mock_getenv.side_effect = [None, 'dotenv_api_key']
                
                api_key = load_api_key()
                assert api_key == 'dotenv_api_key'
    
    @patch.dict('os.environ', {}, clear=True)
    @patch('weather_app.load_dotenv', side_effect=ImportError())
    def test_load_api_key_no_dotenv_module(self, mock_load_dotenv):
        """python-dotenv 모듈이 없는 경우 테스트"""
        api_key = load_api_key()
        assert api_key is None
    
    @patch.dict('os.environ', {}, clear=True)
    def test_load_api_key_not_found(self):
        """API 키를 찾을 수 없는 경우 테스트"""
        with patch('weather_app.load_dotenv', side_effect=ImportError()):
            api_key = load_api_key()
            assert api_key is None


class TestMain:
    """main 함수 테스트"""
    
    @patch('weather_app.load_api_key')
    @patch('weather_app.WeatherApp')
    def test_main_with_api_key(self, mock_weather_app_class, mock_load_api_key):
        """API 키가 있는 경우 main 함수 테스트"""
        # Mock 설정
        mock_load_api_key.return_value = "test_api_key"
        mock_app_instance = Mock()
        mock_weather_app_class.return_value = mock_app_instance
        
        # main 함수 실행
        from weather_app import main
        main()
        
        # 검증
        mock_weather_app_class.assert_called_once_with("test_api_key")
        mock_app_instance.run.assert_called_once()
    
    @patch('weather_app.load_api_key')
    @patch('weather_app.print')
    def test_main_without_api_key(self, mock_print, mock_load_api_key):
        """API 키가 없는 경우 main 함수 테스트"""
        # Mock 설정
        mock_load_api_key.return_value = None
        
        # main 함수 실행
        from weather_app import main
        main()
        
        # 검증 - API 키 오류 메시지 출력 확인
        mock_print.assert_any_call("❌ OpenWeatherMap API 키를 찾을 수 없습니다.")


if __name__ == "__main__":
    # 테스트 실행
    pytest.main([__file__, "-v"])