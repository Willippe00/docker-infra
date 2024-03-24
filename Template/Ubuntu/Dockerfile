# Dockerfile
FROM ubuntu:latest

# Installer SSH
RUN apt-get update && \
    apt-get install -y openssh-server && \
    mkdir /var/run/sshd && \
    echo 'root:root' | chpasswd && \
    sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config

# Exposer le port SSH standard
EXPOSE 22

CMD ["/usr/sbin/sshd", "-D"]
