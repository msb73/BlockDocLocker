// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;
pragma experimental ABIEncoderV2;
contract Handle {
    
/*      Final
    documentId = ( caseId + documentId ) 
     -> (caseId * 1000000000) + documentId

*/
// mapping ( address => User ) issuers;

address owner;
enum userType {
        ISSUER,
		USER
    }
enum Status {
        APPROVE,
        REJECTED,
        PENDING
    }



// addUser              I/P -> User O/P 
// removeUser           I/P -> userIds O/P None 
// removeDocuments      mapping (uint256 => Document) documents; remove docid
// allDocuments
// refreshAll           go through all users[DocumentId] with help of address [] userIds and all requests with   
// addCaseIds           assign caseIds to mapping  (uint256 caseId => address ) caseids in users
// changeIncharge       remove caseIds from caseids and add to other address
//listUsers


// uploadDocuments   mapping (uint256 => Document) documents;   documentId will be combination of CaseId and dcoumentId
// viewDocuments     will retrieve data from users["adress"]
// allDocuments      get all documentiDs from uint256[] documentIds
// sendRequest       add to users of ownersRequests by checking if doc  exists in users
// checkRequest      return all requests of ownersReqeusts and viewsers Reqeusts
// approve request   add to documentIds to users uint256[] documents


//internal 
// get last doc id
mapping (address => User ) users; 
mapping (uint256 => Document) documents;
mapping (uint256 caseId => Case) cases ;
mapping(uint256 index => Request) requests;
address [] userIds;
uint256 documentsCount = 1;
uint256 last_index = 1;
uint256[] removedCaseIds;

struct IOUser {
        address userId;
        userType usertype;
		string username;
		uint256 deptNumber;
}

struct User {
        address userId;   // store address
        userType usertype;  // ISSUER / USER
		string username; // Name of User
		uint256 deptNumber; // 
        bool isActive; // Deleted or Not
        uint256 [] caseIds; // Actual caseIds Incharge
        mapping(uint256 documentId => uint256 time ) shareddocs; // time  
        uint256[] sharedDocsRequestIndex; // shared address documentid 
        uint256 arr_index; 
}



struct Case {
    string caseName;
    uint256 [] documentIds;
    address incharge;
    uint [] requests;
}

struct Document{
        string documentName;
		uint256 caseNo;  // deptNumber + CaseNo 
		uint256 documentId; // caseNo + Increment
		string _cid;
		uint256 _timeStamp;
		string _documentType;
		address _issuer;
        string description;

        
}
 
struct IODocument{
    string documentName;
    uint256 documentId;
}

struct Request {
    address sender;
    uint256 documentId;
    uint256 _timestamp;
    uint256 required_time;
    Status status;

}

struct SharedDoc{
    uint256 documentId;
    uint256 required_time;
}

struct IORequest {
    uint256 index;
    address sender;
    string username;
    uint256 documentId;
    string documentName;
    uint256 _timestamp;
    uint256 required_time;
}

struct IOCases{
    uint256 caseNo;
    string CaseName;
}

constructor () {
    owner = msg.sender;
}

modifier onlyOwner() {
    require(msg.sender == owner, "^Only the owner can call this function$");
    _;
    }

modifier validUser() { 
    require(users[msg.sender].isActive, "^User does not exist or inactive$"); 
    _;

    }
    
function refresh () external  onlyOwner{
    
}

function addUsers (IOUser [] calldata userstoAdd) external onlyOwner  {
         for(uint8 i = 0; i < userstoAdd.length; i++){
            require(userstoAdd[i].userId != users[userstoAdd[i].userId].userId, "^User Already Exists$");
            users[userstoAdd[i].userId].userId = userstoAdd[i].userId;
            users[userstoAdd[i].userId].usertype = userstoAdd[i].usertype;
            users[userstoAdd[i].userId].username = userstoAdd[i].username;
            users[userstoAdd[i].userId].deptNumber = userstoAdd[i].deptNumber;
            users[userstoAdd[i].userId].isActive = true;
            users[userstoAdd[i].userId].arr_index = userIds.length;
            userIds.push(userstoAdd[i].userId);
         }
		// require contract owner
		// add new User to users mapping
}



function removeUsers (address [] calldata addresses) external onlyOwner {

        for(uint8 i = 0; i < addresses.length; i++){
            for(uint8 j = 0; j < users[addresses[i] ].caseIds.length; j++){
                //change caseses Incharge to owner
                cases[users[addresses[i] ].caseIds[j]].incharge = msg.sender;
                removedCaseIds.push(users[addresses[i] ].caseIds[j]);
                documentsCount -= cases[users[addresses[i] ].caseIds[j]].documentIds.length;
            }
            users[userIds[userIds.length -1]].arr_index = users[addresses[i]].arr_index;  
            userIds[users[addresses[i]].arr_index] = userIds[userIds.length -1];
            delete users[addresses[i]];
            userIds.pop();
         }
}

function allUsers() public  view onlyOwner returns (address[] memory,  string[] memory){ 
    string [] memory names = new string[] (userIds.length);
    for(uint256 i = 0 ; i < userIds.length; i++){
        names[i] = users[userIds[i]].username;
    } 
    return (userIds, names);

}



function viewDocuments() validUser external view returns (Document[]  memory)  {
        uint256 len = 0; // for toViewCount
        for( uint256 i = 0; i < users[msg.sender].caseIds.length ; i++ ){
            len+= cases[users[msg.sender].caseIds[i]].documentIds.length;
        }
        Document  [] memory toView = new Document[]( len + users[msg.sender].sharedDocsRequestIndex.length);
        len = 0;
        for( uint256 i = 0; i < users[msg.sender].caseIds.length ; i++ ){
            for ( uint256 j = 0; j < cases[users[msg.sender].caseIds[i]].documentIds.length ; j++ ){
                toView[len] = documents[ cases[ users[msg.sender].caseIds[i] ].documentIds[j]];
                toView[len]._issuer = 0x0000000000000000000000000000000000000000;
                len +=1;
            }
        }
        uint[] storage indexes = users[msg.sender].sharedDocsRequestIndex; 
        for (uint8 i = 0; i < indexes.length; i++){
            if ( requests[indexes[i]].required_time  > block.timestamp ){
                toView[len] = documents[ requests[indexes[i]].documentId ];
                toView[len]._issuer = 0x0000000000000000000000000000000000000000;
                len +=1;
            } 
        }
        return  toView ;
}

function allDocuments() validUser external view returns ( IODocument[] memory, uint256 [] memory,  string [] memory)  {
    IODocument [] memory docs = new IODocument[](documentsCount);
    uint256 [] memory idxs = new uint256[](userIds.length);
    string [] memory uNames = new string[](userIds.length);

    uint256 len = 0;
    // i = index of array of users
    for (uint256 i = 0; i < userIds.length;  i++){
                uNames[i] = users[  userIds[i] ].username;
                idxs[i] = len;

    // // j = index of per users caseid
        for ( uint256 j = 0; j < users[ userIds[i] ].caseIds.length ; j++ ){

            // k = index of per user per caseid document 
            for ( uint256 k = 0; k < cases[users[userIds[i]].caseIds[j]].documentIds.length ; k++ ){
                docs[len].documentId = cases[users[userIds[i]].caseIds[j]].documentIds[k];
                docs[len].documentName = documents[ cases[users[userIds[i]].caseIds[j]].documentIds[k] ].documentName;
                len+=1;
                }
                
            }
        }
    return (docs, idxs, uNames);
}


function uploadDocument( Document [] calldata uploads ) validUser external {

        require( users[msg.sender].usertype == userType.ISSUER, "^User is Not Issuer$");
        for(uint8 i = 0 ; i < uploads.length; i++){
            require(cases[ uploads[i].caseNo].incharge == msg.sender, "^User is not Authorized for that caseid$");
            // Duplicated will be manage at ipfs level
                uint docid = (uploads[i].caseNo * 1000000000)  + last_index;
                documents[docid] = uploads[i];
                documents[docid].documentId = docid;
                documents[docid]._timeStamp = block.timestamp;
                documents[docid]._issuer = msg.sender;
                cases[ documents[docid].caseNo ].documentIds.push((uploads[i].caseNo * 1000000000)  + last_index);
                last_index +=1;
                documentsCount +=1;
            
        }
}




function userCases() external view  returns (uint[]  memory){
    return users[msg.sender].caseIds;
}





function addCases(Case [] calldata caseToadd, uint256 [] calldata caseIds ) external onlyOwner {

    for(uint8 i = 0; i < caseToadd.length; i++){
        if( users[caseToadd[i].incharge].isActive){
            if(users[caseToadd[i].incharge].usertype == userType.USER){
                users[caseToadd[i].incharge].usertype = userType.ISSUER;
            }
            cases[caseIds[i]] = caseToadd[i];
            users[ caseToadd[i].incharge ].caseIds.push( caseIds[i] );
    }
    }
    }

function changeInCharge(uint256 [] calldata caseIds, address [] calldata addresses ) external onlyOwner  {
    for(uint8 i = 0; i < caseIds.length ; i++){
        if (cases[caseIds[i]].incharge == addresses[i]){ continue ;}
        if(users[addresses[i]].usertype != userType.ISSUER){
            users[addresses[i]].usertype = userType.ISSUER;
        }
        
        for(uint8 j = 0; j < users[cases[caseIds[i]].incharge].caseIds.length  ; j++){
            // get index of caseid in curr owner to delete
            if( users[cases[caseIds[i]].incharge ].caseIds[j] == caseIds[i] ){

                uint256 len = users[cases[caseIds[ i]].incharge ].caseIds.length;
                users[cases[caseIds[i]].incharge ].caseIds[j] = users[cases[caseIds[i]].incharge ].caseIds[len-1];
                users[cases[caseIds[i]].incharge ].caseIds.pop();
                users[addresses[i]].caseIds.push(caseIds[i]);
                cases[caseIds[i]].incharge = addresses[i];
                break;
            }
        }
    }
}



function allCases() external view onlyOwner returns (IOCases [] memory , address []  memory, string[] memory){
    uint256 len = 0;
    for (uint256 i = 0; i < userIds.length; i ++){
        len += users[userIds[i]].caseIds.length;
    }
    IOCases [] memory  iocases= new IOCases[](len);
    len = 0;

    for (uint256 i = 0; i < userIds.length; i ++){
        for (uint256 j = 0 ; j < users[userIds[i]].caseIds.length; j++){
            iocases[len].caseNo = users[userIds[i]].caseIds[j];
            iocases[len].CaseName = cases[users[userIds[i]].caseIds[j]].caseName;
            len+=1;
        }
    }
    for (uint256 j = 0 ; j < removedCaseIds.length; j++){
            iocases[len].caseNo = removedCaseIds[j];
            iocases[len].CaseName = cases[removedCaseIds[j]].caseName;
            len+=1;
        }
    string [] memory names = new string[] (userIds.length);
    for(uint256 i = 0 ; i < userIds.length; i++){
        names[i] = users[userIds[i]].username;
    } 
    return (iocases,userIds, names);

}

// function checkRequests() external view validUser returns (uint256 [] memory, string[] memory){
//     uint256 [] memory documentIds = new uint256[](users[msg.sender].sharedDocsRequestIndex.length);
//     string [] memory documentNames = new string[](users[msg.sender].sharedDocsRequestIndex.length);    
//     for (uint8 i = 0; i < users[msg.sender].sharedDocsRequestIndex.length; i++){
//         if (requests[users[msg.sender].sharedDocsRequestIndex[i]].status == Status.PENDING){
//         documentIds[i] = requests[users[msg.sender].sharedDocsRequestIndex[i]].documentId;
//         documentNames[i] = documents[documentIds[i]].documentName;
//     }
//     }
//     return (documentIds, documentNames);
// }

function sendRequests( uint256 [] calldata ids, uint256 [] calldata reqtimes ) external validUser  {

    for (uint8 i = 0; i < ids.length; i++){
        if(cases[ documents[ids[i]].caseNo ].incharge != msg.sender){
            
            if(users[msg.sender].shareddocs[ids[i]] == 0){
                requests[last_index] = Request({
                    sender : msg.sender, 
                    documentId : ids[i], 
                    _timestamp : block.timestamp + 86400, 
                    required_time : reqtimes[i],
                    status : Status.PENDING
            });
                
            // users[msg.sender].sharedDocsRequestIndex.push(last_index);
            cases[ documents[ids[i]].caseNo ].requests.push(last_index);
            last_index +=1;
            }

        }
    }

    
	
}


function checkApprovals() external view validUser returns (IORequest[] memory){
    require (users[msg.sender].usertype == userType.ISSUER, "^User is Not Issuer$");
    uint len = 0;
    for (uint8 i = 0; i < users[msg.sender].caseIds.length; i++){
        len += cases[users[msg.sender].caseIds[i]].requests.length;
    }

    IORequest [] memory reqs = new IORequest[](len);
    len = 0;
    for (uint8 i = 0; i < users[msg.sender].caseIds.length; i++){
        uint[] storage userreqs = cases[users[msg.sender].caseIds[i]].requests;

        for (uint8 j = 0; j < userreqs.length; j++){
            if (requests[userreqs[j]].status == Status.PENDING){
        // timeout requests check no need because refresh every 24 hrs
                reqs[len].index = userreqs[j];
                reqs[len].sender = requests[ userreqs[j] ].sender;
                reqs[len].username = users[reqs[i].sender].username;
                reqs[len].documentId = requests[ userreqs[j] ].documentId;
                reqs[len].documentName = documents[reqs[i].documentId].documentName;
                reqs[len]._timestamp = requests[userreqs[j]]._timestamp;
                reqs[len].required_time = requests[userreqs[j]].required_time;
                len+=1;
    }
    }
    }
    return reqs ;
}




function approveRequests(uint[] calldata indexes) external validUser  {
    // add index to sharedDocsRequestIndex 
    // change requets status to approve
    require (users[msg.sender].usertype == userType.ISSUER, "^User is Not Issuer$");
    for (uint256 i = 0; i < indexes.length; i++){ 
        if (cases[documents[requests[indexes[i]].documentId].caseNo].incharge == msg.sender){
            users[requests[indexes[i]].sender].sharedDocsRequestIndex.push(indexes[i]);

            requests[indexes[i]].status = Status.APPROVE;
        }
    }
}



function getreqArr(uint index) external view validUser returns (Request memory){

    return requests[index];
}

}
    