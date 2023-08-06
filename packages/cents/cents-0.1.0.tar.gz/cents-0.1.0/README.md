# Cents

Your Python package manager.

Its works:

- Download packages from the centers registry.
- Download package from GitHub/Git repository.
- Create application through repository.
- Packaged applications.

## Quick get start

Install Cents from _PIPY_

``` bash
pip install cents
```

Or from _GitHub_

``` bash
git clone https://github.com/karoshe/cents.git
cd cents
python setup.py install
```

---

(1). Download from Github

``` bash
cents i pallets/flask --github

Download target repository: https://github.com/pallets/flask
Download was ok ...
Running setup.py (Python File)
Everything was Ok!
```

(2). Download from Git repository

``` bash
cents i https://github.com/pallets/flask.git -git

Download target repository: https://github.com/pallets/flask
Download was ok ...
Running setup.py (Python File)
Everythng was Ok!
```

(3). Download from Our registry

``` bash
cents i player

Find "player" in cents registry (karoshe/registry) ...
Git links: https://github.com/karoshe/player
Download target repository: https://github.com/karoshe/palyer
Download was ok ...
Running setup.py (Python File)
Everythng was Ok!
```

(4). Show Packages info from Our registry

``` bash
cents info player

Find "player" in cents registry (karoshe/registry) ...

=========================

Name: player
Describe: A Python package to play and created by cents.
Author: karoshe (GitHub)
Email: karoshe@qq.com
Creat Time: 2020/2/18 11:17 (UTC)
Package Size: 3KB
Newest Version: 0.1.0

Show more to visit:
https://github.com/karoshe/registry
https://github.com/karoshe/palyer
```

(5). Upload Packages by Our registry

__package.json__

``` json
{
    "name":"player",
    "describe":"A Python package to play and created by cents.",
    "author":"karoshe",
    "email":"karoshe@qq.com",
    "version":"0.1.0"
}
```

__package.py__

``` python
Write Your Code ...
```

## Links

Repository: https://github.com/karoshe/cents
Registry: https://github.com/karoshe/registry
Player: https://github.com/karoshe/player

## Author

Karoshe ([@karoshe](https://github.com/karoshe))
Ceorleorn ([@ceorleorn](https://github.com/ceorleorn))

# License

MIT