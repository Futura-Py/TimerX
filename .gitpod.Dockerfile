# https://hub.docker.com/r/gitpod/workspace-python-tk-vnc # Python with Tk and VNC
FROM gitpod/workspace-python-tk-vnc:branch-tk-dev

# RUN echo "Installing Node.js for Docusaurus"
# RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.1/install.sh | bash
# RUN export NVM_DIR="$([ -z "${XDG_CONFIG_HOME-}" ] && printf %s "${HOME}/.nvm" || printf %s "${XDG_CONFIG_HOME}/nvm")" [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh" # This loads nvm
# RUN source ~/.bashrc
# RUN echo "NVM installed."
# RUN nvm install 14
# RUN nvm use 14
