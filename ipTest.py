import subprocess
p = subprocess.Popen("sudo arp-scan -l --interface=wlp3s0 | grep 192.168.178.62", stdout=subprocess.PIPE, shell=True)
(output, err) = p.communicate()
p_status = p.wait()
if output:
    print("connected")
else:
    print("not connected")