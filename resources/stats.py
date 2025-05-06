# resources/stats.py
from fastmcp import Context
import time

# 통계 추적을 위한 전역 변수
usage_stats = {
    "search_count": 0,
    "fetch_count": 0,
    "analysis_count": 0,
    "last_reset": time.time()
}

def register_stats(mcp):
    """통계 정보 리소스 등록"""
    
    @mcp.resource("news://stats")
    async def get_stats(ctx: Context = None) -> dict:
        """크롤링 통계 정보를 제공합니다."""
        
        # 도구 사용 통계 복사
        stats = dict(usage_stats)
        
        # 가동 시간 계산
        uptime = time.time() - stats["last_reset"]
        days, remainder = divmod(uptime, 86400)
        hours, remainder = divmod(remainder, 3600)
        minutes, seconds = divmod(remainder, 60)
        
        stats["uptime"] = {
            "days": int(days),
            "hours": int(hours),
            "minutes": int(minutes),
            "seconds": int(seconds)
        }
        
        # 총 사용량
        stats["total_requests"] = stats["search_count"] + stats["fetch_count"] + stats["analysis_count"]
        
        return stats
    
    # 통계 업데이트 함수 추가
    # 도구 데코레이터 옵션으로 설정하거나 별도 함수로 구현
    @mcp.tool("update_stats")
    async def update_stats(tool_name: str) -> bool:
        """내부 통계 업데이트용 도구"""
        if tool_name == "search_news":
            usage_stats["search_count"] += 1
        elif tool_name == "fetch_article":
            usage_stats["fetch_count"] += 1
        elif tool_name == "analyze_article":
            usage_stats["analysis_count"] += 1
        return True