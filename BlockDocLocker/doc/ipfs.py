from pinatapy import PinataPy
import requests
from django.contrib import messages
import os
from dotenv import load_dotenv
load_dotenv()
pinata = PinataPy(os.getenv("JSWT"), os.getenv("PINATA_API_KEY"))

def upload(file, description):
    response=pinata.pin_file_to_ipfs(file, 
                                 options= {"pinataMetadata" : {
                                     "name" : file.name,
                                     "fileType" : file.content_type,
                                     "description" : description
                                 }}
                                 )
    
    print(response)
    if response.get("isDuplicate"):
        raise ValueError("Document Already exists")
    return(response.get('IpfsHash'))


def retrive(cid):
    url='https://ipfs.io/ipfs/'+cid
    response = requests.get(url)
    if response is not None:
        return (response)
# files = upload('D:\arch\Documents\BlockDocLocker\BlockDocLocker\doc\tests.py')