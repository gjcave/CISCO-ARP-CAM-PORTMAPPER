#!/usr/bin/python3

fh = open('/home/gcave/Dropbox/cam.txt')
farp = open('/home/gcave/Dropbox/arp-ddc.txt')

lst = []
l4_lst = []
sort_lst = []

def build_tup(*a):
    '''
    get Vlan, MAC, interface, IP wildcard
    '''
    return a

def getKey(item):
    '''
    Change to sort different fields
    vlan=0, mac=1, interface=2, IP=-1 
    '''
    return item[-1]

# Assemble the CAM table
for line in fh:
    if not line.startswith('*'):
        continue
    line = line.split()

    if not line[3] == 'dynamic':
        continue
    if line[-1].startswith('G'):
        vlan = line[1]
        mac = line[2]
        interface = line[-1]
        switch = build_tup(vlan, mac, interface)
        lst.append(switch)

# Assemble the ARP table     
for arp_lst in farp:
    if not arp_lst.startswith('Internet'):
        continue
    arp_lst = arp_lst.split()
    if arp_lst[3] == 'Incomplete':
        continue
    else:
        l4 = arp_lst[1]
        arp_mac = arp_lst[-3]
        arp = build_tup(l4, arp_mac)
        l4_lst.append(arp)

# Verify ARP entry in CAM table
for i in lst:
    t0 = i[1]
    for j in l4_lst:
        t1 =(j[-1])
        if t0 in t1:
            vlan = i[0]
            mac_addr = i[1].upper()
            interface = i[2]
            ip_addr = j[0]
            switch = build_tup(vlan, mac_addr, interface, ip_addr)
            sort_lst.append(switch)

#Sort tuples by field
s = sorted(sort_lst, key=getKey)

# Print sorted list
for i in s:
    vlan = i[0]
    mac_addr = i[1]
    interface = i[2]
    ip_addr = i[-1]
    print('IP:%s \tMAC:%s \tInterface:%s \tVlan%s'%(ip_addr, mac_addr, interface, vlan))
    # print('IP:' + ip_addr, '\tMAC:' + mac_addr, "\tInterface:" + interface, '\tVlan'+ vlan)





                           
