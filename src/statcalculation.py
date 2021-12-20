
import numpy as np
from activate import Event

class Statistic():

    def __init__(self,model_len,ntime):
        self.__Model_len=model_len
        self.__ntime=ntime

    def mean(self,Data,nR):
        import numpy as np
        A=np.empty([self.__Model_len,self.__ntime]); temp=np.empty([self.__Model_len,nR])
        for i in range(self.__ntime):
            A[:,i]=np.mean(Data[:,nR*i:nR*(i+1)],axis=1)
        return A
    #-------------------Location Standard deviation------------------------------------------------
    def Standard_deviation(self,Data,nR):
        import numpy as np
        A=np.empty([self.__Model_len,self.__ntime]); temp=np.empty([self.__Model_len,nR])
        for i in range(self.__ntime):
            Mean=np.mean(Data[:,nR*i:nR*(i+1)],axis=1)
            #print(Mean)
            for j in range(nR):
                temp[:,j]=Mean
            #A[:,i]=np.mean((Data[:,nR*i:nR*(i+1)]-np.mean(Data[:,nR*i:nR*(i+1)],axis=1))**2)
            A[:,i]=np.mean(np.sqrt((Data[:,nR*i:nR*(i+1)]-temp)**2),axis=1)
        return A
    #-----------------------------------Location variance-----------------------------------------------------------
    def Variance(self,Data,nR):
        import numpy as np
        A=np.empty([self.__Model_len,self.__ntime]); temp=np.empty([self.__Model_len,nR])
        for i in range(self.__ntime):
            Mean=np.mean(Data[:,nR*i:nR*(i+1)],axis=1)
            #print(Mean)
            for j in range(nR):
                temp[:,j]=Mean
            #A[:,i]=np.mean((Data[:,nR*i:nR*(i+1)]-np.mean(Data[:,nR*i:nR*(i+1)],axis=1))**2)
            A[:,i]=np.mean((Data[:,nR*i:nR*(i+1)]-temp)**2,axis=1)
        return A
    #----------------------------------Location Covariance-------------------------------------------------------

    def Covariance(self,Y1,Y2,nR):
        import numpy as np
        A=np.empty([self.__Model_len,self.__ntime]); temp1=np.empty([self.__Model_len,nR]); temp2=np.empty([self.__Model_len,nR])
        for i in range(self.__ntime):
            Mean1=np.mean(Y1[:,nR*i:nR*(i+1)],axis=1)
            Mean2=np.mean(Y2[:,nR*i:nR*(i+1)],axis=1)
            for j in range(nR):
                temp1[:,j]=Mean1
                temp2[:,j]=Mean2
            #A[:,i]=np.mean((Data[:,nR*i:nR*(i+1)]-np.mean(Data[:,nR*i:nR*(i+1)],axis=1))**2)
            A[:,i]=np.mean((Y1[:,nR*i:nR*(i+1)]-temp1)*(Y2[:,nR*i:nR*(i+1)]-temp2),axis=1)
        return A
    
    def Covariance_Parallel(Y1,Y2,nR,Model_len,ntime):
        import numpy as np
        A=np.empty([Model_len,ntime]); temp1=np.empty([Model_len,nR]); temp2=np.empty([Model_len,nR])
        for i in range(ntime):
            Mean1=np.mean(Y1[:,nR*i:nR*(i+1)],axis=1)
            Mean2=np.mean(Y2[:,nR*i:nR*(i+1)],axis=1)
            for j in range(nR):
                temp1[:,j]=Mean1
                temp2[:,j]=Mean2
            #A[:,i]=np.mean((Data[:,nR*i:nR*(i+1)]-np.mean(Data[:,nR*i:nR*(i+1)],axis=1))**2)
            A[:,i]=np.mean((Y1[:,nR*i:nR*(i+1)]-temp1)*(Y2[:,nR*i:nR*(i+1)]-temp2),axis=1)
        return A

    #----------------------------------Location Correlation Coefficient (same location)-------------------------------------
    def Correlation(self,Y1,Y2,nR):
        import numpy as np
        A=np.empty([self.__Model_len,self.__ntime]); temp1=np.empty([self.__Model_len,nR]); temp2=np.empty([self.__Model_len,nR])
        for i in range(self.__ntime):
            Mean1=np.mean(Y1[:,nR*i:nR*(i+1)],axis=1)
            Mean2=np.mean(Y2[:,nR*i:nR*(i+1)],axis=1)
            for j in range(nR):
                temp1[:,j]=Mean1
                temp2[:,j]=Mean2
            #A[:,i]=np.mean((Data[:,nR*i:nR*(i+1)]-np.mean(Data[:,nR*i:nR*(i+1)],axis=1))**2)
            A[:,i]=np.mean((Y1[:,nR*i:nR*(i+1)]-temp1)*(Y2[:,nR*i:nR*(i+1)]-temp2),axis=1)/np.std(Y1[:,nR*i:nR*(i+1)],axis=1)/np.std(Y2[:,nR*i:nR*(i+1)],axis=1)

        return A
    
    def Correlation_Parallel(Y1,Y2,nR,Model_len,ntime):
        import numpy as np
        A=np.empty([Model_len,ntime]); temp1=np.empty([Model_len,nR]); temp2=np.empty([Model_len,nR])
        for i in range(ntime):
            Mean1=np.mean(Y1[:,nR*i:nR*(i+1)],axis=1)
            Mean2=np.mean(Y2[:,nR*i:nR*(i+1)],axis=1)
            for j in range(nR):
                temp1[:,j]=Mean1
                temp2[:,j]=Mean2
            #A[:,i]=np.mean((Data[:,nR*i:nR*(i+1)]-np.mean(Data[:,nR*i:nR*(i+1)],axis=1))**2)
            A[:,i]=np.mean((Y1[:,nR*i:nR*(i+1)]-temp1)*(Y2[:,nR*i:nR*(i+1)]-temp2),axis=1)/np.std(Y1[:,nR*i:nR*(i+1)],axis=1)/np.std(Y2[:,nR*i:nR*(i+1)],axis=1)

        return A   
    #----------------------------------Uncertainty------------------------------------
    def Max_Min(self,y,nR):
        import numpy as np
        MAX=np.empty([self.__Model_len,self.__ntime]);MIN=np.empty([self.__Model_len,self.__ntime])
        for i in range(self.__Model_len):
            for j in range(self.__ntime):
                MAX[i,j]=np.max(y[i,nR*j:nR*(j+1)])
                MIN[i,j]=np.min(y[i,nR*j:nR*(j+1)])
        Data=[MAX,MIN]
            #print("X=",len(MAX[:][0]))
        return Data

    def Confidence_intervals(self,y_mean,std_y):
        import numpy as np
        R_upper=np.empty([self.__Model_len,self.__ntime,3]);R_down=np.empty([self.__Model_len,self.__ntime,3])
        for i in range(3):
            for j in range(self.__Model_len):
                for k in range(self.__ntime):
                    if i==0:
                        R_upper[j,k,i]=y_mean[j,k]+std_y[j,k]
                        R_down[j,k,i]=y_mean[j,k]-std_y[j,k]
                    if i==1:
                        R_upper[j,k,i]=y_mean[j,k]+2*std_y[j,k]
                        R_down[j,k,i]=y_mean[j,k]-2*std_y[j,k]
                    if i==2:
                        R_upper[j,k,i]=y_mean[j,k]+3*std_y[j,k]
                        R_down[j,k,i]=y_mean[j,k]-3*std_y[j,k]
        return [R_upper, R_down]            
