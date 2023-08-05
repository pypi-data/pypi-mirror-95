# [Amazon S3 API](http://s3-api.hive.pt)

Simple Python based API client for Amazon S3.

## Configuration

| Name              | Type  | Default                     | Description                                                                               |
| ----------------- | ----- | --------------------------- | ----------------------------------------------------------------------------------------- |
| **S3_BASE_URL**   | `str` | `https://s3.amazonaws.com/` | The base URL to be used for the API calls.                                                |
| **S3_ACCESS_KEY** | `str` | `None`                      | Secret key to be used to authenticate API request.                                        |
| **S3_SECRET**     | `str` | `None`                      | String value to be kept secret and used in the request signing process as the secret key. |
| **S3_REGION**     | `str` | `None`                      | The name of the region where the request are going to be sent by default (defaults to `). |

## License

Amazon S3 API is currently licensed under the [Apache License, Version 2.0](http://www.apache.org/licenses/).

## Build Automation

[![Build Status](https://travis-ci.com/hivesolutions/s3_api.svg?branch=master)](https://travis-ci.com/hivesolutions/s3_api)
[![Build Status GitHub](https://github.com/hivesolutions/s3_api/workflows/Main%20Workflow/badge.svg)](https://github.com/hivesolutions/s3_api/actions)
[![Coverage Status](https://coveralls.io/repos/hivesolutions/s3_api/badge.svg?branch=master)](https://coveralls.io/r/hivesolutions/s3_api?branch=master)
[![PyPi Status](https://img.shields.io/pypi/v/s3_api.svg)](https://pypi.python.org/pypi/s3_api)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://www.apache.org/licenses/)
