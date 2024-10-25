## VM
> https://yandex.cloud/ru/docs/cli/quickstart  
> https://yandex.cloud/ru/docs/compute/operations/vm-connect/os-login?from=int-console-help-center-or-nav
```commandline
yc compute instance list
```
```commandline
yc compute ssh <id>
```

## Docker
**[Docker guide](https://vladilen.notion.site/Docker-2021-a72201ec8573461c8a2e62e2fcf33aa3)**
```commandline
docker build -t <repository>:latest -f Dockerfile .
```
```commandline
docker push <repository>:latest
```
```commandline
docker pull <repository>:latest
```
```commandline
docker run -p 8501:8501 cicd
```

## Create ssh keys on local machine

```commandline
ssh-keygen -t ed25519
```



## Create User on VM
Full doc https://yandex.cloud/ru/docs/compute/operations/vm-connect/ssh?from=int-console-help-center-or-nav

```commandline
sudo useradd -m -d /home/testuser -s /bin/bash testuser
```

```commandline
sudo su - testuser
```

```commandline
mkdir .ssh

touch .ssh/authorized_keys

chmod 700 ~/.ssh
chmod 600 ~/.ssh/authorized_keys
```

```commandline
echo "<публичный_ключ>" >> /home/testuser/.ssh/authorized_keys
```

```commandline
exit
```

restart VM 

Save the ssh and user credentials

## Не запрашивать пароль у юзера с VM
Дока https://losst.pro/otklyuchaem-parol-sudo-v-linux

```commandline
sudo visudo
```
Добавить строчку 
username ALL=(ALL) NOPASSWD: ALL

