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
    allDocuments : callContractFunction,
    checkApprovals : callContractFunction,
    allUsers : callContractFunction,
    allCases : callContractFunction,
}
// Because init process of the MetaMaskSDK is async.
 setTimeout( async () => {
  await MMSDK.init()
    // if(!ethereum.isConnected()){
    const ethereum = MMSDK.getProvider();
  // } // You can also access via window.ethereum
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
                "internalType": "string",
                "name": "caseName",
                "type": "string"
              },
              {
                "internalType": "uint256[]",
                "name": "documentIds",
                "type": "uint256[]"
              },
              {
                "internalType": "address",
                "name": "incharge",
                "type": "address"
              }
            ],
            "internalType": "struct Handle.Case[]",
            "name": "caseToadd",
            "type": "tuple[]"
          },
          {
            "internalType": "uint256[]",
            "name": "caseIds",
            "type": "uint256[]"
          }
        ],
        "name": "addCases",
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
              }
            ],
            "internalType": "struct Handle.IOUser[]",
            "name": "userstoAdd",
            "type": "tuple[]"
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
            "internalType": "uint256[]",
            "name": "indexes",
            "type": "uint256[]"
          }
        ],
        "name": "approveRequests",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
      },
      {
        "inputs": [
          {
            "internalType": "uint256[]",
            "name": "caseIds",
            "type": "uint256[]"
          },
          {
            "internalType": "address[]",
            "name": "addresses",
            "type": "address[]"
          }
        ],
        "name": "changeInCharge",
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
            "name": "ids",
            "type": "uint256[]"
          },
          {
            "internalType": "uint256[]",
            "name": "reqtimes",
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
                "name": "_documentType",
                "type": "string"
              },
              {
                "internalType": "address",
                "name": "_issuer",
                "type": "address"
              },
              {
                "internalType": "string",
                "name": "description",
                "type": "string"
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
        "name": "allCases",
        "outputs": [
          {
            "components": [
              {
                "internalType": "uint256",
                "name": "caseNo",
                "type": "uint256"
              },
              {
                "internalType": "string",
                "name": "CaseName",
                "type": "string"
              }
            ],
            "internalType": "struct Handle.IOCases[]",
            "name": "",
            "type": "tuple[]"
          },
          {
            "internalType": "address[]",
            "name": "",
            "type": "address[]"
          },
          {
            "internalType": "string[]",
            "name": "",
            "type": "string[]"
          }
        ],
        "stateMutability": "view",
        "type": "function"
      },
      {
        "inputs": [],
        "name": "allDocuments",
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
                "name": "documentId",
                "type": "uint256"
              }
            ],
            "internalType": "struct Handle.IODocument[]",
            "name": "",
            "type": "tuple[]"
          },
          {
            "internalType": "uint256[]",
            "name": "",
            "type": "uint256[]"
          },
          {
            "internalType": "string[]",
            "name": "",
            "type": "string[]"
          }
        ],
        "stateMutability": "view",
        "type": "function"
      },
      {
        "inputs": [],
        "name": "allUsers",
        "outputs": [
          {
            "internalType": "address[]",
            "name": "",
            "type": "address[]"
          },
          {
            "internalType": "string[]",
            "name": "",
            "type": "string[]"
          }
        ],
        "stateMutability": "view",
        "type": "function"
      },
      {
        "inputs": [],
        "name": "checkApprovals",
        "outputs": [
          {
            "components": [
              {
                "internalType": "uint256",
                "name": "index",
                "type": "uint256"
              },
              {
                "internalType": "address",
                "name": "sender",
                "type": "address"
              },
              {
                "internalType": "string",
                "name": "username",
                "type": "string"
              },
              {
                "internalType": "uint256",
                "name": "documentId",
                "type": "uint256"
              },
              {
                "internalType": "string",
                "name": "documentName",
                "type": "string"
              },
              {
                "internalType": "uint256",
                "name": "_timestamp",
                "type": "uint256"
              },
              {
                "internalType": "uint256",
                "name": "required_time",
                "type": "uint256"
              }
            ],
            "internalType": "struct Handle.IORequest[]",
            "name": "",
            "type": "tuple[]"
          }
        ],
        "stateMutability": "view",
        "type": "function"
      },
      {
        "inputs": [],
        "name": "checkRequests",
        "outputs": [
          {
            "internalType": "uint256[]",
            "name": "",
            "type": "uint256[]"
          },
          {
            "internalType": "string[]",
            "name": "",
            "type": "string[]"
          }
        ],
        "stateMutability": "view",
        "type": "function"
      },
      {
        "inputs": [
          {
            "internalType": "address",
            "name": "value",
            "type": "address"
          }
        ],
        "name": "listCaseIdsperUser",
        "outputs": [
          {
            "internalType": "uint256[]",
            "name": "data",
            "type": "uint256[]"
          }
        ],
        "stateMutability": "view",
        "type": "function"
      },
      {
        "inputs": [
          {
            "internalType": "uint256",
            "name": "value",
            "type": "uint256"
          }
        ],
        "name": "listCases",
        "outputs": [
          {
            "components": [
              {
                "internalType": "string",
                "name": "caseName",
                "type": "string"
              },
              {
                "internalType": "uint256[]",
                "name": "documentIds",
                "type": "uint256[]"
              },
              {
                "internalType": "address",
                "name": "incharge",
                "type": "address"
              }
            ],
            "internalType": "struct Handle.Case",
            "name": "",
            "type": "tuple"
          }
        ],
        "stateMutability": "view",
        "type": "function"
      },
      {
        "inputs": [],
        "name": "sendIncharge",
        "outputs": [
          {
            "components": [
              {
                "internalType": "string",
                "name": "caseName",
                "type": "string"
              },
              {
                "internalType": "uint256[]",
                "name": "documentIds",
                "type": "uint256[]"
              },
              {
                "internalType": "address",
                "name": "incharge",
                "type": "address"
              }
            ],
            "internalType": "struct Handle.Case",
            "name": "data",
            "type": "tuple"
          }
        ],
        "stateMutability": "view",
        "type": "function"
      },
      {
        "inputs": [
          {
            "internalType": "uint256",
            "name": "i",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "j",
            "type": "uint256"
          }
        ],
        "name": "viewdocsextra",
        "outputs": [
          {
            "internalType": "uint256",
            "name": "use",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "cas",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "doc",
            "type": "uint256"
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
                "name": "_documentType",
                "type": "string"
              },
              {
                "internalType": "address",
                "name": "_issuer",
                "type": "address"
              },
              {
                "internalType": "string",
                "name": "description",
                "type": "string"
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
      return  new w3.eth.Contract(abi, "0xC1a49AF548F77769c3721Eb3dc260490f8928fEa");

}

async function sendDataTransaction(methodName, args) {
    // console.log(...args);
    // Use the 'send' function for transactions 
    obj = {
      from: account,
      to : "0xC1a49AF548F77769c3721Eb3dc260490f8928fEa",
      gasPrice: await w3.eth.getGasPrice(),
      'chainId': 1337,
    }
    try{
        var transaction ;
        try{ transaction =  contract.methods[methodName]( ...args).send(obj)}
        catch (TypeError){ transaction =  contract.methods[methodName]( args).send(obj) }

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
            to : "0xC1a49AF548F77769c3721Eb3dc260490f8928fEa",
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
      



