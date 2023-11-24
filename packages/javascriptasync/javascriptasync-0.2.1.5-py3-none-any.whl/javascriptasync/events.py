from __future__ import annotations
import asyncio
import time, threading, json, sys
from typing import Any, Callable, Dict, List, Tuple

from . import pyi, config
from queue import Queue
from weakref import WeakValueDictionary
from .core.abc import (
    ThreadTaskStateBase,
    EventLoopBase
)

from .core.jslogging import(
    log_debug,
    log_print,
)

from .connection import ConnectionClass
from .util import generate_snowflake
from .asynciotasks import EventLoopMixin


class CrossThreadEvent(asyncio.Event):
    """Initalize Asyncio Event and pass in a specific
    Asyncio event loop, and ensure that the event can be
    Set outside an asyncio event loop."""

    def __init__(self, _loop=None, *args, **kwargs):
        self._loop=None
        super().__init__(*args, **kwargs)
        if self._loop is None:
            self._loop = _loop

    def set(self):
        self._loop.call_soon_threadsafe(super().set)

    def clear(self):
        self._loop.call_soon_threadsafe(super().clear)


class ThreadState(ThreadTaskStateBase):
    """
    Represents the state of a wrapped "AsyncThread" function.

    This should be the first parameter to all wrapped "AsyncThread" functions.

    Attributes:
        stopping (bool): When this is set to true, the "AsyncThread" function should stop.
        sleep (function): Alias for the wait function.
    """

    def __init__(self):
        self.stopping: bool = False
        self.sleep: Callable = self.wait

    def wait(self, sec: float):
        """
        Wait for a specified duration, and will automatically exit the process once self.stopping is true.

        Args:
            sec (float): The duration to wait in seconds.
        """

        stop_time = time.time() + sec
        while time.time() < stop_time and not self.stopping:
            time.sleep(0.2)
        if self.stopping:
            # This feels unsafe, but it works for threads.
            # Will remove when I find something I consider safer.
            sys.exit(1)


class EventExecutorThread(threading.Thread):
    """Represents a thread for executing Pythonside Callbacks.

    Attributes:
        running (bool): Indicates whether the thread is running.
        jobs (Queue[Tuple(str,str,Callable,Tuple[Any, ...])]): A queue for storing jobs to be executed.
        doing (list): A list of jobs currently being executed.
    """

    def __init__(self):
        self.doing: List[Any] = []
        self.running: bool = True
        self.jobs: Queue[Tuple(str, str, Callable, Tuple[Any, ...])] = Queue()
        super().__init__(daemon=True)
        # self.daemon=True

    def add_job(self, request_id, cb_id, job, args):
        """
        Add a job to the event executor thread.

        Args:
            request_id: The ID of the request.
            cb_id: The ID of the callback.
            job: The job function to execute.
            args: Arguments for the job.
        """
        if request_id in self.doing:
            return  # We already are doing this
        self.doing.append(request_id)
        self.jobs.put([request_id, cb_id, job, args])

    def run(self):
        """
        Run the event executor thread.
        """
        while self.running:
            request_id, cb_id, job, args = self.jobs.get()
            log_debug("EVT %s, %s,%s,%s", request_id, cb_id, job, args)
            ok = job(args)
            if self.jobs.empty():
                self.doing = []


# The event loop here is shared across all threads. All of the IO between the
# JS and Python happens through this event loop. Because of Python's "Global Interperter Lock"
# only one thread can run Python at a time, so no race conditions to worry about.
class EventLoop(EventLoopBase, EventLoopMixin):
    """
    A shared syncronous event loop which manages all IO between Python and Node.JS.

    Attributes:
        active (bool): Indicates whether the event loop is active.
        queue (Queue): A queue for storing events to be processed.  When a job is added to the queue, the loop continues.
        freeable (list): A list of freeable items.
        callbackExecutor (EventExecutorThread): An event executor thread for handling callbacks.
        callbacks (WeakValueDictionary): A dictionary of active callbacks that are being tracked.
        threads (list): A list of threads managed by the event loop.
        outbound (list): A list of outbound payloads.
        requests (dict): A dictionary of request IDs and locks.
        responses (dict): A dictionary of response data and barriers.
        conn(ConnectionClass): Instance of the connection class.
        conf(JSConfig): The JSConfig instance this class belongs to.
    """

    def __init__(self, config_container: config.JSConfig):
        """
        Initialize the EventLoop.

        Args:
            config_container (config.JSConfig): Reference to the active JSConfig object
        """
        self.active: bool = True
        self.queue = Queue()
        self.freeable = []

        self.callbackExecutor = EventExecutorThread()

        # This contains a map of active callbacks that we're tracking.
        # As it's a WeakRef dict, we can add stuff here without blocking GC.
        # Once this list is empty (and a CB has been GC'ed) we can exit.
        # Looks like someone else had the same idea :)
        # https://stackoverflow.com/questions/21826700/using-python-weakset-to-enable-a-callback-functionality
        self.callbacks = WeakValueDictionary()

        # The threads created managed by this event loop.
        self.threads = []
        self.tasks = []
        self.outbound = []

        # After a socket request is made, it's ID is pushed to self.requests. Then, after a response
        # is recieved it's removed from requests and put into responses, where it should be deleted
        # by the consumer.
        self.requests = {}  # Map of requestID -> threading.Lock
        self.responses = {}  # Map of requestID -> response payload
        self.conn = ConnectionClass(config_container)
        self.conf = config_container
        # if not amode:
        self.conn.start()
        self.callbackExecutor.start()
        self.pyi: pyi.PyInterface = pyi.PyInterface(config_container, self, None)

    # async def add_loop(self):
    #     loop=asyncio.get_event_loop()
    #     self.conn.set_conn(loop)

    # self.callbackExecutor.start()
    def stop(self):
        """
        Stop the event loop.
        """
        self.conn.stop()

    # === THREADING ===
    def newTaskThread(self, handler, *args):
        """
        Create a new task thread.

        Args:
            handler: The handler function for the thread.
            *args: Additional arguments for the handler function.

        Returns:
            threading.Thread: The created thread.
        """
        state = ThreadState()
        t = threading.Thread(target=handler, args=(state, *args), daemon=True)
        self.threads.append([state, handler, t])
        log_debug("EventLoop: adding Task Thread. state=%s. handler=%s, args=%s", str(state), str(handler), args)

        return t

    def startThread(self, method):
        """
        Start a thread.

        Args:
            method: The method associated with the thread.
        """
        for state, handler, thread in self.threads:
            if method == handler:
                thread.start()
                return
        t = self.newTaskThread(method)
        t.start()

    # Signal to the thread that it should stop. No forcing.
    def stopThread(self, method):
        """
        Stop a thread.

        Args:
            method: The method associated with the thread.
        """
        for state, handler, thread in self.threads:
            if method == handler:
                log_debug("EventLoop: stopping thread with handler %s", str(method))
                state.stopping = True

    # Force the thread to stop -- if it doesn't kill after a set amount of time.
    def abortThread(self, method, killAfter=0.5):
        """
        Abort a thread.

        Args:
            method: The method associated with the thread.
            killAfter (float): Time in seconds to wait before forcefully killing the thread.
        """
        for state, handler, thread in self.threads:
            if handler == method:
                state.stopping = True
                killTime = time.time() + killAfter
                log_debug("EventLoop: aborting thread with handler %s, kill time %f", str(method), (killAfter))
                while thread.is_alive():
                    time.sleep(0.2)
                    if time.time() < killTime:
                        thread.terminate()

        self.threads = [x for x in self.threads if x[1] != method]

    # Stop the thread immediately
    def terminateThread(self, method):
        """
        Terminate a thread.

        Args:
            method: The method associated with the thread.
        """
        for state, handler, thread in self.threads:
            if handler == method:
                log_debug("EventLoop: terminate thread with handler %s", str(method))
                thread.terminate()
        self.threads = [x for x in self.threads if x[1] != method]

    # == IO ==

    # `queue_request` pushes this event onto the Payload
    def queue_request(self, request_id, payload, timeout=None, asyncmode=False, loop=None) -> threading.Event:
        """
        Queue a request to be sent with the payload

        Args:
            request_id: The ID of the request.
            payload: The payload to be sent.
            timeout (float): Timeout duration in seconds.

        Returns:
            threading.Event: An event for waiting on the response.
        """
        self.outbound.append(payload)
        if asyncmode:
            lock = CrossThreadEvent(_loop=loop)
        else:
            lock = threading.Event()
        self.requests[request_id] = [lock, timeout]
        log_debug(
            "EventLoop: queue_request. rid %s. payload=%s,  lock=%s, timeout:%s",
            str(request_id),
            str(payload),
            str(lock),
            timeout,
        )
        self.queue.put("send")
        return lock

    def queue_payload(self, payload):
        """
        Just send the payload to be sent.

        Args:
            payload: The payload to be sent.
        """
        self.outbound.append(payload)
        log_debug("EventLoop: added %s to payload", str(payload))
        self.queue.put("send")

    def await_response(self, request_id, timeout=None, asyncmode=False, loop=None) -> threading.Event:
        """
        Await a response for a request.

        Args:
            request_id: The ID of the request.
            timeout (float): Timeout duration in seconds.

        Returns:
            threading.Event: An event for waiting on the response.
        """
        if asyncmode:
            lock = CrossThreadEvent(_loop=loop)
        else:
            lock = threading.Event()
        self.requests[request_id] = [lock, timeout]
        log_debug("EventLoop: await_response. rid %s.  lock=%s, timeout:%s", str(request_id), str(lock), timeout)
        self.queue.put("send")
        return lock

    def on_exit(self):
        """
        Handle the exit of the event loop.
        """
        log_print("calling self.exit")
        log_print(str(self.responses))
        log_print(str(self.requests))
        log_print(str(self.pyi))
        if len(self.callbacks):
            log_debug("%s,%s", "cannot exit because active callback", self.callbacks)
        while len(self.callbacks) and self.conn.is_alive():
            time.sleep(0.4)
        time.sleep(0.8)  # Allow final IO
        self.callbackExecutor.running = False
        self.queue_payload({"r": generate_snowflake(4092, 0), "action": "shutdown"})
        self.queue.put("exit")

    def get_response_from_id(self, request_id: int) -> Tuple[Any, threading.Barrier]:
        """Retrieve a response and associated barrier for a given request ID,
         and then removes it from the internal responces dictionary

        Args:
            request_id (int): The request ID for which the response and barrier are needed.

        Returns:
            Tuple[Any, threading.Barrier]: A tuple containing the response and the
            threading.Barrier associated with the request.

        Raises:
            KeyError: If the specified request ID does not exist in the responses.

        """
        if not request_id in self.responses:
            raise KeyError(f"Response id {request_id} not in self.responses")
        res, barrier = self.responses[request_id]
        del self.responses[request_id]
        return res, barrier
    def process_job(self, job:str, r:int) -> int:
        """
        send/recieve all outbound/inbound messages to/from connection.

        First, the job will be logged for debugging purposes. Then, all outbound messages will be
        sent via the connection. After that, the function will check each thread to see if they are
        still alive, and remove any dead threads from the thread list. 
        If the length of self.freeable exceeds 40,
        a payload to free the job is added to the queue.

        The last part of the process is reading the inbound data
        and routing it to the correct handler.
        This function ends by returning the request id.

        Args:
            job (str): A string representing the job to be processed.
            r (int): The id of the request being processed.

        Returns:
            int: The id of the processed request.
        """
        # log_debug("Loop: Queue get got %s",qu)
        # Empty the jobs & start running stuff !
        # NOTE: self.queue.empty does not empty queue, 
        # it just checks if the queue is empty.
        # commented out.
        # self.queue.empty() -

        # Send the next outbound request batch
        log_debug(f"Running job {job}, r")
        self.conn.writeAll(self.outbound)

        self.outbound = []

        # Iterate over the open threads and check if any have been killed, if so
        # remove them from self.threads
        # log_debug("Loop: checking self.threads %s",",".join([str(s) for s in self.threads]))
        self.threads = [x for x in self.threads if x[2].is_alive()]
        self.tasks = [x for x in self.tasks if x[2].done() == False]

        if len(self.freeable) > 40:
            #
            self.queue_payload({"r": r, "action": "free", "ffid": "", "args": self.freeable})
            self.freeable = []

        # Read the inbound data and route it to correct handler
        inbounds = self.conn.readAll()
        for inbound in inbounds:
            log_debug("Loop: inbounds was %s", str(inbound))
            r = inbound["r"]
            cbid = inbound["cb"] if "cb" in inbound else None
            if "c" in inbound and inbound["c"] == "pyi":
                log_debug("Loop, inbound C request was %s", str(inbound))
                # print(inbound)
                j = inbound
                self.callbackExecutor.add_job(r, cbid, self.pyi.inbound, inbound)
            if r in self.requests:
                lock, timeout = self.requests[r]
                barrier = threading.Barrier(2, timeout=5)
                self.responses[r] = inbound, barrier
                del self.requests[r]
                # print(inbound,lock)
                lock.set()  # release, allow calling thread to resume
                barrier.wait()
        return r
        # log_debug("Loop: Queue get got %s",qu)
        # Empty the jobs & start running stuff !
        # NOTE: self.queue.empty does not empty queue's, it just checks if the queue
        # is empty.
        # self.queue.empty() -

        # Send the next outbound request batch
        log_debug(f"Running job {job}, r")
        self.conn.writeAll(self.outbound)

        self.outbound = []

        # Iterate over the open threads and check if any have been killed, if so
        # remove them from self.threads
        # log_debug("Loop: checking self.threads %s",",".join([str(s) for s in self.threads]))
        self.threads = [x for x in self.threads if x[2].is_alive()]
        self.tasks = [x for x in self.tasks if x[2].done() == False]

        if len(self.freeable) > 40:
            #
            self.queue_payload({"r": r, "action": "free", "ffid": "", "args": self.freeable})
            self.freeable = []

        # Read the inbound data and route it to correct handler
        inbounds = self.conn.readAll()
        for inbound in inbounds:
            log_debug("Loop: inbounds was %s", str(inbound))
            r = inbound["r"]
            cbid = inbound["cb"] if "cb" in inbound else None
            if "c" in inbound and inbound["c"] == "pyi":
                log_debug("Loop, inbound C request was %s", str(inbound))
                # print(inbound)
                j = inbound
                self.callbackExecutor.add_job(r, cbid, self.pyi.inbound, inbound)
            if r in self.requests:
                lock, timeout = self.requests[r]
                barrier = threading.Barrier(2, timeout=5)
                self.responses[r] = inbound, barrier
                del self.requests[r]
                # print(inbound,lock)
                lock.set()  # release, allow calling thread to resume
                barrier.wait()
        return r
    # === LOOP ===
    def loop(self):
        """
        Main loop for processing events and managing IO.
        """
        r = 0
        while self.active:
            # Wait until we have jobs
            # if self.queue.empty():
            #     log_print('not empty')
            #     time.sleep(0.4)
            #     continue
            job = self.queue.get(block=True)
            if job == "exit":
                self.active = False
                break
            r=self.process_job(job,r)
            
