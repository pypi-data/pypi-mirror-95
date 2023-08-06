# Scrap Utils
This is small package that contains some code regularly repeated when scraping.

It has the following functions:
```python
load_json(filepath, encoding=None, errors=None, parse_float=None,
	parse_int=None, parse_constant=None)

dump_json(data, filepath, encoding=None, errors=None, indent=4, skipkeys=False,
	ensure_ascii=False, separators=None, sort_keys=False)

to_csv(dataset, filepath, mode="a", encoding=None, errors=None, newline='',
	header=True, dialect='excel', **fmtparams)

requests_get(url, trials=0, sleep_time=30, max_try=math.inf, **requests_kwargs)

requests_post(url, trials=0, sleep_time=30, max_try=math.inf, **requests_kwargs)
```

To-do list I'm considering:
* remove print statements
* add unittest
* soup_get()
* driver_get()
* start_firefox()
* read_csv()

Feel free to add your contribution [here](https://github.com/bizzyvinci/scrap-utils)