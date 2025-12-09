import os
import json
import requests
from mcp.server.fastmcp import FastMCP

session = requests.Session()
session.headers["user-agent"]="iFlow-Cli"
mcp = FastMCP("IFlow-Search", json_response=False)


def get_api_key()->str:
    # 获取用户主目录
    home_dir = os.path.expanduser("~")

    # 组合配置文件路径：例如 C:\Users\Admin\.iflow\settings.json
    settings_path = os.path.join(home_dir, ".iflow", "settings.json")

    api_key = None

    if os.path.exists(settings_path):
        with open(settings_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        api_key = data.get("searchApiKey")

    # 如果文件不存在或字段缺失，则回退到环境变量
    if not api_key:
        api_key = os.getenv("IFLOW_SEARCH_API_KEY")

    if not api_key:
        raise KeyError("searchApiKey not found in settings.json or IFLOW_SEARCH_API_KEY env var")

    return api_key


def search_web(query: str) -> str:
    """调用 iFlow 检索接口，返回原始 JSON 字符串。

    :param query: 查询文本
    :return: 接口响应的 JSON 字符串（UTF-8，保留中文）
    """

    api_key = get_api_key()
    url = "https://apis.iflow.cn/v1/chat/retrieve"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "content-type": "application/json",
        "user-agent":"iFlow-Cli"
    }

    payload = {
        "phase": "MULTI_ENGINE_UNIFY",
        "query": query,
        "appCode": "SEARCH_CHATBOT",
        "enableIntention": True,
        "enableQueryRewrite": True,
        "enableSafe": False,
        "enableRetrievalSecurity": False,
        "history": {},
    }

    resp = requests.post(url, headers=headers, json=payload, timeout=20)
    resp.raise_for_status()
    return resp.json()


def format_search_result(j: str) -> str:
    """Convert the JSON result from search() into a human-readable text.

    Expected input is the JSON object returned by search(), and this function
    will list each item with: title, URL and summary.
    """
    items = j.get("data") or []
    if not isinstance(items, list) or not items:
        return "No related results found."

    lines: list[str] = []
    for idx, item in enumerate(items, start=1):
        if not isinstance(item, dict):
            continue

        title = item.get("title") or "(No title)"
        url = item.get("url") or "(No URL)"
        abstract = item.get("abstractInfo") or ""
        time = item.get("time") or "(No time)"
        lines.append(
            f"[Result {idx}]\n"
            f"Title: {title}\n"
            f"Time: {time}\n"
            f"URL: {url}\n"
            f"Summary: {abstract}\n"
        )

    return "\n".join(lines).strip()

@mcp.tool(description="use iflow to search the Internet, get Title, URL and Summary")
def iflow_search(query:str)->str:
    result = search_web(query)
    return format_search_result(result)


def main():
    mcp.run()

if __name__ == "__main__":
    main()