# config.py
import os

# 기본 설정
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 크롤링 설정
FOX_MAX_PAGES = 3
REUTERS_MAX_PAGES = 3
REQUEST_DELAY = 1.0  # 요청 간 지연 시간(초)
DEFAULT_LIMIT = 5    # 기본 검색 결과 개수

# HTTP 요청 설정
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Safari/605.1.15"
]

# 분석 설정
ENGLISH_STOPWORDS = ["the", "a", "an", "in", "on", "at", "to", "for", "of", "and", "is", "are", "was", "were"]
MAX_KEYWORDS = 10    # 최대 키워드 수