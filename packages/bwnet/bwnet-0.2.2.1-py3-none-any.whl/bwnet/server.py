
import collections
import selectors
import socket
import threading
import time

from . import utils


E_NO_ERROR = 0
E_NOT_INITIALIZED = 1
E_ALREADY_INITIALIZED = 2
E_INVALID_PORT = 3
E_TCP_ERROR = 4
E_SERVER_IS_FULL = 5
E_CLIENT_NOT_FOUND = 6
E_ALREADY_SENDING = 7
E_EMPTY_MESSAGE = 8

Process = collections.namedtuple('Process', (
        'address',
        'port',
        # Integer unix timestamp, at which process estabilished the connection
        # It is sometimes used to distinguish sockets from each other
        'birthday'
))
Process.__str__ = lambda self: f'{self.address}:{self.port}'

_logger = utils.get_console_logger(__name__)
_sel = None
_handling_thread = None
_lis_sock = None
_loop_iter_dur = None
_max_clients = None
_buffer_size = None
_cl_socks = None
_cl_procs = None
_cl_buffs = None
_stopping = False
is_initialized = False


def _handle_selector():
    # Detect write/read events of the registered listening socket
    # Call appropriate functions for guests (incoming connections) and clients
    # Meet expectation on loop iterations count per second using blocking call to select()
    while is_initialized:
        events = _sel.select(timeout=0)
        for skey, mask in events:
            if skey.data is None:
                _serve_guest(skey)
            else:
                _serve_client(skey, mask)
        time.sleep(_loop_iter_dur)  # It saves lots of power

def _save_client(sock: socket.socket, proc: Process) -> int:
    global _cl_socks, _cl_procs, _cl_buffs
    for cl_id in range(len(_cl_socks)):
        # Find free slot for a guest to occupy and become a client
        if _cl_socks[cl_id] is None:
            _cl_socks[cl_id] = sock
            _cl_procs[cl_id] = proc
            _cl_buffs[cl_id] = b''
            # TODO: Check if that is the port he connecting to AAA...
            _logger.info(f'Guest with address {proc.address} connected through port {proc.port} successfully')
            return cl_id
    else:
        # No free slots were found, server is full
        _logger.error(f'Refused connection from a guest because server is full')
        return -1

def _get_client_info(sock: socket.socket = None, proc: Process = None) -> tuple:
    fd = None if sock is None else sock.fileno()
    for cl_id in range(len(_cl_socks)):
        # Find a client identified by provided data (sock, proc or both)
        if (sock and sock == _cl_socks[cl_id]) or (proc and proc == _cl_procs[cl_id]):
            _logger.info(f'Collected information about a client (socket: {fd}, process: {proc})')
            return (cl_id, _cl_socks[cl_id], _cl_procs[cl_id], _cl_buffs[cl_id])
    
    _logger.error(f'Cannot find a client using given data (socket: {fd}, process: {proc}')
    return ( None, None, None, None )

def _forget_client(sock: socket.socket = None, proc: Process = None) -> int:
    global _cl_socks, _cl_procs, _cl_buffs
    cl_id, cl_sock, cl_proc, _ = _get_client_info(sock=sock, proc=proc)
    if cl_id is not None:
        # Client is found, so it can be forgotten
        _sel.unregister(cl_sock)
        cl_sock.close()
        # Make space occupied by the client available for guests
        _cl_socks[cl_id] = None
        _cl_procs[cl_id] = None
        _cl_buffs[cl_id] = b''
        _logger.info(f'Client with address {cl_proc.address} and port {cl_proc.port} disconnected successfully')
        return E_NO_ERROR
    else:
        return E_CLIENT_NOT_FOUND

def _serve_guest(skey: selectors.SelectorKey):
    cl_sock, cl_addr = skey.fileobj.accept()
    cl_sock.setblocking(False)
    cl_proc = Process(*cl_addr, int(time.time()))
    cl_id = _save_client(cl_sock, cl_proc)
    if cl_id == -1:
        cl_sock.close()
    else:
        # There is available space, listen for the client socket events
        # Attach the client id to save computation power later
        _sel.register(cl_sock, selectors.EVENT_READ | selectors.EVENT_WRITE, data=cl_id)
        on_client_join(cl_proc)

def _serve_client(skey: selectors.SelectorKey, mask: int):
    global _handling_thread, _cl_buffs, _stopping, is_initialized
    # Get data of a client handled using this function
    cl_id = skey.data
    cl_sock = _cl_socks[cl_id]
    cl_proc = _cl_procs[cl_id]
    if cl_sock is None:
        # Sometimes client loses connection during message receivement
        return
    
    if mask & selectors.EVENT_READ:
        b_msg = None
        try:
            b_msg = cl_sock.recv(_buffer_size)
        except:
            b_msg = b''
        
        if len(b_msg) == 0 or (len(b_msg) == 1 and b_msg[0] == 0):
            # Client sent the null character '\0' to inform that it wants to disconnect
            _logger.info(f'Client with address {cl_proc.address} and port {cl_proc.port} requested disconnection')
            _forget_client(proc=cl_proc)
            on_client_quit(cl_proc)
            # Before stopping the server completely, all clients need to be disconnected first
            if _stopping and not any(_cl_socks):
                _stopping = False
                close()
            return
        else:
            # Other messages are considered valid messages
            s_msg = b_msg.decode()
            _logger.info(f'Client with address {cl_proc.address} and port {cl_proc.port} sent a message: {s_msg} ({len(s_msg)} bytes)')
            on_client_message(cl_proc, s_msg)
    
    if mask & selectors.EVENT_WRITE:
        buff = _cl_buffs[cl_id]
        if len(buff) != 0:
            # Filled buffer is detected, its contents are sent and then it is emptied
            cl_sock.send(buff)
            _cl_buffs[cl_id] = b''

def init(host: str, port: int, max_clients: int, buffer_size: int = 256, loop_fps: int = 0, show_logs: bool = False) -> tuple:
    global _sel, _handling_thread, _lis_sock, _loop_iter_dur, _max_clients, _buffer_size, _cl_socks, _cl_procs, _cl_buffs, is_initialized
    if is_initialized:
        _logger.error('Server is already initialized')
        return ( E_ALREADY_INITIALIZED, -1 )

    # Set up all variables
    _logger.disabled = not show_logs
    _sel = selectors.DefaultSelector()
    _lis_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    _lis_sock.setblocking(False)
    try:
        _lis_sock.bind((host, port))
    except socket.error as exc:
        _logger.error(f'Failed binding the server, TCP error {exc.errno} occurred')
        return ( E_TCP_ERROR, exc.errno )
    except OverflowError:
        _logger.error('Invalid port')
        return ( E_INVALID_PORT, -1 )
    _lis_sock.listen()
    _sel.register(_lis_sock, selectors.EVENT_READ)
    _loop_iter_dur = 0 if loop_fps == 0 else 1 / loop_fps
    _max_clients = max_clients
    _buffer_size = buffer_size
    _cl_socks = [None] * max_clients
    _cl_procs = [None] * max_clients
    _cl_buffs = [b''] * max_clients
    is_initialized = True
    # Create a thread for listening the server socket events
    _handling_thread = threading.Thread(target=_handle_selector)
    _handling_thread.start()
    _logger.info('Initialized server')
    return ( E_NO_ERROR, -1 )

def close() -> int:
    global _stopping, is_initialized
    if is_initialized and not _stopping:
        if get_clients_count() == 0:
            # This works when no clients are connected or everyone got disconnected
            is_initialized = False  # This will stop the server handling thread
            _sel.unregister(_lis_sock)
            _lis_sock.close()
            _logger.info('Closed the server')
        else:
            for cl_proc in filter(lambda s: s is not None, _cl_procs):
                # Request disconnection from all connected clients
                send(cl_proc, '\0')
            _logger.info('Finished requesting disconnection from all clients')
            # After setting this flag, the last disconnecting client calls this function again,
            # but then there will be no clients so this setting will not happen again
            _stopping = True
        return E_NO_ERROR
    else:
        return E_NOT_INITIALIZED

def disconnect(cp: Process) -> int:
    if is_initialized:
        # Request disconnection of the client
        return send(cp, '\0')
        #return _forget_client(proc=cp)
    else:
        return E_NOT_INITIALIZED

def send(cp: Process, msg: str) -> int:
    global _cl_buffs
    if not is_initialized:
        return E_NOT_INITIALIZED
    
    cl_id, _, cl_proc, cl_buff = _get_client_info(proc=cp)
    if len(cl_buff) == 0:
        _cl_buffs[cl_id] = msg.encode()
        _logger.info(f'Server sent a message to client with address {cl_proc.address} and port {cl_proc.port} ({len(msg)} bytes)')
        return E_NO_ERROR
    else:
        _logger.error(f'Server is already sending a message to client with address {cl_proc.address} and port {cl_proc.port}')
        return E_ALREADY_SENDING

def get_clients_count() -> int:
    return len(tuple(filter(lambda clp: clp is not None, _cl_procs)))

def get_client_by_id(cl_id: int) -> Process:
    if cl_id < 0 or cl_id >= get_clients_count():
        _logger.error(f'Client with id {cl_id} is not found')
        return None
    return _cl_procs[cl_id]

def on_client_join(cp: Process):
    return

def on_client_message(cp: Process, msg: str):
    return msg

def on_client_quit(cp: Process):
    return
