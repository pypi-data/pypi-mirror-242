# -*- coding: UTF-8 -*-
from .result import ResultsCollectorJSONCallback
from ansible import context
from ansible.module_utils.common.collections import ImmutableDict
from ansible.parsing.dataloader import DataLoader
from ansible.inventory.manager import InventoryManager
from ansible.vars.manager import VariableManager
from ansible.playbook.play import Play
from ansible.executor.task_queue_manager import TaskQueueManager
import shutil
import ansible.constants as C
import json
import ansible
from ansible.executor.playbook_executor import PlaybookExecutor


class AnsibleApi:
    def __init__(self,
                 connection='smart',
                 hosts: list[str] = None,
                 remote_user=None,
                 remote_password=None,
                 private_key_file=None,
                 become=None,
                 become_method=None,
                 become_user=None,
                 verbosity=3,
                 ):
        context.CLIARGS = ImmutableDict(
            connection=connection,
            remote_user=remote_user,
            private_key_file=private_key_file,
            become=become,
            become_method=become_method,
            become_user=become_user,
            verbosity=verbosity,
            check=False, diff=False, syntax=None, start_at_task=None, isthosts=None, listtasks=None, listtags=None
        )
        self.hosts = hosts
        self.sources = ','.join(hosts)
        if len(hosts) == 1:
            self.sources += ','
        self.loader = DataLoader()
        self.inv_obj = InventoryManager(loader=self.loader, sources=self.sources)

        self.password = remote_password
        self.results_callback = ResultsCollectorJSONCallback()
        self.variable_manager = VariableManager(self.loader, self.inv_obj)

        ansible.constants.HOST_KEY_CHECKING = False
        ansible.constants.DEPRECATION_WARNINGS = False

    def run(self, module, args='', task_time=0):
        play_source = dict(
            name="Ad-hoc",
            hosts=self.hosts,
            gather_facts="no",
            tasks=[
                {"action": {"module": module, "args": args}, "async": task_time, "poll": 0}
            ],
        )
        play = Play().load(play_source, variable_manager=self.variable_manager, loader=self.loader)
        tqm = None
        try:
            tqm = TaskQueueManager(
                inventory=self.inv_obj,
                variable_manager=self.variable_manager,
                loader=self.loader,
                passwords=self.password,
                stdout_callback=self.results_callback
            )
            tqm.run(play)
        except Exception as e:
            raise e
        finally:
            if tqm is not None:
                tqm.cleanup()
            shutil.rmtree(C.DEFAULT_LOCAL_TMP, True)

    def playbook(self, playbooks, dynamic_inv: dict):
        try:
            inventory = InventoryManager(loader=self.loader, sources=None)
            for group in dynamic_inv.keys():
                inventory.add_group(group)
                host_list = dynamic_inv.get(group)
                for host in host_list:
                    inventory.add_host(host, group=group)

            variable_manager = VariableManager(self.loader, inventory)
            playbook = PlaybookExecutor(
                playbooks=playbooks,
                inventory=inventory,
                variable_manager=variable_manager,
                loader=self.loader,
                passwords=self.password
            )
            playbook.run()
        except Exception as e:
            raise e

    def get_result(self):
        result_raw = {'success': {}, 'failed': {}, 'unreachable': {}}

        for host, result in self.results_callback.host_ok.items():
            result_raw['success'][host] = result._result
        for host, result in self.results_callback.host_failed.items():
            result_raw['failed'][host] = result._result
        for host, result in self.results_callback.host_unreachable.items():
            result_raw['unreachable'][host] = result._result

        return json.dumps(result_raw)
