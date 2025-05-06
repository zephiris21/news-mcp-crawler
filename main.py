# main.py
from fastmcp import FastMCP

# 도구와 리소스 가져오기
from tools.search import register_search_tools
from tools.fetch import register_fetch_tools
from tools.analysis import register_analysis_tools
from resources.sources import register_sources
from resources.stats import register_stats
from prompts.templates import register_prompts

# MCP 서버 생성
mcp = FastMCP(name="News Crawler")

# 도구, 리소스, 프롬프트 등록
register_search_tools(mcp)
register_fetch_tools(mcp)
register_analysis_tools(mcp)
register_sources(mcp)
register_stats(mcp)
register_prompts(mcp)

# 서버 실행
if __name__ == "__main__":
    mcp.run()