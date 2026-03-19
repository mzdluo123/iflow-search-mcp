from mcp.server.fastmcp import FastMCP

from iflow_client import search_web, format_search_result

mcp = FastMCP("IFlow-Search", json_response=False)


@mcp.tool(description="use iflow to search the Internet, get Title, URL and Summary")
def iflow_search(query: str) -> str:
    result = search_web(query)
    return format_search_result(result)


def run_server():
    mcp.run()
