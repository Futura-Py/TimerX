install:
    pip3 install -r requirements.txt

build-win: install
    set shell := ["pwsh.exe", "-c" ]
    python3 setup.py bdist_msi

build-tux: install
    set shell := ["sh", "-s"]
    python3 setup.py bdist_rpm
    cd dist
    sudo apt install alien -y
    sudo alien -d TimerX-*.tar.gz --version=1.0
    sudo alien -r TimerX-*.tar.gz

build_darwin: install
    set shell := ["sh", "-s"]
    python3 setup.py bdist_dmg

install-docs:
    npm docs-install

build-docs: install-docs
    npm docs-build

fmt:
    npx prettier --write .
