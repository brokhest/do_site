import requests

class Files_client(object):

    def get_files():
        url = "http://127.0.0.1:8000/files/"
        res = requests.get(url)
        print (res.text)
        return res
    
    def delete_file(name):
        url = "http://127.0.0.1:8000/files/"+name
        res = requests.delete(url)
        print (res)
        return res

    def post_file(name):
        files ={
            'file':open(name, 'rb')
        }
        url = "http://127.0.0.1:8000/files/"
        res = requests.post(url,files=files)
        print (res.text)
        return 1
        