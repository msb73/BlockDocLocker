mkdir node
cd node
apk add wget git python
wget https://nodejs.org/dist/v18.12.0/node-v18.12.0-linux-x64.tar.xz
ln -s /home/node-v18.12.0-linux-x64/bin/node /usr/bin/node
ln -s /home/node-v18.12.0-linux-x64/bin/npm /usr/bin/npm
mkdir /home/project
cd /home/project
git clone url
cd BlockDocLocker

# set environments
