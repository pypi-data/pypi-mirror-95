
import threading
import socket
import time

from xenavalkyrie.api.BaseSocket import BaseSocket
from xenavalkyrie.api.xena_keepalive import KeepAliveThread


class XenaCommandError(Exception):
    pass


class XenaSocket(object):

    reply_ok = '<OK>'
    reply_errors = ('#Syntax error', '#Index error', '#Internal deparse error',
                    '<BADPARAMETER>', '<BADINDEX>', '<BADPORT>', '<NOTRESERVED>', '<NOTWRITABLE>')

    def __init__(self, logger, hostname, port=22611, timeout=5):
        self.logger = logger
        self.hostname = hostname
        self.port = port
        logger.debug("Initializing")
        self.bsocket = BaseSocket(hostname, port, timeout)
        self.access_semaphor = threading.Semaphore(1)
        self.keepalive_thread = None
        self.last_command_timestamp = time.time()

    def is_connected(self):
        return self.bsocket.is_connected()

    def connect(self):
        self.logger.debug('Try to connect to {}:{}'.format(self.hostname, self.port))
        self.access_semaphor.acquire()
        try:
            self.bsocket.connect()
        except Exception as e:
            self.access_semaphor.release()
            raise IOError('Failed to connect to {}:{} {}'.format(self.hostname, self.port, e))
        self.bsocket.set_keepalives()
        self.access_semaphor.release()
        self.logger.info('Connected to {}:{}'.format(self.hostname, self.port))
        self.keepalive_thread = KeepAliveThread(self.logger, self)
        self.keepalive_thread.start()

    def disconnect(self):
        self.logger.info('Disconnect from {}:{}'.format(self.hostname, self.port))
        if self.keepalive_thread:
            self.keepalive_thread.stop()
        self.access_semaphor.acquire()
        self.bsocket.disconnect()
        self.access_semaphor.release()

    def __del__(self):
        self.access_semaphor.acquire()
        self.bsocket.disconnect()
        self.access_semaphor.release()

    def sendCommand(self, cmd):
        self.logger.debug("sendCommand(%s)", cmd)
        if not self.is_connected():
            raise socket.error("sendCommand on a disconnected socket")

        self.access_semaphor.acquire()
        self.last_command_timestamp = time.time()
        self.bsocket.sendCommand(cmd)
        self.access_semaphor.release()
        self.logger.debug("sendCommand(%s) returning", cmd)

    def __sendQueryReplies(self, cmd):
        # send the command followed by cmd SYNC to find out
        # when the last reply arrives.
        self.access_semaphor.acquire()
        self.last_command_timestamp = time.time()
        self.bsocket.sendCommand(cmd.strip('\n'))
        self.bsocket.sendCommand('SYNC')
        replies = []
        msg = self.bsocket.readReply()
        while True:
            if '\n' in msg:
                (reply, msgleft) = msg.split('\n', 1)
                # check for syntax problems
                if reply.rfind('Syntax') != -1:
                    self.access_semaphor.release()
                    raise XenaCommandError("Multiline: syntax error - {}".format(reply))

                if reply.rfind('<SYNC>') == 0:
                    self.logger.debug("Multiline EOL SYNC message")
                    self.access_semaphor.release()
                    return replies

                self.logger.debug("Multiline reply: %s", reply)
                replies.append(reply + '\n')
                msg = msgleft
            else:
                # more bytes to come
                msgnew = self.bsocket.readReply()
                msg = msgleft + msgnew

    def __sendQueryReply(self, cmd):
        self.access_semaphor.acquire()
        self.last_command_timestamp = time.time()
        reply = self.bsocket.sendQuery(cmd).strip('\n')
        self.access_semaphor.release()
        return reply

    def sendQuery(self, cmd, multilines=False):
        """ Send command, wait for response (single or multi lines), test for errors and return the returned code.

        :param cmd: command to send
        :param multilines: True - multiline response, False - single line response.
        :return: command return value.
        """
        self.logger.debug('sendQuery({})'.format(cmd))
        if not self.is_connected():
            raise socket.error('sendQuery on a disconnected socket')

        if multilines:
            replies = self.__sendQueryReplies(cmd)
            for reply in replies:
                if reply.startswith(XenaSocket.reply_errors):
                    raise XenaCommandError('sendQuery({}) reply({})'.format(cmd, replies))
            self.logger.debug("sendQuery(%s) -- Begin", cmd)
            for l in replies:
                self.logger.debug("%s", l.strip())
            self.logger.debug("sendQuery(%s) -- End", cmd)
            return replies
        else:
            reply = self.__sendQueryReply(cmd)
            if reply.startswith(XenaSocket.reply_errors):
                raise XenaCommandError('sendQuery({}) reply({})'.format(cmd, reply))
            self.logger.debug('reply({})'.format(reply))
            return reply

    def sendQueryVerify(self, cmd):
        """ Send command without return value, wait for completion, verify success.

        :param cmd: command to send
        """
        cmd = cmd.strip()
        self.logger.debug("sendQueryVerify(%s)", cmd)
        if not self.is_connected():
            raise socket.error("sendQueryVerify on a disconnected socket")

        resp = self.__sendQueryReply(cmd)
        if resp != self.reply_ok:
            raise XenaCommandError('Command {} Fail Expected {} Actual {}'.format(cmd, self.reply_ok, resp))
        self.logger.debug("SendQueryVerify(%s) Succeed", cmd)

    def keep_alive(self):
        """ Send keep alive message. """
        self.logger.debug("Send KeepAlive message")
        self.sendQuery('')
