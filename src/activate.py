
class Event():
    
    def __init__(self):
        self.listbox=[]
        self.linecolor=['olive','g','darkorange','r','b','y']
        self.linesymbol=['-o','-s','-<','-d','-^','-p']
        self.linestyle=['-', '--', '-.', ':']
        self.linewidth_LPM=2
        self.linewidth_NPM=1
        self.linstyle_index=2
        self.Markersize=5
        self.Markevery=3
        self.progress_judge=1



    def button_event_Data(self,IPM_Folderpath,DPM_Folderpath,Random_Variable,nR,cpu_number):
        import os
        import numpy as np
        import pandas as pd
        import time
        from multiprocessing import Pool
        import statcalculation
        from datareading import Stochastic_read
        from datareading import Deterministic_read

        #self.save_checker=False
        self.progress_judge=0
        # File path for IPM
        D_path=IPM_Folderpath+'\\Displacement\\'
        P_path=IPM_Folderpath+'\\Pressure\\'
        T_path=IPM_Folderpath+'\\Temperature\\'
        V_path=IPM_Folderpath+'\\Volumetric_strain\\'
        H_path=IPM_Folderpath+'\\Hydraulic\\'
        kc_path=IPM_Folderpath+'\\HeatCouductivity\\'
        Cp_path=IPM_Folderpath+'\\HeatCapacity\\'
        aT_path=IPM_Folderpath+'\\ThermalExpansion\\'
        E_path=IPM_Folderpath+"\\Young's_modulus\\"
        
        # File path for DPM
        D2_path=DPM_Folderpath+'\\Displacement\\'
        P2_path=DPM_Folderpath+'\\Pressure\\'
        T2_path=DPM_Folderpath+'\\Temperature\\'
        V2_path=DPM_Folderpath+'\\Volumetric_strain\\'
        H2_path=DPM_Folderpath+'\\Hydraulic\\'
        kc2_path=DPM_Folderpath+'\\HeatCouductivity\\'
        Cp2_path=DPM_Folderpath+'\\HeatCapacity\\'
        aT2_path=DPM_Folderpath+'\\ThermalExpansion\\'
        E2_path=DPM_Folderpath+"\\Young's_modulus\\"

        # Detect the data format (Model length, time length)
        
        a=os.listdir(D_path)
        z=pd.read_table(D_path+a[0],header=None,encoding='gb2312',sep='\s+')
        
        self.Model_len=np.shape(z)[0]
        self.ntime=np.shape(z)[1]-1
        
        D=np.zeros([self.Model_len,nR*self.ntime]);D2=np.zeros([self.Model_len,nR*self.ntime])
        P=np.zeros([self.Model_len,nR*self.ntime]);P2=np.zeros([self.Model_len,nR*self.ntime])
        T=np.zeros([self.Model_len,nR*self.ntime]);T2=np.zeros([self.Model_len,nR*self.ntime])
        V=np.zeros([self.Model_len,nR*self.ntime]);V2=np.zeros([self.Model_len,nR*self.ntime])
        H=np.zeros([self.Model_len,nR*self.ntime]);H2=np.zeros([self.Model_len,nR*self.ntime])
        
        #-----------------Single core mode------------------------------------------------
        if cpu_number==1:  
  
            D_temp=Stochastic_read(D_path,self.Model_len,nR)
            P_temp=Stochastic_read(P_path,self.Model_len,nR)
            T_temp=Stochastic_read(T_path,self.Model_len,nR)
            V_temp=Stochastic_read(V_path,self.Model_len,nR)
            #H_temp=self.Datareading(H_path,self.__Model_len,nR,H_rdata,self.check)
            
            if Random_Variable==0:
                H_temp=Stochastic_read(H_path,self.Model_len,nR)
                H_temp=np.log(H_temp)
                self.RV_name="Hydraulic conductivity"
            elif Random_Variable==1:
                H_temp=Stochastic_read(kc_path,self.Model_len,nR)
                self.RV_name="Thermal conductivity"
            elif Random_Variable==2:
                H_temp=Stochastic_read(Cp_path,self.Model_len,nR)
                self.RV_name="Specific Heat"
            elif Random_Variable==3:
                H_temp=Stochastic_read(aT_path,self.Model_len,nR)
                self.RV_name="Thermal Expansion coefficient"
            elif Random_Variable==4:
                H_temp=Stochastic_read(E_path,self.Model_len,nR)
                self.RV_name="Young's modulus"
            
            # Data reading (DPM)
            D2_temp=Stochastic_read(D2_path,self.Model_len,nR)
            P2_temp=Stochastic_read(P2_path,self.Model_len,nR)
            T2_temp=Stochastic_read(T2_path,self.Model_len,nR)
            V2_temp=Stochastic_read(V2_path,self.Model_len,nR)
            
            if Random_Variable==0:
                H2_temp=Stochastic_read(H2_path,self.Model_len,nR)
                H2_temp=np.log(H2_temp)
            elif Random_Variable==1:
                H2_temp=Stochastic_read(kc2_path,self.Model_len,nR)
            elif Random_Variable==2:
                H2_temp=Stochastic_read(Cp2_path,self.Model_len,nR)
            elif Random_Variable==3:
                H2_temp=Stochastic_read(aT2_path,self.Model_len,nR)
            elif Random_Variable==4:
                H2_temp=Stochastic_read(E2_path,self.Model_len,nR)
            
            for i in range(self.ntime):

                D[:,nR*i:nR*(i+1)]=D_temp[:][i]
                P[:,nR*i:nR*(i+1)]=P_temp[:][i]
                V[:,nR*i:nR*(i+1)]=V_temp[:][i]
                H[:,nR*i:nR*(i+1)]=H_temp[:][i]

                D2[:,nR*i:nR*(i+1)]=D2_temp[:][i]
                P2[:,nR*i:nR*(i+1)]=P2_temp[:][i]
                V2[:,nR*i:nR*(i+1)]=V2_temp[:][i]
                H2[:,nR*i:nR*(i+1)]=H2_temp[:][i]
                
                T[:,nR*i:nR*(i+1)]=T_temp[:][i]
                T2[:,nR*i:nR*(i+1)]=T2_temp[:][i]
            
            stat=statcalculation.Statistic(self.Model_len,self.ntime)

            # mean
            self.D_mean=stat.mean(D,nR);self.D2_mean=stat.mean(D2,nR)
            self.P_mean=stat.mean(P,nR);self.P2_mean=stat.mean(P2,nR)
            self.T_mean=stat.mean(T,nR);self.T2_mean=stat.mean(T2,nR)
            self.V_mean=stat.mean(V,nR);self.V2_mean=stat.mean(V2,nR)

            # Standard deviation
            self.D_std=stat.Standard_deviation(D,nR);self.D2_std=stat.Standard_deviation(D2,nR)
            self.P_std=stat.Standard_deviation(P,nR);self.P2_std=stat.Standard_deviation(P2,nR)
            self.T_std=stat.Standard_deviation(T,nR);self.T2_std=stat.Standard_deviation(T2,nR)
            self.V_std=stat.Standard_deviation(V,nR);self.V2_std=stat.Standard_deviation(V2,nR)

            # Variance
            self.D_var=stat.Variance(D,nR);self.D2_var=stat.Variance(D2,nR)
            self.P_var=stat.Variance(P,nR);self.P2_var=stat.Variance(P2,nR)
            self.T_var=stat.Variance(T,nR);self.T2_var=stat.Variance(T2,nR)
            self.V_var=stat.Variance(V,nR);self.V2_var=stat.Variance(V2,nR)

            # Covariance
            self.DP_cov=stat.Covariance(D,P,nR);self.DP2_cov=stat.Covariance(D2,P2,nR)
            self.DH_cov=stat.Covariance(D,H,nR);self.DH2_cov=stat.Covariance(D2,H2,nR)
            self.HP_cov=stat.Covariance(H,P,nR);self.HP2_cov=stat.Covariance(H2,P2,nR)
            self.DT_cov=stat.Covariance(D,T,nR);self.DT2_cov=stat.Covariance(D2,T2,nR)
            self.TP_cov=stat.Covariance(T,P,nR);self.TP2_cov=stat.Covariance(T2,P2,nR)

            #Correlation
            self.DP_corr=stat.Correlation(D,P,nR);self.DP2_corr=stat.Correlation(D2,P2,nR)
            self.DH_corr=stat.Correlation(D,H,nR);self.DH2_corr=stat.Correlation(D2,H2,nR)
            self.HP_corr=stat.Correlation(H,P,nR);self.HP2_corr=stat.Correlation(H2,P2,nR)
            self.DT_corr=stat.Correlation(D,T,nR);self.DT2_corr=stat.Correlation(D2,T2,nR)
            self.TP_corr=stat.Correlation(T,P,nR);self.TP2_corr=stat.Correlation(T2,P2,nR)            
        #----------------Multi core mode------------------------------------------------
        else:
    
            pool = Pool(processes=cpu_number)

            # Data Reading (Parallel) 
                  
            if Random_Variable==0:
                RV_path=H_path
                RV2_path=H2_path
            elif Random_Variable==1:
                RV_path=kc_path
                RV2_path=kc2_path
            elif Random_Variable==2:
                RV_path=Cp_path
                RV2_path=Cp2_path
            elif Random_Variable==3:
                RV_path=aT_path
                RV2_path=aT2_path
            elif Random_Variable==4:
                RV_path=E_path
                RV2_path=E2_path
            
            SyncList=[D_path,P_path,V_path,RV_path,D2_path,P2_path,V2_path,RV2_path]
            ML=[]
            RL=[]
            CL=[]
            #AdopterL=[]

            for i in range(len(SyncList)):
                #AdopterL.append(0)
                ML.append(self.Model_len)
                RL.append(nR)
  
            a=pool.starmap(Stochastic_read,zip(SyncList,ML,RL))
            b=pool.starmap(Stochastic_read,zip([T_path,T2_path],ML,RL))

            for i in range(self.ntime):

                D[:,nR*i:nR*(i+1)]=(a[0][:])[:][i]
                P[:,nR*i:nR*(i+1)]=(a[1][:])[:][i]
                V[:,nR*i:nR*(i+1)]=(a[2][:])[:][i]
                H[:,nR*i:nR*(i+1)]=(a[3][:])[:][i]

                D2[:,nR*i:nR*(i+1)]=(a[4][:])[:][i]
                P2[:,nR*i:nR*(i+1)]=(a[5][:])[:][i]
                V2[:,nR*i:nR*(i+1)]=(a[6][:])[:][i]
                H2[:,nR*i:nR*(i+1)]=(a[7][:])[:][i]

                T[:,nR*i:nR*(i+1)]=(b[0][:])[:][i]
                T2[:,nR*i:nR*(i+1)]=(b[1][:])[:][i]

            # Transform to natural log Hydraulic

            H=np.log(H)
            H2=np.log(H2)

            stat=statcalculation.Statistic(self.Model_len,self.ntime)

            # mean
            self.D_mean=stat.mean(D,nR);self.D2_mean=stat.mean(D2,nR)
            self.P_mean=stat.mean(P,nR);self.P2_mean=stat.mean(P2,nR)
            self.T_mean=stat.mean(T,nR);self.T2_mean=stat.mean(T2,nR)
            self.V_mean=stat.mean(V,nR);self.V2_mean=stat.mean(V2,nR)

            # Standard deviation
            self.D_std=stat.Standard_deviation(D,nR);self.D2_std=stat.Standard_deviation(D2,nR)
            self.P_std=stat.Standard_deviation(P,nR);self.P2_std=stat.Standard_deviation(P2,nR)
            self.T_std=stat.Standard_deviation(T,nR);self.T2_std=stat.Standard_deviation(T2,nR)
            self.V_std=stat.Standard_deviation(V,nR);self.V2_std=stat.Standard_deviation(V2,nR)

            # Variance
            self.D_var=stat.Variance(D,nR);self.D2_var=stat.Variance(D2,nR)
            self.P_var=stat.Variance(P,nR);self.P2_var=stat.Variance(P2,nR)
            self.T_var=stat.Variance(T,nR);self.T2_var=stat.Variance(T2,nR)
            self.V_var=stat.Variance(V,nR);self.V2_var=stat.Variance(V2,nR)

            # Covariance (Parallel)

            SyncList1=[D,D,H,D2,D2,H2,D,D2,T,T2]
            SyncList2=[P,H,P,P2,H2,P2,T,T2,P,P2]
            nR_list=[]
            Model_lenL=[]
            n_timeL=[]
            
            for i in range(len(SyncList1)):
                nR_list.append(nR)
                Model_lenL.append(self.Model_len)
                n_timeL.append(self.ntime)
            
            L_Cov=pool.starmap(statcalculation.Statistic.Covariance_Parallel,zip(SyncList1,SyncList2,nR_list,Model_lenL,n_timeL))
            #L_Cov=Task.map_sync(stat.Covariance_Parallel,SyncList1,SyncList2,nR_list,Model_lenL,n_timeL)

            self.DP_cov=L_Cov[0][:];self.DP2_cov=L_Cov[3][:]
            self.DH_cov=L_Cov[1][:];self.DH2_cov=L_Cov[4][:]
            self.HP_cov=L_Cov[2][:];self.HP2_cov=L_Cov[5][:]
            self.DT_cov=L_Cov[6][:];self.DT2_cov=L_Cov[7][:]
            self.TP_cov=L_Cov[8][:];self.TP2_cov=L_Cov[9][:]

            #Correlation (Parallel)
            L_Corr=pool.starmap(statcalculation.Statistic.Correlation_Parallel,zip(SyncList1,SyncList2,nR_list,Model_lenL,n_timeL))
            #L_Corr=Task.map_sync(MC_Plot.Correlation_Parallel,SyncList1,SyncList2,nR_list,Model_lenL,n_timeL)

            self.DP_corr=L_Corr[0][:];self.DP2_corr=L_Corr[3][:]
            self.DH_corr=L_Corr[1][:];self.DH2_corr=L_Corr[4][:]
            self.HP_corr=L_Corr[2][:];self.HP2_corr=L_Corr[5][:]
            self.DT_corr=L_Corr[6][:];self.DT2_corr=L_Corr[7][:]
            self.TP_corr=L_Corr[8][:];self.TP2_corr=L_Corr[9][:]
            print("I sucessed")
            
        PlotList=["Mean_Displacement","Mean_Pressure","Mean_Temperature","Mean_Volumetricstrain",
                  "C(u,u)","C(P,P)","C(v,v)","C(u,P)","C(y,P)","C(y,u)","C(u,T)","C(T,P)",
                 "Corr(u,u)","Corr(P,P)","Corr(v,v)","Corr(u,P)","Corr(y,P)","Corr(y,u)",
                 "Corr(u,T)","Corr(T,P)"]
        
        self.listbox=[]
        for item in PlotList:
            self.listbox.append(item)

        self.progress_judge=1
        
    def button_event_Plot(self,figdir,t_list,fdpi):
        import matplotlib.pyplot as plt
        #MC_Plot=Stochastic_Plot()

        plt.figure(num=0,figsize=(10,8))
        self.Plotting(self.D_mean,self.D2_mean,t_list)

        plt.figure(num=1,figsize=(10,8))
        self.Plotting(self.D_mean,self.D2_mean,t_list)
        plt.grid(alpha=0.6)
        plt.ylabel('Displacement (m)',fontsize='28')
        plt.tight_layout()
        plt.savefig(figdir+'D.png',dpi=fdpi)

        plt.figure(num=2,figsize=(10,8))
        self.Plotting(self.P_mean,self.P2_mean,t_list)
        plt.grid(alpha=0.6)
        plt.ylabel('Pressure (Pa)',fontsize='28')
        plt.tight_layout()
        plt.savefig(figdir+'P.png',dpi=fdpi)


        plt.figure(num=3,figsize=(10,8))
        self.Plotting(self.T_mean,self.T2_mean,t_list)
        plt.grid(alpha=0.6)
        plt.ylabel('Temperature (K)',fontsize='28')
        plt.ticklabel_format(style='plain',axis='y',scilimits=(0,0),useMathText=False,useOffset=False)
        plt.tight_layout()
        plt.savefig(figdir+'T.png',dpi=fdpi)

        plt.figure(num=4,figsize=(10,8))
        self.Plotting(self.V_mean,self.V2_mean,t_list)
        plt.grid(alpha=0.6)
        plt.ylabel('Volumetric strain (-)',fontsize='28')
        plt.tight_layout()
        plt.savefig(figdir+'V.png',dpi=fdpi)

        #-----------------------------------Variance------------------------------------
        plt.figure(num=5,figsize=(10,8))
        self.Plotting(self.D_var,self.D2_var,t_list)
        plt.grid(alpha=0.6)
        plt.ylabel('C(u$_{x}$,u$_{x}$)',fontsize='28')
        plt.tight_layout()
        plt.savefig(figdir+'C(u,u).png',dpi=fdpi)

        plt.figure(num=6,figsize=(10,8))
        self.Plotting(self.P_var,self.P2_var,t_list)
        plt.grid(alpha=0.6)
        plt.ylabel('C(P,P)',fontsize='28')
        plt.tight_layout()
        plt.savefig(figdir+'C(P,P).png',dpi=fdpi)

        plt.figure(num=7,figsize=(10,8))
        self.Plotting(self.T_var,self.T2_var,t_list)
        plt.grid(alpha=0.6)
        plt.ylabel('C(T,T)',fontsize='28')
        plt.ticklabel_format(style='plain',axis='y',scilimits=(0,0),useMathText=False,useOffset=False)
        plt.tight_layout()
        plt.savefig(figdir+'C(T,T).png',dpi=fdpi)

        plt.figure(num=8,figsize=(10,8))
        self.Plotting(self.V_var,self.V2_var,t_list)
        plt.grid(alpha=0.6)
        plt.ylabel('C(v,v)',fontsize='28')
        plt.tight_layout()
        plt.savefig(figdir+'C(v,v).png',dpi=fdpi)

        #-------------------------------------------Covariance-----------------------------------

        plt.figure(num=9,figsize=(9,7))
        self.Plotting(self.DP_cov,self.DP2_cov,t_list)
        plt.grid(alpha=0.6)
        plt.ylabel('C(u$_{x}$,P)',fontsize='28')
        plt.tight_layout()
        plt.savefig(figdir+'C(u,P).png',dpi=fdpi)

        plt.figure(num=10,figsize=(9,7))
        self.Plotting(self.HP_cov,self.HP2_cov,t_list)
        plt.grid(alpha=0.6)
        plt.ylabel('C(y,P)',fontsize='28')
        plt.tight_layout()
        plt.savefig(figdir+'C(y,P).png',dpi=fdpi)

        plt.figure(num=11,figsize=(9,7))
        self.Plotting(self.DH_cov,self.DH2_cov,t_list)
        plt.grid(alpha=0.6)
        plt.ylabel('C(y,u$_{x}$)',fontsize='28')
        #plt.ticklabel_format(style='plain',axis='y',scilimits=(0,0),useMathText=False,useOffset=False)
        plt.tight_layout()
        plt.savefig(figdir+'C(y,u).png',dpi=fdpi)

        plt.figure(num=12,figsize=(9,7))
        self.Plotting(self.DT_cov,self.DT2_cov,t_list)
        plt.grid(alpha=0.6)
        plt.ylabel('C(u$_{x}$,T)',fontsize='28')
        #plt.ticklabel_format(style='plain',axis='y',scilimits=(0,0),useMathText=False,useOffset=False)
        plt.tight_layout()
        plt.savefig(figdir+'C(u,T).png',dpi=fdpi)

        plt.figure(num=13,figsize=(9,7))
        self.Plotting(self.TP_cov,self.TP2_cov,t_list)
        plt.grid(alpha=0.6)
        plt.ylabel('C(T,P)',fontsize='28')
        #plt.ticklabel_format(style='plain',axis='y',scilimits=(0,0),useMathText=False,useOffset=False)
        plt.tight_layout()
        plt.savefig(figdir+'C(T,P).png',dpi=fdpi)

        #----------------------------------------------Correlation Coefficient----------------------------------------

        plt.figure(num=110,figsize=(9,7))
        self.Plotting(self.DH_corr,self.DH2_corr,t_list)
        plt.grid(alpha=0.6)
        plt.ylabel('Corr(y,u$_{x}$)',fontsize='28')
        #plt.ticklabel_format(style='plain',axis='y',scilimits=(0,0),useMathText=False,useOffset=False)
        plt.tight_layout()
        plt.savefig(figdir+'Corr(y,u).png',dpi=fdpi)

        plt.figure(num=111,figsize=(9,7))
        self.Plotting(self.HP_corr,self.HP2_corr,t_list)
        plt.grid(alpha=0.6)
        plt.ylabel('Corr(y,P)',fontsize='28')
        #plt.ticklabel_format(style='plain',axis='y',scilimits=(0,0),useMathText=False,useOffset=False)
        plt.tight_layout()
        plt.savefig(figdir+'Corr(y,P).png',dpi=fdpi)

        plt.figure(num=112,figsize=(9,7))
        self.Plotting(self.DP_corr,self.DP2_corr,t_list)
        plt.grid(alpha=0.6)
        plt.ylabel('Corr(u$_{x}$,P)',fontsize='28')
        #plt.ticklabel_format(style='plain',axis='y',scilimits=(0,0),useMathText=False,useOffset=False)
        plt.tight_layout()
        plt.savefig(figdir+'Corr(u,P).png',dpi=fdpi)

        plt.figure(num=113,figsize=(9,7))
        self.Plotting(self.DT_corr,self.DT2_corr,t_list)
        plt.grid(alpha=0.6)
        plt.ylabel('Corr(u$_{x}$,T)',fontsize='28')
        #plt.ticklabel_format(style='plain',axis='y',scilimits=(0,0),useMathText=False,useOffset=False)
        plt.tight_layout()
        plt.savefig(figdir+'Corr(u,T).png',dpi=fdpi)

        plt.figure(num=114,figsize=(9,7))
        self.Plotting(self.TP_corr,self.TP2_corr,t_list)
        plt.grid(alpha=0.6)
        plt.ylabel('Corr(T,P)',fontsize='28')
        #plt.ticklabel_format(style='plain',axis='y',scilimits=(0,0),useMathText=False,useOffset=False)
        plt.tight_layout()
        plt.savefig(figdir+'Corr(T,P).png',dpi=fdpi)
    
        plt.close('all')

