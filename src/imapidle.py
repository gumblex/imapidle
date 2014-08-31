# Copyright (c) 2012 Mathieu Lecarme
# This code is licensed under the MIT license (see LICENSE for details)

import imaplib


def idle(connection):
    tag = connection._new_tag()
    connection.send("%s IDLE\r\n" % tag)
    response = connection.readline()
    if response != '+ idling\r\n':
        raise Exception("IDLE not handled? : %s" % response)
    connection.loop = True
    while connection.loop:
        try:
            resp = connection._get_response()
        except connection.abort:
            connection.done()
        else:
            uid, message = resp.split()[1:]
            yield uid, message


def done(connection):
    connection.send("DONE\r\n")
    connection.loop = False

imaplib.IMAP4.idle = idle
imaplib.IMAP4.done = done
