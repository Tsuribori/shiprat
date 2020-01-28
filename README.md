## Shiprat

A simple dockerized python script that will run commands whenever a branch is
updated on GitHub. Meant to be a sort of CD tool to be used with docker-compose
projects when the staging/deployment has several local changes.

### Usage

Create a shiprat.yml in the same directory as docker-compose.yml:

```
interval: 5  # Time between each query to GitHub if branch has updated in minutes
repo:  # Define which repo and branch to check for updates
  name: tsuribori/shiprat
  branch: master
preinstall:  # Commands to run in shiprat container when it first start
  - apk add git
steps:  # Commands to run when branch updates
  - git stash
  - git pull
  - docker-compose up --build
  - git stash apply
```

To start the container and watch for updates (in the same directory):

```
docker run -v /var/run/docker.sock:/var/run/docker.sock \
-v $PWD:$PWD -e PDIR=$PWD tsuribori/shiprat
```
