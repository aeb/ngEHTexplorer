
from kivy.app import App

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.graphics import Ellipse, Color, Line, Point
from kivy.metrics import dp, sp
from kivy.uix.label import Label
from kivy.clock import Clock

from kivy.properties import StringProperty, NumericProperty, ObjectProperty, BooleanProperty

import numpy as np


_mypb_stop = False


class LogoProgressWheel(FloatLayout) :    

    completion_percentage = NumericProperty(0)
    fps = NumericProperty(30)
    
    def __init__(self,**kwargs) :
        super().__init__(**kwargs)

        # Choose some scales
        self.outer_size = dp(200)
        # self.outer_size = dp(100)
        self.background_color = (0,0.6,1,0.25)
        self.color = (1,1,1,1)
        self.color_red = 0.75
        self.width = dp(2)
        
        # Set a message
        self.text = "Making image ..."
        self.lbl = None

        # Generate the circle details
        self.radius_list = np.array([1.0, 0.80, 0.69, 0.53, 0.41, 0.24])
        self.phi0_list = np.array([0, 90, 180, 240, 30, 180, 180])
        self.total_phi0_list = (self.phi0_list[1:]-self.phi0_list[:-1]+360.0)%360.0 + 360.0
        self.dx_list = np.zeros(len(self.radius_list))
        self.dy_list = np.zeros(len(self.radius_list))
        for j in range(1,len(self.radius_list)) :
            self.dx_list[j] = (self.radius_list[j]-self.radius_list[j-1]) * np.sin(self.phi0_list[j]*np.pi/180.0) + self.dx_list[j-1]
            self.dy_list[j] = (self.radius_list[j]-self.radius_list[j-1]) * np.cos(self.phi0_list[j]*np.pi/180.0) + self.dy_list[j-1]

        # Specify the pulse parameters
        self.Npulse = 5
        max_lag_length = 60.0 # 60 degrees total
        min_lag_length = 1.0 # 1 deg
        # self.pulse_lag = np.logspace(np.log10(max_lag_length),np.log10(min_lag_length),self.Npulse)
        self.pulse_lag = min_lag_length + (max_lag_length-min_lag_length)*(np.linspace(1,0,self.Npulse+1)[:-1])**2
        self.pulse_color_red = np.linspace(self.color_red,1.0,self.Npulse+1)[1:]
        # self.pulse_width = np.logspace(np.log10(dp(2)),np.log10(dp(6)),self.Npulse+1)[1:]
        self.pulse_width = dp(2) + (dp(6)-dp(2))*np.linspace(0,1,self.Npulse+1)[1:]

        
        
        print("Pulse details:")
        print("  ",self.pulse_color_red)
        print("  ",self.pulse_lag)
        print("  ",self.pulse_width)

        # Find the relrrative times for all of this
        self.time_frac = np.zeros(len(self.radius_list)+1)
        for j in range(1,len(self.time_frac)) :
            self.time_frac[j] = self.time_frac[j-1] + self.total_phi0_list[j-1]*self.radius_list[j-1]*np.pi/180.0
        self.time_frac = self.time_frac / self.time_frac[-1] * 100.0


        total_phi0 = np.sum(self.total_phi0_list)
        self.time_frac = self.time_frac * total_phi0 / (total_phi0+max_lag_length)

        print("Circle max rotation:")
        print("  ",self.total_phi0_list)
        print("  ",self.time_frac)
        
    def draw_progress_bar(self,completion_percentage) :

        if (not self.lbl is None) :
            self.lbl.parent.remove_widget(self.lbl)

        self.canvas.clear()

        c = np.maximum(0, (self.total_phi0_list/360.0)*(completion_percentage-self.time_frac[:-1])/(self.time_frac[1:]-self.time_frac[:-1]) )
        circ_scale = 0.45*self.outer_size

        with self.canvas :
            Color(self.background_color[0],self.background_color[1],self.background_color[2],self.background_color[3])
            Ellipse(pos=(0.5*self.width-0.5*self.outer_size,0.5*self.height-0.5*self.outer_size),size=(self.outer_size,self.outer_size))

            for j in range(len(c)) :
                if (c[j]>0) :

                    xc = 0.5*self.width-self.dx_list[j]*circ_scale
                    yc = 0.5*self.height-self.dy_list[j]*circ_scale
                    rc = self.radius_list[j]*circ_scale
                    dphi = 360.0*c[j]
                    
                    Color(self.color_red*self.color[0],self.color_red*self.color[1],self.color_red*self.color[2],self.color[3])
                    Line(circle=(xc,yc,rc,self.phi0_list[j],self.phi0_list[j]+dphi),width=dp(2))

                    for k in range(self.Npulse) :
                        Color(self.pulse_color_red[k]*self.color[0],self.pulse_color_red[k]*self.color[1],self.pulse_color_red[k]*self.color[2],self.color[3])

                        phi_tail = self.phi0_list[j] + max(0,dphi-self.pulse_lag[k])
                        phi_head = min( self.phi0_list[j]+dphi, self.phi0_list[j] + self.total_phi0_list[j] )
                        
                        if (phi_tail<self.total_phi0_list[j]+self.phi0_list[j]) :
                            Line(circle=(xc,yc,rc,phi_tail,phi_head),width=self.pulse_width[k])

                    
        self.lbl = Label(pos=(0,-0.5*self.outer_size-dp(20)),text=self.text,color=self.color,font_size=dp(15))
        self.add_widget(self.lbl)

    def pulse_circle(self,color_red,width,alpha,alpha_list=None) :

        if (not self.lbl is None) :
            self.lbl.parent.remove_widget(self.lbl)
            # print("Killing past label")

        if (alpha_list is None) :
            alpha_list = np.ones(len(self.radius_list))*alpha
        
        self.canvas.clear()

        circ_scale = 0.45*self.outer_size

        with self.canvas :
            Color(self.background_color[0],self.background_color[1],self.background_color[2],self.background_color[3]*alpha)
            Ellipse(pos=(0.5*self.width-0.5*self.outer_size,0.5*self.height-0.5*self.outer_size),size=(self.outer_size,self.outer_size))

            for j in range(len(self.radius_list)) :
                Color(color_red*self.color[0],color_red*self.color[1],color_red*self.color[2],self.color[3]*alpha_list[j])
                xc = 0.5*self.width-self.dx_list[j]*circ_scale
                yc = 0.5*self.height-self.dy_list[j]*circ_scale
                rc = self.radius_list[j]*circ_scale
                Line(circle=(xc,yc,rc),close=True,width=width)

        self.lbl = Label(pos=(0,-0.5*self.outer_size-dp(20)),text=self.text,color=(color_red*self.color[0],color_red*self.color[1],color_red*self.color[2],self.color[3]*alpha),font_size=dp(15))
        self.add_widget(self.lbl)


    def evolving_pulse_circle(self,x) :

        f = self.pulse_function(10*x)
        cr = self.color_red+(1.0-self.color_red)*f
        wd = dp(2)+dp(2)*f
        alf = 1.0/(1.0 + np.exp( 2*(10*x-5) ))

        self.pulse_circle(cr,wd,alf)

    def pulse_function(self,x) :
        return np.exp(2-1.0/x-x)
        
    def fermi(self,x,xcut,beta) :
        return 1.0/(1.0 + np.exp( beta*(x-xcut) ) )
        
    def evolving_pulse_drop_circle(self,x) :

        f = self.pulse_function(10*x)
        cr = self.color_red+(1.0-self.color_red)*f
        wd = dp(2)+dp(2)*f
        alf = self.fermi(10*x,5,1)
        alf_list = np.zeros(len(self.radius_list))
        for j in range(len(alf_list)) :
            alf_list[j] = self.fermi(10*x,5+2*float(j)/len(alf_list),5)

        self.pulse_circle(cr,wd,alf,alpha_list=alf_list)
                
    def complete(self,total_time=2) :
        for dt in np.linspace(0,total_time,int(total_time*self.fps)) :
            # Clock.schedule_once( lambda x : self.evolving_pulse_circle(x/total_time), dt)
            Clock.schedule_once( lambda x : self.evolving_pulse_drop_circle(x/total_time), dt)

    def clock_run(self,total_time) :
        for dt in np.linspace(0,total_time,int(total_time*self.fps)) :
            Clock.schedule_once( lambda x : self.draw_progress_bar(100*x/total_time) , dt)

            
