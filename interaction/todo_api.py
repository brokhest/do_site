from pickle import FALSE
import requests
import re
import json

class Client(object):
    
    def register(login, password):
        
        url = "http://127.0.0.1:8000/todo/register/"

        
        data = {
            "user":{
                "username": login,
                "password": password
            }
        }
        headers = {'Content-Type': "application/json", "Accept": "*/*"}
        res = requests.post(url,data=json.dumps(data), headers=headers)
        return 1

    def login(login,password):
        #r = requests.request()
        url = "http://127.0.0.1:8000/todo/login/"

        data = {
            "user":{
                "username": login,
                "password": password
            }
        }
        headers = {'Content-Type': "application/json", "Accept": "*/*"}
        res = requests.post(url, data=json.dumps(data), headers=headers).text
        #data = res.text
        data = json.loads(res)
        #token = res.json('user')['token']
        return data['token']

    def add_task(self, login, token, task_title, task_desc=""):
        #token = self.login(login, password)
        url = "http://127.0.0.1:8000/todo/task_list/"
        data = {
            "user":{
                "login": login
            },
            "task":{
                "title": task_title,
                "desc": task_desc,
                "completion": False
            }
        }
        headers = {'Content-Type': "application/json", "Accept": "*/*", "Authorization": "Token "+ token}
        #print (json.dumps(data))
        res = requests.post(url, data=json.dumps(data), headers=headers)
        return 1

    def get_task_all(self, login, token):
        url = "http://127.0.0.1:8000/todo/task_list/"
        data = {
        "user":{
            "login": login
        }
        }
        headers = {'Content-Type': "application/json", "Accept": "*/*", "Authorization": "Token "+ token}
        res = requests.get(url, data=json.dumps(data), headers=headers)
        #print (res.text)
        return res
    def get_task(self, login, token, task_title):
        res = self.get_task_all(self, login, token)
        tasks = json.loads(res.text)
        for task in tasks:
            if task["title"] == task_title:
                url = "http://127.0.0.1:8000/todo/task_get/"+str(task['pk'])
                data = {
                    "user":{
                        "login": login,
                
                            }
                        }
                headers = {'Content-Type': "application/json", "Accept": "*/*", "Authorization": "Token "+ token}
                res = requests.get(url,data=json.dumps(data), headers=headers)
                print (res.text)
                return res
                
        return 0
        

    def update_task(self, login, token, task_title, new_task_title=None, task_desc = None, task_completion = None):
        res = self.get_task_all(self, login, token)
        tasks = json.loads(res.text)
        for task in tasks:
            if task["title"] == task_title:
                url = "http://127.0.0.1:8000/todo/task_list/"+str(task['pk'])
                if new_task_title is None:
                    new_task_title = task['title']
                if task_desc is None:
                    task_desc = task['description']
                if task_completion is None:
                    task_completion = task['completion']
                data = {
                    "user":{
                        "login": login
                    },
                    "task":{
                        "title": new_task_title,
                        "desc": task_desc,
                        "completion": task_completion
                    }
                }
                headers = {'Content-Type': "application/json", "Accept": "*/*", "Authorization": "Token "+ token}
                res = requests.put(url,data=json.dumps(data), headers=headers)
                #print(res.text)
                return res
            
        return 0

    def delete_task(self, login, token, task_title):
        res = self.get_task_all(self, login, token)
        tasks = json.loads(res.text)
        for task in tasks:
            if task["title"] == task_title:
                url = "http://127.0.0.1:8000/todo/task_list/"+str(task['pk'])
                data = {
                    "user":{
                        "login": login
                    }
                }
                headers = {'Content-Type': "application/json", "Accept": "*/*", "Authorization": "Token "+ token}
                res = requests.delete(url,data=json.dumps(data), headers=headers)
                #print(res.text)
                return res
        return 0
    


