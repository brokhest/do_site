import requests

import re

class Client(object):



    def register(login, password):
        s = requests.Session()
        url = "http://167.99.245.100/register"
        s.get(url)
        # print(s.cookies)
        csrf_token = s.cookies['csrftoken']
        data = {'username': login, 'password1': password, 'password2': password,'csrfmiddlewaretoken':csrf_token}
        # s.cookies.clear()
        # s.cookies.set("X-CSRFToken", csrf_token, domain="167.99.24.100")
        s.post(url,data)
        return 1

    def login(login, password):
        s = requests.Session()
        url = "http://167.99.245.100/login"
        s.get(url)
        csrf_token = s.cookies['csrftoken']
        data = {'username': login, 'password': password, 'csrfmiddlewaretoken': csrf_token}
        s.post(url, data)
        return s

    def add_task(self,login, password, task_name, task_desc=None):
        s = self.login(login, password)
        csrf_token = s.cookies['csrftoken']
        data = {'title': task_name, 'desc': task_desc,'csrfmiddlewaretoken': csrf_token }
        url = "http://167.99.245.100/task/add"
        s.post(url,data)
        return 1

    def delete_task(self, login, password, task_name):
        s = self.login(login, password)
        csrf_token = s.cookies['csrftoken']
        s.get("http://167.99.245.100/")
        url = re.search('a href="/task(.*)'+task_name,s.get("http://167.99.245.100/").text)
        if url != None:
            s.post("http://167.99.245.100/task-delete/"+url.group(0).split("/")[2]+'/',data={'csrfmiddlewaretoken': csrf_token})
            return 1
        return 0

    def update_task(self, login, password, task_name, new_task_name=None, task_description=None, task_completion=None):
        s = self.login(login, password)
        csrf_token = s.cookies['csrftoken']
        s.get("http://167.99.245.100/")
        url = re.search('a href="/task(.*)' + task_name, s.get("http://167.99.245.100/").text)
        if url == None:
            return 0
        task_url="http://167.99.245.100/task-update/"+url.group(0).split("/")[2]+'/'
        page = s.get(task_url).text
        if new_task_name == None:
            new_task_name = re.search('name="title" value="(.*)"',page).group(0).split('"')[3]
        if task_description == None:

            task_description = re.search('(.*)</textarea>',page).group(0).split('<')[0]
        if task_completion==None:
            task_completion = re.search('id="id_completion"(.*)</p>',page).group(0)
            task_completion = re.findall('checked',task_completion)
            if not task_completion:
                task_completion=False
            else:
                task_completion=True
        data={'title': new_task_name, 'desc': task_description, 'completion': task_completion, 'csrfmiddlewaretoken': csrf_token}
        s.post(task_url,data)
        return 1





