[![image](https://img.shields.io/pypi/v/clients.svg)](https://pypi.org/project/clients/)
![image](https://img.shields.io/pypi/pyversions/clients.svg)
[![image](https://pepy.tech/badge/clients)](https://pepy.tech/project/clients)
![image](https://img.shields.io/pypi/status/clients.svg)
[![image](https://github.com/coady/clients/workflows/build/badge.svg)](https://github.com/coady/clients/actions)
[![image](https://codecov.io/gh/coady/clients/branch/main/graph/badge.svg)](https://codecov.io/gh/coady/clients/)
[![image](https://github.com/coady/clients/workflows/codeql/badge.svg)](https://github.com/coady/clients/security/code-scanning)
[![image](https://img.shields.io/badge/code%20style-black-000000.svg)](https://pypi.org/project/black/)
[![image](https://mypy-lang.org/static/mypy_badge.svg)](https://mypy-lang.org/)

Clients originally provided [requests](https://python-requests.org) wrappers to encourage best practices, particularly always using Sessions to connect to the same host or api endpoint. The primary goals were:
* provide a `Client` object with a convenient constructor
* support a base url so that requests can provide a relative path
* provide the same interface for asyncio

Since then [httpx](https://www.encode.io/httpx) has emerged as the successor to `requests`, and supports the above features natively. So `clients.Client` can be replaced with `httpx.Client` for most use cases. The project will continue to be maintained for additional features, such as the `Resource` object.

## Usage
Typical `requests` usage is redundant and inefficient, by not taking advantage of connection pooling.

```python
r = requests.get('https://api.github.com/user', headers={'authorization': token})
r = requests.get('https://api.github.com/user/repos', headers={'authorization': token})
```

Using sessions is the better approach, but more verbose and in practice requires manual url joining.

```python
s = requests.Session()
s.headers['authorization'] = token
r = s.get('https://api.github.com/user')
r = s.get('https://api.github.com/user/repos')
```

### Client
Clients make using sessions easier, with implicit url joining.

```python
client = clients.Client('https://api.github.com/', headers={'authorization': token})
r = client.get('user')
r = client.get('user/repos')
```

### Resource
Resources extend Clients to implicitly handle response content, with proper checking of status_code and content-type.

```python
github = clients.Resource('https://api.github.com/', headers={'authorization': token})
for repo in github.get('user/repos', params={'visibility': 'public'}):
    ...
```

Resources also implement syntactic support for methods such as __getattr__ and __call__, providing most of the benefits of custom clients as is.

```python
for repo in github.user.repos(visibility='public'):
    ...
```

Asynchronous variants of all client types are provided, e.g., `AsyncClient`. Additional clients for [RPC](https://en.wikipedia.org/wiki/Remote_procedure_call), [GraphQL](https://graphql.org), and proxies also provided.

## Installation
```console
% pip install clients
```

## Dependencies
* httpx

## Tests
100% branch coverage.
```console
% pytest [--cov]
```
