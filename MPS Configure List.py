import pyvisa
import time 

try:
    #List all available VISA resources
    rm = pyvisa.ResourceManager()
    li = rm.list_resources()
    choice = ''
    while(choice == ''):
        for index in range(len(li)):
            print(str(index)+" - "+li[index])
        choice = input("Select DUT: ")
        try: 
            if(int(choice) > len(li) - 1 or int(choice) < 0):
                choice = ''
                print("Invalid Input\n")
        except:
            print("Invalid Input\n")
            choice = ''

except:
    # could not connect
    print('Could not establish communication with resource. Exiting')
    inst.exit()
    inst.close()

inst = rm.open_resource(li[int(choice)]) 

print('Instrument Connected: ' + li[int(choice)] + "\n")

def instrumentInit():
    # initialize instrument parameters and query ID
    inst.timeout = 10000 # 10s
    inst.chunk_size = 10400
    inst.read_termination = '\r\n'
    inst.write_termination = '\r\n'
    inst.delay = 0.05

    inst.write("SYST:REM")
    time.sleep(.25)
    ID = inst.query("*IDN?")
    print("Instrument ID = " + ID + "\n")
    errorquery()
    inst.write("*RST")
    errorquery()
    inst.write("*CLS")
    return;

def errorquery():
    #Query error bus
    err = inst.query("SYST:ERR?")
    print("reported error = " + err + "\n")
    return;

def SelectCH():
    CH_In = int(input("Please enter the channel to be configured (1 to 4): "))
    CH = "INST %"%CH_In-1
    inst.write(CH)
    return;

def readVOLT():
    try: 
        while True:
            print("VOLT = " + inst.query("MEAS:VOLT?"))
            errorquery()

    except KeyboardInterrupt:
        print("Data Acquired")
    return;

def configVOLT():
    voltage = input("Enter set voltage value: ")
    time.sleep(.02)
    inst.write("VOLT "+ voltage)
    errorquery()
    inst.write("OUTP 1")
    return;

def ConfigureListSetup():
    Pace=int(input("Please select the triggering mode pace (0:Dwell ; 1: Trigger) "))
    Last=int(input("Please select the output state after the list elapses (0:DC ; 1: Last) "))
    Trig=int(input("Please select the trigger source (0:Manual ; 1: External ; 2:Remote) "))

    inst.write("SOUR:LIST:STEP %"%Pace)
    inst.write("SOUR:LIST:LAST %"%Last)
    inst.writ("TRIG:SEQ %"%Trig)
    errorquery()
    return;

def COnfigureListStep():

    for i in range(COUNT):
        inst.write("LIST:STEP:NUMB " +str(i))
        try:
            Volt, Current, Dwell_Time = map(int, input("Enter the voltage current and dwell time integers separated by spaces. These values will apply to channel" +str(i+1)+ ": ").split())
            print("You entered:")
            print(f"Value 1: {a}, type: {type(a)}")
            print(f"Value 2: {b}, type: {type(b)}")
            print(f"Value 3: {c}, type: {type(c)}")
        except ValueError:
            print("Invalid input. Please enter three valid integers.")

        inst.write("LIST:VOLT "+str(Volt)+";:LIST:CURR "+str(Current)+";:LIST:DWEL "+str(Dwell_Time))
        
    time.sleep(.200)
    errorquery()
    inst.write("LIST:SAVE")
        time.sleep(.200)
    errorquery()
    return;


def main():

    instrumentInit()
    SelectCH()
    ConfigureListSetup()
    COnfigureListStep()
    inst.close()
    

if __name__ == '__main__': 
    proc = main()