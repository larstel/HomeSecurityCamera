import subprocess
# p = subprocess.Popen("bluetoothctl connect 00:57:C1:59:9F:A8 | grep 'Connection successful'", stdout=subprocess.PIPE, shell=True)
p = subprocess.Popen("bluetoothctl disconnect 00:57:C1:59:9F:A8 | grep 'Successful disconnected'", stdout=subprocess.PIPE, shell=True)
(output, err) = p.communicate()
p_status = p.wait()
if output:
    print("connected")
else:
    print("not connected")
