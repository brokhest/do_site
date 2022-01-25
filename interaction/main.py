from multiprocessing.connection import Client
from pydoc import cli
from todo_api import Client
from files_api import Files_client


login = "from api"
password = "Test_pas1"
test_client = Client
#token = test_client.login(login, password)
#test_client.delete_task(test_client, login, token, "Prikoli")
files = Files_client
#files.get_files()
#files.post_file("steam acc.txt")
files.delete_file("steam acc.txt")
#test_client.register(login, password)
# test_client.login(login, password)
#test_client.add_task(test_client,login, token, 'Задача из клиента')
#print (test_client.login(login, password))
#print(test_client.add_task(test_client, login, password, "from libraty"))
#test_client.get_task_all(test_client, login, token)
#test_client.delete_task(test_client, login, token, "super_prikoli")