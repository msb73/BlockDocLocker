import json
from datetime import datetime as dt
from django.utils.html import format_html
from .names import *
from .ipfs import upload
from django.urls import reverse
# table View

class Mapping:
    def get_context(context):
        return {"web3method" : context,
                   "redirect" : reverse(context)} 
    
    def down_view_documents(data ) -> list[dict]:
        ls = []
        for i in json.loads(data):
                    ls.append({
                        tableViewDocs[0] : i[0],
                        tableViewDocs[1] : int(i[1]),
                        tableViewDocs[2] : int(i[2]),
    		    	    tableViewDocs[3] : format_html("<a href = '{}' target='_blank'> Click </a>","https://ipfs.io/ipfs/"+ i[3]),
    		    	    tableViewDocs[4] : dt.fromtimestamp((int)(i[4])),
    		    	    tableViewDocs[5] : i[6], 
                    })
        return (ls)
    
    def down_user_cases(data : str) -> list[int]:
        return [(int(i), int(i)) for i in json.loads(data)] 

    def down_check_approvals(data : str) -> list[dict]:
        ls = []
        for i in json.loads(data):
            ls.append({
                tableCheckApprovals[0] : i[3], 
                tableCheckApprovals[1] :i[4], 
                tableCheckApprovals[2] : i[2],
                tableCheckApprovals[3] :dt.fromtimestamp((int)(i[5])) , 
                tableCheckApprovals[4] : dt.fromtimestamp((int)(i[6])),
	            "CheckBox" : format_html(f"<input type='checkbox' id='option{i[0]}' name='selected_options' value='{i[0]}' onclick='updateSessionStorage(this)'> "), 
                    })
        return ls

    def down_all_cases(self, dic) -> (list[tuple], list[tuple]):
        # allCases I/P -> {'0': [['102', 'Ginson vs Yogi']], '1': ['0x28379662D72D25660af75b7F71D645303713C1cf', '0xbd5E32346805A87aaBD814D495404F6c04eB89a9'], '2': ['owner', 'Milind']}
        cases, users = [] , []
        # dic = json.loads(data)
        # cases
        for i in dic["0"]:
            cases.append((i[0] +  "          "  + i[1], i[0]))    

        for i in range(len(dic["1"])):
            users.append((dic["1"][i] +  "              " + dic["2"][i], dic["1"][i]))
        return (cases, users)

    def down_all_users(data : str) -> list[tuple]:
        ls = []
        addressName = json.loads(data)
        for i in range(len(addressName["0"])):
            ls.append(
                (addressName["0"][i], addressName["1"][i] +  "              " + addressName["0"][i])
            )
        return ls

    def down_all_documents(data: str) -> list[dict]:
        data = json.loads(data)
        case_data = {}
        #{"0":[["case101-1","101000000003"],["case102-1","102000000001"],["case102-2","102000000002"],["","0"]],"1":["0","3"],"2":["Owner","Sagar"]}            case_data = {}
        # it = iter(data["2"])
        # case_data = {
        #     'case1': [{'documentId': 'doc1', 'issuer': 'Issuer1'}, {'documentId': 'doc2', 'issuer': 'Issuer2'}],
        #     'case2': [{'documentId': 'doc3', 'issuer': 'Issuer3'}, {'documentId': 'doc4', 'issuer': 'Issuer4'}],
        # }
        for v in data["0"]:
            if v[0]:
                if v[1][:5] in case_data:
                    case_data[v[1][:5]].append({formCheckRequests[0]: int(v[1]), formCheckRequests[1] : v[0]})
                else:
                    case_data[v[1][:5]] = [{formCheckRequests[0] : int(v[1]), formCheckRequests[1] : v[0]}]
        return case_data

    def down_check_requests(self, data : str):
        ls = []
        data = json.loads(data)
        for i in range(len(data["0"])):
            if data["0"][i] == "0":
                continue
            ls.append({
                "documentName" : data["1"][i],
                "documentId" : data["0"][i]
            })
            

class UPMapping:
    
    def get_context(context, func = None, data = None,**kwargs):
        return {"web3method" : context,
                   "content" : func(data = data)}
              
    def up_approve_requests(data):
        return json.loads(data)
    
    def up_send_requests(data):
        print("called")
        dic = data.copy()
        # ids = len(data) -2
        # for i in range(ids):
        ls = [[], []]
        dic.pop("csrfmiddlewaretoken") 
        dates = iter(dic.pop("dates"))
        for key in dic.keys():
            for documentId in dic.getlist(key):
                print(documentId)
                ls[0].append(int(documentId))
                ls[1].append( int(dt.timestamp(dt.strptime(next(dates), "%Y-%H-%d"))) )
                              
        return ls    
            
        # print(dates)
        # [('csrfmiddlewaretoken', 'kbmaZP3Gsoin2bxWAw3e6JEF7WUPo4uUr7lNt257tXYOzeNTF8kT2IGj9OJqKV9n'), ('case_10100', '101000000003'), ('dates', '2024-01-13'), ('case_10200', '102000000001')]
        # print(list(data.items()))
            
    def up_add_users(data):
        ls = []
        userId = data.getlist(formAddUser[0])
        username = data.getlist(formAddUser[1])
        deptNumber = data.getlist(formAddUser[2])
        userType = data.getlist(formAddUser[3])
        for i in range(len(username)):
            ls.append([ userId[i], userType[i], username[i], deptNumber[i] ])
        return ls
            
    def up_add_cases(data):
        caseName = data.getlist(formAddCases[0])
        caseNo = data.getlist(formAddCases[1])
        incharge = data.getlist(formAddCases[2])
        ls = []
        for i, j in zip(caseName,  incharge):
            ls.append([i, [], j, []])
        return [ls, caseNo]
    
    def up_remove_users(data):
        return [i for i in data.getlist("users")]
    
    def up_change_incharge(data):
        ls = [[], []]
        for case, user in zip(data.getlist("cases"), data.getlist("users")):
            ls[0].append(int(case))
            ls[1].append(user)
        return ls
    
    def up_upload_documents(cls, data, **kwargs):
        documentName = data.getlist(formUploadDocuments[0])
        caseNo = data.getlist(formUploadDocuments[1])
        files = kwargs["form"].cleaned_data[formUploadDocuments[2]]
        description = data.getlist(formUploadDocuments[3])
        ls = []
        for i, file in enumerate(files):
            doctype= file.content_type
            for _ in range(3):
                cid = False
                cid = upload(file, "None")
                if cid: break
            else:   raise ValueError(f"CID cannot be created please try later  {file.name}")
            ls.append([
                documentName[i], int(caseNo[i]), 0000000, cid, 0000000, doctype , "0x0000000000000000000000000000000000000000", description[i]
            ])
        return ls

