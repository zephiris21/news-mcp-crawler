# prompts/templates.py
from fastmcp import Context

def register_prompts(mcp):
    """프롬프트 템플릿 등록"""
    
    @mcp.prompt()
    async def news_summary_prompt(article_data: dict, focus: str = None) -> str:
        """
        뉴스 기사 요약을 위한 프롬프트
        
        Args:
            article_data: 기사 데이터
            focus: 요약 시 집중할 측면 (경제적, 정치적 등)
        """
        metadata = article_data["metadata"]
        title = metadata.get("headline", "")
        source = metadata.get("source", "")
        date = metadata.get("published_date", "")
        
        # 본문 내용 추출
        content = ""
        for item in article_data["content"]:
            if item["type"] == "text":
                content += item.get("content", "") + " "
        
        # 특정 측면에 집중하는 경우
        focus_instruction = ""
        if focus:
            focus_instruction = f"특히 {focus} 측면에 중점을 두고 요약하세요. "
        
        prompt = f"""다음 뉴스 기사를 간결하고 객관적으로 요약해주세요. {focus_instruction}
        
제목: {title}
출처: {source}
날짜: {date}

기사 내용:
{content[:1000]}...

요약:"""
        
        return prompt
    
    @mcp.prompt()
    async def compare_news_prompt(articles: list, topic: str) -> str:
        """
        여러 뉴스 기사 비교를 위한 프롬프트
        
        Args:
            articles: 기사 목록
            topic: 비교 주제
        """
        article_summaries = []
        
        for i, article in enumerate(articles, 1):
            metadata = article["metadata"]
            title = metadata.get("headline", "")
            source = metadata.get("source", "")
            date = metadata.get("published_date", "")
            
            article_summaries.append(f"기사 {i}:\n제목: {title}\n출처: {source}\n날짜: {date}")
        
        articles_text = "\n\n".join(article_summaries)
        
        prompt = f"""다음 뉴스 기사들을 '{topic}' 주제로 비교 분석해주세요.

{articles_text}

비교 분석:
1. 각 기사의 관점과 주요 주장
2. 기사 간의 유사점과 차이점
3. 정보의 신뢰성과 편향성 분석
4. 전반적인 결론

분석 결과:"""
        
        return prompt