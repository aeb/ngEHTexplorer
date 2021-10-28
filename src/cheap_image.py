__cheap_image_perf__ = False

if (__cheap_image_perf__) :
    import time
    print("--- %15.8g --- cheap_image.py start"%(time.perf_counter()))

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mi
import matplotlib.tri as tri
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

if (__cheap_image_perf__) :
    print("--- %15.8g --- imported matplotlib"%(time.perf_counter()))

from kivy.clock import Clock
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.graphics import RenderContext, Color, Rectangle, BindTexture
from kivy.graphics.texture import Texture
from kivy.properties import ListProperty, NumericProperty

if (__cheap_image_perf__) :
    print("--- %15.8g --- imported kivy"%(time.perf_counter()))

from array import array

if (__cheap_image_perf__) :
    print("--- %15.8g --- imported array"%(time.perf_counter()))


# import threading
# import time

# Data dictionary: datadict has form {'u':u,'v':v,'V':V,'s1':s1d,'s2':s2d,'t':t,'err':err}
# Station dictionary: statdict has form {<station code>:{'on':<True/False>,'name':<name>,'loc':(x,y,z)}}


__cheap_image_debug__ = False


class InteractivePlotWidget(Widget):

    tex_coords = ListProperty([0, 1, 1, 1, 1, 0, 0, 0])
    
    default_zoom_factor = NumericProperty(1.0)
    
    def __init__(self, **kwargs):
        if (__cheap_image_perf__) :
            print("--- %15.8g --- InteractivePlotWidget.__init__ start"%(time.perf_counter()))
        
        self.canvas = RenderContext()

        self.nx = 1024
        self.ny = self.nx

        # print("On init:",self.nx,self.ny)
        
        with self.canvas:
            Color(1, 1, 1)
            self.texture = Texture.create(size=(self.nx,self.ny))
            # self.buf = [0,0,0,255]*(self.nx*self.ny)
            # self.arr = array('B',self.buf)
            self.arr = bytearray([0,0,0,255]*(self.nx*self.ny))
            # self.update_mpl()
            self.texture.blit_buffer(self.arr, colorfmt='rgba', bufferfmt='ubyte')
            BindTexture(texture=self.texture, index=0)
            self.texture.wrap = 'clamp_to_edge'
            
            # create a rectangle on which to plot texture (will be at index 0)
            Color(1,1,1)
            self.rect = Rectangle(size=(self.default_zoom_factor*self.nx,self.default_zoom_factor*self.ny),texture=self.texture)
            self.rect.tex_coords = self.tex_coords

        if (__cheap_image_perf__) :
            print("--- %15.8g --- InteractivePlotWidget.__init__ made canvas"%(time.perf_counter()))
            
        self.plot_frozen = False
        
        # call the constructor of parent
        # if they are any graphics objects, they will be added on our new
        # canvas
        super(InteractivePlotWidget, self).__init__(**kwargs)

        # We'll update our glsl variables in a clock
        # Clock.schedule_interval(self.update_glsl, 0)        
        Clock.schedule_interval(self.texture_init, 0)

        # Generate some default resizing behaviors
        self.bind(height=self.resize)
        self.bind(width=self.resize)
        
        if (__cheap_image_perf__) :
            print("--- %15.8g --- InteractivePlotWidget.__init__ done"%(time.perf_counter()))
            

        
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
            self.tex_coords = self.check_boundaries(self.tex_coords)
            self.rect.tex_coords = self.tex_coords

    def on_touch_down(self,touch) :
        if (touch.is_double_tap) :
            self.tex_coords = [0, 1, 1, 1, 1, 0, 0, 0]
            self.rect.tex_coords = self.tex_coords
            maxwidth = self.default_zoom_factor*max(self.width,self.height*self.nx/self.ny)
            self.rect.size = self.check_size((maxwidth,self.ny*maxwidth/self.nx))
            self.rect.pos = (0.5*(self.width-self.rect.size[0]),(self.height-self.rect.size[1]))
            x_shift = 0.0
            y_shift = -0.5*(self.height-self.rect.size[1])/self.rect.size[1]
            for i in range(0,8,2) :
                self.tex_coords[i] = self.tex_coords[i] + x_shift
                self.tex_coords[i+1] = self.tex_coords[i+1] + y_shift
            self.tex_coords = self.check_boundaries(self.tex_coords)
            self.rect.tex_coords = self.tex_coords
            
    def zoom_in(self) :
        if (__cheap_image_debug__) :
            print("InteractivePlotWidget.zoom_in:",self.rect.tex_coords,self.height)
        old_size = self.rect.size
        self.rect.size = self.check_size((self.rect.size[0]*1.414,self.rect.size[1]*1.414))
        self.rect.pos = (0.5*(self.width-self.rect.size[0]),(self.height-self.rect.size[1]))
        y_shift = 0.5 * (self.rect.size[0]/old_size[0]-1.0) * self.height/self.rect.size[1]
        x_shift = 0
        if (__cheap_image_debug__) :
            print("InteractivePlotWidget.zoom_in:",old_size,self.rect.size,y_shift)
        for i in range(0,8,2) :
            self.tex_coords[i] = self.tex_coords[i] + x_shift
            self.tex_coords[i+1] = self.tex_coords[i+1] + y_shift
        self.tex_coords = self.check_boundaries(self.tex_coords)
        self.rect.tex_coords = self.tex_coords
        if (__cheap_image_debug__) :
            print("                             :",self.rect.tex_coords,self.height)

    def zoom_out(self) :
        old_size = self.rect.size
        self.rect.size = self.check_size((self.rect.size[0]*0.707,self.rect.size[1]*0.707))
        self.rect.pos = (0.5*(self.width-self.rect.size[0]),(self.height-self.rect.size[1]))
        y_shift = 0.5 * (self.rect.size[0]/old_size[0]-1.0) * self.height/self.rect.size[1]
        x_shift = 0
        if (__cheap_image_debug__) :
            print("InteractivePlotWidget.zoom_out:",old_size,self.rect.size,y_shift)
        for i in range(0,8,2) :
            self.tex_coords[i] = self.tex_coords[i] + x_shift
            self.tex_coords[i+1] = self.tex_coords[i+1] + y_shift
        self.tex_coords = self.check_boundaries(self.tex_coords)
        self.rect.tex_coords = self.tex_coords

    def resize(self,widget,newsize) :
        if (__cheap_image_debug__) :
            print("InteractivePlotWidget.resize:",newsize)
        self.tex_coords = [0, 1, 1, 1, 1, 0, 0, 0]
        self.rect.tex_coords = self.tex_coords
        maxwidth = self.default_zoom_factor*max(self.width,self.height*self.nx/self.ny)
        self.rect.size = self.check_size((maxwidth,self.ny*maxwidth/self.nx))
        self.rect.pos = (0.5*(self.width-self.rect.size[0]),(self.height-self.rect.size[1]))
        x_shift = 0.0
        y_shift = -0.5*(self.height-self.rect.size[1])/self.rect.size[1]
        for i in range(0,8,2) :
            self.tex_coords[i] = self.tex_coords[i] + x_shift
            self.tex_coords[i+1] = self.tex_coords[i+1] + y_shift
        self.tex_coords = self.check_boundaries(self.tex_coords)
        self.rect.tex_coords = self.tex_coords
        
    # def set_zoom_factor(self,value) :
    #     self.rect.size = self.check_size([self.nx*value,self.ny*value])
    #     x_shift = -0.5*(self.width-self.rect.size[0])/float(self.rect.size[0])
    #     y_shift = 0.5*(self.height-self.rect.size[1])/float(self.rect.size[1])
    #     self.tex_coords = [0, 1, 1, 1, 1, 0, 0, 0]        
    #     for i in range(0,8,2) :
    #         self.tex_coords[i] = self.tex_coords[i] + x_shift
    #         self.tex_coords[i+1] = self.tex_coords[i+1] + y_shift
    #     self.tex_coords = self.check_boundaries(self.tex_coords)
    #     self.rect.tex_coords = self.tex_coords
    #     self.rect.pos = (max(0,0.5*(self.width-self.rect.size[0])),(self.height-self.rect.size[1]))

    def set_zoom_factor(self,value) :
        if (__cheap_image_debug__) :
            print("InteractivePlotWidget.set_zoom_factor:",self.rect.tex_coords,self.height)
        old_size = self.rect.size
        self.rect.size = self.check_size((self.nx*value,self.ny*value))
        self.rect.pos = (0.5*(self.width-self.rect.size[0]),(self.height-self.rect.size[1]))
        y_shift = 0.5 * (self.rect.size[0]/old_size[0]-1.0) * self.height/self.rect.size[1]
        x_shift = 0
        if (__cheap_image_debug__) :
            print("InteractivePlotWidget.set_zoom_factor:",old_size,self.rect.size,y_shift)
        for i in range(0,8,2) :
            self.tex_coords[i] = self.tex_coords[i] + x_shift
            self.tex_coords[i+1] = self.tex_coords[i+1] + y_shift
        self.tex_coords = self.check_boundaries(self.tex_coords)
        self.rect.tex_coords = self.tex_coords
        if (__cheap_image_debug__) :
            print("                             :",self.rect.tex_coords,self.height)

        
    def check_boundaries(self,tex_coords) :
        new_tex_coords = [0]*len(tex_coords)
        max_x_shift = max((self.rect.size[0]-self.width)/self.rect.size[0],0)
        new_tex_coords[0] = max(min(tex_coords[0],max_x_shift),0)
        new_tex_coords[2] = max(min(tex_coords[2],1+max_x_shift),1)
        new_tex_coords[4] = max(min(tex_coords[4],1+max_x_shift),1)
        new_tex_coords[6] = max(min(tex_coords[6],max_x_shift),0)
        max_y_shift = max((self.rect.size[1]-self.height)/self.rect.size[1],0)
        new_tex_coords[1] = max(min(tex_coords[1],1+max_y_shift),1)
        new_tex_coords[3] = max(min(tex_coords[3],1+max_y_shift),1)
        new_tex_coords[5] = max(min(tex_coords[5],max_y_shift),0)
        new_tex_coords[7] = max(min(tex_coords[7],max_y_shift),0)
        return new_tex_coords

    def check_size(self,size) :
        return size
    
    def update_mpl(self,**kwargs) :

        if (__cheap_image_perf__) :
            print("--- %15.8g --- InteractivePlotWidget.update_mpl start"%(time.perf_counter()))
        # print("Started update_mpl in thread")
        
        fig = Figure(figsize=(self.nx/64,self.ny/64),dpi=64)
        canvas = FigureCanvas(fig)
        ax = fig.add_subplot(111,position=[0,0,1,1])
        self.generate_mpl_plot(fig,ax,**kwargs)

        if (__cheap_image_perf__) :
            print("--- %15.8g --- InteractivePlotWidget.update_mpl generated mpl"%(time.perf_counter()))

        # print("Made mpl plot in update_mpl in thread")
        canvas.draw()

        if (__cheap_image_perf__) :
            print("--- %15.8g --- InteractivePlotWidget.update_mpl drew canvas"%(time.perf_counter()))

        # print("Drew canvas in update_mpl in thread")
        # self.buf = np.asarray(canvas.buffer_rgba()).ravel()

        if (__cheap_image_perf__) :
            print("--- %15.8g --- InteractivePlotWidget.update_mpl cast to buf"%(time.perf_counter()))

        # print("Assigned buf in update_mpl in thread")
        # self.arr = array('B', self.buf)
        # self.arr = bytearray(self.buf)
        self.arr = bytearray(np.asarray(canvas.buffer_rgba()).ravel())
        
        if (__cheap_image_perf__) :
            print("--- %15.8g --- InteractivePlotWidget.update_mpl cast to byte array"%(time.perf_counter()))

        # print("Assigned arr in update_mpl in thread")
        self.texture.blit_buffer(self.arr, colorfmt='rgba', bufferfmt='ubyte')

        # print("Finished update_mpl in thread")

        if (__cheap_image_perf__) :
            print("--- %15.8g --- InteractivePlotWidget.update_mpl done"%(time.perf_counter()))
        
    def generate_mpl_plot(self,fig,ax,**kwargs) :
        # This is where we insert a Matplotlib figure.  Must use ax. and fig. child commands.
        pass



class InteractiveImageReconstructionPlot(InteractivePlotWidget) :
    
    def __init__(self,**kwargs) :
        if (__cheap_image_perf__) :
            print("--- %15.8g --- InteractiveImageReconstructionPlot.__init__ start"%(time.perf_counter()))

        self.xarr = 0
        self.yarr = 0
        self.Iarr = 1

        self.ddict = {}
        self.sdict = {}

        # self.argument_hash = None
        
        super().__init__(**kwargs)

        if (__cheap_image_perf__) :
            print("--- %15.8g --- InteractiveImageReconstructionPlot.__init__ done"%(time.perf_counter()))
        
    ##########
    # Low-level image reconstruction function
    def reconstruct_image(self,datadict,statdict,time_range=None,snr_cut=None,ngeht_diameter=6,f=2,method='cubic',make_hermitian=False) :

        # print("Started image reconstruction in thread")
        if (__cheap_image_perf__) :
            print("--- %15.8g --- InteractiveImageReconstructionPlot.reconstruct_image start"%(time.perf_counter()))
        
        # Useful constant
        uas2rad = np.pi/180.0/3600e6

        # Exclude stations not in array
        stations = list(np.unique(np.array(list(statdict.keys()))))
        keep = np.array([ (datadict['s1'][j] in stations) and (datadict['s2'][j] in stations) for j in range(len(datadict['s1'])) ])
        ddtmp = {}
        for key in ['u','v','V','s1','s2','t','err'] :
            ddtmp[key] = datadict[key][keep]

        if (len(ddtmp['u'])==0) :
            return None,None,None

        # Exclude stations that are "off"
        keep = np.array([ statdict[ddtmp['s1'][j]]['on'] and statdict[ddtmp['s2'][j]]['on'] for j in range(len(ddtmp['s1'])) ])
        ddnew = {}
        for key in ['u','v','V','s1','s2','t','err'] :
            ddnew[key] = ddtmp[key][keep]

        if (len(ddnew['u'])==0) :
            return None,None,None

        # Exclude data points outside the specified time range
        if (not time_range is None) :
            keep = (ddnew['t']>=time_range[0])*(ddnew['t']<time_range[1])
            for key in ['u','v','V','s1','s2','t','err'] :
                ddnew[key] = ddnew[key][keep]

        if (len(ddnew['u'])==0) :
            return None,None,None
                
        # Cut points with S/N less than the specified minimum value
        if (not snr_cut is None) and snr_cut>0:
            # Get a list of error adjustments based on stations
            diameter_correction_factor = {}
            for s in stations :
                if (statdict[s]['exists']) :
                    diameter_correction_factor[s] = 1.0
                else :
                    diameter_correction_factor[s] = statdict[s]['diameter']/ngeht_diameter

            # Baseline-by-baseline filtering
            # keep = np.array([ np.abs(ddnew['V'][j])/(ddnew['err'][j].real * diameter_correction_factor[ddnew['s1'][j]] * diameter_correction_factor[ddnew['s2'][j]]) > snr_cut for j in range(len(ddnew['s1'])) ])

            # Ad hoc phasing
            keep = np.array([True]*len(ddnew['s1']))
            jtot = np.arange(ddnew['t'].size)
            for tscan in np.unique(ddnew['t']) :
                inscan = (ddnew['t']==tscan)
                s1_scan = ddnew['s1'][inscan]
                s2_scan = ddnew['s2'][inscan]
                snr_scan = np.array([ ddnew['V'][inscan][j]/( ddnew['err'][inscan][j] * diameter_correction_factor[s1_scan[j]] * diameter_correction_factor[s2_scan[j]] ) for j in range(len(s1_scan)) ])
                detection_station_list = []
                for ss in np.unique(np.append(s1_scan,s2_scan)) :
                    snr_scan_ss = np.append(snr_scan[s1_scan==ss],snr_scan[s2_scan==ss])
                    if np.any(snr_scan_ss > snr_cut ) :
                        detection_station_list.append(ss)
                keep[jtot[inscan]] = np.array([ (s1_scan[k] in detection_station_list) and (s2_scan[k] in detection_station_list) for k in range(len(s1_scan)) ])
            
            
            for key in ['u','v','V','s1','s2','t','err'] :
                ddnew[key] = ddnew[key][keep]

        if (len(ddnew['u'])==0) :
            return None,None,None

        # Double up data to make V hemitian
        if (make_hermitian) :
            ddnew['u'] = np.append(ddnew['u'],-ddnew['u'])
            ddnew['v'] = np.append(ddnew['v'],-ddnew['v'])
            ddnew['V'] = np.append(ddnew['V'],np.conj(ddnew['V']))

        if (len(ddnew['u'])<=2) :
            return None,None,None

        if (__cheap_image_perf__) :
            print("--- %15.8g --- InteractiveImageReconstructionPlot.reconstruct_image station selection done"%(time.perf_counter()))
        
        # Get the region on which to compute gridded visibilities
        umax = np.max(ddnew['u'])
        vmax = np.max(ddnew['v'])
        u2,v2 = np.meshgrid(np.linspace(-f*umax,f*umax,256),np.linspace(-f*vmax,f*vmax,256))

        # SciPy
        # pts = np.array([ddnew['u'],ddnew['v']]).T
        # V2r = si.griddata(pts,np.real(ddnew['V']),(u2,v2),method=method,fill_value=0.0)
        # V2i = si.griddata(pts,np.imag(ddnew['V']),(u2,v2),method=method,fill_value=0.0)

        # Maptlotlib
        triang = tri.Triangulation(ddnew['u'], ddnew['v'])
        if (__cheap_image_perf__) :
            print("--- %15.8g --- InteractiveImageReconstructionPlot.reconstruct_image triangulation done"%(time.perf_counter()))
        
        if (method=='linear') :
            V2r = np.array(np.ma.fix_invalid(tri.LinearTriInterpolator(triang, np.real(ddnew['V']))(u2,v2),fill_value=0.0))
            V2i = np.array(np.ma.fix_invalid(tri.LinearTriInterpolator(triang, np.imag(ddnew['V']))(u2,v2),fill_value=0.0))
        elif (method=='cubic') :
            # V2r = np.array(np.ma.fix_invalid(tri.CubicTriInterpolator(triang, np.real(ddnew['V']),kind='geom')(u2,v2),fill_value=0.0))
            # V2i = np.array(np.ma.fix_invalid(tri.CubicTriInterpolator(triang, np.imag(ddnew['V']),kind='geom')(u2,v2),fill_value=0.0))
            V2r = np.array(np.ma.fix_invalid(tri.CubicTriInterpolator(triang, ddnew['V'].real,kind='geom')(u2,v2),fill_value=0.0))
            V2i = np.array(np.ma.fix_invalid(tri.CubicTriInterpolator(triang, ddnew['V'].imag,kind='geom')(u2,v2),fill_value=0.0))

        else :
            print("ERROR: method %s not implemented"%(method))
        
        V2 = V2r + 1.0j*V2i

        if (__cheap_image_perf__) :
            print("--- %15.8g --- InteractiveImageReconstructionPlot.reconstruct_image interpolation done"%(time.perf_counter()))

        
        ### Filter to smooth at edges
        # Cosine filter
        # V2 = V2 * np.cos(u2/umax*0.5*np.pi) * np.cos(v2/vmax*0.5*np.pi)
        # Blackman filter
        # hu = 0.42 - 0.5*np.cos(2.0*np.pi*(u2+umax)/(2*umax)) + 0.08*np.cos(4.0*np.pi*(u2+umax)/(2*umax))
        # hv = 0.42 - 0.5*np.cos(2.0*np.pi*(v2+umax)/(2*umax)) + 0.08*np.cos(4.0*np.pi*(v2+umax)/(2*umax))
        # V2 = V2*hu*hv
        # Gaussian beam filter
        uvmax2 = np.max(ddnew['u']**2+ddnew['v']**2)
        gaussian_filter = np.exp(-np.pi**2*(u2**2+v2**2)/(4.0*np.log(2.0)*uvmax2))
        V2 = V2*gaussian_filter

        # Generate the x,y grid on which to image
        x1d = np.fft.fftshift(np.fft.fftfreq(u2.shape[0],d=(u2[1,1]-u2[0,0])*1e9)/uas2rad)
        y1d = np.fft.fftshift(np.fft.fftfreq(v2.shape[1],d=(v2[1,1]-v2[0,0])*1e9)/uas2rad)
        xarr,yarr = np.meshgrid(-x1d,-y1d)

        # Compute image estimate via FFT
        Iarr = np.fft.fftshift(np.real(np.fft.ifft2(np.fft.ifftshift(V2))))
        # Iarr = np.fft.fftshift(np.abs(np.fft.ifft2(np.fft.ifftshift(V2))))

        if (__cheap_image_perf__) :
            print("--- %15.8g --- InteractiveImageReconstructionPlot.reconstruct_image iFFT done"%(time.perf_counter()))

        # print("Finished image reconstruction in thread")
        
        # Return
        return xarr,yarr,Iarr


    def estimate_dynamic_range(self,x,y,I) :
        peak_flux = np.max(I)
        peak_negative_flux = np.max(np.maximum(-I,0.0))
        return peak_flux/peak_negative_flux
    
    def generate_mpl_plot(self,fig,ax,**kwargs) :

        if (__cheap_image_debug__) :
            print("InteractiveImageReconstructionPlot.generate_mpl_plot: start")
        
        # This is where we insert a Matplotlib figure.  Must use ax. and fig. child commands.
        # You probably want, but do not require, the following in your over-lay
        self.plot_image_reconstruction(ax,self.ddict,self.sdict,**kwargs)
        ax.set_facecolor((0,0,0,1))
        fig.set_facecolor((0,0,0,1))

    def update(self,datadict,statdict,**kwargs) :
        self.sdict = statdict
        self.ddict = datadict
        # print("Started update, initiating thread:",kwargs)
        self.update_mpl(**kwargs)


        # # create the thread to invoke other_func with arguments (2, 5)
        # andrews_specific_name = threading.Thread(target=self.update_mpl, kwargs=kwargs)
        # # # set daemon to true so the thread dies when app is closed
        # andrews_specific_name.daemon = True
        # # start the thread
        # andrews_specific_name.start()
        # # wait for end for now
        # andrews_specific_name.join()
        # #time.sleep(10) # HACK
        

        # print("Finished update, should have finished thread")
        

    def replot(self,datadict,statdict,**kwargs) :
        self.sdict = statdict
        self.ddict = datadict
        self.update_mpl(**kwargs)

        # print("Started replot, initiating thread")

        # # create the thread to invoke other_func with arguments (2, 5)
        # t = threading.Thread(target=self.update_mpl, kwargs=kwargs)
        # # # set daemon to true so the thread dies when app is closed
        # # t.daemon = True
        # # start the thread
        # t.start()
        # # wait for end for now
        # t.join()

        # print("Finished replot, should have finished thread")
        
    def check_boundaries(self,tex_coords) :
        return tex_coords

    def check_size(self,size) :
        if (size[0]<self.width) :
            size = (self.width, size[1]/size[0] * self.width)
        elif  (size[1]<self.height) :
            size = (size[0]/size[1] * self.height, self.height)
        return size

    ############
    # High-level plot generation
    def plot_image_reconstruction(self,axs,datadict,statdict,time_range=None,snr_cut=None,ngeht_diameter=6,limits=None,show_map=True,show_contours=True) :

        if (__cheap_image_perf__) :
            print("--- %15.8g --- InteractiveImageReconstructionPlot.plot_image_reconstruction start"%(time.perf_counter()))
        
        if (len(statdict.keys())==0) :
            return
        
        # Reconstruct image
        self.xarr,self.yarr,self.Iarr=self.reconstruct_image(datadict,statdict,time_range=time_range,snr_cut=snr_cut,ngeht_diameter=ngeht_diameter)

        if (__cheap_image_perf__) :
            print("--- %15.8g --- InteractiveImageReconstructionPlot.plot_image_reconstruction reconstruction done"%(time.perf_counter()))

        
        self.replot_image_reconstruction(axs,time_range=time_range,limits=limits,show_map=show_map,show_contours=show_contours)
        

        if (__cheap_image_perf__) :
            print("--- %15.8g --- InteractiveImageReconstructionPlot.plot_image_reconstruction done"%(time.perf_counter()))


    ############
    # High-level plot generation
    def replot_image_reconstruction(self,axs,time_range=None,limits=None,show_map=True,show_contours=True) :


        if (__cheap_image_perf__) :
            print("--- %15.8g --- InteractiveImageReconstructionPlot.replot_image_reconstruction start"%(time.perf_counter()))
        

        if (self.Iarr is None) :
            axs.text(0.5,0.5,"Insufficient Data!",color='w',fontsize=24,ha='center',va='center')
            return


        # Plot linear image
        if (show_map) :
            axs.imshow(self.Iarr,origin='lower',extent=[self.xarr[0,0],self.xarr[0,-1],self.yarr[0,0],self.yarr[-1,0]],cmap='afmhot',vmin=0,interpolation='spline16')

        if (__cheap_image_perf__) :
            print("--- %15.8g --- InteractiveImageReconstructionPlot.replot_image_reconstruction image plotted"%(time.perf_counter()))

            
        # Plot the log contours
        if (show_contours) :
            lI = np.log10(np.maximum(0.0,self.Iarr)/np.max(self.Iarr)+1e-20)
            lmI = np.log10(np.maximum(0.0,-self.Iarr)/np.max(self.Iarr)+1e-20)
            
            lev10lo = max(np.min(lI[self.Iarr>0]),-4)
            lev10 = np.sort( -np.arange(0,lev10lo,-1) )
            axs.contour(self.xarr,self.yarr,-lI,levels=lev10,colors='cornflowerblue',alpha=0.5)
            #plt.contour(self.x,self.y,-lmI,levels=lev10,colors='green',alpha=0.5)            
            lev1 = []
            for l10 in -lev10[1:] :
                lev1.extend( np.log10(np.array([2,3,4,5,6,7,8,9])) + l10 )
            lev1 = np.sort(-np.array(lev1))
            axs.contour(self.xarr,self.yarr,-lI,levels=lev1,colors='cornflowerblue',alpha=0.5,linewidths=0.5)
            axs.contour(self.xarr,self.yarr,-lmI,levels=lev1[-10:],colors='green',alpha=0.5,linewidths=0.5)

        if (__cheap_image_perf__) :
            print("--- %15.8g --- InteractiveImageReconstructionPlot.replot_image_reconstruction contours plotted"%(time.perf_counter()))

        # Fix the limits
        if (not limits is None) :
            axs.set_xlim((limits[0],limits[1]))
            axs.set_ylim((limits[2],limits[3]))
        else :
            xmin = min(np.min(self.xarr[lI>-2]),np.min(self.yarr[lI>-2]))
            xmax = max(np.max(self.xarr[lI>-2]),np.max(self.yarr[lI>-2]))
            axs.set_xlim((xmax,xmin))
            axs.set_ylim((xmin,xmax))

        if (__cheap_image_perf__) :
            print("--- %15.8g --- InteractiveImageReconstructionPlot.replot_image_reconstruction done"%(time.perf_counter()))
            
