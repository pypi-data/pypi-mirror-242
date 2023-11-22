import requests
import typer
import time
from typing import List
from rich import print
from enum import Enum
from json.decoder import JSONDecodeError
import json as json_package
from .__version__ import package_version, package_name

app = typer.Typer(add_completion=False)

class HttpMethod(str, Enum):
    """http请求枚举"""

    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"
    OPTIONS = "OPTIONS"
    HEAD = "HEAD"


def process_list_data(value: list) -> dict:
    """处理列表"""
    return dict(map(lambda item: item.split("="), value))


def process_json_data(value: str) -> str:
    """处理json"""
    # 如果字符串以单引号或双引号包裹，则去掉外围的引号
    try:
        if value.startswith("'") and value.endswith("'"):
            value = value[1:-1]
        elif value.startswith('"') and value.endswith('"'):
            value = value[1:-1]
    # 如果json为空，就返回空对象
    except AttributeError:
        return None
    # 将单引号替换为双引号
    value_with_double_quotes = value.replace("'", '"')
    # 解析为 Python 对象
    return json_package.loads(value_with_double_quotes)


def version_callback(value: bool):
    if value:
        print(f"{package_name} Version: {package_version}")
        raise typer.Exit()

@app.command()
def main(
    url: str = typer.Argument(help="目标URL",show_default=False),
    method: HttpMethod = typer.Option(
        "GET",
        "--method",
        "-m",
        help="请求方法",
    ),
    params: List[str] = typer.Option(
        None,
        "--params",
        "-p",
        help="请求（查询）参数,可以多个参数.例子：-p page=2 -p limit=30",
        show_default=False,
    ),
    data: List[str] = typer.Option(
        None,
        "--data",
        "-d",
        help="请求体使用Form数据,可以多个参数.例子：-d name=admin",
        show_default=False,
    ),
    json: str = typer.Option(
        None,
        "--json",
        "-j",
        help='请求体使用JSON数据,应为json格式.例子：-j \'{"name":"admin"}\'',
        show_default=False,
        callback=process_json_data,
    ),
    headers: str = typer.Option(
        None,
        "--headers",
        "-h",
        help="设置请求头,应为json格式.例子：-h \"{'Content-Type':'application/json'}\"",
        show_default=False,
        callback=process_json_data,
    ),
    timeout: float = typer.Option(
        None,
        "--timeout",
        "-t",
        help="超时时间,单位秒(s).例子：-t 3.2",
        show_default=False,
    ),
    cookies: str = typer.Option(
        None,
        "--cookies",
        help="cookie包含在请求中,应为json格式.例子：--cookies \"{'your cookie name':'your cookies'}\"",
        show_default=False,
        callback=process_json_data,
    ),
    verbose: bool = typer.Option(
        False,
        "--verbose",
        "-v",
        help="输出详细信息",
        show_default=False,
    ),
    version: bool = typer.Option(
        False,
        "--version",
        "-V",
        help="输出版本信息",
        show_default=False,
        is_eager=True,
        callback=version_callback,
    ),
):
    """requests cli工具"""
    if params:
        # 格式化列表为字典
        params = process_list_data(params)
    if data:
        # 格式化列表为字典
        data = process_list_data(data)
    # 创建会话
    session = requests.session()
    try:
        first_time = time.time()
        # 请求
        res = session.request(
            method=method,
            url=url,
            params=params,
            json=json,
            data=data,
            headers=headers,
            timeout=timeout,
            cookies=cookies,
        )
        last_time = time.time() - first_time
    except Exception as e:
        print(e)
        raise typer.Exit()
    # 打印url
    print(method, res.status_code, url,f"ResponseTime:{last_time}s", end="\n\n")
    # 判断verbose
    if verbose:
        # 打印请求头
        print("[bold blue]Request Headers:[/bold blue]")
        for k, v in res.request.headers.items():
            print(f"{k}:{v}")

        # 换行用
        print()
    # 打印响应头
    print("[bold blue]Response Headers:[/bold blue]")
    for k, v in res.headers.items():
        print(f"{k}:{v}")
    # 换行用
    print()
    # 打印响应体
    try:
        print("[bold blue]Response Body:[/bold blue]")
        print(res.json(), end="\n\n")
    except JSONDecodeError:
        print(res.text, end="\n\n")


if __name__ == "__main__":
    app()
