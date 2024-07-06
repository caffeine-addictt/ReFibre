# ReFiber
NYP Semester 2, group3 appdev project

## Installation
Clone the repository
```sh
git clone https://github.com/caffeine-addictt/ReFiber
cd ReFiber
code .
```

## Setup virtural Environment
```sh
py|python|python3 -m venv venv

venv\Scripts\activate # Windows
source venv/bin/activate # Linux/Mac
```

## Install dependencies
```sh
pip install -r requirements.txt
```

# Testing Locally
```sh
pip install pytest
pytest -s -v
```

# Commit to remote repository
```sh
git commit -m "<commit message>" # Saves it local repository(branch)
git push # Saves it to remote repository
```

# To merge main branch to local branch
```sh
git checkout main # Changes your from your local branch to local main branch
git pull origin main # Pull and merge changes from the remote main branch into your local main branch
git checkout <your branch name>
git pull origin <your branch name>
```
