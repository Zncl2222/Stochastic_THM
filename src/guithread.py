import threading

class GUI_thread():
    
    def thread(func,*args):
        t=threading.Thread(target=func,args=args)
        t.setDaemon(True)
        t.start()
        