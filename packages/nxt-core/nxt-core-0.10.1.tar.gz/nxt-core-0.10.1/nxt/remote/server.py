# Builin
import os
import sys

import subprocess
import logging.handlers
import json
import socket

if sys.version_info[0] == 2:
    from SocketServer import ThreadingMixIn
    from SimpleXMLRPCServer import SimpleXMLRPCServer
else:
    from socketserver import ThreadingMixIn
    from xmlrpc.server import SimpleXMLRPCServer

# Internal
import nxt
from nxt.stage import GraphError
from nxt.remote import get_server_info_filepath
import nxt.remote.contexts
from nxt import nxt_path, nxt_io, nxt_log

server = None
logger = logging.getLogger('nxt')


class NxtServerException(GraphError):
    pass


class NxtServer(ThreadingMixIn, SimpleXMLRPCServer):
    def __init__(self, address, allow_none=True, log_requests=False):
        """Simple Threaded XMLRPCServer.
        :param address: tuple of (HOST, PORT)
        :param allow_none: If True None type objects are marshaled.
        :param log_requests: If True connection requests are logged.
        """
        SimpleXMLRPCServer.__init__(self, addr=address, allow_none=allow_none,
                                    logRequests=log_requests)


class ServerFunctions(object):
    def __init__(self, log_filepath):
        self.cache_file = None
        self.log_filepath = log_filepath

    def get_log_location(self):
        """Simple method for getting the filepath of the file the server is
        logging to. May be an empty string if the server isn't logging to a
        custom filepath.
        :return: str
        """
        return self.log_filepath or ''

    @staticmethod
    def is_alive():
        """Simple method for clients to use to check if the server is still
        alive.
        :return: True
        """
        logger.info("rpc server is alive and ready")
        return True

    @staticmethod
    def exec_in_headless(filepath, start_node, cache_path,
                         parameters, context_name):
        """Executed the given graph (filepath) with the given start_node in the
        dcc exe (as a sub-process). The temp path (if provided) must be a
        location that the server can read/write. If no temp path is given one
        will be generated. The file at the temp path is used to store the
        cache data to be returned to the caller. Only the file path is
        returned to the caller, not the actual data.
        :param filepath: Path to nxt save file
        :param start_node: start node path
        :param cache_path: Path to store output cache data (if none is given
        one will be generated)
        :param parameters: Optional parameters dict
        :param context_name: name of context, defaults to python
        :return: filepath to temp file
        """
        # Fixme: Contexts must be accessed like this to avoid importing them
        #  again and thus emptying the list of user contexts.
        context = nxt.remote.contexts.find_context_by_name(context_name)
        if not context:
            known = nxt.remote.contexts.iter_context_names()
            logger.debug('Known contexts: \n{}'.format('\n'.join(known)))
            raise NameError('Unknown context "{}"'.format(context_name))
        context_exe = context.exe
        if not context or not context_exe:
            raise TypeError('Unable to find context exe for: '
                            '{}'.format(context))

        context_graph = context.graph
        context_graph = nxt_path.full_file_expand(context_graph)
        if not context_graph:
            raise TypeError('No launch script found for context: '
                            '{}'.format(context))
        # Setup cache file if none provided
        if not cache_path:
            cache_path = nxt_io.generate_temp_file()
        cache_path = cache_path.replace(os.sep, '/')
        # Setup parameters file if parameters provided
        if parameters:
            parameters_file = nxt_io.generate_temp_file()
            parameters_file = parameters_file.replace(os.sep, '/')
            with open(parameters_file, 'w+') as fp:
                json.dump(parameters, fp, separators=(',', ': '))
        else:
            parameters_file = ''
        context_graph = context_graph.replace(os.sep, '/')
        logger.info('Starting \n'
                    'Context: {} \n'
                    'Interpreter: {} \n'
                    'Context Graph: {}\n'.format(context, context_exe,
                                                 context_graph))
        logger.info('Cache location: {}\n'.format(cache_path))
        # Format the cli call
        safe_graph_path = nxt_path.full_file_expand(filepath)
        # open context with graph and parameters
        os.environ[nxt_log.VERBOSE_ENV_VAR] = 'socket'
        cli_args = ['exec', context_graph, '-p',
                '/.graph_file', safe_graph_path,
                '/.cache_file', cache_path,
                '/.parameters_file', parameters_file]
        if not context.args:
            args = [context_exe, '-m'] + cli_args
            if start_node:
                args += ['/enter/call_graph._start', start_node]
        script = os.path.join(os.path.dirname(__file__), '..', 'cli.py')
        script = os.path.abspath(script)
        script = script.replace(os.sep, '/')
        if context.args:
            extra_args = []
            if context.args:
                extra_args = list(context.args)
            args = [context_exe] + extra_args + [script, '--'] + cli_args
        # HACK solution only until refined context system rolls out to relate
        # format strings to context names to include space for cli args.
        if 'UE4Editor' in context_exe:
            args = context_exe.format(cli_path=script,
                                      cli_args=' '.join(cli_args))

        logger.debug('call:  {}'.format(args))
        # TODO: Find a clean way to raise exceptions from the subprocess.
        try:
            subprocess.call(args)
        except subprocess.CalledProcessError:
            raise RuntimeError('Remote context graph "{}" failed! See log...'
                               ''.format(safe_graph_path))
        return cache_path

    def kill(self):
        """Shuts down the running rpc server and attemps to remove the server
        log file if there is one.
        :return: None
        """
        global server
        if server:
            logger.warning('Shutting down rpc server!')
            server.shutdown()
            if self.log_filepath:
                try:
                    logger.debug('Removing server log file: '
                                 '{}'.format(self.log_filepath))
                    os.remove(self.log_filepath)
                except:
                    logger.warning('Failed to remove server log file, '
                                   'if it was an autogenerated file nxt_log '
                                   'will remove it when determined it is '
                                   'stale.')


def secure_address():
    server_info_filepath = get_server_info_filepath()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 0))
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    _, port = s.getsockname()
    with open(server_info_filepath, 'w+') as fp:
        fp.write('localhost' + '\n')
        fp.write(str(port))
    return 'localhost', port


def run_server(address=None, log_requests=False):
    nxt_root = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                            '../..')).replace(os.sep, '/')
    os.chdir(nxt_root)
    global server
    if address is None:
        address = secure_address()
    server = NxtServer(address, log_requests=log_requests)
    server.register_instance(ServerFunctions(log_filepath=None))
    server.allow_reuse_address = True
    logger.info('Threaded nxt rpc server started!')
    logger.debug('Listening on:  {}'.format(address))
    server.serve_forever()


if __name__ == '__main__':
    logger.info('Available contexts: '
                '{}'.format(list(nxt.remote.contexts.iter_context_names())))
    # TODO: Fix logging so non-hosting apps can get the stdout and logs
    # logger.debug('Logging to: {}'.format(log_file))
    logger.info('Starting up server...')
    run_server()
    # logger.info('Logging rpc stdout to: {}'.format(log_file))
