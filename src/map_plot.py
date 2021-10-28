import numpy as np

from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Ellipse, Color, Line
from kivy.metrics import dp
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.widget import Widget
from kivy.graphics import RenderContext, Color, Rectangle
from kivy.properties import ListProperty, StringProperty
from kivy.core.image import Image

from kivymd.theming import ThemableBehavior

from os import path
import copy

# Station dictionary: statdict has form {<station code>:{'on':<True/False>,'name':<name>,'loc':(x,y,z)}}

__map_plot_debug__ = False


class InteractiveWorldMapWidget(ThemableBehavior,Widget):

    tex_coords = ListProperty([0, 1, 1, 1, 1, 0, 0, 0])
    texture_wrap = StringProperty('repeat')
    
    def __init__(self, **kwargs):
        self.canvas = RenderContext()

        self.nx = 1024
        self.ny = self.nx//2

        if (__map_plot_debug__) :
            print("On init:",self.nx,self.ny)
        
        with self.canvas:
            # Background texture
            # self.texture = Image(path.abspath(path.join(path.dirname(__file__),'images/world_spherical.jpg'))).texture
            # self.texture = Image(path.abspath(path.join(path.dirname(__file__),'images/world_spherical_grey.jpg'))).texture
            self.texture = Image(path.abspath(path.join(path.dirname(__file__),'images/world_spherical_grey2.jpg'))).texture
            self.texture.wrap = self.texture_wrap
            self.rect = Rectangle(size=(self.nx,self.ny),texture=self.texture)
            self.rect.tex_coords = self.tex_coords

        if (__map_plot_debug__) :
            print("InteractiveWorldMapWidget._init__ rect.size:",self.rect.size)
            
        # Don't restrict zooming at start
        self.plot_frozen = False
        
        # call the constructor of parent
        # if they are any graphics objects, they will be added on our new
        # canvas
        super(InteractiveWorldMapWidget, self).__init__(**kwargs)

        # We'll update our glsl variables in a clock
        # Clock.schedule_interval(self.update_glsl, 0)        
        Clock.schedule_interval(self.texture_init, 0)

        # Generate some default resizing behaviors
        self.bind(height=self.resize)
        self.bind(width=self.resize)

        self.theme_cls.bind(theme_style=self.set_theme)

        self.map_type_light = 'grey_light'
        self.map_type_dark = 'grey_dark'
        
        
    def set_map_true_color(self,true_color) :
        if (true_color) :
            self.map_type_light = 'color'
            self.map_type_dark = 'color'
        else :
            self.map_type_light = 'grey_light'
            self.map_type_dark = 'grey_dark'
        self.set_theme(None,self.theme_cls.theme_style)
            
        
    def choose_map(self,map_type='color') :
        if (map_type=='color') :
            self.texture = Image(path.abspath(path.join(path.dirname(__file__),'images/world_spherical.jpg'))).texture
        elif (map_type=='grey_light') :
            self.texture = Image(path.abspath(path.join(path.dirname(__file__),'images/world_spherical_grey.jpg'))).texture
        elif (map_type=='grey_dark') :
            self.texture = Image(path.abspath(path.join(path.dirname(__file__),'images/world_spherical_grey2.jpg'))).texture
        else :
            print("ERROR: Unrecognized option %s."%(map_type))
        self.texture.wrap = self.texture_wrap
        self.rect.texture = self.texture
        self.rect.tex_coords = self.tex_coords

        
    def set_theme(self,widget,value) :
        if (value=='Dark') :
            self.choose_map(map_type=self.map_type_dark)
        elif (value=='Light') :
            self.choose_map(map_type=self.map_type_light)

    def update_glsl(self, *largs):
        # This is needed for the default vertex shader.
        self.canvas['projection_mat'] = Window.render_context['projection_mat']
        self.canvas['modelview_mat'] = Window.render_context['modelview_mat']

    def texture_init(self, *args):
        self.texture = self.canvas.children[-1].texture
        self.update_glsl()

    def on_touch_move(self,touch) :
        if (not self.plot_frozen) :
            x_shift = - touch.dpos[0]/float(self.rect.size[0])
            y_shift = touch.dpos[1]/float(self.rect.size[1])
            
            for i in range(0,8,2) :
                self.tex_coords[i] = self.tex_coords[i] + x_shift
                self.tex_coords[i+1] = self.tex_coords[i+1] + y_shift

            if (__map_plot_debug__) :
                print("InteractiveWorldMapWidget.on_touch_move:")
                print("   tex_coords before :",self.tex_coords)
                print("   size/pos/width/height :",self.rect.size,self.rect.pos,self.width,self.height)
                
            self.tex_coords = self.check_boundaries(self.tex_coords)
            
            if (__map_plot_debug__) :
                print("InteractiveWorldMapWidget.on_touch_move:")
                print("   tex_coords  after :",self.tex_coords)
                print("   size/pos/width/height :",self.rect.size,self.rect.pos,self.width,self.height)
            
            self.rect.tex_coords = self.tex_coords

    def on_touch_down(self,touch) :
        if (touch.is_double_tap) :
            self.tex_coords = [0, 1, 1, 1, 1, 0, 0, 0]
            self.rect.tex_coords = self.tex_coords
            self.rect.size = self.check_size((self.nx*self.height/self.ny,self.height))
            self.rect.pos = (max(0,0.5*(self.width-self.rect.size[0])),(self.height-self.rect.size[1]))

    def zoom_in(self) :
        if (__map_plot_debug__) :
            print("InteractiveWorldMapWidget.zoom_in A",self.rect.size,self.rect.pos,self.width,self.rect.tex_coords)
        self.rect.size = self.check_size((self.rect.size[0]*1.414,self.rect.size[1]*1.414))
        self.rect.pos = (max(0,0.5*(self.width-self.rect.size[0])),(self.height-self.rect.size[1]))
        x_shift = self.width/self.rect.size[0]*(1.414-1.0)
        y_shift = 0.5*self.height/self.rect.size[1]*(1.414-1.0)
        for i in range(0,8,2) :
            self.tex_coords[i] = self.tex_coords[i] + x_shift
            self.tex_coords[i+1] = self.tex_coords[i+1] + y_shift
        self.tex_coords = self.check_boundaries(self.tex_coords)
        self.rect.tex_coords = self.tex_coords
        if (__map_plot_debug__) :
            print("InteractiveWorldMapWidget.zoom_in B",self.rect.size,self.rect.pos,self.width,self.rect.tex_coords)
            
    def zoom_out(self) :
        self.rect.size = self.check_size((self.rect.size[0]*0.707,self.rect.size[1]*0.707))
        self.rect.pos = (max(0,0.5*(self.width-self.rect.size[0])),(self.height-self.rect.size[1]))
        x_shift = self.width/self.rect.size[0]*(0.707-1.0)
        y_shift = 0.5*self.height/self.rect.size[1]*(0.707-1.0)
        for i in range(0,8,2) :
            self.tex_coords[i] = self.tex_coords[i] + x_shift
            self.tex_coords[i+1] = self.tex_coords[i+1] + y_shift
        self.tex_coords = self.check_boundaries(self.tex_coords)
        self.rect.tex_coords = self.tex_coords
        if (__map_plot_debug__) :
            print("InteractiveWorldMapWidget.zoom_in:",self.rect.size,self.rect.pos,self.width)

    def resize(self,widget,newsize) :
        self.tex_coords = [0, 1, 1, 1, 1, 0, 0, 0]
        self.rect.tex_coords = self.tex_coords
        self.rect.size = self.check_size((self.nx*self.height/self.ny,self.height))
        self.rect.pos = (max(0,0.5*(self.width-self.rect.size[0])),(self.height-self.rect.size[1]))
        if (__map_plot_debug__) :
            print("InteractiveWorldMapWidget.resize(): replotting",self.rect.size,self.rect.pos)

    def set_zoom_factor(self,value) :
        self.rect.size = self.check_size((self.nx*value,self.ny*value))
        x_shift = -0.5*(self.width-self.rect.size[0])/float(self.rect.size[0])
        y_shift = 0.5*(self.height-self.rect.size[1])/float(self.rect.size[1])
        self.tex_coords = [0, 1, 1, 1, 1, 0, 0, 0]        
        for i in range(0,8,2) :
            self.tex_coords[i] = self.tex_coords[i] + x_shift
            self.tex_coords[i+1] = self.tex_coords[i+1] + y_shift
        self.tex_coords = self.check_boundaries(self.tex_coords)
        self.rect.tex_coords = self.tex_coords
        self.rect.pos = (max(0,0.5*(self.width-self.rect.size[0])),(self.height-self.rect.size[1]))

    def check_boundaries(self,tex_coords) :
        new_tex_coords = copy.copy(tex_coords)
        max_y_shift = max((self.rect.size[1]-self.height)/self.rect.size[1],0)
        new_tex_coords[1] = max(min(tex_coords[1],1+max_y_shift),1)
        new_tex_coords[3] = max(min(tex_coords[3],1+max_y_shift),1)
        new_tex_coords[5] = max(min(tex_coords[5],max_y_shift),0)
        new_tex_coords[7] = max(min(tex_coords[7],max_y_shift),0)
        return new_tex_coords

    def check_size(self,size) :
        return size
        


class InteractiveBaselineMapPlot_kivygraph(InteractiveWorldMapWidget):

    statdict = {}
    gcdict = {}
    lldict = {}
    
    def __init__(self,**kwargs) :

        self.statdict = {}

        super().__init__(**kwargs)
            
        self.off_color = (0.5,0,0)
        self.on_color = (1,0.75,0.25)
        
        self.gcdict = {}
        self.lldict = {}

        

        
    # def generate_mpl_plot(self,fig,ax,**kwargs) :
    #     # This is where we insert a Matplotlib figure.  Must use ax. and fig. child commands.
    #     # You probably want, but do not require, the following in your over-lay
    #     self.plot_map(ax,self.statdict)
    #     ax.set_facecolor((0,0,0,0))
    #     fig.set_facecolor((0,0,0,0))

    
    def update(self,datadict,statdict,**kwargs) :

        self.statdict = statdict
        if (__map_plot_debug__):
            print("InteractiveBaselineMapPlot.update:",self.statdict.keys())

        if (list(self.lldict.keys()) != list(self.statdict.keys())) :
            if (__map_plot_debug__):
                print("InteractiveBaselineMapPlot.update: remaking circles")
            lims=[-180,180,-90,90]
            self.generate_all_station_latlon(statdict)
            if ('SP' in self.statdict.keys()) :
                self.lldict['SP']=[-85.0, 0.5*(lims[0]+lims[1])]
            self.generate_all_great_circles(self.lldict, lims)

        # self.bmc.plot_stations(self.statdict,self.lldict,self.gcdict,self.rect.size)
        # self.update_mpl(**kwargs)

    def replot(self,datadict,statdict,**kwargs) :

        if (__map_plot_debug__):
            print("InteractiveBaselineMapPlot.replot:",self.statdict.keys())

        self.update(datadict,statdict,**kwargs)


                    
    # limits is a list that has in degrees the min longitude, max longitude, min latitude, max latitude to be plotted.
    def plot_map(self,axs,statdict) :
        if (__map_plot_debug__):
            print("InteractiveBaselineMapPlot.plot_map:",statdict.keys())
        lims=[-180,180,-90,90]
        for i in self.gcdict.keys() :
            if (self.statdict[self.gcdict[i]['s1']]['on']==False or self.statdict[self.gcdict[i]['s2']]['on']==False) :
                axs.plot(self.gcdict[i]['x'],self.gcdict[i]['y'],'-',color=self.off_color,alpha=0.5)
                axs.plot(self.gcdict[i]['x']-360,self.gcdict[i]['y'],'-',color=self.off_color,alpha=0.5)
        for i in self.gcdict.keys() :
            if (self.statdict[self.gcdict[i]['s1']]['on']==True and self.statdict[self.gcdict[i]['s2']]['on']==True) :
                axs.plot(self.gcdict[i]['x'],self.gcdict[i]['y'],'-',color=self.on_color,alpha=0.5)
                axs.plot(self.gcdict[i]['x']-360,self.gcdict[i]['y'],'-',color=self.on_color,alpha=0.5)
        for s in self.statdict.keys() :
            if (self.statdict[s]['on']==False) :
                axs.plot(self.lldict[s][1], self.lldict[s][0], 'o', color = self.off_color)
        for s in self.statdict.keys() :
            if (self.statdict[s]['on']==True) :
                axs.plot(self.lldict[s][1], self.lldict[s][0], 'o', color = self.on_color)
        # Set limits
        axs.set_xlim((lims[:2]))
        axs.set_ylim((lims[2:]))
        # Eliminate axes
        for sdir in ['left','right','top','bottom'] :
            axs.spines[sdir].set_visible(False)
        axs.xaxis.set_tick_params(bottom='off',top='off')
        axs.yaxis.set_tick_params(left='off',right='off')
        
    def generate_all_station_latlon(self, statdict) :
        self.lldict = {}
        for s in statdict.keys():
            self.lldict[s] = self.xyz_to_latlon(statdict[s]['loc'])
        return statdict

    def generate_all_great_circles(self,lldict,limits,N=128) :
        self.gcdict = {}
        i = 0
        for k,s1 in enumerate(list(lldict.keys())) :
            for s2 in list(lldict.keys())[(k+1):] :
                ll1 = lldict[s1]
                ll2 = lldict[s2]
                llgA = self.great_circle(ll1,ll2,N=N)
                lonc = 0.5*(limits[0]+limits[1])
                y = llgA[0]
                x = llgA[1] - (llgA[1][0]-lonc) + (llgA[1][0]-lonc)%360 
                x,y = self.resample_by_length(x,y,N=32)
                self.gcdict[i] = {'s1':s1,'s2':s2,'x':x,'y':y}
                i += 1

    def resample_by_length(self,x0,y0,N=None) :
        ds = np.sqrt( (x0[1:]-x0[:-1])**2 + (y0[1:]-y0[:-1])**2 )
        s = np.cumsum(ds)
        s = np.append([0],s/s[-1])
        if (N is None) :
            N = len(x0)
        t = np.linspace(0,1,N)
        x = np.interp(t,s,x0)
        y = np.interp(t,s,y0)
        
        return x,y

                
    def great_circle(self,pos1,pos2,N=32) :

        lat1, lon1 = pos1
        lat2, lon2 = pos2

        # First, rotate about z so that latlon1 is in the x-z plane
        ll1 = [lat1, 0]
        ll2 = [lat2, lon2-lon1]
    
        # Second, rotate about y so that ll1 is at the north pole
        ll1 = self.xyz_to_latlon(self.RotateY(self.latlon_to_xyz(ll1),angle=-(90-lat1)))
        ll2 = self.xyz_to_latlon(self.RotateY(self.latlon_to_xyz(ll2),angle=-(90-lat1)))
    
        # Third, generate a great circle that goes through the pole (easy) and ll2 (not hard)
        latA = np.linspace(ll2[0],90.0,N)
        lonA = 0*latA + ll2[1]
        llgA = np.array([latA,lonA])

        # Fourth, unrotate about y
        llgA = self.xyz_to_latlon(self.RotateY(self.latlon_to_xyz(llgA),angle=(90-lat1)))
        llgA[1] = llgA[1] + lon1

        return llgA

    def latlon_to_xyz(self,latlon,radius=1) :

        lat_rad = latlon[0]*np.pi/180.
        lon_rad = latlon[1]*np.pi/180.

        x = radius*np.cos(lat_rad)*np.cos(lon_rad)
        y = radius*np.cos(lat_rad)*np.sin(lon_rad)
        z = radius*np.sin(lat_rad)

        return np.array([x,y,z])

    def xyz_to_latlon(self,xyz) :
        lat = np.arcsin( xyz[2]/np.sqrt(xyz[0]**2+xyz[1]**2+xyz[2]**2) ) * 180./np.pi
        lon = np.arctan2( xyz[1], xyz[0] ) * 180.0/np.pi
        return np.array([lat,lon])

    def RotateY(self,xyz,angle=0) :

        angle = angle*np.pi/180.0
        xyz2 = 0*xyz
        xyz2[0] = xyz[0]*np.cos(angle) + xyz[2]*np.sin(angle)
        xyz2[1] = xyz[1]
        xyz2[2] = xyz[2]*np.cos(angle) - xyz[0]*np.sin(angle)

        return xyz2

    def check_size(self,size) :
        if (size[0]==0 or size[1]==0) :
            return size

        # if (size[0]<self.width and size[1]<self.height) :
        #     if (self.width/size[0] < self.height/size[1]) :
        #         size = (self.width, size[1]/size[0] * self.width)
        #     else :
        #         size = (size[0]/size[1] * self.height, self.height)

        if (size[0]<Window.width and size[1]<Window.height) :
            if (Window.width/size[0] < Window.height/size[1]) :
                size = (Window.width, size[1]/size[0] * Window.width)
            else :
                size = (size[0]/size[1] * Window.height, Window.height)
                
        if (__map_plot_debug__) :
            print("InteractiveBaselineMapPlot_kivygraph.check_size",self.width,self.height,size,Window.width,Window.height)
        return size



    
class BaselineMapCanvas(FloatLayout) :

    def __init__(self,**kwargs) :
        super().__init__(**kwargs)
        self.off_color = (0.5,0,0)
        self.on_color = (1,0.75,0.25)

        self.plot_cursor = False
        self.limits = [-180,180,-90,90]

        
    def plot_stations(self,statdict,lldict,gcdict,rect) :
        if (__map_plot_debug__):
            print("BaselineMapCanvas.plot_stations:",statdict.keys())

        if (rect.size[0]==0  or rect.size[1]==0) :
            return
            

        lon_to_xpx_scale = rect.size[0]/(self.limits[1]-self.limits[0]) 
        lon_to_xpx_offset = lon_to_xpx_scale*(-self.limits[0]) + rect.pos[0] - rect.tex_coords[0]*rect.size[0]/(rect.tex_coords[2]-rect.tex_coords[0])
        lat_to_ypx_scale = rect.size[1]/(self.limits[3]-self.limits[2])
        lat_to_ypx_offset = lat_to_ypx_scale*(-self.limits[2]) + rect.pos[1] - rect.tex_coords[5]*rect.size[1]/(rect.tex_coords[5]-rect.tex_coords[1])

        
        # Index manipulation stuff
        j = np.arange(len(gcdict[0]['x']))
        j2 = 2*j
        j2p1 = 2*j+1
        points = np.arange(2*len(j))
        
        linewidth = 2


        reticle_circ = dp(30)
        reticle_out = dp(50)
        reticle_in = dp(10)
        reticle_linewidth = dp(1)                    

        
        # Get the current limits.
        self.canvas.clear()        
        with self.canvas :

            igc = 0
            Color(self.off_color[0],self.off_color[1],self.off_color[2],0.5)
            for k,s1 in enumerate(list(statdict.keys())) :
                for s2 in list(statdict.keys())[(k+1):] :
                    if (statdict[s1]['on']==False or statdict[s2]['on']==False) :
                        total_x_shift = ( (lon_to_xpx_scale*gcdict[igc]['x'][0] + lon_to_xpx_offset)//rect.size[0]  )*rect.size[0] - 0.5*linewidth
                        
                        points[j2] = lon_to_xpx_scale*gcdict[igc]['x'] + lon_to_xpx_offset - total_x_shift
                        points[j2p1] = lat_to_ypx_scale*gcdict[igc]['y'] + lat_to_ypx_offset
                        Line(points=list(points),width=linewidth)
                        if (points[0]<0 or points[-2]<0) :
                            points[j2] = points[j2]+lon_to_xpx_scale*360 
                            Line(points=list(points),width=linewidth)
                            points[j2] = points[j2]-lon_to_xpx_scale*360
                        if (points[0]>self.width or points[-2]>self.width) :
                            points[j2] = points[j2]-lon_to_xpx_scale*360
                            Line(points=list(points),width=linewidth)
                    igc += 1

            igc = 0
            Color(self.on_color[0],self.on_color[1],self.on_color[2],0.5)
            for k,s1 in enumerate(list(statdict.keys())) :
                for s2 in list(statdict.keys())[(k+1):] :
                    if (statdict[s1]['on']==True and statdict[s2]['on']==True) :
                        total_x_shift = ( (lon_to_xpx_scale*gcdict[igc]['x'][0] + lon_to_xpx_offset)//rect.size[0]  )*rect.size[0] - 0.5*linewidth
                        
                        points[j2] = lon_to_xpx_scale*gcdict[igc]['x'] + lon_to_xpx_offset - total_x_shift
                        points[j2p1] = lat_to_ypx_scale*gcdict[igc]['y'] + lat_to_ypx_offset
                        Line(points=list(points),width=linewidth)
                        if (points[0]<0 or points[-2]<0) :
                            points[j2] = points[j2]+lon_to_xpx_scale*360 
                            Line(points=list(points),width=linewidth)
                            points[j2] = points[j2]-lon_to_xpx_scale*360
                        if (points[0]>self.width or points[-2]>self.width) :
                            points[j2] = points[j2]-lon_to_xpx_scale*360
                            Line(points=list(points),width=linewidth)
                    igc += 1


            for s in statdict.keys() :
                if (statdict[s]['on']==False) :
                    xpx = (lon_to_xpx_scale*lldict[s][1] + lon_to_xpx_offset)%(rect.size[0])
                    ypx = lat_to_ypx_scale*lldict[s][0] + lat_to_ypx_offset
                    Color(0,0,0,0.1)
                    Ellipse(pos=(xpx-dp(7),ypx-dp(7)),size=(dp(14),dp(14)))
                    Ellipse(pos=(xpx-dp(6),ypx-dp(6)),size=(dp(12),dp(12)))
                    Color(self.off_color[0],self.off_color[1],self.off_color[2])
                    Ellipse(pos=(xpx-dp(5),ypx-dp(5)),size=(dp(10),dp(10)))
                    # if (__map_plot_debug__) :
                    #     print("Adding OFF circle for",s,xpx,ypx,self.on_color,self.height,rect.size,rect.pos)
                    
            for s in statdict.keys() :
                if (statdict[s]['on']==True) :
                    xpx = (lon_to_xpx_scale*lldict[s][1] + lon_to_xpx_offset)%(rect.size[0])
                    ypx = lat_to_ypx_scale*lldict[s][0] + lat_to_ypx_offset
                    Color(0,0,0,0.1)
                    Ellipse(pos=(xpx-dp(7),ypx-dp(7)),size=(dp(14),dp(14)))
                    Ellipse(pos=(xpx-dp(6),ypx-dp(6)),size=(dp(12),dp(12)))
                    Color(self.on_color[0],self.on_color[1],self.on_color[2])
                    Ellipse(pos=(xpx-dp(5),ypx-dp(5)),size=(dp(10),dp(10)))
                    # if (__map_plot_debug__) :
                    #     print("Adding ON circle for",s,xpx,ypx,self.on_color,self.height,rect.size,rect.pos)


            if (self.plot_cursor) :
                # Plot the target (circle + cross hairs?)
                Color(self.on_color[0],self.on_color[1],self.on_color[2])
                xpx = (lon_to_xpx_scale*(self.cursor_lon) + lon_to_xpx_offset)%(rect.size[0])
                ypx = lat_to_ypx_scale*self.cursor_lat + lat_to_ypx_offset
                Line(circle=(xpx,ypx,reticle_circ),width=reticle_linewidth)
                Line(points=[(xpx-reticle_out,ypx),(xpx-reticle_in,ypx)],width=reticle_linewidth)
                Line(points=[(xpx+reticle_out,ypx),(xpx+reticle_in,ypx)],width=reticle_linewidth)
                Line(points=[(xpx,ypx-reticle_out),(xpx,ypx-reticle_in)],width=reticle_linewidth)
                Line(points=[(xpx,ypx+reticle_out),(xpx,ypx+reticle_in)],width=reticle_linewidth)
                

    def px_to_coords(self,xpx,ypx,rect) :
        lon_to_xpx_scale = rect.size[0]/(self.limits[1]-self.limits[0]) 
        lon_to_xpx_offset = lon_to_xpx_scale*(-self.limits[0]) + rect.pos[0] - rect.tex_coords[0]*rect.size[0]/(rect.tex_coords[2]-rect.tex_coords[0])
        lat_to_ypx_scale = rect.size[1]/(self.limits[3]-self.limits[2])
        lat_to_ypx_offset = lat_to_ypx_scale*(-self.limits[2]) + rect.pos[1] - rect.tex_coords[5]*rect.size[1]/(rect.tex_coords[5]-rect.tex_coords[1])
        lon = ((xpx) - lon_to_xpx_offset)/lon_to_xpx_scale
        lat = ((ypx) - lat_to_ypx_offset)/lat_to_ypx_scale
        lon = (lon+180)%360 + 180

        return (lat,lon)
            
    def get_center(self,rect) :
        return self.px_to_coords(0.5*Window.width,0.5*Window.height,rect)

    def coords_to_px(self,lat,lon,rect) :
        lon_to_xpx_scale = rect.size[0]/(self.limits[1]-self.limits[0]) 
        lon_to_xpx_offset = lon_to_xpx_scale*(-self.limits[0]) + rect.pos[0] - rect.tex_coords[0]*rect.size[0]/(rect.tex_coords[2]-rect.tex_coords[0])
        lat_to_ypx_scale = rect.size[1]/(self.limits[3]-self.limits[2])
        lat_to_ypx_offset = lat_to_ypx_scale*(-self.limits[2]) + rect.pos[1] - rect.tex_coords[5]*rect.size[1]/(rect.tex_coords[5]-rect.tex_coords[1])
        xpx = (lon_to_xpx_scale*lon + lon_to_xpx_offset)%(rect.size[0])
        ypx = lat_to_ypx_scale*lat + lat_to_ypx_offset

        return (xpx,ypx)
                
    def cursor_on(self,rect) :
        (self.cursor_lat,self.cursor_lon) = self.get_center(rect)
        self.plot_cursor = True

    def cursor_off(self,rect) :
        self.plot_cursor = False
        return self.cursor_lat,self.cursor_lon
    
