const Web3 = require('web3');

// Replace with your Ethereum client's RPC endpoint
const rpcURL = 'http://localhost:8545';

const web3 = new Web3(rpcURL);

// Replace with your Ethereum address and password
const address = '0xeAD643b9A02A33997e69bCd8eDA3b735Fa1d2194';
const password = '112233';

web3.eth.personal.unlockAccount(address, password, 0)
  .then(() => {
    console.log(`Account ${address} unlocked successfully.`);
  })
  .catch(error => {
    console.error(`Error unlocking account: ${error}`);
  });
