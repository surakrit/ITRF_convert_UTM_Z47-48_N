import numpy as np
import math

class ITRFThai:
    def __init__(self,dataEN,Tx,Ty,Tz,zone):
        # EN
        self.E=dataEN[2]
        self.N=dataEN[1]
        self.zone=zone
        # Tx Ty Tz
        self.Tx = Tx
        self.Ty = Ty
        self.Tz = Tz
        # Datum parameter (WGS84)
        self.a = 6378137
        self.b = 6356752.31424518
        self.f = (self.a-self.b)/self.a
        self.f1 = 1/self.f
        self.e = np.sqrt((2*self.f)-(pow(self.f,2)))
        self.e2 = pow(self.e,2)
        #UTM var
        self.long0=np.radians(self.zone*6-183)
        self.k0 = 0.9996
        self.E0 = 500000
        self.n = self.f/(2-self.f)
        self.A = (self.a/(1+self.n))*(1+(pow(self.n,2))/4+pow(self.n,4)/64)
        self.a1 = self.n/2-(2/3)*pow(self.n,2)+(5/16)*pow(self.n,3)
        self.a2 = (13/48)*pow(self.n,2)-(3/5)*pow(self.n,3)
        self.a3 = 61*pow(self.n,3)/240
        self.B1 = (self.n/2-(2/3)*pow(self.n,2))+(37/96)*pow(self.n,3)
        self.B2 = (1/48)*pow(self.n,2)+(1/15)*pow(self.n,3)
        self.B3 = (17/480)*pow(self.n,3)
        self.b1 = 2*self.n-(2/3)*pow(self.n,2)-2*pow(self.n,3)
        self.b2 = (7/3)*pow(self.n,2)-(8/5)*pow(self.n,3)
        self.b3 = (56/15)*pow(self.n,3)

    def EN2latlong(self):
        e=self.N/(self.k0*self.A)
        n=(self.E-self.E0)/(self.k0*self.A)
        et=e-(self.B1*np.sin(2*e)*np.cosh(2*n)+self.B2*np.sin(4*e)*np.cosh(4*n)+self.B3*np.sin(6*e)*np.cosh(6*n))
        nt=n-(self.B1*np.cos(2*e)*np.sinh(2*n)+self.B2*np.cos(4*e)*np.sinh(4*n)+self.B3*np.cos(6*e)*np.sinh(6*n))
        X=np.asin(np.sin(et)/np.cosh(nt))
        self.lat=X+(self.b1*np.sin(2*X)+self.b2*np.sin(4*X)+self.b3*np.sin(6*X))
        self.long=self.long0+np.atan2(np.sinh(nt),np.cos(et))
        # return self.lat,self.long
        # print(np.degrees(self.lat),np.degrees(self.long))
    
    def latlong2XYZ(self):
        N=self.a/(np.sqrt(1-self.e2*pow(np.sin(self.lat),2)))
        self.X = N*np.cos(self.lat)*np.cos(self.long)
        self.Y = N*np.cos(self.lat)*np.sin(self.long)
        self.Z = (1-self.e2)*N*np.sin(self.lat)
        # print(self.X,self.Y,self.Z)
    
    def ITRF(self):
        self.X = self.X+self.Tx
        self.Y = self.Y+self.Ty
        self.Z = self.Z+self.Tz
        # print(self.X,self.Y,self.Z)

    def XYZ2latlong(self):
        self.long = np.atan2(self.Y,self.X)
        p = np.sqrt(pow(self.X,2)+pow(self.Y,2))
        self.lat = np.atan2(self.Z,(1-self.e2)*p)
        # print(np.degrees(self.lat),np.degrees(self.long))

    def latlong2EN(self):
        t = np.sinh(np.atanh(np.sin(self.lat))-((2*np.sqrt(self.n))/(1+self.n))*np.atanh(((2*np.sqrt(self.n))/(1+self.n))*np.sin(self.lat)))
        et = np.atan2(t,np.cos(self.long-self.long0))
        nt = np.atanh(np.sin(self.long-self.long0)/np.sqrt(1+pow(t,2)))
        self.E = self.E0 + self.k0*self.A*(nt+(self.a1*np.cos(2*et)*np.sinh(2*nt)+self.a2*np.cos(4*et)*np.sinh(4*nt)+self.a3*np.cos(6*et)*np.sinh(6*nt)))
        self.N = self.k0*self.A*(et+(self.a1*np.sin(2*et)*np.cosh(2*nt)+self.a2*np.sin(4*et)*np.cosh(4*nt)+self.a3*np.sin(6*et)*np.cosh(6*nt)))
        # print(self.N,self.E)



a= ITRFThai([1,1525000.627,666575.053],-0.21,-0.029,-0.076,47)
a.EN2latlong()
a.latlong2XYZ()
a.XYZ2latlong()
a.latlong2EN()
a.ITRF()
a.XYZ2latlong()
a.latlong2EN()
