###
# Copyright (c) 2013, Fredrik Johansson
# All rights reserved.
#
#
###

import supybot.utils as utils
from supybot.commands import *
import supybot.plugins as plugins
import supybot.ircutils as ircutils
import supybot.callbacks as callbacks
import sqlite3

dvds = (
    (1, 'Hoch klingt das Lied von U-Boot-Mann'),
    (2, 'Red October'),
    (3, 'film3'),
)

def iso88591(text):
    try:
        return text.decode('utf-8').encode('iso-8859-1')
    except:
        return text.decode('iso-8859-1').encode('iso-8859-1')

class DVD(callbacks.Plugin):
    """Add the help for "@plugin help DVD" here
    This should describe *how* to use this plugin."""
    threaded = True

    def __init__(self, irc):
        self.__parent = super(DVD, self)
        self.__parent.__init__(irc)
        self.db = 'data/dvd.db'

        conn = sqlite3.connect(self.db)

        with conn:
            cur = conn.cursor()
            try:
                cur.execute("SELECT * FROM DVDs")
            except:
                log.debug('Error: could not query DB, check permissions etc')


            rows = cur.fetchall()
            if len(rows) == 0:
                cur.execute("CREATE TABLE DVDs(id INT, name TEXT)")
                cur.executemany("INSERT INTO DVDs VALUES(?, ?)", dvds)


    def _query(self):

        conn = sqlite3.connect(self.db)

        with conn:
            cur = conn.cursor()
            cur.execute("select * FROM DVDs ORDER BY random() LIMIT 1")
            return cur.fetchone()[1]

    def dvd(self, irc, msg, args):
        log.debug("%s" % args)

        channel = msg.args[0]
        nick = msg.nick

        quote = self._query()

        try:
            irc.reply(iso88591(quote))
        except:
            irc.reply(iso88591("Damn, couldn't find any"))

Class = DVD


# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
