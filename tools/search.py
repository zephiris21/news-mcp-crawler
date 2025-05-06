# tools/search.py
import asyncio
from fastmcp import Context
from crawlers.fox_crawler import FoxCrawler
from crawlers.reuters_crawler import ReutersCrawler
from config import DEFAULT_LIMIT

# 크롤러 인스턴스 생성
fox_crawler = FoxCrawler()
reuters_crawler = ReutersCrawler()

def register_search_tools(mcp):
    """검색 관련 도구 등록"""
    
    @mcp.tool()
    async def search_news(query: str, source: str = "all", limit: int = DEFAULT_LIMIT, ctx: Context = None) -> list:
        """
        뉴스 검색 도구
        
        Args:
            query: 검색어
            source: 뉴스 소스 (fox, reuters, all)
            limit: 최대 결과 수
            
        Returns:
            검색된 뉴스 기사 목록
        """
        if ctx:
            await ctx.info(f"'{query}' 관련 뉴스를 {source} 소스에서 검색합니다.")
        
        results = []
        tasks = []
        
        # 소스에 따라 적절한 크롤러 사용
        if source in ["fox", "all"]:
            if ctx:
                await ctx.info("Fox News에서 검색 중...")
            tasks.append(fox_crawler.fetch_articles(query))
            
        if source in ["reuters", "all"]:
            if ctx:
                await ctx.info("Reuters에서 검색 중...")
            tasks.append(reuters_crawler.fetch_articles(query))
        
        # 병렬로 검색 실행
        crawl_results = await asyncio.gather(*tasks)
        
        # 결과 합치기
        for result in crawl_results:
            results.extend(result)
        
        # 날짜순 정렬 및 개수 제한
        results = sorted(results, key=lambda x: x.get("date", ""), reverse=True)[:limit]
        
        if ctx:
            await ctx.info(f"{len(results)}개의 기사를 찾았습니다.")
        
        return results