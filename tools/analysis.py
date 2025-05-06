# tools/analysis.py
import re
from collections import Counter
from fastmcp import Context
from config import ENGLISH_STOPWORDS, MAX_KEYWORDS

def register_analysis_tools(mcp):
    """분석 관련 도구 등록"""
    
    @mcp.tool()
    async def extract_keywords(text: str, count: int = 5, ctx: Context = None) -> list:
        """
        텍스트에서 주요 키워드를 추출합니다.
        
        Args:
            text: 분석할 텍스트
            count: 추출할 키워드 수
            
        Returns:
            주요 키워드 목록
        """
        if ctx:
            await ctx.info(f"텍스트에서 키워드 {count}개를 추출합니다...")
        
        # 텍스트 정제
        text = text.lower()
        # HTML 태그 제거
        text = re.sub(r'<.*?>', '', text)
        # 특수 문자 제거
        text = re.sub(r'[^\w\s]', '', text)
        
        # 단어 분리
        words = text.split()
        
        # 불용어 제거
        words = [word for word in words if word not in ENGLISH_STOPWORDS and len(word) > 2]
        
        # 빈도수 계산
        word_freq = Counter(words)
        
        # 상위 키워드 추출
        keywords = word_freq.most_common(min(count, MAX_KEYWORDS))
        
        result = [{"word": word, "count": count} for word, count in keywords]
        
        if ctx:
            await ctx.info(f"{len(result)}개의 키워드를 추출했습니다.")
        
        return result
    
    @mcp.tool()
    async def analyze_article(article_data: dict, ctx: Context = None) -> dict:
        """
        기사 내용을 분석하여 요약 정보를 제공합니다.
        
        Args:
            article_data: fetch_article 도구로 가져온 기사 데이터
            
        Returns:
            분석 결과 (키워드, 문장 수, 단어 수 등)
        """
        if ctx:
            await ctx.info("기사 분석 중...")
        
        if not article_data or "content" not in article_data:
            if ctx:
                await ctx.error("유효하지 않은 기사 데이터입니다.")
            return {"error": "유효하지 않은 기사 데이터"}
        
        # 전체 텍스트 추출
        full_text = ""
        for item in article_data["content"]:
            if item["type"] in ["text", "quote", "subheading"]:
                full_text += " " + item.get("content", "")
        
        # 텍스트 정제
        full_text = re.sub(r'<.*?>', '', full_text)
        
        # 기본 통계
        sentences = re.split(r'[.!?]+', full_text)
        sentences = [s.strip() for s in sentences if s.strip()]
        words = full_text.split()
        
        # 키워드 추출
        keywords = await extract_keywords(full_text, 10, ctx)
        
        result = {
            "title": article_data["metadata"].get("headline", ""),
            "source": article_data["metadata"].get("source", ""),
            "date": article_data["metadata"].get("published_date", ""),
            "stats": {
                "sentence_count": len(sentences),
                "word_count": len(words),
                "avg_sentence_length": len(words) / len(sentences) if sentences else 0
            },
            "keywords": keywords
        }
        
        if ctx:
            await ctx.info("기사 분석을 완료했습니다.")
        
        return result