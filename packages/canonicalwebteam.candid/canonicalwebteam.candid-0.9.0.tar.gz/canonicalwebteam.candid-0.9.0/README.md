# Canonical Candid - Python package

[![Test live APIs](https://github.com/canonical-web-and-design/canonicalwebteam.store-api/workflows/Test%20live%20APIs/badge.svg)](https://github.com/canonical-web-and-design/canonicalwebteam.store-api/actions?query=workflow%3ATest%20live%20APIs)
[![Tests](https://github.com/canonical-web-and-design/canonicalwebteam.store-api/workflows/Tests/badge.svg)](https://github.com/canonical-web-and-design/canonicalwebteam.store-api/actions?query=workflow%3A)
[![Publish](https://github.com/canonical-web-and-design/canonicalwebteam.store-api/workflows/Publish/badge.svg)](https://github.com/canonical-web-and-design/canonicalwebteam.store-api/actions?query=workflow%3APublish)
[![Code coverage](https://codecov.io/gh/canonical-web-and-design/canonicalwebteam.store-api/branch/master/graph/badge.svg)](https://codecov.io/gh/canonical-web-and-design/canonicalwebteam.store-api)

canonicalwebteam.candid provides authentication with Candid, a macaroon-based
authentication service.


See: https://github.com/canonical/candid


This client only support the browser-redirect login protocol that
provides a mechanism for a user to authenticate with candid, and
subsequently discharge macaroons, by redirecting a web browser via
the candid login pages.

## How to install

To install this extension as a requirement in your project, you can use PIP:

```bash
pip install canonicalwebteam.candid
```

See also the documentation for [pip install](https://pip.pypa.io/en/stable/reference/pip_install/).

## Development

The package leverages [poetry](https://poetry.eustace.io/) for dependency management.
