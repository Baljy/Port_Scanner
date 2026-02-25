import socket
import threading
from queue import Queue
FunzionePorte = {
    21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP",
    53: "DNS", 80: "HTTP", 110: "POP3", 143: "IMAP",
    443: "HTTPS", 445: "SMB", 3306: "MySQL",
    3389: "RDP", 8080: "HTTP-Alt", 8443: "HTTPS-Alt"
}
target=input("Inserisci l'indirizzo ip della rete da  scansionare: ")
Porte=[]
Porte_queue=Queue()
threads=[]
PorteAperte=[]
def riempi_queue(Porte):
    for x  in Porte:
        Porte_queue.put(x)

def portscan(port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)  
        sock.connect((target, port))
        sock.close()
        return True
    except:
        return False
def scansione():
    while not Porte_queue.empty():
        Porta=Porte_queue.get()
        if portscan(Porta):
            print(f"La porta {Porta} è aperta")
            PorteAperte.append(Porta)

       


Scan=input("Scansionare tutte le porte 1-1024? [Y/n]: ")

if Scan.lower()=='n':
    N_porte=int(input("Inserisci quante porte vuoi scansionare: "))
    for x in range(N_porte):
        Porta=int(input("Inserisci la porta da scansionare: "))
        Porte.append(Porta) 
    riempi_queue(Porte) 

else:
    Porte=range(1,1024)
    riempi_queue(Porte)

for t in range(100):
    thread=threading.Thread(target=scansione)
    threads.append(thread)
for thread in threads:
    thread.start()
for thread in threads:
    thread.join()
print("-----------------------------PORTE APERTE-----------------------------")
if PorteAperte:
    for porta in sorted(PorteAperte):
        servizio = FunzionePorte.get(porta," ")
        print(f"  Porta {porta:5}  {servizio}")
else:
    print("Nessuna porta aperta trovata")

print("----------------------------------------------------------------------")
