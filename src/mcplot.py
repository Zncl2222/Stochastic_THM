import numpy as np
import matplotlib.pyplot as plt
from activate import Event
#from gui import main_GUI

class Stochastic_Plot(Event):

    def Plotting(self,IPM,DPM,t_list):

        #-----------------------------------Parameter setting-------------------------------------
        legend=[]
        tc=['5','25','50','125','150','200','300','400','500','800']
        t=[0,0,0,0,0,0,0,0,0]
        I=["LPM 5a","LPM 25a","LPM 50a","LPM 125a","LPM 150a","LPM 200a","LPM 300a","LPM 400a","LPM 500a","LPM 500a"]
        D=["NPM 5a","NPM 25a","NPM 50a","NPM 125a","NPM 150a","NPM 200a","NPM 300a","NPM 400a","NPM 500a","NPM 800a"]
        color=self.linecolor
        linestyle=self.linestyle
        Dsymbol=self.linesymbol
        x=np.linspace(0,self.Model_len-1,self.Model_len)
        #------------------------------------Plotting(Spatial domain)---------------------------------------------- 
     
        for i in range(len(tc)):
            if t_list.count(tc[i])==1:
                t[i]=1
        count=0
        symbol=0
        for i in range(len(t)):
            if t[i]==1:
                Line_color=self.linecolor[symbol]
                if Line_color.count(',')>0:
                    Line_color=Line_color.split(',')
                    Line_color=[float(x)/255 for x in Line_color]
                ax,=plt.plot(x,IPM[:,count],color=Line_color,linestyle=self.linestyle[self.linstyle_index],linewidth=self.linewidth_LPM)
                legend.append(I[count])
                symbol=symbol+1
            count=count+1

        count=0
        symbol=0
        for item in t:
            if item==1:
                Line_color=self.linecolor[symbol]
                if Line_color.count(',')>0:
                    Line_color=Line_color.split(',')
                    Line_color=[float(x)/255 for x in Line_color]
                ax,=plt.plot(x,DPM[:,count],self.linesymbol[symbol],linewidth=self.linewidth_NPM,color='k',markerfacecolor=Line_color,
                              markeredgecolor='k',markersize=self.Markersize,markevery=self.Markevery)
                legend.append(D[count])
                symbol=symbol+1
            count=count+1


        plt.legend(legend,ncol=2,fontsize=self.legendfontsize,edgecolor='k')
        plt.xlabel('Distance(m)',fontsize=self.xlabelsize)
        plt.ticklabel_format(style=self.notation,axis='y',scilimits=(0,0),useMathText=True,useOffset=False)
        #plt.rc('font', size=17)
        plt.xticks(fontsize=self.XYTickssize),plt.yticks(fontsize=self.XYTickssize)

    def Uncertainty_Plot(Mean_Variable,MAX_MIN,Z_std,t_index):
    
        import numpy as np
        import matplotlib.pyplot as plt
        
        #------------------------Parameters----------------------------------------------
        Title=['t=5(a)','t=25(a)','t=50(a)','t=125(a)','t=150(a)','t=200(a)','t=300(a)','t=400(a)','t=500(a)','t=800(a)']       
        #-------------------------Plot max and min-----------------------------------------------
        maximum,=plt.plot(MAX_MIN[0][:,t_index],'--k',zorder=3)
        minimun,=plt.plot(MAX_MIN[1][:,t_index],'-.k',zorder=3)
        meanvalue,=plt.plot(Mean_Variable[:,t_index],zorder=3,color='b',linewidth='3')

        x=np.linspace(0,self.Model_len-1,self.Model_len)
        
        s1,=plt.plot(Z_std[0][:,t_index,0],linestyle='-.',color='b',zorder=3)
        plt.plot(Z_std[1][:,t_index,0],linestyle='-.',color='b',zorder=3)

        s2,=plt.plot(Z_std[0][:,t_index,1],linestyle='-.',color='r',zorder=3)
        plt.plot(Z_std[1][:,t_index,1],linestyle='-.',color='r',zorder=3)

        s3,=plt.plot(Z_std[0][:,t_index,2],linestyle='-.',color='g',zorder=3)
        plt.plot(Z_std[1][:,t_index,2],linestyle='-.',color='g',zorder=3)

        plt.fill_between(x,Mean_Variable[:,t_index],Z_std[0][:,t_index,0],alpha=0.7,color='g',zorder=1)
        plt.fill_between(x,Mean_Variable[:,t_index],Z_std[1][:,t_index,0],alpha=0.7,color='g',zorder=1)

        plt.fill_between(x,Z_std[0][:,t_index,0],Z_std[0][:,t_index,1],alpha=0.4,color='g',zorder=1)
        plt.fill_between(x,Z_std[1][:,t_index,0],Z_std[1][:,t_index,1],alpha=0.4,color='g',zorder=1)

        plt.fill_between(x,Z_std[0][:,t_index,1],Z_std[0][:,t_index,2],alpha=0.2,color='g',zorder=1)
        plt.fill_between(x,Z_std[1][:,t_index,1],Z_std[1][:,t_index,2],alpha=0.2,color='g',zorder=1)

        plt.xlabel("Distance (m)", fontsize='28')  
        plt.ticklabel_format(style='sci',axis='y',scilimits=(0,0),useMathText=True,useOffset=False)
        plt.rc('font', size=17)
        plt.xticks(fontsize=25);plt.yticks(fontsize=25)
        plt.legend(handles=[maximum,minimun,meanvalue,s1,s2,s3],labels=["max","min","μ (mean)","μ ± σ","μ ± 2σ","μ ± 3σ"],ncol=2,fontsize='18',loc='best',edgecolor='k')
        plt.grid(alpha=0.3,zorder=2)
        plt.title("Host Rock: "+Title[t_index],fontsize=28)

    def Canvas_parameters(self,*args):
        self.index=args[0]
        self.index2=args[1]
        self.f1=args[2]
        self.f2=args[3]
        self.canvas=args[4]
        
    def Cavanas_Plot(self,canvas_n,t_list):
        
        import numpy as np
        import pandas as pd
        import matplotlib.pyplot as plt
        import time
        time.sleep(0.1)


        plotlist=[self.D_mean,self.P_mean,self.T_mean,self.V_mean,self.D_var,self.P_var,self.T_var,self.V_var,
                    self.HP_cov,self.DH_cov,self.DP_cov,self.DT_cov,self.TP_cov,self.HP_corr,self.DH_corr,
                    self.DP_corr,self.DT_corr,self.TP_corr,self.D,self.P,self.T,self.V,self.H]

        plotlist2=[self.D2_mean,self.P2_mean,self.T2_mean,self.V2_mean,self.D2_var,self.P2_var,self.T2_var,self.V2_var,
                    self.HP2_cov,self.DH2_cov,self.DP2_cov,self.DT2_cov,self.TP2_cov,self.HP2_corr,self.DH2_corr,
                    self.DP2_corr,self.DT2_corr,self.TP2_corr,self.D2,self.P2,self.T2,self.V2,self.H2]

        if canvas_n==self.f1:
            IPM=plotlist[self.index]
            DPM=plotlist2[self.index]

        if canvas_n==self.f2:
            IPM=plotlist[self.index2]
            DPM=plotlist2[self.index2]

        #-----------------------------------Parameter setting------------------------------------------------------
        legend=[]
        tc=['5','25','50','125','150','200','300','400','500','800']
        t=[0,0,0,0,0,0,0,0,0,0]
        t_nRplot=[0,0,0,0,0,0,0,0,0,0]
        I=["LPM 5a","LPM 25a","LPM 50a","LPM 125a","LPM 150a","LPM 200a","LPM 300a","LPM 400a","LPM 500a","LPM 800a"]
        D=["NPM 5a","NPM 25a","NPM 50a","NPM 125a","NPM 150a","NPM 200a","NPM 300a","NPM 400a","NPM 500a","NPM 800a"]
        color=self.linecolor
        linestyle=self.linestyle
        Dsymbol=self.linesymbol
        x=np.linspace(0,self.Model_len-1,self.Model_len)

        #------------------------------------Plotting(Spatial domain)---------------------------------------------- 
        for i in range(len(tc)):
            if t_list.count(tc[i])==1:
                t[i]=1
                t_nRplot[i]=(self.nR*i+self.nR_plotselect)
        count=0
        symbol=0
        print(t_nRplot)
        for i in range(len(t)):
            
            if t[i]==1:
                Line_color=self.linecolor[symbol]
                if Line_color.count(',')>0:
                    Line_color=Line_color.split(',')
                    Line_color=[float(x)/255 for x in Line_color]
                if np.shape(IPM)[1]<50:
                    canvas_n.plot(x,IPM[:,count],color=Line_color,linestyle=self.linestyle[self.linstyle_index],linewidth=self.linewidth_LPM)
                    legend.append(I[count])
                elif self.nRPlotLPM_check==1:
                    #canvas_n.plot(x,IPM[:,range(self.nR*self.timeselect+self.nR_plotstart,self.nR*self.timeselect+self.nR_plotend,self.plot_steps)],
                                #linestyle=self.linestyle[self.linstyle_index],linewidth=self.linewidth_LPM)
                    canvas_n.plot(x,IPM[:,t_nRplot[count]],linestyle=self.linestyle[self.linstyle_index],linewidth=self.linewidth_LPM,label=I[count])
                    legend.append(I[count])
                symbol=symbol+1
            count=count+1
        
        count=0
        symbol=0
        for item in t:
            if item==1:
                Line_color=self.linecolor[symbol]
                if Line_color.count(',')>0:
                    Line_color=Line_color.split(',')
                    Line_color=[float(x)/255 for x in Line_color]
                if np.shape(DPM)[1]<50:
                    canvas_n.plot(x,DPM[:,count],self.linesymbol[symbol],linewidth=self.linewidth_NPM,color='k',markerfacecolor=Line_color,
                                markeredgecolor='k',markersize=self.Markersize,markevery=self.Markevery)
                    legend.append(D[count])
                elif self.nRPlotNPM_check==1:
                    #canvas_n.plot(x,DPM[:,range(self.nR*self.timeselect+self.nR_plotstart,self.nR*self.timeselect+self.nR_plotend,self.plot_steps)],
                                #self.linesymbol[symbol],linewidth=self.linewidth_NPM,markeredgecolor='k',markersize=self.Markersize,markevery=self.Markevery)
                    canvas_n.plot(x,DPM[:,t_nRplot[count]],self.linesymbol[symbol],linewidth=self.linewidth_NPM,
                                markeredgecolor='k',markersize=self.Markersize,markevery=self.Markevery,label=D[count])
                    legend.append(D[count])
                
                symbol=symbol+1
            count=count+1

        canvas_n.grid(alpha=0.3)
        canvas_n.legend(legend,ncol=2,fontsize='9',edgecolor='k')
        plt.ticklabel_format(style=self.notation,axis='y',scilimits=(0,0),useMathText=True,useOffset=False)
        plt.rc('font', size=9)
  
        self.canvas.draw_idle()

class Deterministic_Plot(Event):

    def Plotting(self,IPM,DPM,t_list):

        #-----------------------------------Parameter setting-------------------------------------
        legend=[]
        tc=['5','25','50','125','150','200','300','400','500','800']
        t=[0,0,0,0,0,0,0,0,0,0]
        I=["LPM 5a","LPM 25a","LPM 50a","LPM 125a","LPM 150a","LPM 200a","LPM 300a","LPM 400a","LPM 500a","LPM 800a"]
        D=["NPM 5a","NPM 25a","NPM 50a","NPM 125a","NPM 150a","NPM 200a","NPM 300a","NPM 400a","NPM 500a","NPM 800a"]
        color=self.linecolor
        linestyle=self.linestyle
        Dsymbol=self.linesymbol
        x=np.linspace(0,self.Model_len-1,self.Model_len)
        #------------------------------------Plotting(Spatial domain)---------------------------------------------- 
     
        for i in range(len(tc)):
            if t_list.count(tc[i])==1:
                t[i]=1
        count=0
        symbol=0
        for i in range(len(t)):
            if t[i]==1:
                Line_color=self.linecolor[symbol]
                if Line_color.count(',')>0:
                    Line_color=Line_color.split(',')
                    Line_color=[float(x)/255 for x in Line_color]
                ax,=plt.plot(IPM.iloc[:,0],IPM.iloc[:,count+1],color=Line_color,linestyle=self.linestyle[self.linstyle_index],linewidth=self.linewidth_LPM)
                legend.append(I[count])
                symbol=symbol+1
            count=count+1

        count=0
        symbol=0
        for item in t:
            if item==1:
                Line_color=self.linecolor[symbol]
                if Line_color.count(',')>0:
                    Line_color=Line_color.split(',')
                    Line_color=[float(x)/255 for x in Line_color]
                ax,=plt.plot(DPM.iloc[:,0],DPM.iloc[:,count+1],self.linesymbol[symbol],linewidth=self.linewidth_NPM,color='k',markerfacecolor=Line_color,
                              markeredgecolor='k',markersize=self.Markersize,markevery=self.Markevery)
                legend.append(D[count])
                symbol=symbol+1
            count=count+1


        plt.legend(legend,ncol=2,fontsize=self.legendfontsize,edgecolor='k')
        plt.xlabel('Distance(m)',fontsize=self.xlabelsize)
        plt.ticklabel_format(style=self.notation,axis='y',scilimits=(0,0),useMathText=True,useOffset=False)
        #plt.rc('font', size=17)
        plt.xticks(fontsize=self.XYTickssize),plt.yticks(fontsize=self.XYTickssize)

    def Plotting_MX80(IPM,DPM,t_list):
        #-----------------------------------Parameter setting-------------------------------------
        legend=[]
        tc=['1h','5h','10h','30h','50h','1','5','15','25','100','200','300']
        t=[0,0,0,0,0,0,0,0,0,0,0,0]
        I=["LPM 1hr","LPM 5hr","LPM 10hr","LPM 30hr","LPM 50hr","LPM 1d","LPM 5d","LPM 15d","LPM 25d","LPM 100d","LPM 200d","lPM 300d"]
        D=["NPM 1hr","NPM 5hr","NPM 10hr","NPM 30hr","NPM 50hr","NPM 1d","NPM 5d","NPM 15d","NPM 25d","NPM 100d","NPM 200d","NPM 300d"]
        color=['olive','g','darkorange','r','b','y']
        Isymbol=['o','s','<','d','^','o','s','<','d']
        Dsymbol=['o','s','<','d','^','o','s','<','d']
        #------------------------------------Plotting(Spatial domain)----------------------------------------------
        for i in range(len(tc)):
            if t_list.count(tc[i])==1:
                t[i]=1
        count=0
        symbol=0
        for item in t:
            if item==1:
                Line_color=self.linecolor[symbol]
                if Line_color.count(',')>0:
                    Line_color=Line_color.split(',')
                    Line_color=[float(x)/255 for x in Line_color]
                ax,=plt.plot(IPM.iloc[:,0],IPM.iloc[:,count+1],color=Line_color,linestyle=self.linestyle[self.linstyle_index],linewidth=self.linewidth_LPM)
                legend.append(I[count])
                symbol=symbol+1
            count=count+1
        count=0
        symbol=0
        for item in t:
            if item==1:
                Line_color=self.linecolor[symbol]
                if Line_color.count(',')>0:
                    Line_color=Line_color.split(',')
                    Line_color=[float(x)/255 for x in Line_color]
                ax,=plt.plot(DPM.iloc[:,0],DPM.iloc[:,count+1],self.linesymbol[symbol],linewidth=self.linewidth_NPM,color='k',markerfacecolor=Line_color,
                              markeredgecolor='k',markersize=self.Markersize,markevery=self.Markevery)
                legend.append(D[count])
                symbol=symbol+1
            count=count+1
    
        plt.legend(legend,ncol=2,fontsize='14',edgecolor='k')
        plt.xlabel('Distance(m)',fontsize='28')
        plt.xticks(fontsize=25),plt.yticks(fontsize=25)
        plt.ticklabel_format(style='sci',axis='y',scilimits=(0,0),useMathText=True,useOffset=False)
        plt.rc('font', size=17)
    

    def Plotting_time(self,IPM,DPM,location='best'):
        #-----------------------------------Parameter setting-------------------------------------
        legend=[]
        print(IPM.shape[1])
        if IPM.shape[1]==6:
            I=['LPM 11m','LPM 37m','LPM 75m','LPM 113m']
            D=['NPM 11m','NPM 37m','NPM 75m','NPM 113m']
        else:
            I=['LPM 0.1m','LPM 0.2m','LPM 0.3m']
            D=['NPM 0.1m','NPM 0.2m','NPM 0.3m']

        color=['olive','g','darkorange','r','b','y']
        Isymbol=['o','s','<','d','^','o','s','<','d']
        Dsymbol=['o','s','<','d','^','o','s','<','d']
        #------------------------------------Plotting(Spatial domain)---------------------------------------------- 
        count=1 
        symbol=0
        for i in range(len(I)):
            Line_color=self.linecolor[symbol]
            if Line_color.count(',')>0:
                Line_color=Line_color.split(',')
                Line_color=[float(x)/255 for x in Line_color]
            plt.plot(IPM.iloc[:,0],IPM.iloc[:,count],color=Line_color,linestyle=self.linestyle[self.linstyle_index],linewidth=self.linewidth_LPM,markeredgecolor='k')
            legend.append(I[symbol])
            symbol=symbol+1
            count=count+1
        count=1
        symbol=0
        for i in range(len(D)):
            Line_color=self.linecolor[symbol]
            if Line_color.count(',')>0:
                Line_color=Line_color.split(',')
                Line_color=[float(x)/255 for x in Line_color]
            plt.plot(DPM.iloc[:,0],DPM.iloc[:,count],self.linesymbol[symbol],linewidth=self.linewidth_NPM,color='k',markerfacecolor=Line_color,
                    markeredgecolor='k',markersize=self.Markersize,markevery=self.Markevery)
            legend.append(D[symbol])
            symbol=symbol+1
            count=count+1

        plt.legend(legend,ncol=2,fontsize=self.legendfontsize,edgecolor='k',loc=location)
        plt.xlabel('Time(a)',fontsize=self.xlabelsize)
        plt.ticklabel_format(style=self.notation,axis='y',scilimits=(0,0),useMathText=True,useOffset=False)
        plt.xticks(fontsize=self.XYTickssize),plt.yticks(fontsize=self.XYTickssize)

    def Canvas_parameters(self,*args):
        self.index3=args[0]
        self.index4=args[1]
        self.f3=args[2]
        self.f4=args[3]
        self.canvas=args[4]
        
    def Cavanas_Plot(self,canvas_n,t_list):
        
        import numpy as np
        import matplotlib.pyplot as plt
        import time
        time.sleep(0.1)

        plotlist3=[self.Dt_D,self.Dt_P,self.Dt_T,self.Dt_V,self.Dt_H,self.Dt_kc,self.Dt_Cp,self.Dt_n,self.Dt_E,self.Dt_B]
        plotlist4=[self.Dt_D2,self.Dt_P2,self.Dt_T2,self.Dt_V2,self.Dt_H2,self.Dt_kc2,self.Dt_Cp2,self.Dt_n2,self.Dt_E2,self.Dt_B2]


        if canvas_n==self.f3:
            IPM=plotlist3[self.index3]
            DPM=plotlist4[self.index3]

        if canvas_n==self.f4:
            IPM=plotlist3[self.index4]
            DPM=plotlist4[self.index4]

        #-----------------------------------Parameter setting------------------------------------------------------
        legend=[]
        tc=['5','25','50','125','150','200','300','400','500','800']
        t=[0,0,0,0,0,0,0,0,0,0]
        t_nRplot=[0,0,0,0,0,0,0,0,0,0]
        I=["LPM 5a","LPM 25a","LPM 50a","LPM 125a","LPM 150a","LPM 200a","LPM 300a","LPM 400a","LPM 500a","LPM 800a"]
        D=["NPM 5a","NPM 25a","NPM 50a","NPM 125a","NPM 150a","NPM 200a","NPM 300a","NPM 400a","NPM 500a","NPM 800a"]
        color=self.linecolor
        linestyle=self.linestyle
        Dsymbol=self.linesymbol
        x=np.linspace(0,self.Model_len-1,self.Model_len)
        #------------------------------------Plotting(Spatial domain)---------------------------------------------- 
        for i in range(len(tc)):
            if t_list.count(tc[i])==1:
                t[i]=1
        count=0
        symbol=0
        for i in range(len(t)):
            if t[i]==1:
                Line_color=self.linecolor[symbol]
                if Line_color.count(',')>0:
                    Line_color=Line_color.split(',')
                    Line_color=[float(x)/255 for x in Line_color]
                canvas_n.plot(x,IPM.iloc[:,count+1],color=Line_color,linestyle=self.linestyle[self.linstyle_index],linewidth=self.linewidth_LPM)
                legend.append(I[count])
                symbol=symbol+1
            count=count+1
        
        count=0
        symbol=0
        for item in t:
            if item==1:
                Line_color=self.linecolor[symbol]
                if Line_color.count(',')>0:
                    Line_color=Line_color.split(',')
                    Line_color=[float(x)/255 for x in Line_color]
                canvas_n.plot(x,DPM.iloc[:,count+1],self.linesymbol[symbol],linewidth=self.linewidth_NPM,color='k',markerfacecolor=Line_color,
                            markeredgecolor='k',markersize=self.Markersize-3,markevery=self.Markevery)
                legend.append(D[count])
                symbol=symbol+1
            count=count+1

        canvas_n.grid(alpha=0.3)
        canvas_n.legend(legend,ncol=2,fontsize='9',edgecolor='k')
        plt.ticklabel_format(style=self.notation,axis='y',scilimits=(0,0),useMathText=True,useOffset=False)
        plt.rc('font', size=9)
  
        self.canvas.draw_idle()

    def Cavanas_Plot_t(self,canvas_n):
        
        import numpy as np
        import matplotlib.pyplot as plt
        import time
        time.sleep(0.1)

        plotlist3=[self.Dt_D,self.Dt_P,self.Dt_T,self.Dt_V,self.Dt_H,self.Dt_kc,self.Dt_Cp,self.Dt_n,self.Dt_E,self.Dt_B,
                    self.Dt_Dt,self.Dt_Pt,self.Dt_Tt,self.Dt_Vt]
        plotlist4=[self.Dt_D2,self.Dt_P2,self.Dt_T2,self.Dt_V2,self.Dt_H2,self.Dt_kc2,self.Dt_Cp2,self.Dt_n2,self.Dt_E2,self.Dt_B2,
                   self.Dt_Dt2,self.Dt_Pt2,self.Dt_Tt2,self.Dt_Vt2]
        
        Plotlength=4

        if canvas_n==self.f3:
            IPM=plotlist3[self.index3]
            DPM=plotlist4[self.index3]

        if canvas_n==self.f4:
            IPM=plotlist3[self.index4]
            DPM=plotlist4[self.index4]

        #-----------------------------------Parameter setting------------------------------------------------------
        legend=[]
        I=["LPM 11m","LPM 37m","LPM 75m","LPM 113m"]
        D=["NPM 11m","NPM 37m","NPM 75m","NPM 113m"]
        color=self.linecolor
        linestyle=self.linestyle
        Dsymbol=self.linesymbol
        #------------------------------------Plotting(Spatial domain)---------------------------------------------- 
        for i in range(Plotlength): 
            Line_color=self.linecolor[i]
            if Line_color.count(',')>0:
                Line_color=Line_color.split(',')
                Line_color=[float(x)/255 for x in Line_color]
            canvas_n.plot(IPM.iloc[:,0],IPM.iloc[:,i+1],color=Line_color,linestyle=self.linestyle[self.linstyle_index],linewidth=self.linewidth_LPM)
            legend.append(I[i])
 
        for i in range(Plotlength):
            Line_color=self.linecolor[i]
            if Line_color.count(',')>0:
                Line_color=Line_color.split(',')
                Line_color=[float(x)/255 for x in Line_color]
            canvas_n.plot(DPM.iloc[:,0],DPM.iloc[:,i+1],self.linesymbol[i],linewidth=self.linewidth_NPM,color='k',markerfacecolor=Line_color,
                        markeredgecolor='k',markersize=self.Markersize-3,markevery=self.Markevery)
            legend.append(D[i])


        canvas_n.grid(alpha=0.3)
        canvas_n.legend(legend,ncol=2,fontsize='9',edgecolor='k')
        plt.ticklabel_format(style=self.notation,axis='y',scilimits=(0,0),useMathText=True,useOffset=False)
        plt.rc('font', size=9)
  
        self.canvas.draw_idle()

