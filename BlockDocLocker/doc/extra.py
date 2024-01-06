import json
import datetime as dt
from django.utils.html import format_html
from .names import *
from .tables import ViewTable 
from datetime import datetime, timedelta

from django.urls import reverse
# table View

class Template:
    def down_mapping(self):
        pass
    def up_mapping(self):
        pass

class ViewDocuments:
    pass

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
    		    	    tableViewDocs[4] : dt.datetime.fromtimestamp((int)(i[4])),
    		    	    tableViewDocs[5] : i[6], 
                    })
        return (ls )
    
    # for table View form
    def down_check_approvals(self, data : str) -> list[dict]:
        ls = []
        for i in json.loads(data):
            ls.append({
                "documentId" : i[3], 
                "documentName" :i[4], 
                "issuerName" : i[2],
                "timestamp" :dt.datetime.fromtimestamp((int)(i[5])) , 
                "AskedTime" : dt.datetime.fromtimestamp((int)(i[6])),
	            "CheckBox" : format_html(f"<input type='checkbox' id='option{i[0]}' name='selected_options' value='{i[0]}' onclick='updateSessionStorage(this)'> "), 
                    })

    # for 2 drop down
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

    # for drop down
    def down_all_users(self, data : str) -> list[tuple]:
        users = []
        dic = json.loads(data)
        for i in range(len(dic["0"])):
            users.append(
                (dic["0"][i] +  "              " + dic["1"][i], dic["1"][i])
            )

    # for table form view   
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

    # for table view
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
    def get_context(context):
        return {"web3method" : context,
                   "content" : None}
              
    def up_approve_requests(data):
        return json.loads(data)
    
    def up_send_requests(data):
        data = json.loads(data)
        ids = len(data) -2
        # for i in range(ids):
        dates = data.pop("data")
        
    
    def up_add_users(self, data):
        pass
    
    def up_add_cases(self, data):
        pass
    
    def up_change_incharge(self, data):
        pass
    
    def remove_users(self, data):
        pass
    
    def up_upload_documents(self, data):
        pass


