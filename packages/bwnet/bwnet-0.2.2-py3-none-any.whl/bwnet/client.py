
import selectors
import socket
import threading
import time

from . import utils


E_NO_ERROR = 0
E_TCP_ERROR = 1
E_ALREADY_INITIALIZED = 2
E_NOT_CONNECTED = 3
E_ALREADY_SENDING = 4
E_ALREADY_DISCONNECTING = 5
E_EMPTY_MESSAGE = 6

_logger = utils.get_console_logger(__name__)
_sel = None
_handling_thread = None
_ser_sock = None
_buffer_size = None
_init_params = None
_loop_iter_dur = None
_send_buffer = b''
_disconnecting = False
is_initialized = False
is_connected = False


def _reinit():
    global is_initialized, is_connected
    if is_connected:
        # Stop the handling thread loop by unsetting appropriate flag
        # Stop listening for write/read events on the socket, close it afterwards
        is_connected = False  # This will stop the client handling thread
        _sel.unregister(_ser_sock)
        _ser_sock.close()
    # Create a new client socket, it is similar to reinstantiation of a class
    # The same settings are used as in the first initialization
    is_initialized = False
    init(*_init_params)

def _handle_selector():
    # Listen for write/read events on the socket, expected loop iterations count per
    # second is produced by appropriate blocking of the thread execution with select()
    while is_connected:
        events = _sel.select(timeout=0)
        for skey, mask in events:
            _handle_server(skey, mask)
        time.sleep(_loop_iter_dur)  # It saves lots of power

def _handle_server(skey: selectors.SelectorKey, mask: int):
    global _send_buffer
    sock = skey.fileobj

    if mask & selectors.EVENT_READ:
        try:
            b_msg = sock.recv(_buffer_size)
        except ConnectionResetError:
            b_msg = b''
        
        if len(b_msg) == 1 and b_msg[0] == 0:
            # Server can enforce the disconnection by sending null character '\0'
            _logger.info('Server requested disconnection from the client')
            disconnect()
        elif len(b_msg) == 0:
            # Empty message indicates a successfull disconnection
            _logger.info('Server responded with empty message indicating disconnection success')
            on_server_quit()
            _reinit()
            return
        else:
            # Any other message is considered a valid message
            s_msg = b_msg.decode()
            _logger.info(f'Server sent a message: {s_msg} ({len(s_msg)} bytes)')
            on_server_message(s_msg)
    
    if mask & selectors.EVENT_WRITE:
        if len(_send_buffer) != 0:
            # Filled buffer is detected and immediately used, then emptied
            sock.send(_send_buffer)
            _logger.info(f'Client sent a message ({len(_send_buffer)} bytes)')
            _send_buffer = b''

def init(buffer_size: int = 256, loop_fps: int = 0, show_logs: bool = False) -> int:
    global _sel, _handling_thread, _ser_sock, _buffer_size, _init_params, _loop_iter_dur, _send_buffer, _disconnecting, is_initialized, is_connected
    if is_initialized:
        _logger.error('Client is already initialized')
        return E_ALREADY_INITIALIZED
    # Set up all variables
    _logger.disabled = not show_logs
    _sel = selectors.DefaultSelector()
    _handling_thread = None
    _ser_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    _ser_sock.setblocking(False)
    _buffer_size = buffer_size
    _init_params = ( buffer_size, loop_fps, show_logs )  # Used later for reinitialization
    _loop_iter_dur = 0 if loop_fps == 0 else 1 / loop_fps
    _send_buffer = b''
    _disconnecting = False
    is_initialized = True
    is_connected = False
    _logger.info('Initialized client')
    return E_NO_ERROR

def connect(host: str, port: int) -> tuple:
    global is_connected, _handling_thread
    tcp_err = _ser_sock.connect_ex(( host, port ))
    if tcp_err == 0:
        # Register the socket for listening, handle the write/read events in another thread
        _sel.register(_ser_sock, selectors.EVENT_READ | selectors.EVENT_WRITE)
        is_connected = True
        _logger.info(f'Client has connected with {host} on port {port} successfully')
        _handling_thread = threading.Thread(target=_handle_selector)
        _handling_thread.start()
    elif tcp_err == 115:
        # TCP error 115: "Operation in progress" - deal with it by trying again.
        return connect(host, port)
    else:
        _logger.error(f'Failed connecting the client to server, TCP error {tcp_err} occurred')
        return ( E_TCP_ERROR, tcp_err )
    return ( E_NO_ERROR, -1 )

def disconnect() -> int:
    global _disconnecting
    
    if _disconnecting:
        _logger.error('Client is already disconnecting from server')
        return E_ALREADY_DISCONNECTING
    elif is_connected:
        # Request disconnection by sending the null character '\0'
        send('\0')
        _disconnecting = True
        _logger.info('Client requested disconnection from server')
        return E_NO_ERROR
    else:
        _logger.error('Client is not connected')
        return E_NOT_CONNECTED
    
def send(msg: str) -> int:
    global _send_buffer
    if is_connected:
        if len(_send_buffer) == 0:
            # Fill the buffer to trigger message sending
            _send_buffer = msg.encode()
            return E_NO_ERROR
        else:
            _logger.info('Client is already sending a message')
            return E_ALREADY_SENDING
    else:
        _logger.errro('Client is not connected')
        return E_NOT_CONNECTED

def on_server_message(msg: str):
    return msg

def on_server_quit():
    return
