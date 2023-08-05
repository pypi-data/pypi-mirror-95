import os
import argparse
import datetime
import socket
import logging
import traceback

from .engine import Scheduler, TaskNotCompleted, TaskIdNotFound, QueueIsFull
from .messages import *

logger = logging.getLogger('adengine.server')

ADENGINE_UNIX_SOCK = os.environ.get('ADENGINE_UNIX_SOCK', None) or DEFAULT_UNIX_SOCKET


def parse_timedelta(time_str: str):
    """Converts string hh:mm:ss to timedelta."""
    parts = time_str.split(':')
    time_params = dict(zip(['hours', 'minutes', 'seconds'],
                           (int(part) for part in parts)))
    return datetime.timedelta(**time_params)


def parse_args() -> dict:
    parser = argparse.ArgumentParser('ADEngine server')
    parser.add_argument('-qs', '--queue-size',
                        help='Maximum size of the queue with tasks',
                        dest='queue_size',
                        type=int,
                        default=20)
    parser.add_argument('-wn', '--workers-num',
                        help='Number of workers',
                        dest='workers_num',
                        type=int,
                        default=1)
    parser.add_argument('-et', '--extract-timeout',
                        help='Timeout for data extraction in seconds',
                        dest='extract_timeout',
                        type=int,
                        default=5)
    parser.add_argument('-vd', '--virtual-display',
                        help='Use virtual display',
                        dest='virtual_display',
                        action='store_true')
    parser.add_argument('-rt', '--result-ttl',
                        help='Result ttl like hh:mm:ss',
                        dest='result_ttl',
                        type=parse_timedelta,
                        default=datetime.timedelta(minutes=5))
    parser.add_argument('-tb', '--tasks-before-session-restart',
                        help='Number of tasks before restarting PacketTracer session',
                        dest='tasks_before_session_restart',
                        type=int,
                        default=100)
    parser.add_argument('-us', '--unix-socket',
                        help='Path to unix socket',
                        dest='unix_socket',
                        default=ADENGINE_UNIX_SOCK)
    parser.add_argument('-mc', '--max-connections',
                        help='Maximum number of connections to server',
                        dest='max_connections',
                        type=int,
                        default=10)
    return vars(parser.parse_args())


def main():
    args = parse_args()

    unix_socket_path = args['unix_socket']
    if os.path.exists(unix_socket_path):
        logger.info(f'Unix socket {unix_socket_path} already_exists, remove it')
        os.remove(unix_socket_path)

    os.makedirs(os.path.dirname(unix_socket_path), exist_ok=True)
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    sock.bind(unix_socket_path)

    returncode = 0

    logger.info('Starting scheduler...')
    with Scheduler(
            args['queue_size'],
            args['workers_num'],
            args['extract_timeout'],
            args['virtual_display'],
            args['result_ttl'],
            args['tasks_before_session_restart'],
    ) as scheduler:

        sock.listen(args['max_connections'])
        logger.info(f'Listening on unix socket: {unix_socket_path}...')
        while True:
            try:
                conn, _ = sock.accept()
                try:
                    message = recv(conn)
                except RecvError as e:
                    logger.error(f'An error occurred while receiving message:\n'
                                 f'{traceback.format_exception(RecvError, e, e.__traceback__)}')

                if isinstance(message, TaskMessage):
                    try:
                        task_id = scheduler.put(message.activity, message.password)
                    except QueueIsFull:
                        send(conn, QueueIsFullMessage())
                    else:
                        send(conn, TaskIdMessage(task_id))

                elif isinstance(message, TaskIdMessage):
                    try:
                        result = scheduler.get(message.task_id)
                    except TaskIdNotFound:
                        send(conn, TaskIdNotFoundMessage())
                    except TaskNotCompleted:
                        send(conn, TaskNotCompletedMessage())
                    else:
                        send(conn, ResultMessage(result))

                conn.close()

            except KeyboardInterrupt:
                break
            except Exception as e:
                logger.error(f'Unexpected exception:\n'
                             f'{traceback.format_exception(e.__class__, e, e.__traceback__)}')
                break

        logger.info('Stop server...')

    return returncode


if __name__ == '__main__':
    exit(main())
