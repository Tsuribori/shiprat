import yaml
import subprocess
import os
import requests
from time import sleep


def run_commands(steps):
    for step in steps:
        subprocess.run(step, shell=True, cwd=os.getenv("PDIR"))


def is_updated(repo, branch):
    url = "https://api.github.com/repos/{}/branches/{}".format(repo, branch)
    response = requests.get(url)
    if response.status_code == 200:
        commit = response.json()["commit"]["sha"]
        with open("commit.txt", "a+") as f:
            f.seek(0)
            last_commit = f.read()
            if commit != last_commit:
                f.seek(0)
                f.truncate()
                f.write(commit)
                return True
    else:
        print("Failed to get latest commit.")

    return False


def shiprat(data):
    while True:
        if is_updated(data["repo"]["name"], data["repo"]["branch"]):
            run_commands(data['steps'])
        sleep(data['interval'] * 60)


try:
    with open("{}/shiprat.yml".format(os.getenv("PDIR")), "r") as f:
        try:
            data = yaml.safe_load(f)
            run_commands(data["preinstall"])
            shiprat(data)
        except yaml.YAMLError as exc:
            print(exc)
except Exception as exc:
    print(exc)
