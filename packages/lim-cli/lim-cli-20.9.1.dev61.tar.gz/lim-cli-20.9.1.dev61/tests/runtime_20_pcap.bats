load test_helper

# See definition of LIM in test_helpers.bash for why "main" is used
# in tests.

setup_file() {
    # Make sure needed PCAP file is present (don't rely on earlier tests)
    if [[ ! -f 2015-04-09_capture-win2.pcap ]]; then
        if $LIM -q ctu get Botnet-114-1 pcap --no-subdir; then
            echo "Failed to get Botnet-114-1 PCAP file" >&2;
            exit 1
        fi
    fi
}

teardown_file() {
    rm -f 2015-04-09_capture-win2.ips
    rm -f 2015-04-09_capture-win2-time-shifted.pcap
}

setup() {
    true
}

teardown() {
    true
}

@test "\"lim pcap extract ips 2015-04-09_capture-win2.pcap\" works" {
    run bash -c "$LIM pcap extract ips 2015-04-09_capture-win2.pcap"
    [ -f 2015-04-09_capture-win2.ips ]
    run bash -c "cat 2015-04-09_capture-win2.ips"
    assert_output '4.4.4.4
5.9.75.114
8.8.8.8
10.0.2.2
10.0.2.102
37.156.33.254
64.207.134.54
67.18.120.35
77.55.48.40
79.98.28.37
79.133.202.131
93.157.96.122
95.173.189.182
103.245.153.70
112.213.89.90
119.59.124.163
128.199.134.235
185.68.16.202
188.126.72.179
190.110.121.202
192.96.207.46
192.163.239.60
192.185.52.132
192.185.56.215
192.185.76.134
192.185.212.150
195.219.57.34
200.159.128.132
202.44.54.4'
}

@test "\"lim pcap extract ips --stdout 2015-04-09_capture-win2.pcap\" works" {
    run bash -c "$LIM pcap extract ips --stdout 2015-04-09_capture-win2.pcap"
    assert_output '4.4.4.4
5.9.75.114
8.8.8.8
10.0.2.2
10.0.2.102
37.156.33.254
64.207.134.54
67.18.120.35
77.55.48.40
79.98.28.37
79.133.202.131
93.157.96.122
95.173.189.182
103.245.153.70
112.213.89.90
119.59.124.163
128.199.134.235
185.68.16.202
188.126.72.179
190.110.121.202
192.96.207.46
192.163.239.60
192.185.52.132
192.185.56.215
192.185.76.134
192.185.212.150
195.219.57.34
200.159.128.132
202.44.54.4'
}

@test "\"lim pcap shift time 2015-04-09_capture-win2.pcap --start-time 2019-01-01T12:00:01.0+0100\" works" {
    run bash -c "$LIM pcap shift time 2015-04-09_capture-win2.pcap --start-time 2019-01-01T12:00:01.0+0100"
    [ -f 2015-04-09_capture-win2-time-shifted.pcap ]
    run bash -c "TZ=UTC tcpdump -c3 -nntttt -r 2015-04-09_capture-win2-time-shifted.pcap"
    assert_output "reading from file 2015-04-09_capture-win2-time-shifted.pcap, link-type EN10MB (Ethernet)
2019-01-01 11:00:01.000000 ARP, Reply 10.0.2.2 is-at 52:54:00:12:35:02, length 28
2019-01-01 11:00:01.928579 ARP, Reply 10.0.2.2 is-at 52:54:00:12:35:02, length 28
2019-01-01 11:00:03.948389 ARP, Reply 10.0.2.2 is-at 52:54:00:12:35:02, length 28"
}

# vim: set ts=4 sw=4 tw=0 et :
