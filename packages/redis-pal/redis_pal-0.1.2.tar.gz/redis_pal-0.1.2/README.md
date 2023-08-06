# Redis Pal

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/9883436b5c9846398076016645afb36a)](https://app.codacy.com/gh/gabriel-milan/redis-pal?utm_source=github.com&utm_medium=referral&utm_content=gabriel-milan/redis-pal&utm_campaign=Badge_Grade)
[![codecov](https://codecov.io/gh/gabriel-milan/redis-pal/branch/master/graph/badge.svg?token=SYATCHZJAG)](https://codecov.io/gh/gabriel-milan/redis-pal)
[![Build Status](https://travis-ci.com/gabriel-milan/redis-pal.svg?branch=master)](https://travis-ci.com/gabriel-milan/redis-pal)
[![PyPI version](https://badge.fury.io/py/redis-pal.svg)](https://badge.fury.io/py/redis-pal)

Stop worrying about serialization! Store (almost) anything on Redis without even thiking about it.
You can also check the last time you've modified a given key just by calling `get_with_timestamp(key)`.

## Usage

```py
>>> import numpy as np
>>> from redis_pal import RedisPal
>>> rp = RedisPal()
>>> rp.set("test", np.array([1, 2, 3]))
True
>>> rp.get("test")
array([1, 2, 3])
>>> rp.get_with_timestamp("test")
{'value': array([1, 2, 3]), 'last_modified': 1613329082.33473}
```

## Installation

As simple as running

```
pip3 install redis-pal
```