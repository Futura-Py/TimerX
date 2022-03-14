---
sidebar_position: 3
slug: compile
title: Compiling TimerX
---

# Compiling TimerX from source

Before compiling, make soure you have [Python 3.x](https://python.org/downloads/) with PIP and optionally [Git](https://git-scm.org) installed; we recommend you to use Python 3.10 for compiling TimerX.

Make sure Python is added to your PATH while installing.

## Step 1 {#repoclone}

Open your terminal and head to the TimerX folder; if you have Git, clone it with `git clone https://github.com/Futura-Py/TimerX.git` or download the ZIP file from [here](https://github.com/Futura-Py/TimerX/archive/refs/heads/master.zip).

## Step 2 {#packages}

After going inside your directory, make sure that you install the required packages via `pip3` or `pip` if you use Anaconda3:

```console
$ pip3 install -r requirements.txt
$ pip3 install -r requirements-dev.txt
OR, if you use Anaconda3,
$ pip install -r requirements.txt
$ pip install -r requirements-dev.txt
```

If you are on Windows, you can install the Windows requirements file by:

```batch
pip3 install -r windows-requirements.txt
REM or if you use Anaconda3,
pip install -r windows-requirements.txt
```

## Step 3 {#compile}

After you install the required packages, execute these commands in TimerX's root directory:

### Windows compiling

```batch
REM for making an unzipped executable package
python3 setup.py bdist_win
REM for making an installer:
python3 setup.py bdist_msi
```

If you use Anaconda3:

```batch
REM if you want the unzipped package
python setup.py bdist_exe
REM if you need an installer:
python setup.py bdist_msi
```

### Linux compiling

You can generate only a DEB or RPM installer for Linux.
For Debian-based distros:

```shell
# If on Anaconda3, use `python setup.py bdist_rpm`
python3 setup.py bdist_rpm
cd dist
sudo apt install alien
sudo alien -d TimerX-*.tar.gz --version=1.0
```

For RHEL-based distros:

```shell
python3 setup.py bdist_rpm
# Anaconda3
python setup.py bdist_rpm
```
