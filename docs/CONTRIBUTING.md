---
sidebar_position: 2
id: contributing
title: Contributing to TimerX
---

# Contributing to TimerX

TimerX is written in **Python**, so you have to install it if you want to contribute.
You can download the latest version from [here](https://www.python.org/downloads/).
Make sure to check `Add Python 3.10 to PATH` when installing it.
After installing Python, install [Git](https://git-scm.org). It's version control, so that will help you in adding your changes over here.
Click the `Fork` button on the top-right in the GitHub page. Give it a few seconds to fork TimerX and then execute these series of commands in your Terminal/Command Prompt.

```shell
git clone https://github.com/your-username/TimerX && cd TimerX
python3 -m pip install -r requirements.txt
python3 -m pip install -r windows-requirements.txt
```

After following the series of commands, open your favourite text editor. We recommend that you use [Visual Studio Code](https://code.visualstudio.com). Make your changes and before committing, go to the status bar. There will be a place showing branches and the text `master`. Click that, click `New branch` and name your branch, such as `patch-1` or so. Make sure it correlates to your feature, if it's a patch, name it as a patch, if it's a feature, name the feature. Next, go to the Version Control tab from the sidebar and commit the file, _semantically_. We recommend you to use semantic commits since that is more concise.
Commit your changes to that new branch, [open a pull request](https://github.com/Futura-Py/TimerX/compare) (click `Compare across forks`) and someone will review it ASAP.

### Gitpod - Ready to code

We support Gitpod - a ready-to-code environment customised for TimerX. You could either customise the app or the TimerX website. To code on Gitpod, follow the steps below:

#### 1. Click the link

[![Open in Gitpod](https://gitpod.io/button/open-in-gitpod.svg)](https://gitpod.io/#/https://github.com/Futura-Py/TimerX)

#### 2. Log in with GitHub

The link will open a tab where you'll be asked to log in - it won't if you have already logged into Gitpod.

#### 3. Wait for the environment to load

The environment is building itself. You'll have to wait for at least 2 minutes, plus or minus.

#### 4. Start coding!

When Gitpod loads, you will be greeted by a VS Code UI. You could start coding immediately. But be wary - the commits are forced to be semantic. Fortunately, we have a CLI tool called `cz` that could help you on committing.

#### Ready to commit?

First, create a new branch. Name it in a way that it tells your feature in a short, abstract way. After creating your branch, open a new terminal by typing <kbd>Ctrl</kbd> + <kbd>`</kbd>.

The <kbd>`</kbd> symbol is beside the number 1 key or right above the Tab key. Then, type these commands:

```shell
git add . # stages your code to commit.
cz c # The tool for committing the code
```

It will ask you what type of change it is, the scope(just hit enter) and the commit title. Make sure the title is apt and short(~50 letters). Then, add a commit description if you want and choose N for breaking change(although if it's a breaking change, choose yes). Then, go ahead with enters and type this in the end:

```shell
git push
```

After that, you can open a PR [here](https://github.com/Futura-Py/TimerX/pulls/new). Choose your branch and open it and a reviewer will review it soon.

### [Repl.it](https://repl.it)

Go to the Repl.it homepage and click `Create a repl`. On the top right corner, there is a `Import from GitHub` button. Click that and in the place of the URL, type `github.com/Futura-Py/TimerX`. Create the repl and go to it.

The repl will be booted and ready to use.

Happy coding 🚀
