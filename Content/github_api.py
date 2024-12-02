#!/bin/env python

from http.client import HTTPException
from requests import get
from time import sleep
from time import time


WAIT_ADDITIONAL_TIME = 5
WAIT_TIME = 60
headers = {
    "Authorization": "Bearer <API_KEY>",
    "X-GitHub-Api-Version": "2022-11-28",
}


def github_handle_rate_limit(type: str) -> None:
    url = "https://api.github.com/rate_limit"
    response = get(url=url, headers=headers)
    if response.status_code != 200:
        sleep(WAIT_TIME)
        return

    reset = 0
    response_json = response.json()
    if type == 'core':
        reset = response_json['resources']['core']['reset']
    elif type == 'search':
        reset = response_json['resources']['search']['reset']

    wait = reset - time()
    sleep(wait + WAIT_ADDITIONAL_TIME)


def github_request_helper(func) -> dict:
    def inner(*args, **kwargs):
        response = func(*args, **kwargs)
        if response.status_code == 200:
            return response.json()
        if response.status_code == 401:
            raise HTTPException("Unauthorized")
        elif response.status_code == 403:
            github_handle_rate_limit("search")
            return func(*args, **kwargs)
        elif response.status_code == 404:
            raise HTTPException("Page not found")
        elif response.status_code == 422:
            raise HTTPException("Invalid query")
        else:
            raise HTTPException("Unhandled HTTP code {response.status_code}")
        return {}
    return inner


@github_request_helper
def github_search_repositories(query: str, per_page: int, page: int, order: str, sort: str) -> dict:
    url = f"https://api.github.com/search/repositories?q={query}&page={page}&per_page'={per_page}&order={order}&sort={sort}"
    response = get(url=url, headers = headers)
    return response

@github_request_helper
def github_get_commits(owner: str, repo: str, per_page: int, page: int):
    url = f"https://api.github.com/repos/{owner}/{repo}/commits?per_page={per_page}&page={page}"
    response = get(url=url, headers=headers)
    return response.json()

@github_request_helper
def github_get_contents(owner: str, repo: str, path: str) -> dict:
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
    response = get(url=url, headers=headers)
    return response.json()


if __name__ == '__main__':
    for i in range(100):
        print(f'{i} {time()}')
        result = github_search_repositories("Data-Source-API-Analyst-Test", 30, 1, "asc", "indexed")
