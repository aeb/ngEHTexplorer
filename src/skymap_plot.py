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
from kivy.uix.spinner import Spinner, SpinnerOption

from kivymd.theming import ThemableBehavior

from os import path
import copy

# Station dictionary: statdict has form {<station code>:{'on':<True/False>,'name':<name>,'loc':(x,y,z)}}

__skymap_debug__ = False


class InteractiveSkyMapWidget(ThemableBehavior,Widget):

    tex_coords = ListProperty([0, 1, 1, 1, 1, 0, 0, 0])
    texture_wrap = StringProperty('repeat')
    
    def __init__(self, **kwargs):
        self.canvas = RenderContext()

        self.nx = 1024
        self.ny = self.nx//2

        if (__skymap_debug__) :
            print("On init:",self.nx,self.ny)
        
        with self.canvas:
            # Background texture
            self.texture = Image(path.abspath(path.join(path.dirname(__file__),'images/starmap_2020_4k.jpg'))).texture
            self.texture.wrap = self.texture_wrap
            self.rect = Rectangle(size=(self.nx,self.ny),texture=self.texture)
            self.rect.tex_coords = self.tex_coords

        if (__skymap_debug__) :
            print("InteractiveSkyMapWidget._init__ rect.size:",self.rect.size)
            
        # Don't restrict zooming at start
        self.plot_frozen = False
        
        # call the constructor of parent
        # if they are any graphics objects, they will be added on our new
        # canvas
        super(InteractiveSkyMapWidget, self).__init__(**kwargs)

        # We'll update our glsl variables in a clock
        # Clock.schedule_interval(self.update_glsl, 0)        
        Clock.schedule_interval(self.texture_init, 0)

        # Generate some default resizing behaviors
        self.bind(height=self.resize)
        self.bind(width=self.resize)

        self.theme_cls.bind(theme_style=self.set_theme)


        
    def choose_map(self,map_type='Dark') :
        if (map_type=='Dark') :
            self.texture = Image(path.abspath(path.join(path.dirname(__file__),'images/starmap_2020_4k.jpg'))).texture
        elif (map_type=='Light') :
            self.texture = Image(path.abspath(path.join(path.dirname(__file__),'images/starmap_2020_4k_negative.jpg'))).texture
        else :
            print("ERROR: Unrecognized option %s."%(map_type))
        self.texture.wrap = self.texture_wrap
        self.rect.texture = self.texture
        self.rect.tex_coords = self.tex_coords

        
    def set_theme(self,widget,value) :
        self.choose_map(map_type=value)

        
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

            if (__skymap_debug__) :
                print("InteractiveSkyMapWidget.on_touch_move:")
                print("   tex_coords before :",self.tex_coords)
                print("   size/pos/width/height :",self.rect.size,self.rect.pos,self.width,self.height)
                
            self.tex_coords = self.check_boundaries(self.tex_coords)
            
            if (__skymap_debug__) :
                print("InteractiveSkyMapWidget.on_touch_move:")
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
        if (__skymap_debug__) :
            print("InteractiveSkyMapWidget.zoom_in A",self.rect.size,self.rect.pos,self.width,self.rect.tex_coords)
        self.rect.size = self.check_size((self.rect.size[0]*1.414,self.rect.size[1]*1.414))
        self.rect.pos = (max(0,0.5*(self.width-self.rect.size[0])),(self.height-self.rect.size[1]))
        x_shift = self.width/self.rect.size[0]*(1.414-1.0)
        y_shift = 0.5*self.height/self.rect.size[1]*(1.414-1.0)
        for i in range(0,8,2) :
            self.tex_coords[i] = self.tex_coords[i] + x_shift
            self.tex_coords[i+1] = self.tex_coords[i+1] + y_shift
        self.tex_coords = self.check_boundaries(self.tex_coords)
        self.rect.tex_coords = self.tex_coords
        if (__skymap_debug__) :
            print("InteractiveSkyMapWidget.zoom_in B",self.rect.size,self.rect.pos,self.width,self.rect.tex_coords)
            
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
        if (__skymap_debug__) :
            print("InteractiveSkyMapWidget.zoom_in:",self.rect.size,self.rect.pos,self.width)

    def resize(self,widget,newsize) :
        self.tex_coords = [0, 1, 1, 1, 1, 0, 0, 0]
        self.rect.tex_coords = self.tex_coords
        self.rect.size = self.check_size((self.nx*self.height/self.ny,self.height))
        self.rect.pos = (max(0,0.5*(self.width-self.rect.size[0])),(self.height-self.rect.size[1]))
        if (__skymap_debug__) :
            print("InteractiveSkyMapWidget.resize(): replotting",self.rect.size,self.rect.pos)

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
        max_y_shift = max((self.rect.size[1]-self.height)/max(1,self.rect.size[1]),0)
        new_tex_coords[1] = max(min(tex_coords[1],1+max_y_shift),1)
        new_tex_coords[3] = max(min(tex_coords[3],1+max_y_shift),1)
        new_tex_coords[5] = max(min(tex_coords[5],max_y_shift),0)
        new_tex_coords[7] = max(min(tex_coords[7],max_y_shift),0)
        return new_tex_coords

    def check_size(self,size) :
        return size
        

class TargetSelectionSpinnerOptions(SpinnerOption) :
    def __init__(self,**kwargs) :
        super().__init__(**kwargs)

        self.background_color=(1,1,1,0.25)
        self.height = dp(50)
        
    
class TargetSelectionSpinner(Spinner) :

    def __init__(self,targets,**kwargs) :
        super().__init__(**kwargs)

        self.targets = targets

        self.option_cls = TargetSelectionSpinnerOptions
        
        # Set values
        self.values = []
        for ds in self.targets.keys() :
            self.values.append(ds)

        # Choose key
        self.text = list(self.targets.keys())[0]
        
        # Set default RA/DEC
        # self.bind(text=self.select_target)
        
        
    
class StarMapCanvas(FloatLayout) :

    def __init__(self,**kwargs) :
        super().__init__(**kwargs)
        self.off_color = (0.5,0,0)
        self.on_color = (1,0.75,0.25)

        self.limits = [12,-12,-90,90]
        
    def plot_targets(self,tdict,rect,RA,Dec) :
        # if (__skymap_debug__):
        #     print("StarMapCanvas.plot_stations:",tdict.keys())

        if (rect.size[0]==0  or rect.size[1]==0) :
            return
            
        ra_to_xpx_scale = rect.size[0]/(self.limits[1]-self.limits[0]) 
        ra_to_xpx_offset = ra_to_xpx_scale*(-self.limits[0]) + rect.pos[0] - rect.tex_coords[0]*rect.size[0]/(rect.tex_coords[2]-rect.tex_coords[0])
        dec_to_ypx_scale = rect.size[1]/(self.limits[3]-self.limits[2])
        dec_to_ypx_offset = dec_to_ypx_scale*(-self.limits[2]) + rect.pos[1] - rect.tex_coords[5]*rect.size[1]/(rect.tex_coords[5]-rect.tex_coords[1])

        
        reticle_circ = dp(30)
        reticle_out = dp(50)
        reticle_in = dp(10)
        linewidth = dp(1)

        # Get the current limits.
        self.canvas.clear()        
        with self.canvas :

            # Plot the points of known positions
            for t in tdict.keys() :
                if (t!="--- Select ---") :
                    xpx = (ra_to_xpx_scale*tdict[t]['RA'] + ra_to_xpx_offset)%(rect.size[0])
                    ypx = dec_to_ypx_scale*tdict[t]['Dec'] + dec_to_ypx_offset
                    if (ypx<self.height) :
                        # Color(1,1,1,0.1)
                        Color(1,1,1,0.25)
                        #Ellipse(pos=(xpx-dp(9),ypx-dp(9)),size=(dp(18),dp(18)))
                        #Ellipse(pos=(xpx-dp(7),ypx-dp(7)),size=(dp(14),dp(14)))
                        Ellipse(pos=(xpx-dp(6),ypx-dp(6)),size=(dp(12),dp(12)))
                        Color(self.off_color[0],self.off_color[1],self.off_color[2])
                        Ellipse(pos=(xpx-dp(5),ypx-dp(5)),size=(dp(10),dp(10)))

                
            # Plot the target (circle + cross hairs?)
            Color(self.on_color[0],self.on_color[1],self.on_color[2])
            xpx = (ra_to_xpx_scale*(RA) + ra_to_xpx_offset)%(rect.size[0])
            ypx = dec_to_ypx_scale*Dec + dec_to_ypx_offset
            Line(circle=(xpx,ypx,reticle_circ),width=linewidth)
            Line(points=[(xpx-reticle_out,ypx),(xpx-reticle_in,ypx)],width=linewidth)
            Line(points=[(xpx+reticle_out,ypx),(xpx+reticle_in,ypx)],width=linewidth)
            Line(points=[(xpx,ypx-reticle_out),(xpx,ypx-reticle_in)],width=linewidth)
            Line(points=[(xpx,ypx+reticle_out),(xpx,ypx+reticle_in)],width=linewidth)


    def px_to_coords(self,xpx,ypx,rect) :
        ra_to_xpx_scale = rect.size[0]/(self.limits[1]-self.limits[0]) 
        ra_to_xpx_offset = ra_to_xpx_scale*(-self.limits[0]) + rect.pos[0] - rect.tex_coords[0]*rect.size[0]/(rect.tex_coords[2]-rect.tex_coords[0])
        dec_to_ypx_scale = rect.size[1]/(self.limits[3]-self.limits[2])
        dec_to_ypx_offset = dec_to_ypx_scale*(-self.limits[2]) + rect.pos[1] - rect.tex_coords[5]*rect.size[1]/(rect.tex_coords[5]-rect.tex_coords[1])
        RA = ((xpx) - ra_to_xpx_offset)/ra_to_xpx_scale
        Dec = ((ypx) - dec_to_ypx_offset)/dec_to_ypx_scale
        RA = (RA+12)%24 + 12

        # if (__skymap_debug__) :
        #     print("px_to_coords test 1:",xpx,ypx)
        #     xpx2,ypx2 = self.coords_to_px(RA,Dec,rect)
        #     print("px_to_coords test 2:",xpx2,ypx2)

        return (RA,Dec)
            
    def get_center(self,rect) :
        return self.px_to_coords(0.5*Window.width,0.5*Window.height,rect)

    def coords_to_px(self,RA,Dec,rect) :
        ra_to_xpx_scale = rect.size[0]/(self.limits[1]-self.limits[0]) 
        ra_to_xpx_offset = ra_to_xpx_scale*(-self.limits[0]) + rect.pos[0] - rect.tex_coords[0]*rect.size[0]/(rect.tex_coords[2]-rect.tex_coords[0])
        dec_to_ypx_scale = rect.size[1]/(self.limits[3]-self.limits[2])
        dec_to_ypx_offset = dec_to_ypx_scale*(-self.limits[2]) + rect.pos[1] - rect.tex_coords[5]*rect.size[1]/(rect.tex_coords[5]-rect.tex_coords[1])
        xpx = (ra_to_xpx_scale*RA + ra_to_xpx_offset)%(rect.size[0])
        ypx = dec_to_ypx_scale*Dec + dec_to_ypx_offset

        # if (__skymap_debug__) :
        #     print("coords_to_px test:",RA,Dec)
        #     RA2,Dec2 = px_to_coords(xpx,ypx,rect)
        #     print("coords_to_px test:",RA2,Dec2)
        
        return (xpx,ypx)
    


class InteractiveSkyMapPlot(InteractiveSkyMapWidget):

    
    def __init__(self,**kwargs) :

        super().__init__(**kwargs)
            
        self.off_color = (0.5,0,0)
        self.on_color = (1,0.75,0.25)
        
    def update(self,datadict,statdict,**kwargs) :
        if (__skymap_debug__):
            print("InteractiveSkyMapPlot.update:",self.statdict.keys())

    def replot(self,**kwargs) :
        if (__skymap_debug__):
            print("InteractiveBaselineMapPlot.replot:",self.statdict.keys())
        self.update(**kwargs)

    def check_size(self,size) :
        if (size[0]==0 or size[1]==0) :
            return size

        if (size[0]<Window.width and size[1]<Window.height) :
            if (Window.width/size[0] < Window.height/size[1]) :
                size = (Window.width, size[1]/size[0] * Window.width)
            else :
                size = (size[0]/size[1] * Window.height, Window.height)
                
        if (__skymap_debug__) :
            print("InteractiveSkyMapPlot_kivygraph.check_size",self.width,self.height,size,Window.width,Window.height)
        return size

    def set_coord_center(self,RA,Dec) :
        x_shift = (RA+12)/(-24.) - self.tex_coords[0] - 0.5*Window.width/max(1,self.rect.size[0])
        y_shift = (Dec-90)/(-180.) - self.tex_coords[5] - 0.5*Window.height/max(1,self.rect.size[1])
        # if (__skymap_debug__) :
        #     print("InteractiveSkyMapPlot_kivygraph.set_coord_center",(RA+12)/(-24.0),(Dec-90)/(-180.),x_shift,y_shift,RA,Dec)
        #     print("        ",self.tex_coords)
        for i in range(0,8,2) :
            self.tex_coords[i] = self.tex_coords[i] + x_shift
            self.tex_coords[i+1] = self.tex_coords[i+1] + y_shift
        self.tex_coords = self.check_boundaries(self.tex_coords)
        self.rect.tex_coords = self.tex_coords

    def get_coord_center(self) :

        RA = -24.0*( 0.5*Window.width/max(1,self.rect.size[0]) + self.tex_coords[0] ) - 12
        Dec = -180.0*( 0.5*Window.height/max(1,self.rect.size[1]) + self.tex_coords[5] ) + 90

        return RA,Dec
