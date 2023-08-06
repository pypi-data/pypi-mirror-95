# Adminbypasser


Adminbypasser is a dork based admin panel finder and bypasser using SQL injection.


```sh
$ pip install adminbypasser
```

### Usage:


```sh
$ adminbypasser --help
usage: adminbypasser --snip <PAGE> --max <MAX_URL> --out <OUT_FILE> [OPTIONS]

--help, -h      : show help
--snip, -s      : URL snippet part eg: admin.php
--country, -c   : country code for target sites
--max, -m       : maximum URLs
--out, -o       : write bypassable URL to a file
--user-agent, -u : user-agent for requests
```


Finding bypassable admin panels:

```sh
$ adminbypasser -s admin.php -c lk -m 20 -o admin_lk.txt
```

> Disclaimer: causing damage to unauthenticated sites is illegal, please use this tool on your own risk.
