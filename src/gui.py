import numpy as np
import time
import ttkthemes as th
import tkinter as tk
import tkinter.ttk as ttk
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
from tkinter import colorchooser
import pickle
import win32api,win32con
import multiprocessing as mp

import activate
from statcalculation import Statistic
from guithread import GUI_thread
from mcplot import Stochastic_Plot

class main_GUI():

    def __init__(self, root):
        #-----------------------------------------------------Create main window and parameter initialize--------------------------------------------
        from multiprocessing import freeze_support
        freeze_support()
        self.root = root 
        self.root.title("Unititled THM Project")
        self.x_resolution=win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
        self.y_resolution=win32api.GetSystemMetrics(win32con.SM_CYSCREEN)
        padx= int((self.x_resolution-500)/2)
        pady= int((self.y_resolution-300)/2)
        self.root.geometry(f"+{padx}+{pady}")
        self.root.geometry("500x300")
        self.root.resizable(width=0,height=0)
        self.tab_main=ttk.Notebook(self.root)
        self.tab_main.place(relx=0,rely=0,relwidth=1,relheight=1)
        style = th.ThemedStyle(self.root)
        style.set_theme("black")
        self.frame=ttk.Frame(self.root)
        self.frame.place(relx=0,rely=0,relwidth=1,relheight=1)
        self.button = ttk.Button(self.frame, text="Create new\n   project", command=self.create_new_project)
        self.button.place(x=100,y=50,height=100,width=100)
        self.button2 = ttk.Button(self.frame, text="Open project", command=lambda:self.load(0))
        self.button2.place(x=300,y=50,height=100,width=100)
        self.save_checker=True
        self.ProgressCounter=0
        self.PlotList=["Mean_Displacement","Mean_Pressure","Mean_Temperature","Mean_Volumetricstrain",
                    "C(u,u)","C(P,P)","C(T,T)","C(v,v)","C(y,P)","C(y,u)","C(u,P)","C(u,T)","C(T,P)",
                    "Corr(y,P)","Corr(y,u)","Corr(u,P)","Corr(u,T)","Corr(T,P)","Displacement(Realization)",
                    "Pressure(Realization)","Temperature(Realization)","Volumetric strain(Realization)"]
        self.linecolor=['olive','g','darkorange','r','b','y']
        self.linesymbol=['-o','-s','-<','-d','-^','-p']
        self.linestyle=['-', '--', '-.', ':']
        self.linewidth_LPM=2
        self.linewidth_NPM=1
        self.linstyle_index=3
        self.Markersize=5
        self.Markevery=3
        self.figsize=[10,8]
        self.xlabelsize=28
        self.ylabelsize=28
        self.XYTickssize=25
        self.legendfontsize=17
        self.fdpi=300
        global Case1,Case2
        Case1=Stochastic_Plot()
        self.root.protocol("WM_DELETE_WINDOW", self.ShutDown)
        
        #-----------------------------------------------MENU TOOLS-------------------------------------------------------
        menubar = tk.Menu(self.root)
        filemenu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label='File', menu=filemenu)
        filemenu.add_command(label='New', command=self.create_new_project)
        filemenu.add_command(label='Save as', command=self.save)
        filemenu.add_command(label='Load', command=lambda:self.load(1))
        editmenu=tk.Menu(menubar,tearoff=0)
        menubar.add_cascade(label="Edit",menu=editmenu)
        editmenu.add_command(label='Plot preference', command=self.Plot_Options)
        self.root.config(menu=menubar)
    
    def tab_stochastic(self):
        
        padx= int((self.x_resolution-1400)/2)
        pady= int((self.y_resolution-950)/2-50)
        self.root.geometry(f"+{padx}+{pady}")
        self.root.geometry("1400x950")
        self.frame.destroy()
        
        try:
            self.tab1.destroy()
        except:
            print("Tab1 do not exisit")
        
        self.tab1=ttk.Frame(self.tab_main)
        self.tab1.place(x=0,y=30)
        
        self.Plot1=ttk.Notebook(self.tab1)
        self.Plot1.place(x=850,y=0,width=550,height=450)

        self.Plot2=ttk.Notebook(self.tab1)
        self.Plot2.place(x=850,y=460,width=550,height=450)
        
        #global fig,fig2,canvas,canvas2

        self.fig = Figure(figsize=(2, 2), dpi=100,tight_layout=True)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.Plot1)  
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        toolbar = NavigationToolbar2Tk(self.canvas, self.Plot1)

        self.fig2 = Figure(figsize=(2, 2), dpi=100,tight_layout=True)

        self.canvas2 = FigureCanvasTkAgg(self.fig2, master=self.Plot2)  
        self.canvas2.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        toolbar2 = NavigationToolbar2Tk(self.canvas2, self.Plot2)

        self.tab_main.add(self.tab1,text='Stochastic')
        
        #------------------------------------Browse function------------------------------------------------------ 
        def browse_button_IPM():
            filename = tk.filedialog.askdirectory()
            self.IPMPathEntry.delete(0,tk.END)
            self.IPMPathEntry.insert(0,filename)

        def browse_button_DPM():
            filename = tk.filedialog.askdirectory()
            self.DPMPathEntry.delete(0,tk.END)
            self.DPMPathEntry.insert(0,filename)

        def browse_button_Save():
            filename = tk.filedialog.askdirectory()
            self.FigureSavePath.delete(0,tk.END)
            self.FigureSavePath.insert(0,filename)

        #------------------------------------Progress function and label change---------------------------------------------------
        def Progress():
            import time 
            time.sleep(1.5)
            while Case1.progress_judge==0:
                self.Data_Label['text']='Processing.'
                time.sleep(0.2)
                self.Data_Label['text']='Processing..'
                time.sleep(0.2)
                self.Data_Label['text']='Processing...'
                time.sleep(0.2)
                self.Data_Label['text']='Processing....'
                time.sleep(0.2)
                self.Data_Label['text']='Processing.....'
            self.Data_Label["text"]="Data ready"
            self.Data_Label["bg"]='orange'

        def Multicore_label(event):
            if int(self.Select.get())!=1:
                self.button_Parallel_label['text']='Multi-Core mode'
                self.button_Parallel_label['bg']='red'
            else:
                self.button_Parallel_label['text']='Single-Core mode'
                self.button_Parallel_label['bg']='blue'
        #------------------------------------Event function------------------------------------------------------

        def Button_Event_Run():

            nR=int(self.nREntry.get())
            start_time=time.time()
            self.messagelistbox.insert(tk.END,"Number of realizations calculated for: "+str(nR)+" ("+str(time.asctime())+")\n")
    
            self.mybutton_Data['state'] ="disabled"
            self.mybutton_Plot['state']="disabled"
            self.Data_Label["text"]='Processing'
            self.Data_Label["bg"]='red'

            # Data path
            IPM_Folderpath=self.IPMPathEntry.get()
            DPM_Folderpath=self.DPMPathEntry.get()
            cpu_numbers=int(self.Select.get())
            #Random_Variable=self.RV_check.get()

            # Start read and calculate
            GUI_thread.thread(Case1.button_event_Data,IPM_Folderpath,DPM_Folderpath,nR,cpu_numbers)

            while Case1.progress_judge==0:
                time.sleep(0.1)

            self.mybutton_Data['state'] ="normal"
            self.mybutton_Plot['state']="normal"

            for i in range(len(self.PlotList)):
                self.listbox.delete(0,tk.END)
                self.listbox2.delete(0,tk.END)

            for item in self.PlotList:
                self.listbox.insert(tk.END,item)
                self.listbox2.insert(tk.END,item)

            end_time=time.time()
            self.messagelistbox.insert(tk.END,"Computation finish ("+str(time.asctime())+")\n")
            self.messagelistbox.insert(tk.END,"Last computation time: "+str(round(end_time-start_time,2))+" s\n")

        def Button_Plot():
            
            time.sleep(1)
            start_time=time.time()
            
            self.messagelistbox.insert(tk.END,"Start figure plotting ("+str(time.asctime())+")\n")
                
            self.judge=0

            self.mybutton_Data['state'] = "disabled"
            self.mybutton_Plot['state']="disabled"
            
            figdir=self.FigureSavePath.get()+"\\"
            t_list=self.TimeEntry.get().split(',')

            Case1.button_event_Plot(figdir,t_list)
                    
            self.mybutton_Data['state'] = "normal"
            self.mybutton_Plot['state']="normal"
            
            end_time=time.time()
            
            self.messagelistbox.insert(tk.END,"Plot complete ("+str(time.asctime())+")\n")
            self.messagelistbox.insert(tk.END,"Last computation time: "+str(round(end_time-start_time,2))+" s\n")
            
            self.judge=1

        #------------------------------------Plot update function-------------------------------------------------

        def UpdatePlot(event):
            f1,f2,index,index2=0,0,0,0
            index=int(self.listbox.curselection()[0])
            self.fig.clear()     
            P_title=Case1.listbox[int(self.listbox.curselection()[0])]
            f1=self.fig.add_subplot(111,title=P_title,xlabel='Distance (m)',ylabel=P_title)
            plot_time=self.TimeEntry.get().split(',')

            if index >= self.PlotList.index("Displacement(Realization)"):
                
                if not self.nRPlotSelect_Entry.get():
                    error=tk.messagebox.showerror(parent=self.tab1,title = 'Error',message="Please enter the number at 'Realizations Plot'." )
                    return 0
                Case1.nR_plotselect=int(self.nRPlotSelect_Entry.get())
                f1.set_title('Realizations: '+str(Case1.nR_plotselect))

            if Case1.nR<Case1.nR_plotselect:
                error=tk.messagebox.showerror(parent=self.tab1,title = 'Error',message="Please enter the correct number of realizations. Number should be < "+str(Case1.nR+1))
                return 0
            
            Case1.Canvas_parameters(index,index2,f1,f2,self.canvas)
            Case1.Cavanas_Plot(f1,plot_time)

        def UpdatePlot2(event):
            f1,f2,index,index2=0,0,0,0
            index2=int(self.listbox2.curselection()[0])
            self.fig2.clear()
            P_title=Case1.listbox[int(self.listbox2.curselection()[0])]
            f2=self.fig2.add_subplot(111,title=P_title,xlabel='Distance (m)',ylabel=P_title)
            plot_time=self.TimeEntry.get().split(',')
            
            if index2 >= self.PlotList.index("Displacement(Realization)"):
                if not self.nRPlotSelect_Entry.get():
                    error=tk.messagebox.showerror(parent=self.tab1,title = 'Error',message="Please enter the number at 'Realizations Plot'." )
                    return 0
                Case1.nR_plotselect=int(self.nRPlotSelect_Entry.get())
                f2.set_title('Realizations: '+str(Case1.nR_plotselect))
            
            if Case1.nR<Case1.nR_plotselect:
                error=tk.messagebox.showerror(parent=self.tab1,title = 'Error',message="Please enter the correct number of realizations. Number should be < "+str(Case1.nR+1))
                return 0
            

            Case1.Canvas_parameters(index,index2,f1,f2,self.canvas2)
            Case1.Cavanas_Plot(f2,plot_time)

        def nRPlotcheck():
            Case1.nRPlotLPM_check=self.nRPlotLPM_check.get()
            Case1.nRPlotNPM_check=self.nRPlotNPM_check.get()

        #-----------------------------------------List Box and Message Box-------------------------------------------------------

        self.listbox=tk.Listbox(self.tab1)
        self.listbox.place(x=50,y=490,width=300,height=300)
        self.listbox.bind("<<ListboxSelect>>", UpdatePlot)

        Scroll_listbox=tk.Scrollbar(self.listbox)
        Scroll_listbox.pack(side="right",fill="y")
        Scroll_listbox.config(command=self.listbox.yview)
        self.listbox.config(yscrollcommand=Scroll_listbox.set)
        
        self.listbox2=tk.Listbox(self.tab1)
        self.listbox2.place(x=400,y=490,width=300,height=300)
        self.listbox2.bind("<<ListboxSelect>>", UpdatePlot2)
        
        Scroll_listbox2=tk.Scrollbar(self.listbox2)
        Scroll_listbox2.pack(side="right",fill="y")
        Scroll_listbox2.config(command=self.listbox2.yview)
        self.listbox2.config(yscrollcommand=Scroll_listbox2.set)

        self.messagelistbox=tk.Text(self.tab1)
        self.messagelistbox.place(x=250,y=350,width=500,height=100)
        self.messagelistbox.bind("<Key>", lambda e: ctrlEvent(e))
        
        Scroll_message = tk.Scrollbar(self.messagelistbox)
        Scroll_message.pack(side="right", fill="y")
        Scroll_message.config(command=self.messagelistbox.yview)
        self.messagelistbox.config(yscrollcommand=Scroll_message.set)
       
        def ctrlEvent(event):
            if(12==event.state and event.keysym=='c' ):
                return
            else:
                return "break"

        #------------------------------------------Label-------------------------------------------------------
        title=tk.Label(self.tab1,text="Spatial Domain Plotting",background='blue', foreground='white',font='18')
        title.grid(row=0,column=1)
        
        LPM_Label=ttk.Label(self.tab1,text='Path for LPM')
        LPM_Label.grid(row=1,column=0)

        NPM_Label=ttk.Label(self.tab1,text='Path for NPM')
        NPM_Label.grid(row=2,column=0)

        FigureLabel=ttk.Label(self.tab1,text='Path for figure saving')
        FigureLabel.grid(row=3,column=0)

        TimeLabel=ttk.Label(self.tab1,text='Time')
        TimeLabel.grid(row=4,column=0)
        
        self.Data_Label=tk.Label(self.tab1,text='No data',bg='blue', fg='white')
        self.Data_Label.grid(row=6,column=0)
        
        self.button_Parallel_label=tk.Label(self.tab1,text='Single-Core mode',bg='blue', fg='white')
        self.button_Parallel_label.grid(row=7,column=0,padx=5,ipadx=5)

        TimeLabel_2=ttk.Label(self.tab1,text='Format=5,25,50,125,150,200,300,400,500,800')
        TimeLabel_2.grid(row=4,column=2)
        
        nRLabel=ttk.Label(self.tab1,text="Number of Realizations")
        nRLabel.grid(row=5,column=0,padx=30,pady=15,sticky=tk.S)

        CoreLabel=ttk.Label(self.tab1,text='Core numbers')
        CoreLabel.grid(row=5,column=2,sticky=tk.S)

        CanvasLabel=ttk.Label(self.tab1,text="Statistic Plot 1",foreground='#00ffff')
        CanvasLabel.place(x=150,y=465)

        CanvasLabel2=ttk.Label(self.tab1,text="Statistic Plot 2",foreground='#00ffff')
        CanvasLabel2.place(x=505,y=465)

        nRPlotSelect_Label=ttk.Label(self.tab1,text="Realizations Plot ",foreground='#00ffff')
        nRPlotSelect_Label.place(x=50,y=350)
        #------------------------------------------Entry-----------------------------------------------

        self.IPMPathEntry = ttk.Entry(self.tab1)
        self.IPMPathEntry.insert(0,'C:\JianYu\THM project\First_Year\Data(Results)\HostRock_Hydraulic_IPM_20210930_HydraulicRandomVariables')
        self.IPMPathEntry.grid(row=1,column=1,pady=15,ipadx=100)
        
        self.DPMPathEntry=ttk.Entry(self.tab1)
        self.DPMPathEntry.insert(0,'C:\JianYu\THM project\First_Year\Data(Results)\HostRock_Hydraulic_DPM_HydraulicRandomVarialbes_20210930')
        self.DPMPathEntry.grid(row=2,column=1,pady=15,ipadx=100)

        self.FigureSavePath=ttk.Entry(self.tab1)
        self.FigureSavePath.insert(0,'C:\JianYu\THM project\GUITEST\\Stochastic')
        self.FigureSavePath.grid(row=3,column=1,pady=15,ipadx=100)
        
        self.TimeEntry=ttk.Entry(self.tab1)
        self.TimeEntry.insert(0,'25,50,150,300')
        self.TimeEntry.grid(row=4,column=1,pady=15,ipadx=100)
        
        self.nREntry=ttk.Entry(self.tab1)
        self.nREntry.insert(0,'8000')
        self.nREntry.grid(row=5,column=1,padx=30,pady=15)

        self.nRPlotSelect_Entry=ttk.Entry(self.tab1)
        self.nRPlotSelect_Entry.place(x=50,y=380)

        #------------------------------------------Button-----------------------------------------------

        #mybutton_Data = ttk.Button(self.tab1, text="Run", command=lambda:[GUI_thread.thread(Case1.button_event_Data),GUI_thread.thread(Case1.Progress)])
        self.mybutton_Data = ttk.Button(self.tab1, text="Run", command=lambda:[GUI_thread.thread(Button_Event_Run),GUI_thread.thread(Progress)])
        self.mybutton_Data.grid(row=6,column=1,padx=25,pady=10,ipadx=32,sticky=tk.W)

        Browse_button_IPM = ttk.Button(self.tab1,text="Browse", command=browse_button_IPM)
        Browse_button_IPM.grid(row=1, column=2,sticky=tk.W)

        Browse_button_DPM = ttk.Button(self.tab1,text="Browse", command=browse_button_DPM)
        Browse_button_DPM.grid(row=2, column=2,sticky=tk.W)

        Browse_button_Save = ttk.Button(self.tab1,text="Browse", command=browse_button_Save)
        Browse_button_Save.grid(row=3, column=2,sticky=tk.W)
    
        #mybutton_Plot= ttk.Button(self.tab1, text="Plot", command=lambda:[Case1.button_event_Plot,self.Progress_Windows])
        self.mybutton_Plot=ttk.Button(self.tab1,text="Plot save",command=Button_Plot)
        self.mybutton_Plot.grid(row=6,column=1,padx=25,pady=10,ipadx=34,sticky=tk.E)

        #Test_button=ttk.Button(self.tab1, text="Test",command=self.Progress_Windows)
        #Test_button.grid(row=8,column=2)

        self.number = tk.StringVar()
        CPU_List=[]
        for i in range(mp.cpu_count()):
            CPU_List.append(str(i+1))
        self.Select= ttk.Combobox(self.tab1, width=12, textvariable=self.number, state='readonly')
        self.Select['values'] = CPU_List
        self.Select.grid(row=6,column=2)
        self.Select.current(0)
        self.Select.bind('<<ComboboxSelected>>', Multicore_label)
        
        self.nRPlotLPM_check=tk.IntVar()
        self.nRPlotLPM_check.set(1)
        self.nRPlotNPM_check=tk.IntVar()
        self.nRPlotNPM_check.set(1)

        nRPlotLPM_checkbox=ttk.Checkbutton(self.tab1,text="Plot LPM",var=self.nRPlotLPM_check, command=nRPlotcheck)
        nRPlotLPM_checkbox.place(x=50,y=410)

        nRPlotNPM_checkbox=ttk.Checkbutton(self.tab1,text="Plot NPM",var=self.nRPlotNPM_check, command=nRPlotcheck)
        nRPlotNPM_checkbox.place(x=50,y=430)

        '''
        Cp_checkbox=ttk.Radiobutton(self.tab1,text="Specific heat",var=self.RV_check,value=2)
        Cp_checkbox.grid(row=11,column=0)

        aT_checkbox=ttk.Radiobutton(self.tab1,text="Thermal expansion",var=self.RV_check,value=3)
        aT_checkbox.grid(row=12,column=0)

        E_checkbox=ttk.Radiobutton(self.tab1,text="Young's modulus",var=self.RV_check,value=4)
        E_checkbox.grid(row=13,column=0)
        '''
        
    def tab_deterministic(self):
        
        self.frame.destroy()
        
        try:
            self.tab2.destroy()
        except:
            print("Tab2 did not exisit")
        
        self.tab2=ttk.Frame(self.tab_main)
        self.tab2.place(x=10,y=30)
        self.tab_main.add(self.tab2,text='Deterministic')

        self.Plot3=ttk.Notebook(self.tab2)
        self.Plot3.place(x=850,y=0,width=550,height=450)

        self.Plot4=ttk.Notebook(self.tab2)
        self.Plot4.place(x=850,y=460,width=550,height=450)

        global fig3,fig4,canvas3,canvas4

        fig3 = Figure(figsize=(2, 2), dpi=100,tight_layout=True)

        canvas3 = FigureCanvasTkAgg(fig3, master=self.Plot3)  
        canvas3.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        toolbar3 = NavigationToolbar2Tk(canvas3, self.Plot3)

        fig4 = Figure(figsize=(2, 2), dpi=100,tight_layout=True)

        canvas4 = FigureCanvasTkAgg(fig4, master=self.Plot4)  
        canvas4.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        toolbar4 = NavigationToolbar2Tk(canvas4, self.Plot4)

        global listbox3,listbox4
        listbox3=tk.Listbox(self.tab2)
        listbox3.place(x=50,y=490,width=300,height=300)

        listbox4=tk.Listbox(self.tab2)
        listbox4.place(x=400,y=490,width=300,height=300)
        
        #Case2=Dt_Plot()

        title=tk.Label(self.tab2,text="Spatial Domain Plotting",bg='blue', fg='white',font='18')
        title.grid(row=0,column=1)

        label1=ttk.Label(self.tab2,text='Path for LPM')
        label1.grid(row=1,column=0)

        label2=ttk.Label(self.tab2,text='Path for NPM')
        label2.grid(row=2,column=0)

        label3=ttk.Label(self.tab2,text='Path for figure saving')
        label3.grid(row=3,column=0)

        label4=ttk.Label(self.tab2,text='Time')
        label4.grid(row=4,column=0)

        label4_2=ttk.Label(self.tab2,text='Format=5,25,50,125,150,200,300,400,500,800')
        label4_2.grid(row=4,column=3)
        
        global myentry
        myentry = ttk.Entry(self.tab2)
        myentry.insert(0,'C:\JianYu\THM project\First_Year\Data(Results)\HostRock(Test)\IPM')
        myentry.grid(row=1,column=1,pady=15,ipadx=100)
        
        global myentry2
        myentry2=ttk.Entry(self.tab2)
        myentry2.insert(0,'C:\JianYu\THM project\First_Year\Data(Results)\HostRock(Test)\DPM')
        myentry2.grid(row=2,column=1,pady=15,ipadx=100)
        
        global myentry3
        myentry3=ttk.Entry(self.tab2)
        myentry3.insert(0,'C:\JianYu\THM project\GUITEST')
        myentry3.grid(row=3,column=1,pady=15,ipadx=100)
        
        global myentry4
        myentry4=ttk.Entry(self.tab2)
        myentry4.insert(0,'25,50,150,300')
        myentry4.grid(row=4,column=1,pady=15,ipadx=100)

        mybutton = ttk.Button(self.tab2, text='Run', command=lambda:GUI_thread.thread(Dt_Plot.button_event))
        mybutton.grid(row=5,column=1)

        #---------------------------Options for Temporal Plotting--------------------------------------

        title=tk.Label(self.tab2,text="Temporal Domain Plotting",bg='orange', fg='black',font="20")
        title.grid(row=6,column=1,pady=15)

        t_label=ttk.Label(self.tab2,text='Path for LPM')
        t_label.grid(row=7,column=0)

        t_label2=ttk.Label(self.tab2,text='Path for NPM')
        t_label2.grid(row=8,column=0)

        t_label3=ttk.Label(self.tab2,text='Path for figure saving')
        t_label3.grid(row=9,column=0)

        t_plot=ttk.Entry(self.tab2)
        t_plot.insert(0,"C:\JianYu\THM project\First_Year\Data(Results)\HostRock(Test)\\IPM")
        t_plot.grid(row=7,column=1,pady=10,ipadx=100)

        t_plot2=ttk.Entry(self.tab2)
        t_plot2.insert(0,"C:\JianYu\THM project\First_Year\Data(Results)\HostRock(Test)\\DPM")
        t_plot2.grid(row=8,column=1,pady=10,ipadx=100)

        t_plot3=ttk.Entry(self.tab2)
        t_plot3.insert(0,"C:\JianYu\THM project\GUITEST")
        t_plot3.grid(row=9,column=1,pady=10,ipadx=100)

        mybutton2 = ttk.Button(self.tab2, text='Run', command=lambda:MC_plot.button_event2)
        mybutton2.grid(row=10,column=1)
        
    def create_new_project(self):
        
        def close():
            self.root.attributes("-disabled",0)
            newWindow.destroy()
            
        def createproject():
            self.root.attributes("-disabled",0)
            newWindow.destroy()
            if Stochastic_checkvalue.get()==True:
                self.save_checker=False
                self.tab_stochastic()
            if Deterministic_checkvalue.get()==True:
                self.tab_deterministic()
        
        self.root.attributes("-disabled",1)
        
        newWindow = tk.Toplevel(self.root)
        newFrame=ttk.Frame(newWindow)
        newFrame.place(relx=0,rely=0,relwidth=1,relheight=1)
        toplevel_offsetx, toplevel_offsety = self.root.winfo_x() + self.root.winfo_width(), self.root.winfo_y()
        padx= -350
        pady= 100
        newWindow.geometry(f"+{toplevel_offsetx + padx}+{toplevel_offsety + pady}")
        newWindow.geometry("200x150")
        newWindow.protocol("WM_DELETE_WINDOW", close)
        
        Stochastic_checkvalue = tk.BooleanVar() 
        Stochastic_checkvalue.set(False)
        
        Deterministic_checkvalue=tk.BooleanVar()
        Deterministic_checkvalue.set(False)
        
        Stochastic = ttk.Checkbutton(newFrame, text='Stochastic', var= Stochastic_checkvalue) 
        Stochastic.place(x=30,y=25)        
        Deterministic= ttk.Checkbutton(newFrame, text='Deterministic', var=Deterministic_checkvalue) 
        Deterministic.place(x=30,y=50)
        
        OKbutton=ttk.Button(newFrame,text="OK",command=createproject)
        OKbutton.place(x=20,y=110)
        
        Cancelbutton=ttk.Button(newFrame,text="Cancel",command=close)
        Cancelbutton.place(x=100,y=110)
        
                
    def save(self):

        path=tk.filedialog.asksaveasfilename(filetypes=[("Pickle Dumps","*.pkl")],defaultextension='.pickle')
        f1,f2,index,index2,canvas=0,0,0,0,0
        Case1.Canvas_parameters(index,index2,f1,f2,canvas)
        with open(path, 'wb') as f:
            pickle.dump(Case1, f)
            
        f.close()
        self.save_checker=True
        
    def load(self,discriminator):

        path=tk.filedialog.askopenfilename()
        global Case1
        with open(path, 'rb') as f:
            
            Case1=pickle.load(f)
        
        f.close()
        
        if discriminator==0:
            self.frame.destroy()
        if discriminator==1:
            self.tab_main.destroy()
            self.tab_main=ttk.Notebook(self.root)
            self.tab_main.place(relx=0,rely=0,relwidth=1,relheight=1)

        filename=path.split("/")[-1]
        filename=filename.split(".")[0]
        
        self.tab_stochastic()
        self.root.title(filename)
        self.messagelistbox.insert(tk.END,"Load file:"+filename+" ("+str(time.asctime())+")\n")
        self.Data_Label["text"]="Data ready"
        self.Data_Label["bg"]='orange'
        
        for item in self.PlotList:
            self.listbox.insert(tk.END,item)
            self.listbox2.insert(tk.END,item)
            Case1.listbox.append(item)

    def ShutDown(self):

        import threading
        if self.save_checker==True:
            warning=tk.messagebox.askquestion(title = 'Warning',message="Leave?")
            if warning=='no':
                return 0
            else:
                try:
                    self.root.destroy()
                except OSError:
                    print('Shut Down')
        else:
            warning=tk.messagebox.askyesnocancel(title = 'Warning',message="Save file before leave?")
            if warning==False:
                try:
                    self.root.destroy()
                except OSError:
                    print('Shut Down')
            elif warning==True:
                self.save()
                try:
                    self.root.destroy()
                except OSError:
                    print('Shut Down')
            else:
                return 0

    def Progress_Windows(self):
        
        progressWindow = tk.Toplevel(self.root)
        progressWindow.title("Progress")
        
        global progressFrame
        progressFrame=ttk.Frame(progressWindow)
        progressFrame.place(relx=0,rely=0,relwidth=1,relheight=1)
        toplevel_offsetx, toplevel_offsety = self.root.winfo_x() + self.root.winfo_width(), self.root.winfo_y()
        padx= -1000
        pady= 400
        
        progressWindow.geometry(f"+{toplevel_offsetx + padx}+{toplevel_offsety + pady}")
        progressWindow.geometry("600x150")
        pstyle = th.ThemedStyle(progressFrame)
        pstyle.configure("red.Horizontal.TProgressbar", troughcolor ='gray', background='green2',foreground='red')
        global progress
        progress=ttk.Progressbar(progressFrame,orient=tk.HORIZONTAL,length=500,mode='determinate', style="red.Horizontal.TProgressbar")
        progress_label=ttk.Label(progressFrame,text="Plotting....")
        progress_label.place(x=35,y=30)
        progress.place(x=50,y=60)

    ############################################################################################################################
    #                                                                                                                          #
    #-----------------------------------------------------Options Windows------------------------------------------------------#
    #                                                                                                                          #
    ############################################################################################################################

    def Plot_Options(self):
        
        def close():
            self.root.attributes("-disabled",0)
            OptionsWindow.destroy()
            
        def Update_PreViewPlot(canvas_n):
            if canvas_n==Prefig:
                Prefig.clear()
            else:
                Prefig2.clear()
                
            Pref1=canvas_n.add_subplot(111,title="PreView",xlabel='Distance',ylabel="PreView")
            
            for i in range(len(self.linecolor)):
                x=np.linspace(0,10,11)
                y=np.ones_like(x)*i
                y2=y-0.5
                Line_color=self.linecolor[i]
                if Line_color.count(',')>0:
                    Line_color=Line_color.split(',')
                    Line_color=[float(x)/255 for x in Line_color]
                Pref1.plot(x,y,self.linesymbol[i],color='k',linewidth=self.linewidth_NPM,markerfacecolor=Line_color,markeredgecolor='k',
                          markersize=self.Markersize,markevery=self.Markevery)
                Pref1.plot(x,y2,self.linestyle[self.linstyle_index],color=Line_color,linewidth=self.linewidth_LPM)
                
                Pref1.text(10.5,i-0.1,"NPM-"+str(i),color='r')
                Pref1.text(10.5,i-0.6,"LPM-"+str(i),color='b')
            if canvas_n==Prefig:
                Precanvas.draw_idle()
            else:
                Precanvas2.draw_idle()
                
        def Apply_Marker():
            
            self.Markersize=int(Markersize_entry.get())
            self.Markevery=int(Markevery_entry.get())
            self.linstyle_index=int(Linestyle_select.current())
            self.linewidth_LPM=int(Linewidth_LPM_entry.get())
            self.linewidth_NPM=int(Linewidth_NPM_entry.get())
            
            Case1.Markersize=self.Markersize
            Case1.Markevery=self.Markevery
            Case1.linstyle_index=self.linstyle_index
            Case1.linewidth_LPM=self.linewidth_LPM
            Case1.linewidth_NPM=self.linewidth_NPM
            
        def Adjust_color():
            
            def adjustclose():
                AdjustWindow.destroy()
            def adjustok():
                color_var=Value_entry.get()
                index=LineColorlistbox.curselection()[0]
                self.linecolor[index]=color_var
                LineColorlistbox.insert(index,color_var)
                LineColorlistbox.delete(index+1)
                AdjustWindow.destroy()
                
                Case1.linecolor=self.linecolor
                          
            def display_palette():
                (rgb,hx)=colorchooser.askcolor(parent=AdjustWindow)
                var = tk.StringVar()
                var.set(hx)
                r=hx[1:3]
                g=hx[3:5]
                b=hx[5:7]
                Color_str=str(int(r,16))+','+str(int(g,16))+','+str(int(b,16))
                Value_entry.insert(0,Color_str)
                
            if not LineColorlistbox.curselection():
                error=tk.messagebox.showerror(parent=OptionsWindow,title = 'Error',message="Please select one Line color object")
                return 0
           
            AdjustWindow=tk.Toplevel(OptionsWindow)
            AdjustFrame=ttk.Frame(AdjustWindow)
            AdjustFrame.place(relx=0,rely=0,relwidth=1,relheight=1)
            offsetx, offsety = OptionsWindow.winfo_x() + OptionsWindow.winfo_width(), OptionsWindow.winfo_y()
            padx= -600
            pady= 180
            AdjustWindow.geometry(f"+{offsetx + padx}+{offsety + pady}")
            AdjustWindow.geometry("350x150")
            
            Value_Label=ttk.Label(AdjustFrame,text="Input color")
            Value_Label.place(x=20,y=50)
            
            Value_entry=ttk.Entry(AdjustFrame)
            Value_entry.place(x=100,y=50)
            
            Value_OK_button=ttk.Button(AdjustFrame,text="OK",command=adjustok)
            Value_OK_button.place(x=70,y=100)
            
            Value_Cancel_button=ttk.Button(AdjustFrame,text="Cancel",command=adjustclose)
            Value_Cancel_button.place(x=190,y=100)
            
            Palatte_button=ttk.Button(AdjustFrame,text="Palette",command=display_palette)
            Palatte_button.place(x=250,y=47)
            
                
        def Adjust_symbol():

            def adjustclose():
                AdjustWindow.destroy()
            def adjustok():
                symbol_var=Value_entry.get()
                index=Linesymbollistbox.curselection()[0]
                self.linesymbol[index]=symbol_var
                Linesymbollistbox.insert(index,symbol_var)
                Linesymbollistbox.delete(index+1)
                AdjustWindow.destroy()
                
                Case1.linesymbol=self.linesymbol
                
            if not  Linesymbollistbox.curselection():
                error=tk.messagebox.showerror(parent=OptionsWindow,title = 'Error',message="Please select one Line style object")
                return 0
                
            AdjustWindow=tk.Toplevel(OptionsWindow)
            AdjustFrame=ttk.Frame(AdjustWindow)
            AdjustFrame.place(relx=0,rely=0,relwidth=1,relheight=1)
            offsetx, offsety = OptionsWindow.winfo_x() + OptionsWindow.winfo_width(), OptionsWindow.winfo_y()
            padx= -600
            pady= 180
            AdjustWindow.geometry(f"+{offsetx + padx}+{offsety + pady}")
            AdjustWindow.geometry("350x150")
            
            Value_Label=ttk.Label(AdjustFrame,text="Input color")
            Value_Label.place(x=20,y=50)
            
            Value_entry=ttk.Entry(AdjustFrame)
            Value_entry.place(x=100,y=50)
            
            Value_OK_button=ttk.Button(AdjustFrame,text="OK",command=adjustok)
            Value_OK_button.place(x=70,y=100)
            
            Value_Cancel_button=ttk.Button(AdjustFrame,text="Cancel",command=adjustclose)
            Value_Cancel_button.place(x=190,y=100)
        
        def Adjust_Figsettings():
            self.figsize=[int(FigWidth_entry.get()),int(FigHeight_entry.get())]
            self.xlabelsize=int(XLabel_fontsize_entry.get())
            self.ylabelsize=int(YLabel_fontsize_entry.get())
            self.XYTickssize=int(XYTicks_fontsize_entry.get())
            self.legendfontsize=int(Legend_fontsize_entry.get())
            self.fdpi=int(Figuredpi_entry.get())

            Case1.figsize=[int(FigWidth_entry.get()),int(FigHeight_entry.get())]
            Case1.xlabelsize=int(XLabel_fontsize_entry.get())
            Case1.ylabelsize=int(YLabel_fontsize_entry.get())
            Case1.XYTickssize=int(XYTicks_fontsize_entry.get())
            Case1.legendfontsize=int(Legend_fontsize_entry.get())
            Case1.fdpi=int(Figuredpi_entry.get())
            Case1.notation=self.notation.get()

        #--------------------------------------Create options window---------------------------------------------
                              
        self.root.attributes("-disabled",1)
        OptionsWindow=tk.Toplevel(self.root)
        OptionsWindow.title("Plot preference")
        padx= int((self.x_resolution-900)/2)
        pady= int((self.y_resolution-500)/2-50)

        OptionsWindow.geometry(f"+{ padx}+{ pady}")
        OptionsWindow.geometry("900x500")
        OptionsWindow.protocol("WM_DELETE_WINDOW", close)
        
        Optionstab_main=ttk.Notebook(OptionsWindow)
        Optionstab_main.place(relx=0,rely=0,relwidth=1,relheight=1)
        
        Line_tab=ttk.Frame(Optionstab_main)
        Line_tab.place(x=0,y=30)
        Optionstab_main.add(Line_tab,text='Line options')
        
        Marker_tab=ttk.Frame(Optionstab_main)
        Marker_tab.place(x=10,y=30)
        Optionstab_main.add(Marker_tab,text='Marker options')

        Figsettings_tab=ttk.Frame(Optionstab_main)
        Figsettings_tab.place(x=20,y=30)
        Optionstab_main.add(Figsettings_tab,text="Figure settings")
        
        #--------------------------------------Line tab-------------------------------------------------------------------
                
        PrePlot1=ttk.Notebook(Line_tab)
        PrePlot1.place(x=900-550,y=25,width=500,height=400)
        
        global Pref1,Prefig,Prefig2,Precanvas,Precanvas2

        Prefig = Figure(figsize=(2, 2), dpi=100,tight_layout=True)

        Precanvas = FigureCanvasTkAgg(Prefig, master=PrePlot1)  
        Precanvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        Pretoolbar = NavigationToolbar2Tk(Precanvas, PrePlot1)
        
        Listcolor_label=ttk.Label(Line_tab,text="Line color")
        Listcolor_label.place(x=50+18,y=70)
        
        Listsymbol_label=ttk.Label(Line_tab,text="Line symbol")
        Listsymbol_label.place(x=50+18+100+25,y=70)
        
        Adjustbutton=ttk.Button(Line_tab,text='Adjust color',command=Adjust_color)
        Adjustbutton.place(x=50+8,y=100+200+5)
        
        Adjustbutton2=ttk.Button(Line_tab,text='Adjust style',command=Adjust_symbol)
        Adjustbutton2.place(x=50+100+40,y=100+200+5)
        
        PreViewbutton=ttk.Button(Line_tab,text="Plot",command=lambda:Update_PreViewPlot(Prefig))
        PreViewbutton.place(x=50+75,y=350)
        
        ok_button1=ttk.Button(Line_tab,text="OK",command=close)
        ok_button1.place(x=50+75,y=400)
        
        global LineColorlistbox, Linesymbollistbox
        LineColorlistbox=tk.Listbox(Line_tab)
        LineColorlistbox.place(x=50,y=100,width=100,height=200)
        
        Linesymbollistbox=tk.Listbox(Line_tab)
        Linesymbollistbox.place(x=180,y=100,width=100,height=200)

        #----------------------------------Marker tab----------------------------------------------
        
        PrePlot2=ttk.Notebook(Marker_tab)
        PrePlot2.place(x=900-550,y=25,width=500,height=400)

        Prefig2 = Figure(figsize=(2, 2), dpi=100,tight_layout=True)

        Precanvas2 = FigureCanvasTkAgg(Prefig2, master=PrePlot2)  
        Precanvas2.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        Pretoolbar2 = NavigationToolbar2Tk(Precanvas2, PrePlot2)
        
        Markersize_label=ttk.Label(Marker_tab,text='Markersize')
        Markersize_label.place(x=20,y=50)
        
        Markevery_label=ttk.Label(Marker_tab,text='Markevery')
        Markevery_label.place(x=20,y=100)
        
        Linewidth_LPM_label=ttk.Label(Marker_tab,text="LineWidth(LPM)")
        Linewidth_LPM_label.place(x=20,y=150)
        
        Linewidth_NPM_label=ttk.Label(Marker_tab,text="LineWidth(NPM)")
        Linewidth_NPM_label.place(x=20,y=200)
        
        Linestyle_LPM_label=ttk.Label(Marker_tab,text="LinStyle(LPM)")
        Linestyle_LPM_label.place(x=20,y=250)
        
        Markersize_entry=ttk.Entry(Marker_tab)
        Markersize_entry.insert(0,str(self.Markersize))
        Markersize_entry.place(x=150,y=50)
        
        Markevery_entry=ttk.Entry(Marker_tab)
        Markevery_entry.insert(0,str(self.Markevery))
        Markevery_entry.place(x=150,y=100)
        
        Linewidth_LPM_entry=ttk.Entry(Marker_tab)
        Linewidth_LPM_entry.insert(0,str(self.linewidth_LPM))
        Linewidth_LPM_entry.place(x=150,y=150)
        
        Linewidth_NPM_entry=ttk.Entry(Marker_tab)
        Linewidth_NPM_entry.insert(0,str(self.linewidth_NPM))
        Linewidth_NPM_entry.place(x=150,y=200)
        
        self.stylenumber=tk.StringVar()
        Linestyle_select=ttk.Combobox(Marker_tab,width=15,textvariable=self.stylenumber,state='readonly')
        Linestyle_select['values']=self.linestyle
        Linestyle_select.place(x=150,y=250)
        Linestyle_select.current(self.linstyle_index)
        
        PreViewbutton=ttk.Button(Marker_tab,text="Plot",command=lambda:Update_PreViewPlot(Prefig2))
        PreViewbutton.place(x=50+75,y=350)
        
        Applybutton_tab=ttk.Button(Marker_tab,text="Apply",command=Apply_Marker)
        Applybutton_tab.place(x=50+75,y=325)
        
        ok_button2=ttk.Button(Marker_tab,text="OK",command=close)
        ok_button2.place(x=50+75,y=400)
        
        for item in self.linesymbol:
            Linesymbollistbox.insert(tk.END,item)
        for item in self.linecolor:
            LineColorlistbox.insert(tk.END,item)
        
        Update_PreViewPlot(Prefig)
        Update_PreViewPlot(Prefig2)

    #------------------------------------Figsettings tab-----------------------------------------
        
        FigWidth_label=ttk.Label(Figsettings_tab,text='Figure Width [inch]')
        FigWidth_label.place(x=20,y=50)
            
        FigHeight_label=ttk.Label(Figsettings_tab,text='Figure Height [inch]')
        FigHeight_label.place(x=20,y=100)

        XLabel_fontsize_label=ttk.Label(Figsettings_tab,text="Label font size (x)")
        XLabel_fontsize_label.place(x=20,y=150)

        YLabel_fontsize_label=ttk.Label(Figsettings_tab,text="Label font size (y)")
        YLabel_fontsize_label.place(x=20,y=200)

        XYTicks_fontsize_label=ttk.Label(Figsettings_tab,text="Ticks font size (x,y)")
        XYTicks_fontsize_label.place(x=20,y=250)

        Legend_fontsize_label=ttk.Label(Figsettings_tab,text="Legend font size")
        Legend_fontsize_label.place(x=20,y=300)

        Figuredpi_label=ttk.Label(Figsettings_tab,text="Figure dpi")
        Figuredpi_label.place(x=20,y=350)

        Notation_label=ttk.Label(Figsettings_tab,text="Plot notation")
        Notation_label.place(x=365,y=50)

        FigWidth_entry=ttk.Entry(Figsettings_tab)
        FigWidth_entry.insert(0,str(self.figsize[0]))
        FigWidth_entry.place(x=150,y=50)
        
        FigHeight_entry=ttk.Entry(Figsettings_tab)
        FigHeight_entry.insert(0,str(self.figsize[1]))
        FigHeight_entry.place(x=150,y=100)

        XLabel_fontsize_entry=ttk.Entry(Figsettings_tab)
        XLabel_fontsize_entry.insert(0,str(self.xlabelsize))
        XLabel_fontsize_entry.place(x=150,y=150)

        YLabel_fontsize_entry=ttk.Entry(Figsettings_tab)
        YLabel_fontsize_entry.insert(0,str(self.ylabelsize))
        YLabel_fontsize_entry.place(x=150,y=200)

        XYTicks_fontsize_entry=ttk.Entry(Figsettings_tab)
        XYTicks_fontsize_entry.insert(0,str(self.XYTickssize))
        XYTicks_fontsize_entry.place(x=150,y=250)

        Legend_fontsize_entry=ttk.Entry(Figsettings_tab)
        Legend_fontsize_entry.insert(0,str(self.legendfontsize))
        Legend_fontsize_entry.place(x=150,y=300)

        Figuredpi_entry=ttk.Entry(Figsettings_tab)
        Figuredpi_entry.insert(0,str(self.fdpi))
        Figuredpi_entry.place(x=150,y=350)

        self.notation = tk.StringVar()
        Notation_Select= ttk.Combobox(Figsettings_tab, width=12, textvariable=self.notation, state='readonly')
        Notation_Select['values'] = ["plain","sci"]
        Notation_Select.place(x=450,y=50)
        Notation_Select.current(1) 

        Applybutton2=ttk.Button(Figsettings_tab,text="Apply",command=Adjust_Figsettings)
        Applybutton2.place(x=300,y=380)

        OK2=ttk.Button(Figsettings_tab,text="OK",command=close)
        OK2.place(x=300,y=425)