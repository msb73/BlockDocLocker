from pinatapy import PinataPy
import requests
from django.contrib import messages



pinata = PinataPy('b23b221199fef9d86294', '1ac12d07f25c60db854d9f256b1f8d7c549c9ef95cdf2015704dced771cad375')

def upload(file):
    file=pinata.pin_file_to_ipfs(file)
    return(file.get('IpfsHash'))   


def retrive():
    uid='QmeBsXh9CS3tCSvDWT1agkf9a9uJ77xcizdRbE6vPt4etM'
    url='https://ipfs.io/ipfs/'+uid
    response = requests.get(url)
    if response is not None:
        return (response)   

