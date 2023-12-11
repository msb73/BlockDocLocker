// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;
pragma experimental ABIEncoderV2;

contract Handle {
 
// mapping ( address => User ) issuers;

address owner;
enum userType {
        ISSUER,
		USER
    }
enum AccessLevel {
        READ_ONLY,
		SHARE
    }
enum DocType {
		TEXT,
		AUDIO,
		VIDEO,
		IMAGE
}
mapping (address => User ) users; // contains both issuer and users;
mapping (uint256 => Document) documents; // maps with documentid
mapping (uint256 documentId => mapping( address => uint256 )) viewTime;
mapping (address => Refresh) refresh;
mapping (address userId => uint256[])  sharedDocs;
mapping (address userId => uint256[])  owneddocIds;
mapping ( address user => Request[] request )  requests ;
struct  Document { // Document Number
			string documentName;
			uint256 caseNo;  // deptNumber + CaseNo
			uint256 documentId; // caseNo + Increment
			string _cid;
			uint256 _timeStamp;
			string _documentHash;
			DocType _documentType;
			address _issuer;
}

struct User  {   // address
		address userId;
        userType usertype;
		string username;
		uint256 deptNumber;
        bool isActive;

}


struct Refresh {
    uint256 time;
    bool updated;
}


struct  IODocument { // Document Number
			string documentName;
			uint256 caseNo;  // deptNumber + CaseNo
			uint256 documentId; // caseNo + Increment
			string _cid;
			uint256 _timeStamp;
			string _documentHash;
			DocType _documentType;

}

struct Request {
    address sender;
    uint256 documentId;
    uint256 _timestamp;
    uint256 index;
}

constructor () {
    owner = msg.sender;
}

modifier onlyOwner() {
    require(msg.sender == owner, "Only the owner can call this function");
    _;
    }

modifier validUser() {
    require(users[msg.sender].isActive, "User does not exist or inactive"); 
    _;
    }



function addUsers (User [] calldata userstoAdd, address [] calldata addresses) external onlyOwner  {



         for(uint8 i = 0; i < addresses.length; i++){
            require(addresses[i] != users[addresses[i]].userId, "User Already Exists");
            users[addresses[i]] = userstoAdd[i];
            users[addresses[i]].isActive = true;
            users[addresses[i]].userId = addresses[i];
         }
		// require contract owner
		// add new User to users mapping
}

function removeUsers (address [] calldata addresses) external onlyOwner {
        for(uint8 i = 0; i < addresses.length; i++){
            users[addresses[i]].isActive = false;
            for(i = 0; i < sharedDocs[addresses[i]].length ; i++){
                sharedDocs[addresses[0]].pop();
            }
            for(i = 0; i < owneddocIds[addresses[i]].length ; i++){
                owneddocIds[addresses[0]].pop();
            }
         }
}

function uploadDocument( Document [] calldata uploads ) validUser external {

        require( users[msg.sender].usertype == userType.ISSUER, "User is Not Issuer");
		
        for(uint8 i = 0 ; i < uploads.length; i++){

            if (documents[uploads[i].documentId].documentId == 0){
                documents[uploads[i].documentId] = uploads[i];
                documents[uploads[i].documentId]._timeStamp = block.timestamp;
                documents[uploads[i].documentId]._issuer = msg.sender;
                owneddocIds[msg.sender].push(uploads[i].documentId);
            }
            
        }
}

// function removeExpiredSharedDocs(uint[] storage data  ) internal {
//     // remove from viewTime
//         for (uint8 i = 0; i < data.length; i++) {
//             // mapping (uint256 documentId => mapping( address => uint256 )) viewTime;

//             if( viewTime[data[i]][msg.sender] <= block.timestamp  ){
//                     // delete document traces
//                     delete viewTime[data[i]][msg.sender];
//                     //delete form sharedDocs
//                     data[i] = data[data.length -1];
//                     data.pop();
//             }
//     }
//     }
// function removeExpiredRequests(Request [] storage data) internal {
//         for(uint8 i = 0; i < data.length; i++){    // iterate over whole array not till 24hr
//         if  ( data[i]._timestamp >  block.timestamp -  86400) {  // true if timestamp over 24hr
//             data[i] = data[data.length -1];  // append last to first
//             data.pop();  // remove last
//         }
//     }

//     }
//refresh shareDocs View time and requested Requests Time

// function refresher () external { 
//             // require(refresh[msg.sender].time / 86400 != block.timestamp / 86400, "Alrady Refreshed");
//             removeExpiredSharedDocs(sharedDocs[msg.sender]);
//             removeExpiredRequests(requests[msg.sender]);
//             refresh[msg.sender].time = block.timestamp;
            
        
        
// }



function viewDocuments() validUser external view returns (Document [] memory)  {

        
        Document  [] memory toView = new Document[](owneddocIds[msg.sender].length + sharedDocs[msg.sender].length);

        for (uint8 i = 0; i < owneddocIds[msg.sender].length; i++){
                toView[i] = documents[owneddocIds[msg.sender][i]];
                toView[i]._issuer = 0x0000000000000000000000000000000000000000;
        }
        for (uint8 i = 0; i < sharedDocs[msg.sender].length; i++){
                toView[i] = documents[sharedDocs[msg.sender][i]];
                toView[i]._issuer = 0x0000000000000000000000000000000000000000;
        }
        return toView ;
}




function sendRequests(uint256 [] calldata documentIds) external validUser  {
    for (uint8 i = 0; i < documentIds.length; i++){
        if (documents[documentIds[i]]._issuer != msg.sender){ // cannot send request to self
            requests[documents[documentIds[i]]._issuer].push(
            Request({
                sender : msg.sender, documentId : documentIds[i], _timestamp : block.timestamp, index : requests[documents[documentIds[i]]._issuer].length
            })
        );
        }
        
    }
	
}



function checkRequests () external view  returns (Request[] memory)    {
    return requests[msg.sender];
}





function approveRequests (Request[] calldata reqtoApp ) external  validUser {

    for (uint8 i = 0; i < reqtoApp.length; i++){
        require(documents[reqtoApp[i].documentId]._issuer == msg.sender );
        viewTime[reqtoApp[i].documentId][reqtoApp[i].sender] = block.timestamp + reqtoApp[i]._timestamp;
        sharedDocs[reqtoApp[i].sender].push(reqtoApp[i].documentId);
        refresh[msg.sender].updated = true;
    }
}





//extra 
function extra()public {
    owneddocIds[msg.sender].push(20);
users[msg.sender] =  User({
    userId : msg.sender,
    usertype : userType.ISSUER,
    username : "Milind",
    deptNumber : 201,
    isActive : true
});
    documents[20] = Document({
        documentName : "asdfasdf",
        caseNo : 2020,
        documentId : 20,
        _cid : "Dafsadfasdfcafs",
        _timeStamp : block.timestamp,
        _documentHash : "Sdafdsacsfgs",
        _documentType : DocType.TEXT,
        _issuer : msg.sender
    });
}
}
    