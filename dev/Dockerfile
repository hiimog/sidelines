FROM ubuntu:jammy

# allows us to skip passing -y to things
ENV DEBIAN_FRONTEND noninteractive

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

RUN apt-get -qq update \
    && apt-get -qq --no-install-recommends install sudo

# create user developer and remove password for sudo
RUN groupadd -g 999 developer \
    && useradd -u 999 -g developer -G sudo -m -s /bin/bash developer \
    && sed -i /etc/sudoers -re 's/^%sudo.*/%sudo ALL=(ALL:ALL) NOPASSWD: ALL/g' \
    && sed -i /etc/sudoers -re 's/^root.*/root ALL=(ALL:ALL) NOPASSWD: ALL/g' \
    && sed -i /etc/sudoers -re 's/^#includedir.*/## **Removed the include directive** ##"/g' \
    && echo "developer ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers \
    && echo "Customized the sudoers file for passwordless access to the developer user!" \
    && echo "developer user:";  su - developer -c id

USER developer

RUN echo "developer:developer" | sudo chpasswd

# set timezone information without interactive prompts
RUN sudo DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends tzdata \
    && sudo ln -fs /usr/share/zoneinfo/America/New_York /etc/localtime \
    && sudo dpkg-reconfigure -f noninteractive tzdata

# install base software
RUN sudo apt-get -qq update \
    && sudo apt-get -qq --no-install-recommends install \
        bat=0.19.0-1 \
        build-essential=12.9ubuntu3 \
        cmake=3.22.1-1ubuntu1 \
        cmake-data=3.22.1-1ubuntu1 \
        coreutils=8.32-4.1ubuntu1 \
        curl=7.81.0-1ubuntu1.7 \
        diffutils=1:3.8-0ubuntu2 \
        doxygen=1.9.1-2ubuntu2 \
        exa=0.10.1-2 \
        expect=5.45.4-2build1 \
        fd-find=8.3.1-1 \
        fzf=0.29.0-1 \
        gawk=1:5.1.0-1build3 \
        gdb=12.0.90-0ubuntu1 \
        git=1:2.34.1-1ubuntu1.6 \
        gnupg=2.2.27-3ubuntu2.1 \
        graphviz=2.42.2-6 \
        jq=1.6-2.1ubuntu3 \
        lcov=1.15-1 \
        less=590-1build1 \
        libedit-dev=3.1-20210910-1build1 \
        libreadline-dev=8.1.2-1 \
        lsb-release=11.1.0ubuntu4 \
        meld=3.20.4-2 \
        mlocate=1.1.15-1ubuntu2 \
        neovim=0.6.1-3 \
        ninja-build=1.10.1-1 \
        openssh-server=1:8.9p1-3ubuntu0.1 \
        python3-pip=22.0.2+dfsg-1 \
        python3.10-dev=3.10.6-1~22.04.2 \
        python3.10-venv=3.10.6-1~22.04.2 \
        python-is-python3=3.9.2-2 \
        ripgrep=13.0.0-2 \
        silversearcher-ag=2.2.0+git20200805-1 \
        software-properties-common=0.99.22.5 \
        tig=2.5.1-1 \
        tree=2.0.2-1 \
        unzip=6.0-26ubuntu3 \
        util-linux=2.37.2-4ubuntu3 \
        valgrind=1:3.18.1-1ubuntu2 \
        wget=1.21.2-2ubuntu1 \
        xxd=2:8.2.3995-1ubuntu2.3 \
        zsh=5.8.1-1

# install gitdelta for nice command line diffs
RUN sudo wget -O gitdelta.deb https://github.com/dandavison/delta/releases/download/0.13.0/git-delta_0.13.0_amd64.deb \
    && sudo dpkg -i gitdelta.deb \
    && sudo rm gitdelta.deb

# configure sshd and fix ssh login
RUN sudo sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd \
    && sudo mkdir /var/run/sshd \
    && sudo bash -c 'install -m755 <(printf "#!/bin/sh\nexit 0") /usr/sbin/policy-rc.d' \
    && sudo ex +'%s/^#\zeListenAddress/\1/g' -scwq /etc/ssh/sshd_config \
    && sudo ex +'%s/^#\zeHostKey .*ssh_host_.*_key/\1/g' -scwq /etc/ssh/sshd_config \
    && sudo RUNLEVEL=1 dpkg-reconfigure openssh-server \
    && ssh-keygen -A -v \
    && update-rc.d ssh defaults 

# create user key
RUN ssh-keygen -t ed25519 -f /home/developer/.ssh/id_ed25519

