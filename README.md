# Data-Source-API-Analyst-Test

## Overview
Homework assignment for Data Source API Analyst role

## Perository structure
<code>README.md</code> - this overview

<code>Content</code> - standalone Python script

<code>Postman_Collection</code> - Postman collection

## Client Requirements
1 Search Repositories
* Query string based method to search for public repositories

2 Commits
* Method to get repository's commits

3 Contents
* Method to get content of the specified file in the repository

## Github API endpoints used
Searh for repository:
* https://api.github.com/search/repositories

Get commits
* https://api.github.com/repos/{owner}/{repo}/commits

Get file content
* https://api.github.com/repos/{owner}/{repo}/contents/{path}

Get rate limit
* https://api.github.com/rate_limit

## Error Handling
* Script checks 403 error caused if rate limit is exceeded
* Script gets 'rate_limit' and wait until 'reset' time. This way is faster than constant wait
