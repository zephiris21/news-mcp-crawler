# crawlers/fox_crawler.py
import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from datetime import datetime
from crawlers.base_crawler import BaseCrawler
from config import FOX_MAX_PAGES

class FoxCrawler(BaseCrawler):
    """Fox News 크롤러"""
    
    def __init__(self):
        super().__init__()
        self.name = "Fox News"
        self.base_url = "https://moxie.foxnews.com/search/web"
        self.max_pages = FOX_MAX_PAGES
    
    async def fetch_articles(self, query):
        """Fox News에서 기사 검색"""
        base_url = self.base_url
        params = {
            "fields": "web",
            "q": query,
            "start": 1
        }
        
        articles = []
        
        # 첫 페이지 요청
        data = await self.fetch_with_delay(base_url, params=params)
        if not data:
            return articles
            
        # 모든 페이지 처리
        for _ in range(self.max_pages):
            if not data or not isinstance(data, dict):
                break
                
            # 기사 추출
            for article in data.get("data", []):
                if article.get("type") == "article":  
                    attributes = article.get("attributes", {})
                    category = attributes.get("section", "")
                    
                    # 비디오만 있는 기사 제외
                    if category not in ["fox-news.video", "category"]:
                        articles.append({
                            "title": attributes.get("title", ""),
                            "description": attributes.get("description", ""),
                            "url": attributes.get("canonical_url", ""),
                            "thumbnail": attributes.get("thumbnail", ""),
                            "date": attributes.get("publication_date", ""),
                            "category": category,
                            "source": "Fox News"
                        })
            
            # 다음 페이지 URL 확인
            next_url = data.get("links", {}).get("next", None)
            if not next_url:
                break
                
            # 다음 페이지 요청
            data = await self.fetch_with_delay(next_url)
            
        return articles
    
    async def fetch_article_details(self, url):
        """Fox News 기사의 상세 내용 가져오기"""
        html = await self.fetch_with_delay(url)
        if not html:
            return None
            
        soup = BeautifulSoup(html, "html.parser")
        
        # 메타데이터 추출
        metadata = {
            "url": url,
            "category": self._extract_text(soup, ".article-meta-upper .eyebrow a", "Unknown"),
            "headline": self._extract_text(soup, "h1.headline.speakable", "No Headline"),
            "subheadline": self._extract_text(soup, "h2.sub-headline.speakable", ""),
            "author": self._extract_text(soup, ".author-byline a", "Unknown"),
            "published_date": self._extract_text(soup, "span.article-date time", "Unknown"),
            "source": "Fox News"
        }
        
        # 본문 내용 추출
        article_content = []
        article_body = soup.select_one("div.article-body")
        
        if article_body:
            order = 0
            for element in article_body.children:
                if element.name == 'p':
                    content = self._process_paragraph(element)
                    if content:
                        article_content.append({
                            "type": "text",
                            "content": content,
                            "order": order
                        })
                        order += 1
                
                elif element.name == 'blockquote':
                    quote = element.select_one("p.quote-text")
                    if quote:
                        article_content.append({
                            "type": "quote",
                            "content": quote.text.strip(),
                            "order": order
                        })
                        order += 1
                
                elif element.name == 'div' and 'image-ct' in element.get('class', []):
                    img = element.select_one('div.m picture img')
                    if img:
                        img_src = img.get('src', '')
                        
                        # 캡션 추출
                        caption_spans = element.select('div.info div.caption p span')
                        caption_text = ""
                        source_text = ""
                        
                        if len(caption_spans) >= 2:
                            caption_text = caption_spans[0].text.strip()
                            source_text = caption_spans[1].text.strip()
                        
                        article_content.append({
                            "type": "image",
                            "image_url": img_src,
                            "caption": caption_text,
                            "source": source_text,
                            "order": order
                        })
                        order += 1
                
                elif element.name == 'h3':
                    strong = element.select_one('strong')
                    if strong:
                        article_content.append({
                            "type": "subheading",
                            "content": strong.text.strip(),
                            "order": order
                        })
                        order += 1
        
        return {
            "metadata": metadata,
            "content": article_content
        }
    
    def _extract_text(self, soup, selector, default=""):
        """선택자에 해당하는 요소의 텍스트 추출"""
        element = soup.select_one(selector)
        return element.text.strip() if element else default
    
    def _process_paragraph(self, element):
        """단락 요소 처리"""
        content = ''
        for child in element:
            if child.name == 'a':  # 링크가 포함된 경우
                href = urljoin("https://www.foxnews.com", child.get('href', ''))
                text = child.text.strip()
                if href and text:
                    content += f"<x id='{href}'>{text}</x>"  # XML 태그로 감싸기
            else:
                content += str(child)  # 일반 텍스트 추가
        
        return content.strip()