import os, time, PIL, timeit, itertools, GLCD_SDK, platform


GLCD_SDK.initDLL("C:\\Program Files\\Logitech Gaming Software\\LCDSDK_8.57.148\\Lib\\GameEnginesWrapper\\x86\\LogitechLcdEnginesWrapper.dll")
GLCD_SDK.LogiLcdInit("Python",GLCD_SDK.TYPE_COLOR+GLCD_SDK.TYPE_MONO)

if GLCD_SDK.LogiLcdIsConnected(GLCD_SDK.TYPE_MONO):
  #  GLCD_SDK.LogiLcdMonoSetText(0,GLCD_SDK.NAME+" "+GLCD_SDK.VERSION)
   # GLCD_SDK.LogiLcdMonoSetText(1,"Python"+platform.python_version())
    GLCD_SDK.LogiLcdMonoSetText(1,"Mikke to gnuj")
    GLCD_SDK.LogiLcdMonoSetText(2,"A vigen ssie pauke")
  #  GLCD_SDK.LogiLcdMonoSetText(2,platform.platform()+" "+platform.uname()[4])
  #  GLCD_SDK.LogiLcdMonoSetText(3,platform.uname()[1])
GLCD_SDK.LogiLcdUpdate()

if not(GLCD_SDK.LogiLcdIsConnected(GLCD_SDK.TYPE_MONO)):
    print ("Could not connect to a logitch LCD")
    os._exit(-1)

time.sleep(20)        
GLCD_SDK.LogiLcdShutdown()

