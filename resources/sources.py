# resources/sources.py
from fastmcp import Context

def register_sources(mcp):
    """뉴스 소스 정보 리소스 등록"""
    
    @mcp.resource("news://sources")
    async def get_sources(ctx: Context = None) -> dict:
        """지원되는 뉴스 소스 목록을 제공합니다."""
        sources = {
            "fox": {
                "name": "Fox News",
                "url": "https://www.foxnews.com",
                "description": "미국의 24시간 뉴스 채널",
                "topics": ["정치", "경제", "사회", "국제", "건강", "기술", "스포츠"]
            },
            "reuters": {
                "name": "Reuters",
                "url": "https://www.reuters.com",
                "description": "글로벌 뉴스 및 미디어 조직",
                "topics": ["정치", "경제", "비즈니스", "국제", "테크놀로지", "과학"]
            }
        }
        
        return sources