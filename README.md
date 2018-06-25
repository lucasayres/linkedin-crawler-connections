# LinkedIn Crawler Connections

Linkedin crawler to search and collect my connections

## Install

```bash
$ sudo apt-get update && sudo apt-get upgrade
$ sudo apt-get install virtualenv python3 python3-dev python-dev gcc libpq-dev libssl-dev libffi-dev build-essentials
$ virtualenv -p /usr/bin/python3 .env
$ source .env/bin/activate
$ pip install -r requirements.txt
```

## How to use

```bash
$ python linkedin.py <linkedin-username> <linkedin-password>
```

### How it works

1. Open chrome browser
2. Access linkedin login page to authenticate
3. Access page with all your connections
4. Access page by page to get the profile links of each person
5. Access the profile to extract: profile picture, name, occupation, location, email and phone
6. Write the result in connections.csv

## Contributing

Any contribution is appreciated.

#### Submitting a Pull Request (PR)

1. Clone the project:
  ```
  $ git clone https://github.com/lucasayres/linkedin-crawler-connections.git
  ```

2. Make your changes in a new git branch:
  ```
  $ git checkout -b my-branch master
  ```

3. Add your changes.

4. Push your branch to Github.

5. Create a PR to master.
