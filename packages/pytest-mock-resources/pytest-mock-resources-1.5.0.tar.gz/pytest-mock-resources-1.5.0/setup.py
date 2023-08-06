# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pytest_mock_resources',
 'pytest_mock_resources.container',
 'pytest_mock_resources.fixture',
 'pytest_mock_resources.fixture.database',
 'pytest_mock_resources.fixture.database.relational',
 'pytest_mock_resources.fixture.database.relational.redshift',
 'pytest_mock_resources.patch',
 'pytest_mock_resources.patch.redshift']

package_data = \
{'': ['*']}

install_requires = \
['docker>=2.5.1', 'pytest>=1.0', 'responses', 'sqlalchemy']

extras_require = \
{':python_version >= "2.7" and python_version < "2.8"': ['functools32'],
 'mongo': ['pymongo'],
 'mysql:python_version < "3.6"': ['pymysql<1.0'],
 'mysql:python_version >= "3.6"': ['pymysql>=1.0'],
 'postgres': ['psycopg2'],
 'postgres-binary': ['psycopg2-binary'],
 'redis': ['redis'],
 'redshift': ['moto', 'boto3', 'sqlparse']}

entry_points = \
{'console_scripts': ['pmr = pytest_mock_resources.cli:main'],
 'pytest11': ['pytest_mock_resources = pytest_mock_resources']}

setup_kwargs = {
    'name': 'pytest-mock-resources',
    'version': '1.5.0',
    'description': 'A pytest plugin for easily instantiating reproducible mock resources.',
    'long_description': '![CircleCI](https://img.shields.io/circleci/build/gh/schireson/pytest-mock-resources/master) [![codecov](https://codecov.io/gh/schireson/pytest-mock-resources/branch/master/graph/badge.svg)](https://codecov.io/gh/schireson/pytest-mock-resources) [![Documentation Status](https://readthedocs.org/projects/pytest-mock-resources/badge/?version=latest)](https://pytest-mock-resources.readthedocs.io/en/latest/?badge=latest)\n\n\n## Introduction\n\nCode which depends on external resources such a databases (postgres, redshift, etc) can be difficult\nto write automated tests for. Conventional wisdom might be to mock or stub out the actual database\ncalls and assert that the code works correctly before/after the calls.\n\nHowever take the following, _simple_ example:\n\n```python\ndef serialize(users):\n    return [\n        {\n            \'user\': user.serialize(),\n            \'address\': user.address.serialize(),\n            \'purchases\': [p.serialize() for p in user.purchases],\n        }\n        for user in users\n    ]\n\ndef view_function(session):\n    users = session.query(User).join(Address).options(selectinload(User.purchases)).all()\n    return serialize(users)\n```\n\nSure, you can test `serialize`, but whether the actual **query** did the correct thing _truly_\nrequires that you execute the query.\n\n## The Pitch\n\nHaving tests depend upon a **real** postgres instance running somewhere is a pain, very fragile,\nand prone to issues across machines and test failures.\n\nTherefore `pytest-mock-resources` (primarily) works by managing the lifecycle of docker containers\nand providing access to them inside your tests.\n\nAs such, this package makes 2 primary assumptions:\n* You\'re using `pytest` (hopefully that\'s appropriate, given the package name)\n* For many resources, `docker` is required to be available and running (or accessible through remote docker).\n\nIf you aren\'t familiar with Pytest Fixtures, you can read up on them in the [Pytest documentation](https://docs.pytest.org/en/latest/fixture.html).\n\nIn the above example, your test file could look something like\n\n```python\nfrom pytest_mock_resources import create_postgres_fixture\nfrom models import ModelBase\n\npg = create_postgres_fixture(ModelBase, session=True)\n\ndef test_view_function_empty_db(pg):\n  response = view_function(pg)\n  assert response == ...\n\ndef test_view_function_user_without_purchases(pg):\n  pg.add(User(...))\n  pg.flush()\n\n  response = view_function(pg)\n  assert response == ...\n\ndef test_view_function_user_with_purchases(pg):\n  pg.add(User(..., purchases=[Purchase(...)]))\n  pg.flush()\n\n  response = view_function(pg)\n  assert response == ...\n```\n\n## Existing Resources (many more possible)\n\n* SQLite\n\n  ```python\n  from pytest_mock_resources import create_sqlite_fixture\n  ```\n\n* Postgres\n\n  ```python\n  from pytest_mock_resources import create_postgres_fixture\n  ```\n\n* Redshift\n\n  **note** Uses postgres under the hood, but the fixture tries to support as much\n  redshift functionality as possible (including redshift\'s `COPY`/`UNLOAD` commands).\n\n  ```python\n  from pytest_mock_resources import create_redshift_fixture\n  ```\n\n* Mongo\n\n  ```python\n  from pytest_mock_resources import create_mongo_fixture\n  ```\n\n* Redis\n\n  ```python\n  from pytest_mock_resources import create_redis_fixture\n  ```\n  \n * MySQL\n \n   ```python\n   from pytest_mock_resources import create_mysql_fixture\n   ```\n\n## Installing\n\n```bash\n# Basic fixture support\npip install "pytest-mock-resources"\n\n# For postgres install EITHER of the following:\npip install "pytest-mock-resources[postgres-binary]"\npip install "pytest-mock-resources[postgres]"\n\n# For redshift install EITHER of the following:\n# (redshift fixtures require postgres dependencies...)\npip install "pytest-mock-resources[postgres, redshift]"\npip install "pytest-mock-resources[postgres-binary, redshift]"\n\n# For mongo install the following:\npip install "pytest-mock-resources[mongo]"\n\n# For redis\npip install "pytest-mock-resources[redis]"\n\n# For mysql\npip install "pytest-mock-resources[mysql]"\n```\n\n## Possible Future Resources\n\n* Rabbit Broker\n* AWS Presto\n\nFeel free to file an [issue](https://github.com/schireson/pytest-mock-resources/issues) if you find any bugs or want to start a conversation around a mock resource you want implemented!\n',
    'author': 'Omar Khan',
    'author_email': 'oakhan3@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/schireson/pytest-mock-resources',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*',
}


setup(**setup_kwargs)
