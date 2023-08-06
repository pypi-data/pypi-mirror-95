# LiLiLi: List the Licenses of the Libraries

[![PyPI Version](https://img.shields.io/pypi/v/lilili.svg)](https://pypi.org/pypi/lilili/)
[![Python Versions](https://img.shields.io/pypi/pyversions/lilili.svg)](https://pypi.org/pypi/lilili/)
[![License](https://img.shields.io/pypi/l/lilili.svg)](https://github.com/poyo46/lilili/blob/main/LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)

LiLiLi helps you to retrieve and audit software license information.

## Installation

LiLiLi is available on PyPI:

```console
$ pip install lilili
```

You can also use [poetry](https://python-poetry.org/) to add it to a specific Python project.

```console
$ poetry add lilili
```

## Examples
### Search for and list the licenses of libraries

**Python libraries**

```console
$ pip list > pip-list.txt
$ lilili search --yaml pip-list.txt
```

Example of `result.yml`:

```yaml
- domain: pypi
  name: requests
  version: 2.25.1
  licenses:
    - spdx_id: Apache-2.0
      basis: API_EXACT
      source_url: https://pypi.org/pypi/requests/2.25.1/json
  download_url: https://files.pythonhosted.org/packages/29/c1/24814557f1d22c56d50280771a17307e6bf87b70727d975fd6b2ce6b014a/requests-2.25.1-py2.py3-none-any.whl
  homepage: https://requests.readthedocs.io
  git_url: https://github.com/psf/requests
  updated_at: "2021-02-22T17:32:25.323561"
- domain: pypi
  name: idna
  version: "2.10"
  licenses:
    - spdx_id: BSD-3-Clause
      basis: API_LATEST
      source_url: https://pypi.org/pypi/idna/json
    - spdx_id: BSD-3-Clause
      basis: GITHUB_LICENSES_API
      source_url: https://api.github.com/repos/kjd/idna/license
  download_url: https://files.pythonhosted.org/packages/a2/38/928ddce2273eaa564f6f50de919327bf3a00f091b5baba8dfa9460f3a8a8/idna-2.10-py2.py3-none-any.whl
  homepage: https://github.com/kjd/idna
  git_url: https://github.com/kjd/idna
  updated_at: "2021-02-22T17:32:24.035106"
```

**Ruby libraries**

```console
$ bundle list > bundle-list.txt
$ lilili search --yaml bundle-list.txt
```

The output `result.yml` is in the same format as above.

**Node.js libraries**

```console
$ yarn list > yarn-list.txt
$ lilili search --yaml yarn-list.txt
```

The output `result.yml` is in the same format as above.

## Why LiLiLi?

* LiLiLi uses [the SPDX license list](https://spdx.org/licenses/), which is also used by [GitHub Licenses API](https://docs.github.com/en/rest/reference/licenses), so the license notation can be reused.
* If LiLiLi cannot determine the license for a particular version of the library, it will search for the latest version of the license or a license registered in the GitHub repository.
* LiLiLi will reveal the URL of the API on which the licensing decision is based, so you can double-check it yourself.
