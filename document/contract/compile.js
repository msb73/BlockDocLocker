const path = require('path');
const fs = require('fs');
const solc = require('solc');

const contractPath = path.resolve(__dirname, 'StringStorage.sol');
const contractSource = fs.readFileSync(contractPath, 'utf8');

const input = {
  language: 'Solidity',
  sources: {
    'StringStorage.sol': {
      content: contractSource,
    },
  },
  settings: {
    outputSelection: {
      '*': {
        '*': ['*'],
      },
    },
  },
};

const compiledCode = JSON.parse(solc.compile(JSON.stringify(input)));
const contractAbi = compiledCode.contracts['StringStorage.sol']['StringStorage'].abi;
const contractBytecode = compiledCode.contracts['StringStorage.sol']['StringStorage'].evm.bytecode.object;

// Output ABI and Bytecode
console.log('Contract ABI:', contractAbi);
console.log('Contract Bytecode:', contractBytecode);
