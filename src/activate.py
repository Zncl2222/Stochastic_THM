class Event():
    
    def __init__(self):
        self.listbox=[]
        self.linecolor=['olive','g','darkorange','r','b','y']
        self.linesymbol=['-o','-s','-<','-d','-^','-p']
        self.linestyle=['-', '--', '-.', ':']
        self.linewidth_LPM=2
        self.linewidth_NPM=1
        self.linstyle_index=2
        self.Markersize=6
        self.Markevery=3
        self.progress_judge=1
        self.figsize=[10,8]
        self.xlabelsize=28
        self.ylabelsize=28
        self.titlesize=28
        self.XYTickssize=25
        self.legendfontsize=17
        self.fdpi=300
        self.notation='sci'
        self.nR_plotselect=0
        self.nRPlotLPM_check=1
        self.nRPlotNPM_check=1
       

    def button_event_Data(self,IPM_Folderpath,DPM_Folderpath,nR,cpu_number):
        import os
        import numpy as np
        import pandas as pd
        import time
        from multiprocessing import Pool
        import statcalculation
        from datareading import Stochastic_read

        self.nR=nR
        self.nR_plotend=nR
        #self.save_checker=False
        self.progress_judge=0
        # File path for IPM
        D_path=IPM_Folderpath+'\\Displacement\\'
        P_path=IPM_Folderpath+'\\Pressure\\'
        T_path=IPM_Folderpath+'\\Temperature\\'
        V_path=IPM_Folderpath+'\\Volumetric_strain\\'
        H_path=IPM_Folderpath+'\\Hydraulic\\'
        kc_path=IPM_Folderpath+'\\HeatConductivity\\'
        Cp_path=IPM_Folderpath+'\\HeatCapacity\\'
        aT_path=IPM_Folderpath+'\\ThermalExpansion\\'
        E_path=IPM_Folderpath+"\\Young's_modulus\\"
        
        # File path for DPM
        D2_path=DPM_Folderpath+'\\Displacement\\'
        P2_path=DPM_Folderpath+'\\Pressure\\'
        T2_path=DPM_Folderpath+'\\Temperature\\'
        V2_path=DPM_Folderpath+'\\Volumetric_strain\\'
        H2_path=DPM_Folderpath+'\\Hydraulic\\'
        kc2_path=DPM_Folderpath+'\\HeatConductivity\\'
        Cp2_path=DPM_Folderpath+'\\HeatCapacity\\'
        aT2_path=DPM_Folderpath+'\\ThermalExpansion\\'
        E2_path=DPM_Folderpath+"\\Young's_modulus\\"

        # Detect the data format (Model length, time length)
        
        a=os.listdir(D_path)
        z=pd.read_table(D_path+a[0],header=None,encoding='gb2312',sep='\s+')
        
        self.Model_len=np.shape(z)[0]
        self.ntime=np.shape(z)[1]-1
        
        self.D=np.zeros([self.Model_len,nR*self.ntime]);self.D2=np.zeros([self.Model_len,nR*self.ntime])
        self.P=np.zeros([self.Model_len,nR*self.ntime]);self.P2=np.zeros([self.Model_len,nR*self.ntime])
        self.T=np.zeros([self.Model_len,nR*self.ntime]);self.T2=np.zeros([self.Model_len,nR*self.ntime])
        self.V=np.zeros([self.Model_len,nR*self.ntime]);self.V2=np.zeros([self.Model_len,nR*self.ntime])
        self.H=np.zeros([self.Model_len,nR*self.ntime]);self.H2=np.zeros([self.Model_len,nR*self.ntime])
        
        pool = Pool(processes=cpu_number)

        # Data Reading (Parallel) 

        RV_judge=IPM_Folderpath.split("_")
        print(RV_judge)
        
        if RV_judge.count("Hydraulic")==1:
            RV_path=H_path
            RV2_path=H2_path
        elif RV_judge.count("Thermal")==1:
            RV_path=kc_path
            RV2_path=kc2_path
        elif RV_judge.count("123")==1:
            RV_path=Cp_path
            RV2_path=Cp2_path
        elif RV_judge.count("ThermalExpansion")==1:
            RV_path=aT_path
            RV2_path=aT2_path
        elif RV_judge.count("Mechanical")==1:
            RV_path=E_path
            RV2_path=E2_path
        elif RV_judge[-1].split("(").count("type")==1 or RV_judge[-2].split("(").count("type") :
            RV_path=H_path
            RV2_path=H2_path
        
        SyncList=[D_path,P_path,V_path,RV_path,D2_path,P2_path,V2_path,RV2_path]
        ML=[]
        RL=[]
        CL=[]

        for i in range(len(SyncList)):
            ML.append(self.Model_len)
            RL.append(nR)
  
        a=pool.starmap(Stochastic_read,zip(SyncList,ML,RL))
        b=pool.starmap(Stochastic_read,zip([T_path,T2_path],ML,RL))

        for i in range(self.ntime):

            self.D[:,nR*i:nR*(i+1)]=(a[0][:])[:][i]
            self.P[:,nR*i:nR*(i+1)]=(a[1][:])[:][i]
            self.V[:,nR*i:nR*(i+1)]=(a[2][:])[:][i]
            self.H[:,nR*i:nR*(i+1)]=(a[3][:])[:][i]

            self.D2[:,nR*i:nR*(i+1)]=(a[4][:])[:][i]
            self.P2[:,nR*i:nR*(i+1)]=(a[5][:])[:][i]
            self.V2[:,nR*i:nR*(i+1)]=(a[6][:])[:][i]
            self.H2[:,nR*i:nR*(i+1)]=(a[7][:])[:][i]

            self.T[:,nR*i:nR*(i+1)]=(b[0][:])[:][i]
            self.T2[:,nR*i:nR*(i+1)]=(b[1][:])[:][i]

        # Transform to natural log Hydraulic
        if RV_judge.count("Hydraulic")==1 or RV_judge.count("Mechanical")==1:
            self.H=np.log(self.H)
            self.H2=np.log(self.H2)

        stat=statcalculation.Statistic(self.Model_len,self.ntime)

        # mean
        self.D_mean=stat.mean(self.D,nR);self.D2_mean=stat.mean(self.D2,nR)
        self.P_mean=stat.mean(self.P,nR);self.P2_mean=stat.mean(self.P2,nR)
        self.T_mean=stat.mean(self.T,nR);self.T2_mean=stat.mean(self.T2,nR)
        self.V_mean=stat.mean(self.V,nR);self.V2_mean=stat.mean(self.V2,nR)

        # Standard deviation
        self.D_std=stat.Standard_deviation(self.D,nR);self.D2_std=stat.Standard_deviation(self.D2,nR)
        self.P_std=stat.Standard_deviation(self.P,nR);self.P2_std=stat.Standard_deviation(self.P2,nR)
        self.T_std=stat.Standard_deviation(self.T,nR);self.T2_std=stat.Standard_deviation(self.T2,nR)
        self.V_std=stat.Standard_deviation(self.V,nR);self.V2_std=stat.Standard_deviation(self.V2,nR)

        # Variance
        self.D_var=stat.Variance(self.D,nR);self.D2_var=stat.Variance(self.D2,nR)
        self.P_var=stat.Variance(self.P,nR);self.P2_var=stat.Variance(self.P2,nR)
        self.T_var=stat.Variance(self.T,nR);self.T2_var=stat.Variance(self.T2,nR)
        self.V_var=stat.Variance(self.V,nR);self.V2_var=stat.Variance(self.V2,nR)

        # Covariance (Parallel)

        SyncList1=[self.D,self.D,self.H,self.D2,self.D2,self.H2,self.D,self.D2,self.T,self.T2]
        SyncList2=[self.P,self.H,self.P,self.P2,self.H2,self.P2,self.T,self.T2,self.P,self.P2]
        nR_list=[]
        Model_lenL=[]
        n_timeL=[]
            
        for i in range(len(SyncList1)):
            nR_list.append(nR)
            Model_lenL.append(self.Model_len)
            n_timeL.append(self.ntime)
            
        L_Cov=pool.starmap(statcalculation.Statistic.Covariance_Parallel,zip(SyncList1,SyncList2,nR_list,Model_lenL,n_timeL))

        self.DP_cov=L_Cov[0][:];self.DP2_cov=L_Cov[3][:]
        self.DH_cov=L_Cov[1][:];self.DH2_cov=L_Cov[4][:]
        self.HP_cov=L_Cov[2][:];self.HP2_cov=L_Cov[5][:]
        self.DT_cov=L_Cov[6][:];self.DT2_cov=L_Cov[7][:]
        self.TP_cov=L_Cov[8][:];self.TP2_cov=L_Cov[9][:]

        #Correlation (Parallel)
        L_Corr=pool.starmap(statcalculation.Statistic.Correlation_Parallel,zip(SyncList1,SyncList2,nR_list,Model_lenL,n_timeL))

        self.DP_corr=L_Corr[0][:];self.DP2_corr=L_Corr[3][:]
        self.DH_corr=L_Corr[1][:];self.DH2_corr=L_Corr[4][:]
        self.HP_corr=L_Corr[2][:];self.HP2_corr=L_Corr[5][:]
        self.DT_corr=L_Corr[6][:];self.DT2_corr=L_Corr[7][:]
        self.TP_corr=L_Corr[8][:];self.TP2_corr=L_Corr[9][:]

        self.D_MAXMIN=stat.Max_Min(self.D,nR);self.D2_MAXMIN=stat.Max_Min(self.D2,nR)
        self.P_MAXMIN=stat.Max_Min(self.P,nR);self.P2_MAXMIN=stat.Max_Min(self.P2,nR)
        self.T_MAXMIN=stat.Max_Min(self.T,nR);self.T2_MAXMIN=stat.Max_Min(self.T2,nR)
        self.V_MAXMIN=stat.Max_Min(self.V,nR);self.V2_MAXMIN=stat.Max_Min(self.V2,nR)

        self.D_c_interval=stat.Confidence_intervals(self.D_mean,self.D_std);self.D2_c_interval=stat.Confidence_intervals(self.D2_mean,self.D2_std)
        self.P_c_interval=stat.Confidence_intervals(self.P_mean,self.P_std);self.P2_c_interval=stat.Confidence_intervals(self.P2_mean,self.P2_std)
        self.T_c_interval=stat.Confidence_intervals(self.T_mean,self.T_std);self.T2_c_interval=stat.Confidence_intervals(self.T2_mean,self.T2_std)
        self.V_c_interval=stat.Confidence_intervals(self.V_mean,self.V_std);self.V2_c_interval=stat.Confidence_intervals(self.V2_mean,self.V2_std)
            
        PlotList=["Mean_Displacement","Mean_Pressure","Mean_Temperature","Mean_Volumetricstrain",
                    "C(u,u)","C(P,P)","C(T,T)","C(v,v)","C(y,P)","C(y,u)","C(u,P)","C(u,T)","C(T,P)",
                    "Corr(y,P)","Corr(y,u)","Corr(u,P)","Corr(u,T)","Corr(T,P)","Displacement(Realization)",
                    "Pressure(Realization)","Temperature(Realization)","Volumetric strain(Realization)"]
            
        self.listbox=[]
        for item in PlotList:
            self.listbox.append(item)

        self.progress_judge=1

    
    def button_event_Plot(self,figdir,t_list):
        import matplotlib.pyplot as plt

        plt.figure(num=0,figsize=self.figsize)
        self.Plotting(self.D_mean,self.D2_mean,t_list)

        plt.figure(num=1,figsize=self.figsize)
        self.Plotting(self.D_mean,self.D2_mean,t_list)
        plt.grid(alpha=0.6)
        plt.ylabel('Displacement (m)',fontsize=self.ylabelsize)
        plt.tight_layout()
        plt.savefig(figdir+'D.png',dpi=self.fdpi)

        plt.figure(num=2,figsize=self.figsize)
        self.Plotting(self.P_mean,self.P2_mean,t_list)
        plt.grid(alpha=0.6)
        plt.ylabel('Pressure (Pa)',fontsize=self.ylabelsize)
        plt.tight_layout()
        plt.savefig(figdir+'P.png',dpi=self.fdpi)


        plt.figure(num=3,figsize=self.figsize)
        self.Plotting(self.T_mean,self.T2_mean,t_list)
        plt.grid(alpha=0.6)
        plt.ylabel('Temperature (K)',fontsize=self.ylabelsize)
        plt.ticklabel_format(style='plain',axis='y',scilimits=(0,0),useMathText=False,useOffset=False)
        plt.tight_layout()
        plt.savefig(figdir+'T.png',dpi=self.fdpi)

        plt.figure(num=4,figsize=self.figsize)
        self.Plotting(self.V_mean,self.V2_mean,t_list)
        plt.grid(alpha=0.6)
        plt.ylabel('Volumetric strain (-)',fontsize=self.ylabelsize)
        plt.tight_layout()
        plt.savefig(figdir+'V.png',dpi=self.fdpi)

        #-----------------------------------Variance------------------------------------
        plt.figure(num=5,figsize=self.figsize)
        self.Plotting(self.D_var,self.D2_var,t_list)
        plt.grid(alpha=0.6)
        plt.ylabel('C(u$_{x}$,u$_{x}$)',fontsize=self.ylabelsize)
        plt.tight_layout()
        plt.savefig(figdir+'C(u,u).png',dpi=self.fdpi)

        plt.figure(num=6,figsize=self.figsize)
        self.Plotting(self.P_var,self.P2_var,t_list)
        plt.grid(alpha=0.6)
        plt.ylabel('C(P,P)',fontsize=self.ylabelsize)
        plt.tight_layout()
        plt.savefig(figdir+'C(P,P).png',dpi=self.fdpi)

        plt.figure(num=7,figsize=self.figsize)
        self.Plotting(self.T_var,self.T2_var,t_list)
        plt.grid(alpha=0.6)
        plt.ylabel('C(T,T)',fontsize=self.ylabelsize)
        #plt.ticklabel_format(style='plain',axis='y',scilimits=(0,0),useMathText=False,useOffset=False)
        plt.tight_layout()
        plt.savefig(figdir+'C(T,T).png',dpi=self.fdpi)

        plt.figure(num=8,figsize=self.figsize)
        self.Plotting(self.V_var,self.V2_var,t_list)
        plt.grid(alpha=0.6)
        plt.ylabel('C(v,v)',fontsize=self.ylabelsize)
        plt.tight_layout()
        plt.savefig(figdir+'C(v,v).png',dpi=self.fdpi)

        #-------------------------------------------Covariance-----------------------------------

        plt.figure(num=9,figsize=self.figsize)
        self.Plotting(self.DP_cov,self.DP2_cov,t_list)
        plt.grid(alpha=0.6)
        plt.ylabel('C(u$_{x}$,P)',fontsize=self.ylabelsize)
        plt.tight_layout()
        plt.savefig(figdir+'C(u,P).png',dpi=self.fdpi)

        plt.figure(num=10,figsize=self.figsize)
        self.Plotting(self.HP_cov,self.HP2_cov,t_list)
        plt.grid(alpha=0.6)
        plt.ylabel('C(y,P)',fontsize=self.ylabelsize)
        plt.tight_layout()
        plt.savefig(figdir+'C(y,P).png',dpi=self.fdpi)

        plt.figure(num=11,figsize=self.figsize)
        self.Plotting(self.DH_cov,self.DH2_cov,t_list)
        plt.grid(alpha=0.6)
        plt.ylabel('C(y,u$_{x}$)',fontsize=self.ylabelsize)
        #plt.ticklabel_format(style='plain',axis='y',scilimits=(0,0),useMathText=False,useOffset=False)
        plt.tight_layout()
        plt.savefig(figdir+'C(y,u).png',dpi=self.fdpi)

        plt.figure(num=12,figsize=self.figsize)
        self.Plotting(self.DT_cov,self.DT2_cov,t_list)
        plt.grid(alpha=0.6)
        plt.ylabel('C(u$_{x}$,T)',fontsize=self.ylabelsize)
        #plt.ticklabel_format(style='plain',axis='y',scilimits=(0,0),useMathText=False,useOffset=False)
        plt.tight_layout()
        plt.savefig(figdir+'C(u,T).png',dpi=self.fdpi)

        plt.figure(num=13,figsize=self.figsize)
        self.Plotting(self.TP_cov,self.TP2_cov,t_list)
        plt.grid(alpha=0.6)
        plt.ylabel('C(T,P)',fontsize=self.ylabelsize)
        #plt.ticklabel_format(style='plain',axis='y',scilimits=(0,0),useMathText=False,useOffset=False)
        plt.tight_layout()
        plt.savefig(figdir+'C(T,P).png',dpi=self.fdpi)

        #----------------------------------------------Correlation Coefficient----------------------------------------

        plt.figure(num=110,figsize=self.figsize)
        self.Plotting(self.DH_corr,self.DH2_corr,t_list)
        plt.grid(alpha=0.6)
        plt.ylabel('Corr(y,u$_{x}$)',fontsize=self.ylabelsize)
        #plt.ticklabel_format(style='plain',axis='y',scilimits=(0,0),useMathText=False,useOffset=False)
        plt.tight_layout()
        plt.savefig(figdir+'Corr(y,u).png',dpi=self.fdpi)

        plt.figure(num=111,figsize=self.figsize)
        self.Plotting(self.HP_corr,self.HP2_corr,t_list)
        plt.grid(alpha=0.6)
        plt.ylabel('Corr(y,P)',fontsize=self.ylabelsize)
        #plt.ticklabel_format(style='plain',axis='y',scilimits=(0,0),useMathText=False,useOffset=False)
        plt.tight_layout()
        plt.savefig(figdir+'Corr(y,P).png',dpi=self.fdpi)

        plt.figure(num=112,figsize=self.figsize)
        self.Plotting(self.DP_corr,self.DP2_corr,t_list)
        plt.grid(alpha=0.6)
        plt.ylabel('Corr(u$_{x}$,P)',fontsize=self.ylabelsize)
        #plt.ticklabel_format(style='plain',axis='y',scilimits=(0,0),useMathText=False,useOffset=False)
        plt.tight_layout()
        plt.savefig(figdir+'Corr(u,P).png',dpi=self.fdpi)

        plt.figure(num=113,figsize=self.figsize)
        self.Plotting(self.DT_corr,self.DT2_corr,t_list)
        plt.grid(alpha=0.6)
        plt.ylabel('Corr(u$_{x}$,T)',fontsize=self.ylabelsize)
        #plt.ticklabel_format(style='plain',axis='y',scilimits=(0,0),useMathText=False,useOffset=False)
        plt.tight_layout()
        plt.savefig(figdir+'Corr(u,T).png',dpi=self.fdpi)

        plt.figure(num=114,figsize=self.figsize)
        self.Plotting(self.TP_corr,self.TP2_corr,t_list)
        plt.grid(alpha=0.6)
        plt.ylabel('Corr(T,P)',fontsize=self.ylabelsize)
        #plt.ticklabel_format(style='plain',axis='y',scilimits=(0,0),useMathText=False,useOffset=False)
        plt.tight_layout()
        plt.savefig(figdir+'Corr(T,P).png',dpi=self.fdpi)

        plt.close('all')

        '''
        uncertainty_plot_mean=[self.D_mean,self.P_mean,self.T_mean,self.V_mean]

        uncertainty_plot_std=[self.D_c_interval,self.P_c_interval,self.T_c_interval,self.V_c_interval]

        uncertainty_plot_MAXMIN=[self.D_MAXMIN,self.P_MAXMIN,self.T_MAXMIN,self.V__MAXMIN]

        uncertainty_figurename=["D_5a","D_25a","D_50a","D_125a","D_150a","D_200a","D_300a","D_400a","D_500a","D_800a",
                                "P_5a","P_25a","P_50a","P_125a","P_150a","P_200a","P_300a","P_400a","P_500a","P_800a",
                                "T_5a","T_25a","T_50a","T_125a","T_150a","T_200a","T_300a","T_400a","T_500a","T_800a",
                                "V_5a","V_25a","V_50a","V_125a","V_150a","V_200a","V_300a","V_400a","V_500a","V_800a"]
        n=0
        t_list=[25,50,150,300]
        tc=['5','25','50','125','150','200','300','400','500','800']
        for i in range(len(tc)):
            if t_list.count(tc[i])==1:
                t[i]=1
        for i in range(4):
            
            for item in t_list:
                
                plt.figure(num=114+(n+1),figsize=self.figsize)
                self.Uncertainty_Plot(uncertainty_plot_mean[i],uncertainty_plot_MAXMIN[i],uncertainty_plot_std[i],t_index)
                plt.grid(alpha=0.6)
                plt.ylabel(uncertainty_figurename[n],fontsize=self.ylabelsize)
                #plt.ticklabel_format(style='plain',axis='y',scilimits=(0,0),useMathText=False,useOffset=False)
                plt.tight_layout()
                plt.savefig(figdir+uncertainty_figurename[n]+'.png',dpi=self.fdpi)
                n=n+1
        '''
    def button_event_Dt_Read(self,IPM_Folderpath,DPM_Folderpath):

        from datareading import Deterministic_read
        import pandas as pd
        import numpy as np
        # File path for IPM
        D_path=IPM_Folderpath+'\\Displacement.txt'
        P_path=IPM_Folderpath+'\\Pressure.txt'
        T_path=IPM_Folderpath+'\\Temperature.txt'
        V_path=IPM_Folderpath+'\\Volumetric_strain.txt'
        Dt_path=IPM_Folderpath+'\\t_Displacement.txt'
        Pt_path=IPM_Folderpath+'\\t_Pressure.txt'
        Tt_path=IPM_Folderpath+'\\t_Temperature.txt'
        Vt_path=IPM_Folderpath+'\\t_Volumetric_strain.txt'
        H_path=IPM_Folderpath+'\\Hydraulic.txt'
        kc_path=IPM_Folderpath+'\\kc.txt'
        Cp_path=IPM_Folderpath+'\\Cp.txt'
        n_path=IPM_Folderpath+'\\n.txt'
        E_path=IPM_Folderpath+"\\E.txt"
        B_path=IPM_Folderpath+"\\Biot.txt"
        
        # File path for DPM
        D2_path=DPM_Folderpath+'\\Displacement.txt'
        P2_path=DPM_Folderpath+'\\Pressure.txt'
        T2_path=DPM_Folderpath+'\\Temperature.txt'
        V2_path=DPM_Folderpath+'\\Volumetric_strain.txt'
        D2t_path=DPM_Folderpath+'\\t_Displacement.txt'
        P2t_path=DPM_Folderpath+'\\t_Pressure.txt'
        T2t_path=DPM_Folderpath+'\\t_Temperature.txt'
        V2t_path=DPM_Folderpath+'\\t_Volumetric_strain.txt'
        H2_path=DPM_Folderpath+'\\Hydraulic.txt'
        kc2_path=DPM_Folderpath+'\\kc.txt'
        Cp2_path=DPM_Folderpath+'\\Cp.txt'
        n2_path=DPM_Folderpath+'\\n.txt'
        E2_path=DPM_Folderpath+"\\E.txt"
        B2_path=DPM_Folderpath+"\\Biot.txt"

        z=pd.read_table(D_path,header=None,encoding='gb2312',sep='\s+')
        
        self.Model_len=np.shape(z)[0]
        self.ntime=np.shape(z)[1]-1
        self.nR=0

        # Spatial domain data read
        self.Dt_D=Deterministic_read(D_path);self.Dt_D2=Deterministic_read(D2_path)
        self.Dt_P=Deterministic_read(P_path);self.Dt_P2=Deterministic_read(P2_path)
        self.Dt_T=Deterministic_read(T_path);self.Dt_T2=Deterministic_read(T2_path)
        self.Dt_V=Deterministic_read(V_path);self.Dt_V2=Deterministic_read(V2_path)
        # Temporal domain data read
        self.Dt_Dt=Deterministic_read(Dt_path);self.Dt_Dt2=Deterministic_read(D2t_path)
        self.Dt_Pt=Deterministic_read(Pt_path);self.Dt_Pt2=Deterministic_read(P2t_path)
        self.Dt_Tt=Deterministic_read(Tt_path);self.Dt_Tt2=Deterministic_read(T2t_path)
        self.Dt_Vt=Deterministic_read(Vt_path);self.Dt_Vt2=Deterministic_read(V2t_path)
        # Spatial domain parameter data read
        self.Dt_H=Deterministic_read(H_path);self.Dt_H2=Deterministic_read(H2_path)
        self.Dt_kc=Deterministic_read(kc_path);self.Dt_kc2=Deterministic_read(kc2_path)
        self.Dt_Cp=Deterministic_read(Cp_path);self.Dt_Cp2=Deterministic_read(Cp2_path)
        self.Dt_n=Deterministic_read(n_path);self.Dt_n2=Deterministic_read(n2_path)
        self.Dt_E=Deterministic_read(E_path);self.Dt_E2=Deterministic_read(E2_path)
        self.Dt_B=Deterministic_read(B_path);self.Dt_B2=Deterministic_read(B2_path)

        Dt_PlotList=["Displacement","Pressure","Temperature","Volumetricstrain","Hydraulic conductivity",
                    "Thermal conductivity","Specific heat","Porosity","Young's modulus","Biot effective stress coefficient",
                    "Displacement(Temporal)","Pressure(Temporal)","Temperature(Temporal)","Volumetricstrain(Temporal)"]

        self.listbox2=[]
        for item in Dt_PlotList:
            self.listbox2.append(item)

    def button_event_Dt_Plot(self,figdir,t_list):
        import matplotlib.pyplot as plt
        figdir=figdir+'//'

        plt.figure(num=0,figsize=self.figsize)
        self.Plotting(self.Dt_D,self.Dt_D2,t_list)

        plt.figure(num=1,figsize=self.figsize)
        self.Plotting(self.Dt_D,self.Dt_D2,t_list)
        plt.grid(alpha=0.6)
        plt.ylabel('Displacement (m)',fontsize=self.ylabelsize)
        #plt.title("Host rock model (Spatial)",fontsize="28")
        plt.tight_layout()
        plt.savefig(figdir+'Displacement.png',dpi=self.fdpi)

        plt.figure(num=2,figsize=self.figsize)
        self.Plotting(self.Dt_P,self.Dt_P2,t_list)
        plt.grid(alpha=0.6)
        plt.ylabel('Pressure (Pa)',fontsize=self.ylabelsize)
        #plt.title("Host rock model (Spatial)",fontsize="28")
        plt.tight_layout()
        plt.savefig(figdir+'Pressure.png',dpi=self.fdpi)

        plt.figure(num=3,figsize=self.figsize)
        self.Plotting(self.Dt_T,self.Dt_T2,t_list)
        plt.grid(alpha=0.6)
        plt.ylabel('Temperature (℃)',fontsize=self.ylabelsize)
        #plt.title("Host rock model (Spatial)",fontsize="28")
        plt.ticklabel_format(style='plain',axis='y',scilimits=(0,0),useMathText=False,useOffset=False)
        plt.tight_layout()
        plt.savefig(figdir+'Temperature.png',dpi=self.fdpi)

        plt.figure(num=4,figsize=self.figsize)
        self.Plotting(self.Dt_V,self.Dt_V2,t_list)
        plt.grid(alpha=0.6)
        plt.ylabel('Volumetric strain (-)',fontsize=self.ylabelsize)
        #plt.title("Host rock model (Spatial)",fontsize="28")
        plt.tight_layout()
        plt.savefig(figdir+'VolumetricStrain.png',dpi=self.fdpi)
        
        plt.figure(num=5,figsize=self.figsize)
        self.Plotting_time(self.Dt_Dt,self.Dt_Dt2)
        plt.grid(alpha=0.6)
        plt.ylabel('Displacement (m)',fontsize=self.ylabelsize)
        #plt.title("Host rock model (Spatial)",fontsize="28")
        plt.tight_layout()
        plt.savefig(figdir+'t_Displacement.png',dpi=self.fdpi)

        plt.figure(num=6,figsize=self.figsize)
        self.Plotting_time(self.Dt_Pt,self.Dt_Pt2)
        plt.grid(alpha=0.6)
        plt.ylabel('Pressure (Pa)',fontsize=self.ylabelsize)
        #plt.title("Host rock model (Spatial)",fontsize="28")
        plt.tight_layout()
        plt.savefig(figdir+'t_Pressure.png',dpi=self.fdpi)


        plt.figure(num=7,figsize=self.figsize)
        self.Plotting_time(self.Dt_Tt,self.Dt_Tt2)
        plt.grid(alpha=0.6)
        plt.ylabel('Temperature (℃)',fontsize=self.ylabelsize)
        #plt.title("Host rock model (Spatial)",fontsize="28")
        plt.tight_layout()
        plt.savefig(figdir+'t_Temperature.png',dpi=self.fdpi)


        plt.figure(num=8,figsize=self.figsize)
        self.Plotting_time(self.Dt_Vt,self.Dt_Vt2)
        plt.grid(alpha=0.6)
        plt.ylabel('Volumetric strain (-)',fontsize=self.ylabelsize)
        #plt.title("Host rock model (Spatial)",fontsize="28")
        plt.tight_layout()
        plt.savefig(figdir+'t_VolumetricStrain.png',dpi=self.fdpi)

        plt.close('all')



