# crawlers/base_crawler.py
import aiohttp
import asyncio
import random
from config import USER_AGENTS, REQUEST_DELAY

class BaseCrawler:
    """뉴스 크롤러의 기본 클래스"""
    
    def __init__(self):
        self.name = "Base Crawler"
        self.headers = {
            "User-Agent": random.choice(USER_AGENTS),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5"
        }
    
    async def fetch_articles(self, query):
        """검색어에 맞는 기사 목록 가져오기"""
        raise NotImplementedError("서브클래스에서 구현해야 함")
    
    async def fetch_article_details(self, url):
        """특정 URL의 기사 상세 내용 가져오기"""
        raise NotImplementedError("서브클래스에서 구현해야 함")
    
    async def fetch_with_delay(self, url, headers=None, params=None):
        """지연 시간을 적용한 HTTP 요청"""
        if headers is None:
            headers = self.headers
            
        # 요청 간 지연 적용
        await asyncio.sleep(REQUEST_DELAY * (0.5 + random.random()))
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, params=params) as response:
                if response.status != 200:
                    return None
                
                content_type = response.headers.get('Content-Type', '')
                if 'application/json' in content_type:
                    return await response.json()
                else:
                    return await response.text()