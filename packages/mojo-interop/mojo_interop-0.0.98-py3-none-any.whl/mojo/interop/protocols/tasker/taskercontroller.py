"""
.. module:: taskercontroller
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: The :class:`TaskerController` package contains the controller object used to create a distributed
               network of :class:`TaskerService` objects.

.. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2023, Myron W Walker"
__credits__ = []
__version__ = "1.0.0"
__maintainer__ = "Myron Walker"
__email__ = "myron.walker@gmail.com"
__status__ = "Development" # Prototype, Development or Production
__license__ = "MIT"


from typing import List, Optional, Type, Union

from mojo.errors.exceptions import NotOverloadedError, SemanticError

from mojo.results.model.taskingresult import TaskingResult

from mojo.interop.protocols.tasker.itaskingsequencer import ITaskingProtocol
from mojo.interop.protocols.tasker.taskeraspects import TaskerAspects, DEFAULT_TASKER_ASPECTS
from mojo.interop.protocols.tasker.tasking import Tasking, TaskingIdentity
from mojo.interop.protocols.tasker.taskernode import TaskerNode, TaskerClientNode
from mojo.interop.protocols.tasker.taskingresultpromise import TaskingResultPromise
from mojo.interop.protocols.tasker.taskerservice import TaskerService
from mojo.interop.protocols.tasker.taskerservermanager import TaskerServerManager, spawn_tasking_server_process

from mojo.xmods.landscaping.client.clientbase import ClientBase


TASKER_PORT = 8686

class TaskerController:
    """
        The :class:`TaskerController` object lets you startup and control task processing across
        a collection of clients.
    """

    def __init__(self, logging_directory: Optional[str] = None,
                 aspects: Optional[TaskerAspects] = DEFAULT_TASKER_ASPECTS):
        self._logging_directory = logging_directory
        self._aspects = aspects

        self._tasker_nodes: List[TaskerNode] = []
        self._network_started = False
        return

    @property
    def tasker_clients(self) -> List[ClientBase]:
        clients = [ tn.client for tn in self._tasker_nodes]
        return clients

    @property
    def tasker_nodes(self):
        return self._tasker_nodes


    def execute_tasking_on_all_nodes(self, *, tasking: Union[TaskingIdentity, Type[Tasking]], parent_id: str = None,
                                     aspects: Optional[TaskerAspects] = None, **kwargs) -> List[TaskingResultPromise]:

        if aspects is None:
            aspects = self._aspects

        promise_list = []

        if not isinstance(tasking, TaskingIdentity):
            tasking = tasking.get_identity()
        module_name, tasking_name = tasking.as_tuple()

        for node in self._tasker_nodes:
            promise = node.execute_tasking(module_name=module_name, tasking_name=tasking_name, parent_id=parent_id, aspects=aspects, **kwargs)
            promise_list.append(promise)

        return promise_list

    def execute_tasking_on_node(self, node: TaskerNode, *, tasking: Union[TaskingIdentity, Type[Tasking]], parent_id: str = None,
                                aspects: Optional[TaskerAspects] = None, **kwargs) -> TaskingResultPromise:

        if aspects is None:
            aspects = self._aspects

        promise = None

        if not isinstance(tasking, TaskingIdentity):
            tasking = tasking.get_identity()
        module_name, tasking_name = tasking.as_tuple()
        
        promise = node.execute_tasking(module_name=module_name, tasking_name=tasking_name, parent_id=parent_id, aspects=aspects, **kwargs)

        return promise

    def execute_tasking_on_node_list(self, node_list: List[TaskerNode], *, tasking: Union[TaskingIdentity, Type[Tasking]], parent_id: str = None,
                                     aspects: Optional[TaskerAspects] = None, **kwargs) -> List[TaskingResultPromise]:

        if aspects is None:
            aspects = self._aspects

        promise_list = []

        if not isinstance(tasking, TaskingIdentity):
            tasking = tasking.get_identity()
        module_name, tasking_name = tasking.as_tuple()

        for node in node_list:
            promise = node.execute_tasking(module_name=module_name, tasking_name=tasking_name, parent_id=parent_id, aspects=aspects, **kwargs)
            promise_list.append(promise)

        return promise_list

    def reinitialize_logging_on_nodes(self, *, logging_directory: Optional[str] = None,
                                      logging_level: Optional[int] = None,
                                      taskings_log_directory: Optional[str] = None,
                                      taskings_log_level: Optional[int] = None):

        for node in self._tasker_nodes:
            node.reinitialize_logging(logging_directory=logging_directory, logging_level=logging_level,
                                      taskings_log_directory=taskings_log_directory, taskings_log_level=taskings_log_level)

        return

    def set_notify_parameters_on_nodes(self, *, notify_url: str, notify_headers: dict):

        for node in self._tasker_nodes:
            node.set_notify_parameters(notify_url=notify_url, notify_headers=notify_headers)

        return

    def start_tasker_network(self):
        """
        """
        raise NotOverloadedError("The 'start_task_network' method must be overloaded.")


    def wait_for_tasking_results(self, promises: List[TaskingResultPromise],  aspects: Optional[TaskerAspects] = None) -> List[TaskingResult]:
        
        if aspects == None:
            aspects = self._aspects

        timeout = None
        interval = None
        if aspects is not None:
            timeout = aspects.completion_timeout
            interval = aspects.completion_interval

        wait_on = [ np for np in promises ]

        while len(wait_on) > 0:
            np = wait_on.pop()
            np.wait(timeout=timeout, interval=interval)

        results = []
        for np in promises:
            nxtres = np.get_result()
            results.append(nxtres)

        return results


class ProcessTaskerController(TaskerController):

    def __init__(self, logging_directory: Optional[str] = None, aspects: Optional[TaskerAspects] = None):
        super().__init__(logging_directory=logging_directory, aspects=aspects)

        self._svr_manager: List[TaskerServerManager] = []
        self._svr_proxies: List[TaskerService] = []
        return

    def start_tasker_network(self, node_count=5, notify_url: Optional[str] = None, notify_headers: Optional[dict] = None):
        """
        """

        if self._network_started:
            errmsg = "A task network has already been started."
            raise SemanticError(errmsg)

        self._network_started = True

        for _ in range(node_count):
            svr_mgr, tasking_svr_proxy = spawn_tasking_server_process(('0.0.0.0', 0), logging_directory=self._logging_directory)

            tasking_svr_proxy.start()

            self._svr_manager.append(svr_mgr)
            self._svr_proxies.append(tasking_svr_proxy)

            ipaddr, port = tasking_svr_proxy.get_service_endpoint()

            node = TaskerNode(ipaddr=ipaddr, port=port)
            
            if notify_url is not None:
                node.set_notify_parameters(notify_url=notify_url, notify_headers=notify_headers)

            self._tasker_nodes.append(node)

        return


class ClientTaskerController(TaskerController):

    def __init__(self, logging_directory: Optional[str] = None, aspects: Optional[TaskerAspects] = None):
        super().__init__(logging_directory=logging_directory, aspects=aspects)
        return

    def start_tasker_network(self, clients: List[ClientBase], notify_url: Optional[str] = None, notify_headers: Optional[dict] = None):
        """
        """

        if self._network_started:
            errmsg = "A task network has already been started."
            raise SemanticError(errmsg)

        self._network_started = True

        for cl in clients:

            node = TaskerClientNode(client=cl, ipaddr=cl.ipaddr, port=TASKER_PORT)
            
            if notify_url is not None:
                node.set_notify_parameters(notify_url=notify_url, notify_headers=notify_headers)

            self._tasker_nodes.append(node)

        return

