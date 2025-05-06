# crawlers/reuters_crawler.py
import re
from bs4 import BeautifulSoup
from urllib.parse import quote, urljoin, urlsplit
from datetime import datetime
from crawlers.base_crawler import BaseCrawler
from config import REUTERS_MAX_PAGES

class ReutersCrawler(BaseCrawler):
    """Reuters 크롤러"""
    
    def __init__(self):
        super().__init__()
        self.name = "Reuters"
        self.base_url = "https://www.reuters.com/pf/api/v3/content/fetch/articles-by-search-v2"
        self.max_pages = REUTERS_MAX_PAGES
    
    async def fetch_articles(self, query):
        """Reuters에서 기사 검색"""
        articles = []
        size = 20
        offset = 0
        
        for page in range(self.max_pages):
            params = {
                "query": f'{{"keyword":"{quote(query)}","offset":{offset},"orderby":"display_date:desc","size":{size},"website":"reuters"}}',
                "d": "264",
                "mxId": "00000000",
                "_website": "reuters"
            }
            
            data = await self.fetch_with_delay(self.base_url, params=params)
            if not data or not isinstance(data, dict) or 'result' not in data:
                break
                
            page_articles = data['result'].get('articles', [])
            if not page_articles:
                break
                
            for article in page_articles:
                thumbnail_data = article.get("thumbnail", {})
                articles.append({
                    "title": article.get("title", ""),
                    "description": article.get("description", ""),
                    "url": "https://www.reuters.com" + article.get("canonical_url", ""),
                    "thumbnail": thumbnail_data.get("url", "") if thumbnail_data else "",
                    "date": article.get("published_time", ""),
                    "category": article.get("category", ""),
                    "source": "Reuters"
                })
            
            offset += size
            if page == self.max_pages - 1:
                break
        
        return articles
    
    async def fetch_article_details(self, url):
        """Reuters 기사의 상세 내용 가져오기"""
        html = await self.fetch_with_delay(url)
        if not html:
            return None
            
        soup = BeautifulSoup(html, "html.parser")
        
        try:
            # URL에서 카테고리 추출
            path = urlsplit(url).path
            path_parts = [part for part in path.split('/') if part]
            main_category = path_parts[0] if len(path_parts) > 0 else "Uncategorized"
            
            # 메타데이터 추출
            headline = soup.select_one("h1").text.strip() if soup.select_one("h1") else "Untitled"
            
            time_tag = soup.select_one("time")
            published_date = datetime.strptime(
                time_tag["datetime"], "%Y-%m-%dT%H:%M:%SZ"
            ).strftime("%Y-%m-%d %H:%M:%S") if time_tag and "datetime" in time_tag.attrs else datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            authors = [a.text.strip() for a in soup.select("a[rel='author']")]
            author = ", ".join(authors) if authors else ""
            
            metadata = {
                "url": url,
                "headline": headline,
                "author": author,
                "published_date": published_date,
                "source": "Reuters",
                "category": main_category
            }
            
            # 본문 내용 추출
            content = []
            article_body = soup.select_one("div[data-testid='ArticleBody']")
            if not article_body:
                return None
                
            order = 0
            for element in article_body.find_all():
                # 단락 추출
                if "data-testid" in element.attrs and element["data-testid"].startswith("paragraph-"):
                    paragraph_content = self._process_paragraph(element)
                    if paragraph_content:
                        content.append({
                            "type": "text",
                            "content": paragraph_content,
                            "order": order
                        })
                        order += 1
                
                # 이미지 추출
                elif element.name == "figure" and "primary-image__container" in " ".join(element.get("class", [])):
                    img = element.find("img")
                    if img and "srcset" in img.attrs:
                        img_src = img["srcset"].split(",")[-1].split()[0]
                        img_alt = img.get("alt", "Image")
                        
                        # 캡션 추출
                        caption_elem = element.select_one("div[data-testid='Body']")
                        caption = ""
                        if caption_elem:
                            span_texts = [span.get_text(strip=True) for span in caption_elem.find_all("span")]
                            caption = span_texts[0] if span_texts else ""
                        
                        content.append({
                            "type": "image",
                            "image_url": img_src,
                            "alt": img_alt,
                            "caption": caption,
                            "order": order
                        })
                        order += 1
                
                # 부제목 추출
                elif element.name == "h2" and element.get("data-testid") == "Heading":
                    content.append({
                        "type": "subheading",
                        "content": element.text.strip(),
                        "order": order
                    })
                    order += 1
            
            return {"metadata": metadata, "content": content}
            
        except Exception as e:
            print(f"기사 파싱 중 오류: {str(e)}")
            return None
    
    def _process_paragraph(self, element):
        """단락 요소 처리"""
        paragraph_content = ""
        
        for child in element.children:
            if child.name == "a" and "data-testid" in child.attrs and child["data-testid"] == "Link":
                href = urljoin("https://www.reuters.com", child.get("href", ""))
                link_text = "".join(t for t in child.find_all(string=True, recursive=False)).strip()
                
                if href and link_text:
                    paragraph_content += f" <x id='{href}'>{link_text}</x> "
            
            elif child.name is None:  # 일반 텍스트 추가
                paragraph_content += f" {child.strip()} "
        
        return paragraph_content.strip()