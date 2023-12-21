const MMSDK = new MetaMaskSDK.MetaMaskSDK()
//uploadDocumets
const methobj = {
    uploadDocument : sendDataTransaction,
    addUsers : sendDataTransaction,
    removeUsers : sendDataTransaction,
    viewDocuments : callContractFunction,
    sendRequests : sendDataTransaction,
    checkRequests : callContractFunction,
    approveRequests : sendDataTransaction,
}
// Because init process of the MetaMaskSDK is async.
setTimeout(() => {
    if(!ethereum.isConnected()){
    const ethereum = MMSDK.getProvider();} // You can also access via window.ethereum
}, 0);

const accounts = ethereum.request({ method: 'eth_requestAccounts' });

async function retrieveResult() {
    try {
      const resultArray = await accounts;
      console.log('waitttt');
       return resultArray[0];
    } catch (error) {
      console.error("An error occurred:", error);
      throw error; // Re-throw the error if needed
    }
  }

  // Call the function and store the result in a variable
  let account;
  (async () => {
    try {
      account = await retrieveResult();
      console.log(account);
    } catch (error) {
      console.error("Not Connected", error);
    }
  })();
  console.log('executed');

function getAccount(ethereum) {
    return new Web3(ethereum);
}

function connectContract(w3){
    const abi = JSON.parse(`[
      {
        "inputs": [
          {
            "components": [
              {
                "internalType": "address",
                "name": "userId",
                "type": "address"
              },
              {
                "internalType": "enum Handle.userType",
                "name": "usertype",
                "type": "uint8"
              },
              {
                "internalType": "string",
                "name": "username",
                "type": "string"
              },
              {
                "internalType": "uint256",
                "name": "deptNumber",
                "type": "uint256"
              },
              {
                "internalType": "bool",
                "name": "isActive",
                "type": "bool"
              }
            ],
            "internalType": "struct Handle.User[]",
            "name": "userstoAdd",
            "type": "tuple[]"
          },
          {
            "internalType": "address[]",
            "name": "addresses",
            "type": "address[]"
          }
        ],
        "name": "addUsers",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
      },
      {
        "inputs": [
          {
            "components": [
              {
                "internalType": "address",
                "name": "sender",
                "type": "address"
              },
              {
                "internalType": "uint256",
                "name": "documentId",
                "type": "uint256"
              },
              {
                "internalType": "uint256",
                "name": "_timestamp",
                "type": "uint256"
              },
              {
                "internalType": "uint256",
                "name": "index",
                "type": "uint256"
              }
            ],
            "internalType": "struct Handle.Request[]",
            "name": "reqtoApp",
            "type": "tuple[]"
          }
        ],
        "name": "approveRequests",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
      },
      {
        "inputs": [],
        "name": "extra",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
      },
      {
        "inputs": [
          {
            "internalType": "address[]",
            "name": "addresses",
            "type": "address[]"
          }
        ],
        "name": "removeUsers",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
      },
      {
        "inputs": [
          {
            "internalType": "uint256[]",
            "name": "documentIds",
            "type": "uint256[]"
          }
        ],
        "name": "sendRequests",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
      },
      {
        "inputs": [],
        "stateMutability": "nonpayable",
        "type": "constructor"
      },
      {
        "inputs": [
          {
            "components": [
              {
                "internalType": "string",
                "name": "documentName",
                "type": "string"
              },
              {
                "internalType": "uint256",
                "name": "caseNo",
                "type": "uint256"
              },
              {
                "internalType": "uint256",
                "name": "documentId",
                "type": "uint256"
              },
              {
                "internalType": "string",
                "name": "_cid",
                "type": "string"
              },
              {
                "internalType": "uint256",
                "name": "_timeStamp",
                "type": "uint256"
              },
              {
                "internalType": "string",
                "name": "_documentHash",
                "type": "string"
              },
              {
                "internalType": "enum Handle.DocType",
                "name": "_documentType",
                "type": "uint8"
              },
              {
                "internalType": "address",
                "name": "_issuer",
                "type": "address"
              }
            ],
            "internalType": "struct Handle.Document[]",
            "name": "uploads",
            "type": "tuple[]"
          }
        ],
        "name": "uploadDocument",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
      },
      {
        "inputs": [],
        "name": "checkRequests",
        "outputs": [
          {
            "components": [
              {
                "internalType": "address",
                "name": "sender",
                "type": "address"
              },
              {
                "internalType": "uint256",
                "name": "documentId",
                "type": "uint256"
              },
              {
                "internalType": "uint256",
                "name": "_timestamp",
                "type": "uint256"
              },
              {
                "internalType": "uint256",
                "name": "index",
                "type": "uint256"
              }
            ],
            "internalType": "struct Handle.Request[]",
            "name": "",
            "type": "tuple[]"
          }
        ],
        "stateMutability": "view",
        "type": "function"
      },
      {
        "inputs": [],
        "name": "viewDocuments",
        "outputs": [
          {
            "components": [
              {
                "internalType": "string",
                "name": "documentName",
                "type": "string"
              },
              {
                "internalType": "uint256",
                "name": "caseNo",
                "type": "uint256"
              },
              {
                "internalType": "uint256",
                "name": "documentId",
                "type": "uint256"
              },
              {
                "internalType": "string",
                "name": "_cid",
                "type": "string"
              },
              {
                "internalType": "uint256",
                "name": "_timeStamp",
                "type": "uint256"
              },
              {
                "internalType": "string",
                "name": "_documentHash",
                "type": "string"
              },
              {
                "internalType": "enum Handle.DocType",
                "name": "_documentType",
                "type": "uint8"
              },
              {
                "internalType": "address",
                "name": "_issuer",
                "type": "address"
              }
            ],
            "internalType": "struct Handle.Document[]",
            "name": "",
            "type": "tuple[]"
          }
        ],
        "stateMutability": "view",
        "type": "function"
      }
    ]`);
      return  new w3.eth.Contract(abi, "0xB9E95B80cd355fBD36F294A37373062Af0C40996");
}

async function sendDataTransaction(methodName, ...args) {
    // console.log(...args);
    // Use the 'send' function for transactions 
    
    try{
      console.log("sdafsdfasf");
    const transaction =  contract.methods[methodName]( ...args).send({
        from: account,
        to : "0xB9E95B80cd355fBD36F294A37373062Af0C40996",
        gasPrice: await w3.eth.getGasPrice(),
        'chainId': 1337,
    })
    return transaction
    } catch (error) {
        return error.message
    }
    }

async function callContractFunction(methodName, ...args) {
      // alert("sdafsdfasf");
      // console.log(length(...a  rgs));
    try {
      
        const result = contract.methods[methodName](...args).call({
            from: account,
            to : "0xB9E95B80cd355fBD36F294A37373062Af0C40996",
            gasPrice: await w3.eth.getGasPrice(),
            'chainId': 1337,
        });
        return result;
        console.log(`${methodName} Result:::`, result);
        
    } catch (error) {
      return error.message
        // console.error(`Error calling ${methodName}:`, error.message);
    }
  }


const w3 =  getAccount(ethereum);
const contract =  connectContract(w3);

// If the day before two days after today is monday, what day is today?
      



