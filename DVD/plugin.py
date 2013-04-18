# -*- coding: utf_8 -*-
###
#
# Thanks to Knirch/wanders for the iso88591 function
# and
# thanks to http://submarinemovies.com, http://imdb.com, http://wikipedia.org
# for the movies.
#
###

from supybot.commands import *
import supybot.log as log
import supybot.callbacks as callbacks
import sqlite3

mynick = 'jolt'

dvds = (
    ('20,000 Leagues Under The Sea (1916)'),
    ('20,000 Leagues Under The Sea (1954)'),
    ('20,000 Leagues Under The Sea (1973)'),
    ('20,000 Leagues Under The Sea (1985)'),
    ('20,000 Leagues Under The Sea (1995)'),
    ('20,000 Leagues Under The Sea (1997)'),
    ('20,000 Leagues Under The Sea (2002)'),
    ('Above Us the Waves (1955)'),
    ('Agent Red (2000)'),
    ('Airboss III: The Payback (1999)'),
    ('American Heroes: Submarines (2002)'),
    ('Around the World under the Sea (1966)'),
    ('Assault on a Queen (1966)'),
    ('Assault On The Wayne (1971)'),
    ('Battle of the Coral Sea (1959)'),
    ('Below (2002)'),
    ('Captain Nemo and the Underwater City (1969)'),
    ('Counter Measures (1998)'),
    ('Crash Dive (1943)'),
    ('Crash Dive (1996)'),
    ('Crimson Tide (1995)'),
    ('Danger Beneath the Sea (2001)'),
    ('Das Boot (1981)'),
    ('Deep Shock (2003)'),
    ('Deepstar Six (1989)'),
    ('Depth Charge (2008)'),
    ('Destination Tokyo (1943)'),
    ('Devil and the Deep (1932)'),
    ('Down Periscope (1996)'),
    ('Fantastic Voyage (1966)'),
    ('Fer-de-Lance (1974)'),
    ('Forty-Ninth Parallel (1941)'),
    ('Full Fathom Five (1990)'),
    ('Ghostboat (2006)'),
    ('Going Under (1990)'),
    ('Gray Lady Down (1978)'),
    ('Gung Ho (1943)'),
    ('Hell and High Water (1954)'),
    ('Hell Below (1933)'),
    ('Hellcats Of The Navy (1957)'),
    ('Hostile Waters (1997)'),
    ('Hoch klingt das Lied von U-Boot-Mann (1917)'),
    ('Ice Station Zebra (1968)'),
    ('In Enemy Hands (2004)'),
    ('K-19 (2002)'),
    ('Landfall (1949)'),
    ('Men Without Women (1930)'),
    ('Morning Departure (1950)'),
    ('Murphy\'s War (1971)'),
    ('Mystery Submarine (1950)'),
    ('Mystery Submarine (1963)'),
    ('Octopus (2000)'),
    ('On the Beach (1959)'),
    ('On the Beach (2000)'),
    ('Operation Disaster / Morning Departure (1950)'),
    ('Operation Pacific (1951)'),
    ('Operation Petticoat (1959)'),
    ('Out of the Depths (1945)'),
    ('Phantom Submarine U-67 (1931)'),
    ('Run Silent Run Deep (1958)'),
    ('SeaQuest DSV (1993)'),
    ('Silent Venom (2008)'),
    ('Spy In Black (1939)'),
    ('Sub Down (1997)'),
    ('Submarine (1928)'),
    ('Submarine 707R (animated) (2004)'),
    ('Submarine Alert (1943)'),
    ('Submarine Attack (1954)'),
    ('Submarine Base (1943)'),
    ('Submarine Command (1951)'),
    ('Submarine D-1 (1937)'),
    ('Submarine Hawk (1992)'),
    ('Submarine Patrol (1938)'),
    ('Submarine Raider (1942)'),
    ('Submarine Seahawk (1958)'),
    ('Submarine X-1 (1968)'),
    ('Submerged (2001)'),
    ('Submerged (2005)'),
    ('The Abyss (1989)'),
    ('The Atomic Submarine (1959)'),
    ('The Bedford Incident (1965)'),
    ('The Enemy Below (1957)'),
    ('The Fifth Missile (1986)'),
    ('The Flying Missle (aka The Flying Fish) (1950)'),
    ('The Frogmen (1951)'),
    ('The Hunley (1999)'),
    ('The Hunt For Red October (1990)'),
    ('The Inside Man (1984)'),
    ('The Land That Time Forgot (1975)'),
    ('The Last U-Boat (1990)'),
    ('The Life Aquatic (2004)'),
    ('The Mysterious Island (1929)'),
    ('The Rescue (1988)'),
    ('The Rift (1990)'),
    ('The Russians are Coming! The Russians are Coming! (1966)'),
    ('The Silent Service (animated) (1995)'),
    ('The Spy Who Loved Me (1977)'),
    ('The Valiant (1962)'),
    ('Torpedo Alley (1953)'),
    ('Torpedo Run (1958)'),
    ('Trapped in a Submarine (1931)'),
    ('Two-Man Submarine (1944)'),
    ('U-571 (2000)'),
    ('U-Boat Prisoner (1944)'),
    ('Undersea Kingdom (1936)'),
    ('Up Periscope (1959)'),
    ('Voyage To The Bottom Of The Sea (1961)'),
    ('We Dive at Dawn (1943)'),
)

def iso88591(text):
    try:
        return text.decode('utf-8').encode('iso-8859-1')
    except:
        return text.decode('iso-8859-1').encode('iso-8859-1')

class DVD(callbacks.Plugin):
    threaded = True

    def __init__(self, irc):
        self.__parent = super(DVD, self)
        self.__parent.__init__(irc)
        self.db = 'data/dvd.db'

        with sqlite3.connect(self.db) as conn:
            cur = conn.cursor()
            try:
                cur.execute("SELECT * FROM DVDs")
            except:
                log.info('Error: could not query DB, creating a new one')
                cur.execute('CREATE TABLE DVDs (id INTEGER PRIMARY KEY, '
                            'title TEXT, nick TEXT)')
            data = cur.fetchone()
            if data is None:
                log.info('Table is empty, adding stuff')
                dvdlist = [[title, mynick] for title in dvds]
                cur.executemany('insert INTO DVDs VALUES '
                                '((SELECT max(id) FROM DVDs)+1, ?, ?)',
                                dvdlist)

    def _random(self):
        conn = sqlite3.connect(self.db)
        with conn:
            cur = conn.cursor()
            cur.execute("select * FROM DVDs ORDER BY random() LIMIT 1")
            return cur.fetchone()[1]

    def add(self, irc, msg, args, movie):
        # Swedish char's will crap stuff up.
        movie = iso88591(movie)
        movie = movie.decode('latin1')
        with sqlite3.connect(self.db) as conn:
            cur = conn.cursor()
            # do we have it already?
            cur.execute('select * from DVDs WHERE title LIKE ?', (movie,))
            data = cur.fetchone()
            if data is None:
                try:
                    cur.execute('insert into DVDs VALUES ('
                                '(SELECT max(id) FROM DVDs)+1, ?, ?)',
                                (movie, msg.nick))
                except:
                    irc.reply(iso88591('Sorry, I couldn\'t add that movie.'))
                irc.reply(iso88591("Ok."))
            else:
                irc.reply(iso88591("Sorry, %s already added that one." %
                                   data[2]))
    add = wrap(add, ['text'])

    def delete(self, irc, msg, args, movie):
        # Swedish char's will crap stuff up.
        movie = iso88591(movie)
        movie = movie.decode('latin1')
        with sqlite3.connect(self.db) as conn:
            cur = conn.cursor()
            # do we have it?
            cur.execute('select * from DVDs WHERE title LIKE ?', (movie,))
            data = cur.fetchone()
            if data is None:
                irc.reply(iso88591('Sorry, couldn\'t find it in the DB.'))
            else:
                try:
                    cur.execute("delete from DVDs WHERE id=?", (data[0],))
                    irc.reply(iso88591("Ok."))
                except:
                    irc.reply(iso88591('Sorry, something went wrong when '
                                       'deleting.'))
    delete = wrap(delete, ['text'])

    def stats(self, irc, msg, args):
        with sqlite3.connect(self.db) as conn:
            cur = conn.cursor()
            cur.execute('select count(id) from DVDs')
            data = cur.fetchone()
            irc.reply(iso88591('There are %s movies in the DB' % data))
    stats = wrap(stats)


    def dvd(self, irc, msg, args):
        title = self._random()
        try:
            irc.reply(iso88591(title))
        except:
            irc.reply(iso88591("Damn, couldn't find any"))

    dvd = wrap(dvd)

Class = DVD

# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
