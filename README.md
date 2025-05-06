# News Crawler MCP 서버

## 개요

News Crawler는 FastMCP 기반의 뉴스 크롤링 도구로, Fox News와 Reuters에서 기사를 검색하고 내용을 분석할 수 있습니다. Claude Desktop과 연동하여 자연어 명령으로 최신 뉴스를 검색하고 분석할 수 있습니다.

주요 기능:
- 키워드 기반 뉴스 검색
- 기사 전문 가져오기
- 기사 내용 분석 및 키워드 추출
- 여러 기사 비교를 위한 프롬프트 템플릿

## 사용 방법

### 설치

1. 요구 사항:
   - Python 3.10 이상
   - FastMCP 2.0 이상

2. 설치 명령어:
   ```bash
   cd D:\my_projects\mcp-server\news-mcp
   fastmcp install main.py --name "news-crawler" --with aiohttp beautifulsoup4 asyncio
   ```

3. Claude Desktop config.json에 추가:
   ```json
   {
     "mcpServers": {
       "news-crawler": {
         "command": "cmd",
         "args": [
           "/c",
           "D:\\my_projects\\mcp-server\\news-mcp\\.venv\\Scripts\\python.exe",
           "D:\\my_projects\\mcp-server\\news-mcp\\main.py"
         ]
       }
     }
   }
   ```

### 사용 예시

Claude Desktop에서 다음과 같은 명령으로 사용할 수 있습니다:

1. **뉴스 검색**:
   "테슬라 관련 최신 뉴스 5개를 찾아줘"
   
2. **특정 기사 분석**:
   "이 링크의 기사를 분석해서 핵심 키워드를 알려줘: https://www.reuters.com/..."
   
3. **여러 기사 비교**:
   "테슬라와 애플 주가에 관한 기사들을 비교 분석해줘"

## 상세 설명

### 디렉토리 구조

```
D:\my_projects\mcp-server\news-mcp\
├── main.py                  # 메인 FastMCP 서버
├── crawlers\                # 크롤러 모듈
│   ├── __init__.py
│   ├── base_crawler.py      # 기본 크롤러 클래스
│   ├── fox_crawler.py       # Fox News 크롤러
│   ├── reuters_crawler.py   # Reuters 크롤러
├── tools\                   # MCP 도구
│   ├── __init__.py
│   ├── search.py            # 검색 도구
│   ├── fetch.py             # 기사 가져오기
│   ├── analysis.py          # 분석 도구
├── resources\               # MCP 리소스
│   ├── __init__.py
│   ├── sources.py           # 뉴스 소스 정보
│   ├── stats.py             # 사용 통계
├── prompts\                 # 프롬프트 템플릿
│   ├── __init__.py
│   ├── templates.py
├── config.py                # 설정 파일
├── requirements.txt         # 의존성 목록
```

### 주요 도구

1. **search_news**
   - 매개변수: query(검색어), source(뉴스 소스), limit(최대 결과 수)
   - 기능: 여러 뉴스 소스에서 기사 검색

2. **fetch_article**
   - 매개변수: url(기사 URL)
   - 기능: 특정 URL에서 기사 내용 추출

3. **extract_keywords**
   - 매개변수: text(분석할 텍스트), count(키워드 수)
   - 기능: 텍스트에서 주요 키워드 추출

4. **analyze_article**
   - 매개변수: article_data(기사 데이터)
   - 기능: 기사 내용 분석 및 요약 정보 제공

### 리소스

1. **news://sources**
   - 지원되는 뉴스 소스 목록과 메타데이터

2. **news://stats**
   - 도구 사용 통계 및 성능 정보

### 참고 사항

- 이미지는 원본 URL 제공 방식으로 처리됩니다.
- 각 크롤러는 비동기 방식으로 구현되어 효율적으로 여러 기사를 처리합니다.
- 뉴스 사이트 변경에 따라 크롤러를 주기적으로 업데이트해야 할 수 있습니다.

### 개발자 참고

- 새로운 뉴스 소스를 추가하려면 `base_crawler.py`를 상속받아 구현하세요.
- 과도한 크롤링은 뉴스 사이트의 차단을 유발할 수 있으니 `REQUEST_DELAY` 설정을 적절히 조정하세요.

## 제한 사항

- 일부 뉴스 사이트는 크롤링을 제한할 수 있습니다.
- 기사 내용 추출은 웹사이트 구조에 의존하므로 사이트가 변경되면 크롤러도 업데이트해야 합니다.
- 이미지는 원본 URL만 제공되며 직접 다운로드되지 않습니다.

## 라이선스

MIT 라이선스