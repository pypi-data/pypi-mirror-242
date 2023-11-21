from airflow.models.baseoperator import BaseOperator
import requests
from airflow.models import Variable

class YeeduOperator(BaseOperator):
    def __init__(self,tenant_id,job_conf_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tenant_id = tenant_id
        self.job_conf_id = job_conf_id 

    def GenerateToken(self,tenant_id):
        username = Variable.get("MY_USERNAME")
        password = Variable.get("MY_PASSWORD")
        login_url = 'http://10.4.6.104:8080/api/v1/login'
        data = {
            'username': username,
            'password': password,
            'timeout': '48'
        }
        response = requests.post(login_url, json=data)
        result = response.json()
        token = result.get('token')
        headers = {
            'accept': 'application/json',
            'Authorization': f"Bearer {token}",
            'Content-Type': 'application/json'
        }
        associate_url = f'http://10.4.6.104:8080/api/v1/user/select/{tenant_id}'
        response = requests.post(associate_url, headers=headers)
        associate_message = response.json()
        print(associate_message)
        return token

    def job_submit(self,job_conf_id,token):

        headers = {
            'accept': 'application/json',
            'Authorization': f"Bearer {token}",
            'Content-Type': 'application/json'
        }
        job_url = 'http://10.4.6.104:8080/api/v1/spark/job'
        
        data = {
            'job_conf_id': job_conf_id
        }
        response = requests.post(job_url, headers=headers,json=data)
        result = response.json()
        print(result)
        job_id = result.get('job_id')
        return job_id
    
    def get_job_status(self,job_id,token):

        job_status_url = f'http://10.4.6.104:8080/api/v1/spark/job/{job_id}'
        headers = {
            'accept': 'application/json',
            'Authorization': f"Bearer {token}",
            'Content-Type': 'application/json'
        }
        response = requests.get(job_status_url, headers=headers)
        result = response.json()
        job_status = result.get('job_status')
        print(job_status)

    def execute(self, context):
        
        token = self.GenerateToken(self.tenant_id)
        job_id = self.job_submit(self.job_conf_id,token)
        status = self.get_job_status(job_id,token)


