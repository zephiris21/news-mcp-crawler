# tools/fetch.py
from fastmcp import Context
from crawlers.fox_crawler import FoxCrawler
from crawlers.reuters_crawler import ReutersCrawler

# 크롤러 인스턴스 생성
fox_crawler = FoxCrawler()
reuters_crawler = ReutersCrawler()

def register_fetch_tools(mcp):
    """기사 가져오기 관련 도구 등록"""
    
    @mcp.tool()
    async def fetch_article(url: str, ctx: Context = None) -> dict:
        """
        특정 URL에서 뉴스 기사의 전체 내용을 가져옵니다.
        
        Args:
            url: 뉴스 기사 URL
            
        Returns:
            기사 내용이 포함된 사전 (제목, 본문, 날짜, 이미지 등)
        """
        if ctx:
            await ctx.info(f"기사 내용을 가져오는 중: {url}")
        
        # URL에 따라 적절한 크롤러 선택
        if "foxnews.com" in url:
            if ctx:
                await ctx.info("Fox News 기사 분석 중...")
            article_data = await fox_crawler.fetch_article_details(url)
        elif "reuters.com" in url:
            if ctx:
                await ctx.info("Reuters 기사 분석 중...")
            article_data = await reuters_crawler.fetch_article_details(url)
        else:
            if ctx:
                await ctx.error("지원되지 않는 뉴스 소스입니다.")
            return {"error": "지원되지 않는 뉴스 소스"}
        
        if not article_data:
            if ctx:
                await ctx.error("기사 내용을 가져오지 못했습니다.")
            return {"error": "기사 내용을 가져오지 못했습니다."}
        
        if ctx:
            headline = article_data["metadata"].get("headline", "")
            await ctx.info(f"기사 내용을 성공적으로 가져왔습니다: {headline}")
        
        return article_data
    
    @mcp.tool()
    async def batch_fetch_articles(urls: list, ctx: Context = None) -> list:
        """
        여러 URL에서 뉴스 기사의 내용을 일괄 가져옵니다.
        
        Args:
            urls: 뉴스 기사 URL 목록
            
        Returns:
            각 기사 내용이 포함된 목록
        """
        if ctx:
            await ctx.info(f"{len(urls)}개의 기사를 가져오는 중...")
        
        results = []
        total = len(urls)
        
        for i, url in enumerate(urls):
            if ctx:
                progress = (i / total) * 100
                await ctx.report_progress(progress, f"{i+1}/{total} 기사 처리 중")
            
            article = await fetch_article(url, ctx)
            if "error" not in article:
                results.append(article)
        
        if ctx:
            await ctx.info(f"{len(results)}개 기사를 성공적으로 가져왔습니다.")
        
        return results