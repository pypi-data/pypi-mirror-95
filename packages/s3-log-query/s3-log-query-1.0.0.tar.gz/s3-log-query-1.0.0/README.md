# S3 Log Query

S3 Log Query is a Python library that takes one or more log files stored in S3, fetches and aggregates log messages from the files based on certain parameters, and returns the messages in order of occurrence. This library utilizes S3 Select and multithreading for performance.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install S3 Log Query.

```bash
pip install s3-log-query
```

## Usage

```python
from s3_log_query import LogQuery

logs = LogQuery(log_paths={'server1': 'server1/server1.log', 'db server': 'db_server/db_server.log',
                                'server2': 'server2/server2.log', 'server3': 'server3/server3/log'},
                     s3_bucket='mikethoun-logs')

logs.query(start='02/28/2020 5:20:55', entries=100, keys=['server1', 'db server'], min_severity=logging.WARN)
```

## Contributing
Pull requests are welcome.

## License
[Apache License 2.0](http://www.apache.org/licenses/LICENSE-2.0)
