import numpy as np

from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Line, Point
from kivy.metrics import dp, sp
from kivy.uix.label import Label
from kivymd.uix.label import MDLabel
from kivy.properties import StringProperty, NumericProperty, ObjectProperty, BooleanProperty, VariableListProperty
# from kivymd.app import MDApp
# from kivymd.theming import ThemableBehavior
from kivymd.theming import ThemableBehavior

from kivy.utils import get_color_from_hex

# Data dictionary: datadict has form {'u':u,'v':v,'V':V,'s1':s1d,'s2':s2d,'t':t,'err':err}
# Station dictionary: statdict has form {<station code>:{'on':<True/False>,'name':<name>,'loc':(x,y,z)}}

__baseline_plot_debug__ = False


class InteractiveBaselinePlot_kivygraph(ThemableBehavior,FloatLayout) :

    def __init__(self,**kwargs) :

        self.ddict = {}
        self.ddnew = {}
        self.sdict = {}
        
        super().__init__(**kwargs)

        self.xp = np.array([])
        self.yp = np.array([])
        self.on = np.array([])
        self.offset = [0,0]
        self.N = 0

        # Axis label list
        self.labels = []

        # Defined to be [xmin,ymin,(xmax-xmin),(ymax-ymin)]
        self.plot_location = [15,-15,-30,30]

        self.grid_spacing = 2
        
        self.point_size = dp(2)

        self.rescale = 1.0

        self.plot_frozen = False
        
        self.bind(width=self.resize)
        self.bind(height=self.resize)

        self.background_color = (0,0,0,1)
        self.axis_color = (1,1,1,1)
        self.label_color = (1,1,1,1)

        
        self.theme_cls.bind(theme_style=self.set_theme)
        

    def update(self,datadict,statdict,time_range=None,snr_cut=None,ngeht_diameter=6,make_hermitian=False,limits=None) :

        self.sdict = statdict
        self.ddict = datadict

        if (len(statdict.keys())==0 or len(datadict.keys())==0) :
            return
        
        # Exclude stations not in array
        stations = list(statdict.keys())
        keep = np.array([ (datadict['s1'][j] in stations) and (datadict['s2'][j] in stations) for j in range(len(datadict['s1'])) ])
        ddtmp = {}
        for key in ['u','v','V','s1','s2','t','err'] :
            ddtmp[key] = datadict[key][keep]

        self.ddict = ddtmp

        self.xp = self.ddict['u']
        self.yp = self.ddict['v']
        self.on = (self.xp>-np.inf)
        
        # Exclude stations that are "off"
        if (len(self.ddict['u'])>0) :
            keep = np.array([ statdict[ddtmp['s1'][j]]['on'] and statdict[ddtmp['s2'][j]]['on'] for j in range(len(ddtmp['s1'])) ])
            self.on = self.on*keep
                
        # Exclude data points outside the specified time range
        if (len(self.ddict['u'])>0) :
            if (not time_range is None) :
                keep = (self.ddict['t']>=time_range[0])*(self.ddict['t']<time_range[1])
                self.on = self.on*keep

                    
        # Cut points with S/N less than the specified minimum value
        if (not snr_cut is None)  and (snr_cut>0):
            if (len(self.ddict['u'])>0) :
                # Get a list of error adjustments based on stations
                diameter_correction_factor = {}
                for s in stations :
                    if (statdict[s]['exists']) :
                        diameter_correction_factor[s] = 1.0
                    else :
                        diameter_correction_factor[s] = statdict[s]['diameter']/ngeht_diameter

                # Baseline-by-baseline filtering
                # keep = np.array([ np.abs(self.ddict['V'][j])/(self.ddict['err'][j].real * diameter_correction_factor[self.ddict['s1'][j]] * diameter_correction_factor[self.ddict['s2'][j]]) > snr_cut for j in range(len(self.ddict['s1'])) ])
                # Ad hoc phasing
                keep = np.array([True]*len(self.ddict['s1']))
                jtot = np.arange(self.ddict['t'].size)
                for tscan in np.unique(self.ddict['t']) :
                    inscan = (self.ddict['t']==tscan)
                    s1_scan = self.ddict['s1'][inscan]
                    s2_scan = self.ddict['s2'][inscan]
                    snr_scan = np.array([ self.ddict['V'][inscan][j]/( self.ddict['err'][inscan][j] * diameter_correction_factor[s1_scan[j]] * diameter_correction_factor[s2_scan[j]] ) for j in range(len(s1_scan)) ])
                    detection_station_list = []
                    for ss in np.unique(np.append(s1_scan,s2_scan)) :
                        snr_scan_ss = np.append(snr_scan[s1_scan==ss],snr_scan[s2_scan==ss])
                        if np.any(snr_scan_ss > snr_cut ) :
                            detection_station_list.append(ss)
                    keep[jtot[inscan]] = np.array([ (s1_scan[k] in detection_station_list) and (s2_scan[k] in detection_station_list) for k in range(len(s1_scan)) ])
                    
                        
                    
                
                self.on = self.on*keep



        umax = max(np.max(self.ddict['u']),np.max(self.ddict['v']))
        umax = ((2*umax)//5)*5
        self.plot_location = [0.5*umax,-0.5*umax,-umax,umax]

        # Sparsify if too many points for OpenGL
        if (len(self.xp)>15000) :
            skip = int(np.ceil(len(self.xp)/15000))
            iskip = np.arange(0,len(self.xp),skip)
            self.xp = self.xp[iskip]
            self.yp = self.yp[iskip]
            self.on = self.on[iskip]

            
        if __baseline_plot_debug__ :
            print("SIZES:",self.xp.size,self.yp.size,self.on.size)

            
        self.redraw()

    def replot(self,datadict,statdict,**kwargs) :
        self.update(datadict,statdict,**kwargs)
        if __baseline_plot_debug__ :
            print("InteractiveBaselinePlot_kivygraph.replot")
        
    def x_to_screen(self,x) :
        return ((x-self.plot_location[0])*self.width/self.plot_location[2])*self.rescale + self.offset[0]

    def y_to_screen(self,y) :
        return ((y-self.plot_location[1])*self.width/self.plot_location[3])*self.rescale + self.offset[1]
    
    def screen_to_x(self,xpx) :
        return self.plot_location[0] + self.plot_location[2]*(xpx-self.offset[0])/(self.width*self.rescale)
        
    def screen_to_y(self,ypx) :
        return self.plot_location[1] + self.plot_location[3]*(ypx-self.offset[1])/(self.width*self.rescale)

    def set_theme(self,widget=None,value=None) :
        self.background_color = get_color_from_hex(self.theme_cls.colors[self.theme_cls.theme_style]["Background"])
        self.axis_color = self.theme_cls.text_color
        self.label_color = self.theme_cls.text_color
        self.redraw()
        
    def redraw(self) :
        self.redraw_points()
        self.redraw_axes()
        
    def redraw_axes(self) :

        # Background grid
        grid_width = 2


        self.grid_spacing = 2**(np.ceil(np.log2(abs(self.screen_to_x(self.width)-self.screen_to_x(0.0))/12.0)))

        unit = min(max(-9,(((np.log10(self.grid_spacing)+1)//3)*3)),3)
        if (unit==-9) :
            unit_lbl = ' ('+chr(955)+')'
        elif (unit==-6) :
            unit_lbl = ' (k'+chr(955)+')'    
        elif (unit==-3) :
            unit_lbl = ' (M'+chr(955)+')'    
        elif (unit==0) :
            unit_lbl = ' (G'+chr(955)+')'    
        elif (unit==3) :
            unit_lbl = ' (T'+chr(955)+')'    
        unit_factor = 10**(-unit)
                
        
        with self.canvas :
            Color(0.5,0.5,0.5,0.25)
            for xgrid in np.arange(np.sign(self.plot_location[2])*self.grid_spacing,self.screen_to_x(self.width),np.sign(self.plot_location[2])*self.grid_spacing) :
                xpx = self.x_to_screen(xgrid)
                points = [xpx,0,xpx,self.height]
                Line(points=points,width=grid_width)
            for xgrid in np.arange(-np.sign(self.plot_location[2])*self.grid_spacing,self.screen_to_x(0),-np.sign(self.plot_location[2])*self.grid_spacing) :
                xpx = self.x_to_screen(xgrid)
                points = [xpx,0,xpx,self.height]
                Line(points=points,width=grid_width)
            for ygrid in np.arange(np.sign(self.plot_location[3])*self.grid_spacing,self.screen_to_y(self.height),np.sign(self.plot_location[3])*self.grid_spacing) :
                ypx = self.y_to_screen(ygrid)
                points = [0,ypx,self.width,ypx]
                Line(points=points,width=grid_width)
            for ygrid in np.arange(-np.sign(self.plot_location[3])*self.grid_spacing,self.screen_to_y(0),-np.sign(self.plot_location[3])*self.grid_spacing) :
                ypx = self.y_to_screen(ygrid)
                points = [0,ypx,self.width,ypx]
                Line(points=points,width=grid_width)

            # Axis splines
            # Color(1,1,1)
            # Color(self.theme_cls.text_color[0],self.theme_cls.text_color[1],self.theme_cls.text_color[2])
            Color(self.axis_color[0],self.axis_color[1],self.axis_color[2])
            xpx = self.x_to_screen(0.0)
            points = [xpx,0,xpx,self.height]
            if (xpx>0 and xpx<self.width) :
                Line(points=points,width=2)
            ypx = self.y_to_screen(0.0)
            points = [0,ypx,self.width,ypx]
            if (ypx>0 and ypx<self.height) :
                Line(points=points,width=2)


        # Axis labels
        #  First release all labels
        for lbl in self.labels :
            lbl.parent.remove_widget(lbl)
        self.labels = []


        label_spacing_min = sp(40)
        x_label_spacing = np.ceil(abs( (label_spacing_min/self.width) * (self.screen_to_x(self.width)-self.screen_to_x(0)) )/self.grid_spacing) * self.grid_spacing
        
        #  Second tick labels
        ypx = int(self.y_to_screen(0) - 0.5*self.height+0.5) - 0.75*sp(15)
        if (ypx>-0.5*self.height and ypx<0.5*self.height) :
            for xgrid in np.arange(np.sign(self.plot_location[2])*x_label_spacing,self.screen_to_x(self.width),np.sign(self.plot_location[2])*x_label_spacing) :
                xpx = int(self.x_to_screen(xgrid) - 0.5*self.width+0.5)
                # lbl = MDLabel(text='%4.2f'%(xgrid*unit_factor),pos=(xpx,ypx),font_style='Caption',halign='center')
                lbl = Label(text='%4.2f'%(xgrid*unit_factor),pos=(xpx,ypx),font_size=sp(15),color=self.label_color)
                self.labels.append(lbl)
                self.add_widget(lbl)
            for xgrid in np.arange(-np.sign(self.plot_location[2])*x_label_spacing,self.screen_to_x(0),-np.sign(self.plot_location[2])*x_label_spacing) :
                xpx = int(self.x_to_screen(xgrid) - 0.5*self.width+0.5)
                # lbl = MDLabel(text='%4.2f'%(xgrid*unit_factor),pos=(xpx,ypx),font_style='Caption',halign='center')
                lbl = Label(text='%4.2f'%(xgrid*unit_factor),pos=(xpx,ypx),font_size=sp(15),color=self.label_color)
                self.labels.append(lbl)
                self.add_widget(lbl)
        xpx = int(self.x_to_screen(0) - 0.5*self.width+0.5) - 1.75*sp(15)
        if (xpx>-0.5*self.width and xpx<0.5*self.width) :
            for ygrid in np.arange(np.sign(self.plot_location[3])*x_label_spacing,self.screen_to_y(self.height),np.sign(self.plot_location[3])*x_label_spacing) :
                ypx = int(self.y_to_screen(ygrid) - 0.5*self.height+0.5)
                # lbl = MDLabel(text='%4.2f'%(ygrid*unit_factor),pos=(xpx,ypx),font_style='Caption',halign='center')
                lbl = Label(text='%4.2f'%(ygrid*unit_factor),pos=(xpx,ypx),font_size=sp(15),color=self.label_color)
                self.labels.append(lbl)
                self.add_widget(lbl)
            for ygrid in np.arange(-np.sign(self.plot_location[3])*x_label_spacing,self.screen_to_y(0),-np.sign(self.plot_location[3])*x_label_spacing) :
                ypx = int(self.y_to_screen(ygrid) - 0.5*self.height+0.5)
                # lbl = MDLabel(text='%4.2f'%(ygrid*unit_factor),pos=(xpx,ypx),font_style='Caption',halign='center')
                lbl = Label(text='%4.2f'%(ygrid*unit_factor),pos=(xpx,ypx),font_size=sp(15),color=self.label_color)
                self.labels.append(lbl)
                self.add_widget(lbl)
        
        #  Third plot axis labels
        ypx = int(self.y_to_screen(0.0) - 0.5*self.height + 0.5) + 0.75*sp(20)
        if (ypx>-0.5*self.height and ypx<0.5*self.height) :
            xpx = int( 0.375*self.width + 0.5)
            points = [xpx,0,xpx,self.height]
            # xlbl = MDLabel(text='[i]u[/i]'+unit_lbl,pos=(xpx,ypx),font_style='H6',halign='center', markup=True)
            xlbl = Label(text='[i]u[/i]'+unit_lbl,pos=(xpx,ypx),font_size=sp(20),color=self.label_color,halign='right', markup=True)
            self.labels.append(xlbl)
            self.add_widget(xlbl)
        xpx = int(self.x_to_screen(0.0) - 0.5*self.width + 0.5) + 1.5*sp(20)
        if (xpx>-0.5*self.width and xpx<0.5*self.width) :
            ypx = int( 0.375*self.height + 0.5)
            points = [xpx,0,xpx,self.height]
            # ylbl = MDLabel(text='[i]v[/i]'+unit_lbl,pos=(xpx,ypx),font_style='H6',halign='center', markup=True)
            ylbl = Label(text='[i]v[/i]'+unit_lbl,pos=(xpx,ypx),font_size=sp(20),color=self.label_color,halign='right', markup=True)
            self.labels.append(ylbl)
            self.add_widget(ylbl)


            
    def redraw_points(self) :

        self.canvas.clear()
        with self.canvas :

            xpx = self.x_to_screen(self.xp)
            ypx = self.y_to_screen(self.yp)
            
            #Color(0.14,0.14,0.14)
            Color(0.5,0,0)
            p=Point(pointsize=self.point_size)
            for j in range(len(xpx)) :
                if (self.on[j]==False) :
                    if (ypx[j]<self.height) :
                        p.add_point(xpx[j],ypx[j])

            Color(1,0.75,0.25)
            p=Point(pointsize=self.point_size)
            for j in range(len(xpx)) :
                if (self.on[j]==True) :
                    if (ypx[j]<self.height) :
                        p.add_point(xpx[j],ypx[j])

                    
    def on_touch_move(self,touch) :
        if (self.plot_frozen==False) :
            self.offset = (self.offset[0] + touch.dpos[0],self.offset[1] + touch.dpos[1])
            self.redraw()
    
    def resize(self,widget,newsize) :
        self.rescale = 1.0
        self.offset = [0,0.5*(self.height-self.width)]
        self.redraw()

    def on_touch_down(self,touch) :
        if (touch.is_double_tap) :
            self.resize(self,self.width)
        
    def zoom_in(self) :
        self.rescale = self.rescale * 1.414
        self.offset = [ self.offset[0]*1.414 + 0.5*(1.0-1.414)*self.width, self.offset[1]*1.414 + 0.5*(1.0-1.414)*self.height ]
        self.redraw()
        
    def zoom_out(self) :
        self.rescale = self.rescale * 0.707
        self.offset = [ self.offset[0]*0.707 + 0.5*(1.0-0.707)*self.width, self.offset[1]*0.707 + 0.5*(1.0-0.707)*self.height ]
        self.redraw()



# Lux ex termino
# LU XE XT ER MI NO 07 08 09 10 11 12
