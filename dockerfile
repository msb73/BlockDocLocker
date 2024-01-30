FROM apline:latest
WORKDIR /home


RUN npm install --global --quiet truffle ganache
EXPOSE 8545
ENTRYPOINT ["ganache-cli --host 0.0.0.0"]
# wget https://nodejs.org/dist/v18.12.0/node-v18.12.0-linux-x64.tar.xz

# sudo ln -s /home/node-v18.12.0-linux-x64/bin/node /usr/bin/node
# sudo ln -s /home/node-v18.12.0-linux-x64/bin/npm /usr/bin/npm