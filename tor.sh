killall tor
sleep 2
service iptables stop
service iptables start

iptables -F -t nat
iptables -F -t filter
iptables -F


iptables -A OUTPUT -o lo -j ACCEPT 
iptables -A INPUT -i lo -j ACCEPT 
iptables -t nat -A OUTPUT -d 127.0.0.1/24 -j RETURN
iptables -t nat -A OUTPUT -p tcp -m owner --uid-owner anon -m tcp -j REDIRECT --to-ports 9040
iptables -t nat -A OUTPUT -p udp -m owner --uid-owner anon -m udp --dport 53 -j REDIRECT --to-ports 53
iptables -t filter -A OUTPUT -p tcp -m owner --uid-owner anon -m tcp --dport 9040 -j ACCEPT
iptables -t filter -A OUTPUT -p udp -m owner --uid-owner anon -m udp --dport 53 -j ACCEPT
iptables -t filter -A OUTPUT -m owner --uid-owner anon -j DROP


echo "nameserver 127.0.0.1" >> /etc/resolv.conf
tor -f /etc/tor/torrc

