from pinatapy import PinataPy
import requests
from django.contrib import messages

pinata = PinataPy('a2aa63cbb182b72917e7', '179903210e9d74976eb37dfcbac17acda31fd581080244ba6fa68f556da0e236')

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