# awsome-validity  
A simple SDK to use Ansible API.

# usage  
> pip install ansbile-simple  

## ansbile module  
```python
from ansbile-simple.core.api import AnsibleApi

a = AnsibleApi(remote_user="root", hosts=["192.168.13.109", "192.168.13.56"], remote_password={"conn_pass": "password"})
# a.run(module='shell', args='hostname')
# print(a.get_result())
```


## ansible playbook  
```yaml
- name: mydbserver
  hosts: mydbserver
  gather_facts: no
  tasks:
    - name: uptime
      raw: uptime
      register: uptime
    - debug:
        msg: "{{ uptime.stdout }}"
    - name: online pm2 ls
      raw: ls
      register: ls
    - debug:
        msg: "{{ ls.stdout }}"
```
```python
a.playbook(dynamic_inv={"mydbserver":["192.168.13.109", "192.168.13.56"]}, playbooks=['test.yml'])
# print(a.get_result())
```


# reference
> https://packaging.python.org/en/latest/tutorials/packaging-projects/  
> https://docs.ansible.com  