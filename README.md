# torwhoiscollector
Python multithread collector whois information with tor.
##requirements
python2.7

add user anon

install tor

install python whois(https://github.com/relip/python-whois), stem

cp torrc to /etc/tor/torrc

from root:

sh tor.sh
### usage
login as user anon
python torwhoiscollector.py domains.txt out.txt bad.txt
