__version__ = "1.0.0"

__main_debug__ = False
__main_perf__ = False
__generate_fast_start_data__ = False

# Fix the icon imports
import os
os.environ["KIVY_TEXT"] = "pil"
####



if (__main_perf__) :
    import time
    print("--- %15.8g --- main.py start"%(time.perf_counter()))


from kivy.app import App
from kivymd.app import MDApp
from kivy.lang import Builder

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner, SpinnerOption
from kivy.properties import StringProperty, NumericProperty, ObjectProperty, BooleanProperty, ListProperty
from kivy.clock import Clock
from kivy.uix.screenmanager import FadeTransition, SlideTransition
from kivy.metrics import dp,sp
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from kivy.graphics import Color, Line, Rectangle
from kivy.utils import get_hex_from_color
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window

from kivy.uix.screenmanager import Screen
from kivy.loader import Loader

if (__main_perf__) :
    print("--- %15.8g --- imported kivy"%(time.perf_counter()))


from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.behaviors import CircularRippleBehavior
from kivymd.uix.filemanager import MDFileManager
from kivymd.theming import ThemableBehavior
from kivymd.uix.navigationdrawer import MDNavigationLayout
from kivymd.uix.list import MDList, OneLineIconListItem
from kivymd.uix.label import MDLabel
from kivymd.uix.snackbar import Snackbar 
from kivymd.uix.snackbar import BaseSnackbar

if (__main_perf__) :
    print("--- %15.8g --- imported kivymd"%(time.perf_counter()))


from fancy_mdslider import FancyMDSlider


if (__main_perf__) :
    print("--- %15.8g --- imported fancy_mdslider"%(time.perf_counter()))


import numpy as np
from os import path
from pathlib import Path as plP
import copy
import hashlib

if (__main_perf__) :
    print("--- %15.8g --- imported python libraries"%(time.perf_counter()))

####################
# TESTING
# import pickle
# 
# Window.size = (300,500)
##################


try :
    from android.permissions import request_permissions, Permission
    request_permissions([Permission.READ_EXTERNAL_STORAGE])
except:
    print("Could not load android permissions stuff, pobably not on android?")

if (__main_perf__) :
    print("--- %15.8g --- tried android permissions"%(time.perf_counter()))


import ngeht_array
import data
import baseline_plot
import cheap_image
import map_plot
import skymap_plot
import progress_wheel

if (__main_perf__) :
    print("--- %15.8g --- imported project sources"%(time.perf_counter()))


_on_color = (1,0.75,0.25,1)
_off_color = (0.5,0,0,1)

_time_range = [0,24]
_ngeht_diameter = 6
_snr_cut = 7.0
_ngeht_diameter_setting = 6
_snr_cut_setting = 1

_existing_arrays = ['EHT 2017','EHT 2022']
_existing_station_list = ['PV','AZ','SM','LM','AA','AP','SP','JC','GL','PB','KP','HA']

_stationdicts={}
_stationdicts['ngEHT+']=ngeht_array.read_array(path.abspath(path.join(path.dirname(__file__),'arrays/ngeht_ref1.txt')), existing_station_list=_existing_station_list)
#_stationdicts['ngEHT']=ngeht_array.read_array(path.abspath(path.join(path.dirname(__file__),'arrays/ngeht_ref1.txt')), existing_station_list=_existing_station_list)
_stationdicts['ngEHT 10']=ngeht_array.read_array(path.abspath(path.join(path.dirname(__file__),'arrays/ngeht_ref1_10.txt')), existing_station_list=_existing_station_list)
_stationdicts['ngEHT  8']=ngeht_array.read_array(path.abspath(path.join(path.dirname(__file__),'arrays/ngeht_ref1_8.txt')), existing_station_list=_existing_station_list)
_stationdicts['ngEHT  6']=ngeht_array.read_array(path.abspath(path.join(path.dirname(__file__),'arrays/ngeht_ref1_6.txt')), existing_station_list=_existing_station_list)
_stationdicts['ngEHT  4']=ngeht_array.read_array(path.abspath(path.join(path.dirname(__file__),'arrays/ngeht_ref1_4.txt')), existing_station_list=_existing_station_list)


_stationdicts['EHT 2017']=ngeht_array.read_array(path.abspath(path.join(path.dirname(__file__),'arrays/eht2017.txt')),existing_station_list=_existing_station_list)
_stationdicts['EHT 2022']=ngeht_array.read_array(path.abspath(path.join(path.dirname(__file__),'arrays/eht2022.txt')),existing_station_list=_existing_station_list)

_array_index = 1
_array = list(_stationdicts.keys())[_array_index]

_statdict_maximum=_stationdicts['ngEHT+']
_statdict=_stationdicts[_array]
_datadict=data.read_themis_data_file(path.abspath(path.join(path.dirname(__file__),'data/V_M87_ngeht_ref1_230_perfect_scanavg_tygtd.dat')))

_source_RA = 17.7611225
_source_Dec = -29.007810


if (__main_perf__) :
    print("--- %15.8g --- Defined/specified globals"%(time.perf_counter()))


##############################################################################################
class ItemDrawer(OneLineIconListItem):
    icon = StringProperty()
    text_color = ListProperty()
    
    def __init__(self,**kwargs) :
        super().__init__(**kwargs)
        self.text_color = self.theme_cls.text_color
    
class QuickstartNavigationDrawer(ScrollView):
    active_screen = StringProperty(None)
    def __init__(self,**kwargs) :
        super().__init__(**kwargs)
        self.active_screen = "quickstart_source"

        
class ExpertNavigationDrawer(ScrollView):
    active_screen = StringProperty(None)
    def __init__(self,**kwargs) :
        super().__init__(**kwargs)
        self.active_screen = "expert_source"

    
class ContentNavigationDrawer(BoxLayout):
    screen_manager = ObjectProperty()
    nav_drawer = ObjectProperty()

    def __init__(self,**kwargs):
        if (__main_perf__) :
            print("--- %15.8g --- ContentNavigationDrawer.__init__ start"%(time.perf_counter()))

        super().__init__(**kwargs)
        
        self.exp_nd = ExpertNavigationDrawer()
        self.exp_qs = QuickstartNavigationDrawer()

        if (__main_perf__) :
            print("--- %15.8g --- ContentNavigationDrawer.__init__ done"%(time.perf_counter()))
        
        
    def set_nav_drawer_list(self,expert) :
        self.remove_widget(self.children[0])
        if (expert) :
            self.add_widget(self.exp_nd)
            MainApp.get_running_app().root.ids.screen_manager.current = self.exp_nd.active_screen
            MainApp.get_running_app().app_mode = 'expert'
        else :
            self.add_widget(self.exp_qs)
            MainApp.get_running_app().root.ids.screen_manager.current = self.exp_qs.active_screen
            MainApp.get_running_app().app_mode = 'quickstart'
        MainApp.get_running_app().save_setting('app_mode')
            

class ActiveSwitchMDLabel(ThemableBehavior,BoxLayout):
    left_buffer = NumericProperty(dp(15))
    right_buffer = NumericProperty(dp(15))
    prefix_text = StringProperty("")
    deactivated_text = StringProperty(None)
    activated_text = StringProperty(None)
    postfix_text = StringProperty("")
    active = BooleanProperty(False)
    disabled = BooleanProperty(False) 
    
    def active_text(self,text) :
        modtext = '[color='+str(get_hex_from_color(self.theme_cls.primary_color))+']'+text+'[/color]'
        return modtext
    
    def deactive_text(self,text) :
        modtext = '[color=808080]'+text+'[/color]'
        return modtext
    
class DrawerList(ThemableBehavior, MDList):

    def __init__(self,**kwargs) :
        if (__main_perf__) :
            print("--- %15.8g --- DrawerList.__init__ start"%(time.perf_counter()))
        
        super().__init__(**kwargs)
        self.text_color = self.theme_cls.text_color

        if (__main_perf__) :
            print("--- %15.8g --- DrawerList.__init__ done"%(time.perf_counter()))
        
    def set_color_item(self, instance_item):
        '''Called when tap on a menu item.'''

        # Set the color of the icon and text for the menu item.
        for item in self.children:
            if item.text_color == self.theme_cls.primary_color:
                item.text_color = self.theme_cls.text_color
                break
        instance_item.text_color = self.theme_cls.primary_color    




##############################################################################################


class Abbrv_MenuedReconstructionPlot(BoxLayout) :

    plot_maxsize = 750.0
    plot_center = np.array([0.0,0.0])

    menu_id = ObjectProperty(None)

    show_contours = BooleanProperty(True)
    
    def __init__(self,**kwargs) :
        if (__main_perf__) :
            print("--- %15.8g --- Abbrv_MenuedReconstructionPlot.__init__ start"%(time.perf_counter()))

        super().__init__(**kwargs)

        self.irp = cheap_image.InteractiveImageReconstructionPlot()
        self.irp.default_zoom_factor = 8.0
        
        self.time_range = [0,24]
        self.ngeht_diameter = 6
        self.snr_cut = 0

        self.sdict = _statdict
        self.ddict = _datadict

        self.plot_frozen = False

        self.limits = np.array([1,-1,-1,1])*self.plot_maxsize
        self.limits[:2] = self.limits[:2] + self.plot_center[0]
        self.limits[2:] = self.limits[2:] + self.plot_center[1]

        self.show_contours = False
        
        self.argument_hash = None

        if __generate_fast_start_data__ :
            print("Abbrv_MenuedReconstructionPlot: Generating fast start data")
            self.update(self.ddict,self.sdict,time_range=self.time_range,snr_cut=self.snr_cut,ngeht_diameter=self.ngeht_diameter,limits=self.limits)
            np.save("fast_start_data/Abbrv_MenuedReconstructionPlot.npy",[self.argument_hash,self.irp.buf,self.irp.arr])
        else :
            self.argument_hash,self.irp.buf,self.irp.arr = np.load("fast_start_data/Abbrv_MenuedReconstructionPlot.npy",allow_pickle=True)
            self.irp.texture.blit_buffer(self.irp.arr,colorfmt='rgba',bufferfmt='ubyte')
            # self.update(self.ddict,self.sdict,time_range=self.time_range,snr_cut=self.snr_cut,ngeht_diameter=self.ngeht_diameter,limits=self.limits)
            if (__main_debug__) :
                print("Abbrv_MenuedReconstructionPlot: Reloaded fast start data")
                print("   hash:",self.argument_hash)


        self.add_widget(self.irp)

        
        
        if __main_debug__ :
            print("mrp.__init__: finished")

        if (__main_perf__) :
            print("--- %15.8g --- Abbrv_MenuedReconstructionPlot.__init__ done"%(time.perf_counter()))

            

    def check_image_hash(self) :
        kwargs = {}
        kwargs['time_range']=self.time_range
        kwargs['limits']=self.limits
        kwargs['snr_cut']=self.snr_cut
        kwargs['ngeht_diameter']=self.ngeht_diameter
        kwargs['show_contours']=self.show_contours
        new_argument_hash = hashlib.md5(bytes(str(_datadict)+str(_statdict)+str(kwargs),'utf-8')).hexdigest()
        if ( new_argument_hash == self.argument_hash ) :
            return False
        return True
        
            
    def update(self,datadict,statdict,**kwargs) :
        kwargs['time_range']=self.time_range
        kwargs['limits']=self.limits
        kwargs['snr_cut']=self.snr_cut
        kwargs['ngeht_diameter']=self.ngeht_diameter
        kwargs['show_contours']=self.show_contours
        new_argument_hash = hashlib.md5(bytes(str(datadict)+str(statdict)+str(kwargs),'utf-8')).hexdigest()
        if (__main_debug__) :
            print("update kwargs:",kwargs)
            print("update New image md5 hash:",new_argument_hash)
            print("update Old image md5 hash:",self.argument_hash)
        if ( new_argument_hash == self.argument_hash ) :
            return
        self.argument_hash = new_argument_hash
        self.irp.update(datadict,statdict,**kwargs)
        if __main_debug__ :
            print("mrp.update:",self.sdict.keys(),self.size)

    def replot(self,**kwargs) :
        global _datadict, _statdict
        self.ddict = _datadict
        self.sdict = _statdict
        kwargs['time_range']=self.time_range
        kwargs['limits']=self.limits
        kwargs['snr_cut']=self.snr_cut
        kwargs['ngeht_diameter']=self.ngeht_diameter
        kwargs['show_contours']=self.show_contours
        new_argument_hash = hashlib.md5(bytes(str(self.ddict)+str(self.sdict)+str(kwargs),'utf-8')).hexdigest()
        if (__main_debug__):
            print("replot New image md5 hash:",new_argument_hash)
            print("replot Old image md5 hash:",self.argument_hash)
        if ( new_argument_hash == self.argument_hash ) :
            return
        self.argument_hash = new_argument_hash
        self.irp.replot(self.ddict,self.sdict,**kwargs)
        if __main_debug__ :
            print("mrp.replot:",self.sdict.keys(),self.size)

    def refresh(self,**kwargs) :
        kwargs['time_range']=self.time_range
        kwargs['limits']=self.limits
        kwargs['snr_cut']=self.snr_cut
        kwargs['ngeht_diameter']=self.ngeht_diameter
        kwargs['show_contours']=self.show_contours
        new_argument_hash = hashlib.md5(bytes(str(self.ddict)+str(self.sdict)+str(kwargs),'utf-8')).hexdigest()
        if (__main_debug__):
            print("refresh New image md5 hash:",new_argument_hash)
            print("refresh Old image md5 hash:",self.argument_hash)
        if ( new_argument_hash == self.argument_hash ) :
            return
        self.argument_hash = new_argument_hash
        self.irp.replot(self.ddict,self.sdict,**kwargs)
        if __main_debug__ :
            print("mrp.refresh:",self.sdict.keys(),self.size)
            

    def freeze_plot(self) :
        self.irp.plot_frozen = True

    def unfreeze_plot(self) :
        self.irp.plot_frozen = False


class MenuedReconstructionPlot(BoxLayout) :

    plot_maxsize = 750.0
    plot_center = np.array([0.0,0.0])

    menu_id = ObjectProperty(None)

    show_contours = BooleanProperty(True)
    
    def __init__(self,**kwargs) :
        if (__main_perf__) :
            print("--- %15.8g --- MenuedReconstructionPlot.__init__ start"%(time.perf_counter()))

        super().__init__(**kwargs)

        self.irp = cheap_image.InteractiveImageReconstructionPlot()
        
        self.time_range = _time_range
        self.ngeht_diameter = _ngeht_diameter
        self.snr_cut = _snr_cut

        self.sdict = _statdict
        self.ddict = _datadict

        self.plot_frozen = False

        self.limits = np.array([1,-1,-1,1])*self.plot_maxsize
        self.limits[:2] = self.limits[:2] + self.plot_center[0]
        self.limits[2:] = self.limits[2:] + self.plot_center[1]

        self.show_contours = True
        
        self.argument_hash = None

        if __generate_fast_start_data__ :
            print("MenuedReconstructionPlot: Generating fast start data")
            self.update(self.ddict,self.sdict,time_range=self.time_range,snr_cut=self.snr_cut,ngeht_diameter=self.ngeht_diameter,limits=self.limits)
            np.save("fast_start_data/MenuedReconstructionPlot.npy",[self.argument_hash,self.irp.buf,self.irp.arr])
        else :
            self.argument_hash,self.irp.buf,self.irp.arr = np.load("fast_start_data/Abbrv_MenuedReconstructionPlot.npy",allow_pickle=True)
            self.irp.texture.blit_buffer(self.irp.arr,colorfmt='rgba',bufferfmt='ubyte')
            # self.update(self.ddict,self.sdict,time_range=self.time_range,snr_cut=self.snr_cut,ngeht_diameter=self.ngeht_diameter,limits=self.limits)
            if (__main_debug__) :
                print("MenuedReconstructionPlot: Reloaded fast start data")
                print("   hash:",self.argument_hash)

        self.add_widget(self.irp)

        
        if __main_debug__ :
            print("mrp.__init__: finished")
        
        if (__main_perf__) :
            print("--- %15.8g --- MenuedReconstructionPlot.__init__ done"%(time.perf_counter()))

    def check_image_hash(self) :
        kwargs = {}
        kwargs['time_range']=self.time_range
        kwargs['limits']=self.limits
        kwargs['snr_cut']=self.snr_cut
        kwargs['ngeht_diameter']=self.ngeht_diameter
        kwargs['show_contours']=self.show_contours
        new_argument_hash = hashlib.md5(bytes(str(_datadict)+str(_statdict)+str(kwargs),'utf-8')).hexdigest()
        if ( new_argument_hash == self.argument_hash ) :
            return False
        return True
        
            
    def update(self,datadict,statdict,**kwargs) :
        kwargs['time_range']=self.time_range
        kwargs['limits']=self.limits
        kwargs['snr_cut']=self.snr_cut
        kwargs['ngeht_diameter']=self.ngeht_diameter
        kwargs['show_contours']=self.show_contours
        new_argument_hash = hashlib.md5(bytes(str(datadict)+str(statdict)+str(kwargs),'utf-8')).hexdigest()
        if (__main_debug__) :
            print("update kwargs:",kwargs)
            print("update New image md5 hash:",new_argument_hash)
            print("update Old image md5 hash:",self.argument_hash)
        if ( new_argument_hash == self.argument_hash ) :
            return
        self.argument_hash = new_argument_hash
        self.irp.update(datadict,statdict,**kwargs)
        if __main_debug__ :
            print("mrp.update:",self.sdict.keys(),self.size)

    def replot(self,**kwargs) :
        global _datadict, _statdict
        self.ddict = _datadict
        self.sdict = _statdict
        kwargs['time_range']=self.time_range
        kwargs['limits']=self.limits
        kwargs['snr_cut']=self.snr_cut
        kwargs['ngeht_diameter']=self.ngeht_diameter
        kwargs['show_contours']=self.show_contours
        new_argument_hash = hashlib.md5(bytes(str(self.ddict)+str(self.sdict)+str(kwargs),'utf-8')).hexdigest()
        if (__main_debug__):
            print("replot New image md5 hash:",new_argument_hash)
            print("replot Old image md5 hash:",self.argument_hash)
        if ( new_argument_hash == self.argument_hash ) :
            return
        self.argument_hash = new_argument_hash
        self.irp.replot(self.ddict,self.sdict,**kwargs)
        if __main_debug__ :
            print("mrp.replot:",self.sdict.keys(),self.size)

    def refresh(self,**kwargs) :
        kwargs['time_range']=self.time_range
        kwargs['limits']=self.limits
        kwargs['snr_cut']=self.snr_cut
        kwargs['ngeht_diameter']=self.ngeht_diameter
        kwargs['show_contours']=self.show_contours
        new_argument_hash = hashlib.md5(bytes(str(self.ddict)+str(self.sdict)+str(kwargs),'utf-8')).hexdigest()
        if (__main_debug__):
            print("refresh New image md5 hash:",new_argument_hash)
            print("refresh Old image md5 hash:",self.argument_hash)
        if ( new_argument_hash == self.argument_hash ) :
            return
        self.argument_hash = new_argument_hash
        self.irp.replot(self.ddict,self.sdict,**kwargs)
        if __main_debug__ :
            print("mrp.refresh:",self.sdict.keys(),self.size)
            
    def set_start_time(self,val) :
        if __main_debug__ :
            print("mrp.set_start_time:",val)
        self.time_range[1] = self.time_range[1]-self.time_range[0]+val
        self.time_range[0] = val
        self.update(self.ddict,self.sdict)
        
    def set_obs_time(self,val) :
        self.time_range[1] = self.time_range[0] + val
        self.update(self.ddict,self.sdict)

    def set_ngeht_diameter(self,val) :
        global _ngeht_diameter
        self.ngeht_diameter = val
        _ngeht_diameter = self.ngeht_diameter
        self.update(self.ddict,self.sdict)

    def set_snr_cut(self,val) :
        global _snr_cut
        self.snr_cut = val
        if (val is None) :
            self.snr_cut = 0
        _snr_cut = self.snr_cut
        self.update(self.ddict,self.sdict)

    def freeze_plot(self) :
        self.irp.plot_frozen = True

    def unfreeze_plot(self) :
        self.irp.plot_frozen = False

        
class MenuedBaselinePlot(BoxLayout) :

    # ibp = baseline_plot.InteractiveBaselinePlot_kivygraph()
    ibp = ObjectProperty(None)
    menu_id = ObjectProperty(None)

    def __init__(self,**kwargs) :
        if (__main_perf__) :
            print("--- %15.8g --- MenuedBaselinePlot.__init__ start"%(time.perf_counter()))

        super().__init__(**kwargs)

        self.time_range = _time_range
        self.ngeht_diameter = _ngeht_diameter
        self.snr_cut = _snr_cut

        self.sdict = _statdict
        self.ddict = _datadict

        self.plot_frozen = False

        self.limits = [-20,20,20,-20]

        # self.update(self.ddict,self.sdict,limits=self.limits)

        # self.add_widget(self.ibp)
        
        if __main_debug__ :
            print("mp.__init__: finished")

        if (__main_perf__) :
            print("--- %15.8g --- MenuedBaselinePlot.__init__ done"%(time.perf_counter()))
            

    def update(self,datadict,statdict,**kwargs) :

        kwargs['time_range']=self.time_range
        kwargs['limits']=self.limits
        kwargs['snr_cut']=self.snr_cut
        kwargs['ngeht_diameter']=self.ngeht_diameter

        global _datadict, _statdict
        _datadict = datadict
        _statdict = statdict
        self.ddict = _datadict
        self.sdict = _statdict
        
        self.ibp.update(datadict,statdict,**kwargs)
                    
        if __main_debug__ :
            print("bp.update:",self.sdict.keys(),self.size)

    def replot(self,**kwargs) :
        kwargs['time_range']=self.time_range
        kwargs['limits']=self.limits
        kwargs['snr_cut']=self.snr_cut
        kwargs['ngeht_diameter']=self.ngeht_diameter

        global _datadict, _statdict
        self.ddict = _datadict
        self.sdict = _statdict

        self.ibp.replot(self.ddict,self.sdict,**kwargs)
        
        if __main_debug__ :
            print("mp.replot:",self.sdict.keys(),self.size)

    def refresh(self,**kwargs) :
        kwargs['time_range']=self.time_range
        kwargs['limits']=self.limits
        kwargs['snr_cut']=self.snr_cut
        kwargs['ngeht_diameter']=self.ngeht_diameter
        self.ibp.replot(self.ddict,self.sdict,**kwargs)
        
        if __main_debug__ :
            print("mp.refresh:",self.sdict.keys(),self.size)
            
    def set_start_time(self,val) :
        self.time_range[1] = self.time_range[1]-self.time_range[0]+val
        self.time_range[0] = val
        self.refresh()
        
    def set_obs_time(self,val) :
        self.time_range[1] = self.time_range[0] + val
        self.refresh()
        if __main_debug__ :
            print("MenuedBaselinePlot.set_obs_time: set the time")
        
    def set_ngeht_diameter(self,val) :
        global _ngeht_diameter
        self.ngeht_diameter = val
        _ngeht_diameter = self.ngeht_diameter
        self.refresh()

    def set_snr_cut(self,val) :
        global _snr_cut
        self.snr_cut = val
        if (val is None) :
            self.snr_cut = 0
        _snr_cut = self.snr_cut
        self.refresh()

    def freeze_plot(self) :
        self.ibp.plot_frozen = True

    def unfreeze_plot(self) :
        self.ibp.plot_frozen = False

    def zoom_in(self) :
        self.ibp.zoom_in()

    def zoom_out(self) :
        self.ibp.zoom_out()

    
            
class MenuedBaselineMapPlot_kivygraph(BoxLayout) :

    # bmc = map_plot.BaselineMapCanvas()
    # mp = map_plot.InteractiveBaselineMapPlot_kivygraph()
    menu_id = ObjectProperty(None)
    ad_stn_box = ObjectProperty(None)
    
    def __init__(self,**kwargs) :
        if (__main_perf__) :
            print("--- %15.8g --- MenuedBaselineMapPlot_kivygrap.__init__ start"%(time.perf_counter()))

        self.bmc = map_plot.BaselineMapCanvas()
        self.mp = map_plot.InteractiveBaselineMapPlot_kivygraph()

        global _datadict, _statdict
        
        self.sdict = _statdict
        self.ddict = _datadict

        super().__init__(**kwargs)

        self.time_range = _time_range
        self.ngeht_diameter = _ngeht_diameter
        self.snr_cut = _snr_cut

        self.plot_frozen = False

        self.add_widget(self.mp)
        self.add_widget(self.bmc)

        self.pixel_offset = (0,0)

        # Generate some default resizing behaviors
        self.bind(height=self.resize)
        self.bind(width=self.resize)

        # Generate first set of baselines
        self.mp.replot(self.ddict,self.sdict)

        # New station stuff
        self.add_station_btn = Button(text="Add",font_size=sp(18),color=(1,1,1,1),background_color=(0,0,0,0.25))
        self.del_station_btn = Button(text="Del",font_size=sp(18),color=(1,1,1,1),background_color=(0,0,0,0.25))
        self.add_station_btn.bind(on_release=self.add_station)
        self.del_station_btn.bind(on_release=self.del_station)
        self.new_station_name_list_avail = []
        for j in range(20) :
            self.new_station_name_list_avail.append('%02i'%j)
        self.new_station_name_list_used = []
        self.prototype_station = 'BA'
        self.editing_mode_add = False
        self.editing_mode_del = False

        # Snap to source source name
        self.snap_source = None


        # self.theme_cls.bind(theme_style=self.set_theme)
        
        if __main_debug__ :
            print("mp.__init__: finished")

        if (__main_perf__) :
            print("--- %15.8g --- MenuedBaselineMapPlot_kivygrap.__init__ done"%(time.perf_counter()))


    # def set_theme(self,widget,value) :
    #     self.replot()
            
        
    def add_stn_buttons(self) :
        if (__main_debug__) :
            print("MenuedBaselineMapPlot_kivygraph.add_stn_buttons called:",len(self.ad_stn_box.children))
        if ( len(self.ad_stn_box.children)==0 ) :
            self.ad_stn_box.add_widget(self.add_station_btn)
            self.ad_stn_box.add_widget(self.del_station_btn)

    def remove_stn_buttons(self) :
        if (__main_debug__) :
            print("MenuedBaselineMapPlot_kivygraph.remove_stn_buttons called")
        self.ad_stn_box.clear_widgets()

    def add_station(self,widget) :
        global _statdict, _datadict
        if (_array_index==0) :
            if (len(self.new_station_name_list_avail)>0) :
                if (self.editing_mode_add==False) :
                    self.editing_mode_add = True
                    self.editing_mode_del = False
                    self.cursor_on()
                    self.add_station_btn.text = '+'+self.new_station_name_list_avail[0]
                    self.add_station_btn.color = _on_color
                    self.add_station_btn.background_color = (_on_color[0],_on_color[1],_on_color[2],0.75)
                    self.del_station_btn.text = 'Del'
                    self.del_station_btn.color = (1,1,1,1)
                    self.del_station_btn.background_color = (0,0,0,0.25)
                else :
                    self.editing_mode_add = False
                    latlon = self.cursor_off()
                    nn = self.new_station_name_list_avail[0]
                    _stationdicts['ngEHT+'][nn] = copy.deepcopy(_statdict[self.prototype_station])
                    _stationdicts['ngEHT+'][nn]['on'] = True
                    _stationdicts['ngEHT+'][nn]['loc'] = self.mp.latlon_to_xyz(latlon,radius=6.371e6)
                    _stationdicts['ngEHT+'][nn]['name'] = nn
                    if (np.abs(latlon[0])>=65.0) :
                        _stationdicts['ngEHT+'][nn]['cost_factors'] = np.array([7.62, 0.1288])
                    _statdict = _stationdicts['ngEHT+']
                    self.new_station_name_list_used.append(nn)
                    self.new_station_name_list_avail.remove(nn)
                    self.add_station_btn.text = 'Add'
                    self.add_station_btn.color = (1,1,1,1)
                    self.add_station_btn.background_color = (0,0,0,0.25)
                    self.update(_datadict,_statdict)
                    self.menu_id.refresh()
                    
        
    def del_station(self,widget) :
        global _statdict, _datadict
        if (_array_index==0) :
            if (len(self.new_station_name_list_used)>0) :
                if (self.editing_mode_del==False) :
                    self.editing_mode_del = True
                    self.editing_mode_add = False
                    self.cursor_on()
                    self.del_station_btn.text = '-??'
                    self.del_station_btn.color = (1,0,0,1)
                    self.del_station_btn.background_color = (1,0,0,0.75)
                    self.add_station_btn.text = 'Add'
                    self.add_station_btn.color = (1,1,1,1)
                    self.add_station_btn.background_color = (0,0,0,0.25)
                else :
                    self.editing_mode_del = False
                    self.cursor_off()
                    if (self.snap_source in self.new_station_name_list_used) :
                        del _stationdicts['ngEHT+'][self.snap_source]
                        self.new_station_name_list_used.remove(self.snap_source)
                        self.new_station_name_list_avail.append(self.snap_source)
                        self.new_station_name_list_avail.sort()
                        _statdict = _stationdicts['ngEHT+']
                    self.del_station_btn.text = 'Del'
                    self.del_station_btn.color = (1,1,1,1)
                    self.del_station_btn.background_color = (0,0,0,0.25)

                    self.update(_datadict,_statdict)
                    self.menu_id.refresh()
            
    def update(self,datadict,statdict) :
        global _datadict, _statdict
        self.mp.update(datadict,statdict)
        self.bmc.plot_stations(self.mp.statdict,self.mp.lldict,self.mp.gcdict,self.mp.rect)
        if __main_debug__ :
            print("MenuedBaselineMapPlot_kivygraph.update:",self.sdict.keys(),self.size)
            print("         :",_statdict.keys(),self.size)
            print("         :",statdict.keys(),self.size)

        if (_array_index==0) :
            self.add_stn_buttons()
        else :
            self.remove_stn_buttons()
            if (self.editing_mode_add or self.editing_mode_del) :
                self.editing_mode_add = False
                self.editing_mode_del = False
                self.plot_id.cursor_off()

            
    def replot(self) :
        global _datadict, _statdict
        self.ddict = _datadict
        self.sdict = _statdict
        self.mp.replot(self.ddict,self.sdict)
        self.bmc.plot_stations(self.sdict,self.mp.lldict,self.mp.gcdict,self.mp.rect)
        if __main_debug__ :
            print("MenuedBaselineMapPlot_kivygraph.replot:",self.sdict.keys(),self.size)
            print("         :",_statdict.keys(),self.size)

    def set_start_time(self,val) :
        self.time_range[1] = self.time_range[1]-self.time_range[0]+val
        self.time_range[0] = val
        
    def set_obs_time(self,val) :
        self.time_range[1] = self.time_range[0] + val

    def set_ngeht_diameter(self,val) :
        global _ngeht_diameter
        self.ngeht_diameter = val
        _ngeht_diameter = self.ngeht_diameter

    def set_snr_cut(self,val) :
        global _snr_cut
        self.snr_cut = val
        if (val is None) :
            self.snr_cut = 0
        _snr_cut = self.snr_cut

    def freeze_plot(self) :
        self.plot_froze = True
        self.mp.plot_frozen = True

    def unfreeze_plot(self) :
        self.plot_froze = False
        self.mp.plot_frozen = False

    def on_touch_move(self,touch) :
        if (not self.plot_frozen) :
            self.pixel_offset = ( self.pixel_offset[0] + touch.dpos[0], self.pixel_offset[1] + touch.dpos[1] )
        self.mp.on_touch_move(touch)
        self.bmc.plot_stations(self.mp.statdict,self.mp.lldict,self.mp.gcdict,self.mp.rect)
        if __main_debug__ :
            print("MenuedBaselineMapPlot_kivygraph.on_touch_move(): replotting")

    def on_touch_down(self,touch) :
        self.mp.on_touch_down(touch)
        if (touch.is_double_tap) :
            self.bmc.plot_stations(self.mp.statdict,self.mp.lldict,self.mp.gcdict,self.mp.rect)
        if (touch.pos[1]<self.pos[1]+self.height and  touch.is_touch) :
            if (self.editing_mode_add or self.editing_mode_del) :
                self.snap_source = None
                for s in self.mp.statdict.keys() :
                    xpx_src,ypx_src = self.bmc.coords_to_px(self.mp.lldict[s][0],self.mp.lldict[s][1],self.mp.rect)
                    dxpx = (touch.pos[0] - xpx_src + 0.5*self.mp.rect.size[0])%self.mp.rect.size[0] - 0.5*self.mp.rect.size[0]
                    dypx = (touch.pos[1] - ypx_src)
                    if ( dxpx**2 + dypx**2 <= dp(15)**2 ) :
                        self.snap_source = s
                if (self.snap_source is None) :
                    self.bmc.cursor_lat,self.bmc.cursor_lon = self.bmc.px_to_coords(touch.pos[0],touch.pos[1],self.mp.rect)
                    self.bmc.plot_stations(self.mp.statdict,self.mp.lldict,self.mp.gcdict,self.mp.rect)
                else :
                    self.bmc.cursor_lat,self.bmc.cursor_lon = self.mp.lldict[self.snap_source]
                    self.bmc.plot_stations(self.mp.statdict,self.mp.lldict,self.mp.gcdict,self.mp.rect)
                    if (self.del_station_btn.text!='Del') : # Looking to delete
                        if (self.snap_source in self.new_station_name_list_used) :
                            self.del_station_btn.text = '-'+self.snap_source # Set name
                        else :
                            self.del_station_btn.text = '-??' # Unset name

                
        if __main_debug__ :
            print("MenuedBaselineMapPlot_kivygraph.on_touch_down(): replotting",self.size,self.mp.rect.size)
            
    def zoom_in(self) :
        self.mp.zoom_in()
        self.bmc.plot_stations(self.mp.statdict,self.mp.lldict,self.mp.gcdict,self.mp.rect)
        if __main_debug__ :
            print("MenuedBaselineMapPlot_kivygraph.zoom_in(): replotting")

    def zoom_out(self) :
        self.mp.zoom_out()
        self.bmc.plot_stations(self.mp.statdict,self.mp.lldict,self.mp.gcdict,self.mp.rect)
        if __main_debug__ :
            print("MenuedBaselineMapPlot_kivygraph.zoom_out(): replotting")

    def resize(self,widget,newsize) :
        self.mp.resize(widget,newsize)
        # print("MBLMP_kg.resize(): after mp.resize --",self.mp.rect.size,self.mp.rect.pos)
        self.bmc.plot_stations(self.mp.statdict,self.mp.lldict,self.mp.gcdict,self.mp.rect)
        # Hack to fix the plot resize on initialization
        # if (self.mp.rect.size[0]==0 or self.mp.rect.size[1]==0) :
        #     Clock.schedule_once(lambda x : self.replot(), 0.1)
        Clock.schedule_once(lambda x : self.bmc.plot_stations(self.mp.statdict,self.mp.lldict,self.mp.gcdict,self.mp.rect), 0.1)
        
        if __main_debug__ :
            print("MenuedBaselineMapPlot_kivygraph.resize(): replotting with",newsize,self.size,self.mp.rect.size)
            # Clock.schedule_once(self.delayed_report,0.1)
            
    # def delayed_report(self,dt) :
    #     print("MenuedBaselineMapPlot_kivygraph.delayed_report(): replotting with",self.size,self.mp.rect.size)

    def cursor_on(self) :
        self.bmc.cursor_on(self.mp.rect)
        self.bmc.plot_stations(self.mp.statdict,self.mp.lldict,self.mp.gcdict,self.mp.rect)

    def cursor_off(self) :
        lat,lon = self.bmc.cursor_off(self.mp.rect)
        self.bmc.plot_stations(self.mp.statdict,self.mp.lldict,self.mp.gcdict,self.mp.rect)
        return lat,lon

    
        
class DynamicBoxLayout(BoxLayout):

    is_open = BooleanProperty(False)

    opened_height = NumericProperty(None)
    closed_height = NumericProperty(None)

    expand_time = NumericProperty(0.5)
    fps = NumericProperty(30)

    tab_width = NumericProperty(1)
    tab_pos_x = NumericProperty(0)
    
    def __init__(self,**kwargs) :
        if (__main_perf__) :
            print("--- %15.8g --- DynamicBoxLayout.__init__ start"%(time.perf_counter()))

        super().__init__(**kwargs)
        self.is_open = False
        self.animation = 'cubic'
        self.current_opened_height = self.opened_height

        if (__main_perf__) :
            print("--- %15.8g --- DynamicBoxLayout.__init__ done"%(time.perf_counter()))
        
    def expand_model(self, x) :
        if (self.animation=='cubic') :
            return 6.0*(0.25*x - 0.3333333333*(x-0.5)**3 - 0.041666666667)
    
        else :
            raise ValueError("expand model animation type not defined!")


    def set_open_height(self,dt) :
        self.height = self.closed_height + self.expand_model(dt/self.expand_time)*(self.opened_height-self.closed_height)

    def set_close_height(self,dt) :
        self.height = self.closed_height + self.expand_model(1.0-dt/self.expand_time)*(self.current_opened_height-self.closed_height)
        
    def open_box(self) :
        self.current_opened_height = copy.copy(self.opened_height)
        for dt in np.linspace(0,self.expand_time,int(self.expand_time*self.fps)) :
            Clock.schedule_once( self.set_open_height , dt)
        
    def close_box(self) :
        for dt in np.linspace(0,self.expand_time,int(self.expand_time*self.fps)) :
            Clock.schedule_once( self.set_close_height , dt)

    def set_is_open(self,val) :
        self.is_open = val
            
    def toggle_state(self) :
        if (self.is_open) :
            self.close_box()
            Clock.schedule_once(lambda x : self.set_is_open(False), self.expand_time)
        else :
            self.open_box()
            Clock.schedule_once(lambda x : self.set_is_open(True), self.expand_time)

    def reset_state(self) :
        if (self.is_open) :
            self.toggle_state()
            Clock.schedule_once( lambda dt: self.toggle_state(), self.expand_time)
            
        
class VariableToggleList(StackLayout) :

    
    rpp = ObjectProperty(None)
    nstations = NumericProperty(0)
    button_size = ListProperty((dp(50),dp(50)),size=2)

    bkgnd_color = [0,0,0,0]
    
    def __init__(self,**kwargs):
        if (__main_perf__) :
            print("--- %15.8g --- VariableToggleList.__init__ start"%(time.perf_counter()))

        super().__init__(**kwargs)

        self.sdict = _stationdicts[_array]
        _statdict = self.sdict
        
        self.nstations = len(self.sdict.keys())

        self.bs = []
        for s in np.sort(list(self.sdict.keys())) :
            b = ToggleButton(text=s,size_hint=(None,None),size=self.button_size,color=_on_color,background_color=self.bkgnd_color)
            b.bind(on_press=self.on_toggle)
            self.add_widget(b)
            self.bs.append(b)
            self.sdict[s]['on']=True

        if (__main_perf__) :
            print("--- %15.8g --- VariableToggleList.__init__ done"%(time.perf_counter()))
            
            
    def remake(self,sdict) :
        self.sdict = sdict
        self.nstations = len(self.sdict.keys())

        self.clear_widgets()
        self.bs = []
        for s in np.sort(list(self.sdict.keys())) :
            if (self.sdict[s]['on']) :
                b = ToggleButton(text=s,size_hint=(None,None),size=self.button_size,color=_on_color,background_color=self.bkgnd_color,state="normal")
            else :
                b = ToggleButton(text=s,size_hint=(None,None),size=self.button_size,color=_off_color,background_color=self.bkgnd_color,state="down")
            b.bind(on_press=self.on_toggle)
            self.add_widget(b)
            self.bs.append(b)
            #self.sdict[s]['on']=True

        if (__main_debug__) :
            print("VariableToggleList.remake: updating plot")
            
        self.rpp.update(_datadict,self.sdict)
        
    def refresh(self,sdict) :
        self.sdict = sdict        
        self.nstations = len(self.sdict.keys())

        self.clear_widgets()
        self.bs = []
        for s in np.sort(list(self.sdict.keys())) :
            if ( self.sdict[s]['on'] ) :
                b = ToggleButton(text=s,size_hint=(None,None),size=self.button_size,color=_on_color,background_color=self.bkgnd_color,state="normal")
            else :
                b = ToggleButton(text=s,size_hint=(None,None),size=self.button_size,color=_off_color,background_color=self.bkgnd_color,state="down")
            b.bind(on_press=self.on_toggle)
            self.add_widget(b)
            self.bs.append(b)

        if (__main_debug__) :
            print("VariableToggleList.refresh: updating plot")
            
        self.rpp.update(_datadict,self.sdict)
        
    def on_toggle(self,val) :

        if __main_debug__ :
            print("VariableToggleList.on_toggle:",self.rpp,self.sdict)

        for b in self.bs :
            if b.state == "normal" :
                b.color = _on_color
                self.sdict[b.text]['on']=True
            else :
                b.color = _off_color
                self.sdict[b.text]['on']=False
                
        self.rpp.update(_datadict,self.sdict)        

        if __main_debug__ :
            print("                            :",self.rpp,self.sdict)

        
    def turn_all_stations_on(self) :
        for b in self.bs:
            b.color = _on_color
            b.state = 'normal'
            self.sdict[b.text]['on']=True

        self.rpp.update(_datadict,self.sdict)        
            
        
    def turn_all_stations_off(self) :
        for b in self.bs:
            b.color = _off_color
            b.state = 'down'
            self.sdict[b.text]['on']=False

        self.rpp.update(_datadict,self.sdict)        
            
        
        
class Abbrv_StationMenu(DynamicBoxLayout) :

    _array = list(_stationdicts.keys())[_array_index]
    array_name = StringProperty(_array)

    rpp = ObjectProperty(None)
    menu_id = ObjectProperty(None)
    submenu_id = ObjectProperty(None)
    
    array_list = list(_stationdicts.keys())

    def __init__(self,**kwargs) :
        super().__init__(**kwargs)
    
    def cycle_array_backward(self) :
        global _array_index
        _array_index = (_array_index-1+len(_stationdicts.keys()))%len(_stationdicts.keys())
        self.array_name = list(_stationdicts.keys())[_array_index]
        self.submenu_id.remake(_stationdicts[self.array_name])
        self.reset_state()

    def cycle_array_forward(self) :
        global _array_index
        _array_index = (_array_index+1)%len(_stationdicts.keys())
        self.array_name = list(_stationdicts.keys())[_array_index]
        self.submenu_id.remake(_stationdicts[self.array_name])
        self.reset_state()

    def select_array(self,array_index) :

        if __main_debug__ :
            print("StationMenu.select_array:",self.rpp,array_index)
        
        global _array_index,_statdict
        _array_index = array_index
        self.array_name = list(_stationdicts.keys())[_array_index]
        _statdict = _stationdicts[self.array_name]
        self.submenu_id.remake(_stationdicts[self.array_name])
        self.reset_state()

        if __main_debug__ :
            print("                        :",self.rpp,array_index)
        

    def refresh(self) :

        if __main_debug__ :
            print("StationMenu.refresh",self.rpp)
        
        self.array_name = list(_stationdicts.keys())[_array_index]
        self.submenu_id.refresh(_stationdicts[self.array_name])
        self.reset_state()

        
class StationMenu(DynamicBoxLayout) :

    _array = list(_stationdicts.keys())[_array_index]
    array_name = StringProperty(_array)

    rpp = ObjectProperty(None)
    menu_id = ObjectProperty(None)
    submenu_id = ObjectProperty(None)
    ddm_id = ObjectProperty(None)
    
    array_list = list(_stationdicts.keys())

    def __init__(self,**kwargs) :
        super().__init__(**kwargs)
    
    def cycle_array_backward(self) :
        global _array_index
        _array_index = (_array_index-1+len(_stationdicts.keys()))%len(_stationdicts.keys())
        self.array_name = list(_stationdicts.keys())[_array_index]
        self.submenu_id.remake(_stationdicts[self.array_name])
        self.reset_state()

    def cycle_array_forward(self) :
        global _array_index
        _array_index = (_array_index+1)%len(_stationdicts.keys())
        self.array_name = list(_stationdicts.keys())[_array_index]
        self.submenu_id.remake(_stationdicts[self.array_name])
        self.reset_state()

    def select_array(self,array_index) :

        if __main_debug__ :
            print("StationMenu.select_array:",self.rpp,array_index)
        
        global _array_index,_statdict
        _array_index = array_index
        self.array_name = list(_stationdicts.keys())[_array_index]
        _statdict = _stationdicts[self.array_name]
        self.submenu_id.remake(_stationdicts[self.array_name])
        self.reset_state()

        if __main_debug__ :
            print("                        :",self.rpp,array_index)
        

    def refresh(self) :

        if __main_debug__ :
            print("StationMenu.refresh",self.rpp)
        
        self.array_name = list(_stationdicts.keys())[_array_index]
        self.submenu_id.refresh(_stationdicts[self.array_name])
        self.reset_state()
        

class SMESpinnerOption(SpinnerOption):

    def __init__(self, **kwargs):
        if (__main_perf__) :
            print("--- %15.8g --- SMESpinnerOption.__init__ start"%(time.perf_counter()))
        super(SMESpinnerOption,self).__init__(**kwargs)
        self.background_normal = ''
        #self.background_down = ''
        # self.background_color = [0.14,0.14,0.14, 0.75]    # blue colour
        self.background_color = [0.77,0.55,0.17,0.7]    # blue colour        
        self.color = [1, 1, 1, 1]
        self.height = dp(50)
        if (__main_perf__) :
            print("--- %15.8g --- SMESpinnerOption.__init__ done"%(time.perf_counter()))

class Abbrv_SMESpinner(Spinner):

    sme_id = ObjectProperty(None)
    
    def __init__(self, **kwargs):
        if (__main_perf__) :
            print("--- %15.8g --- Abbrv_SMESpinner.__init__ start"%(time.perf_counter()))

        super(Abbrv_SMESpinner,self).__init__(**kwargs)

        self.option_cls = SMESpinnerOption

        self.array_index_dict = {}
        for i,a in enumerate(list(_stationdicts.keys())) :
            self.array_index_dict[a] = i

        self.values = list(_stationdicts.keys())

        self.text = self.values[0]

        if (__main_perf__) :
            print("--- %15.8g --- Abbrv_SMESpinner.__init__ done"%(time.perf_counter()))
        
            
    def on_selection(self,text) :
        
        if __main_debug__ :
            print("SMESpinner.on_selection:",self.text,text)
            
        self.sme_id.select_array(self.array_index_dict[text])
        self.text = self.sme_id.array_name

        
class SMESpinner(Spinner):

    sme_id = ObjectProperty(None)
    ddm_id = ObjectProperty(None)
    
    def __init__(self, **kwargs):
        if (__main_perf__) :
            print("--- %15.8g --- SMESpinner.__init__ start"%(time.perf_counter()))
        super(SMESpinner,self).__init__(**kwargs)

        self.option_cls = SMESpinnerOption

        self.array_index_dict = {}
        for i,a in enumerate(list(_stationdicts.keys())) :
            self.array_index_dict[a] = i

        self.values = list(_stationdicts.keys())

        self.text = self.values[0]

        if (__main_perf__) :
            print("--- %15.8g --- SMESpinner.__init__ done"%(time.perf_counter()))

            
    def on_selection(self,text) :
        
        if __main_debug__ :
            print("SMESpinner.on_selection:",self.text,text)
            
        self.sme_id.select_array(self.array_index_dict[text])
        self.text = self.sme_id.array_name

        if (self.text in _existing_arrays) :
            # print("SME: Disabling slider",self.ddm_id.ddm_id)
            self.ddm_id.ddm_id.dms.disabled = True
        else :
            # print("SME: Enabling slider")
            self.ddm_id.ddm_id.dms.disabled = False


class ObsTimeMenu(DynamicBoxLayout) :
    plot = ObjectProperty(None)
    ots_id = ObjectProperty(None)
    def __init__(self,**kwargs) :
        super().__init__(**kwargs)

    def refresh(self) :

        if __main_debug__ :
            print("ObsTimeMenu.refresh",self.plot)
        
        self.ots_id.refresh()
        
    
class ObsTimeSliders(BoxLayout) :
    plot = ObjectProperty(None)
    top_menu = ObjectProperty(None)
    is_open = BooleanProperty(False)
    def __init__(self,**kwargs) :
        if (__main_perf__) :
            print("--- %15.8g --- ObsTimeSliders.__init__ start"%(time.perf_counter()))

        super().__init__(**kwargs)
        self.orientation = 'vertical'

        self.sts_box = BoxLayout()
        self.sts_box.orientation='horizontal'
        self.sts_label = Label(text='Obs Start:',color=(1,1,1,0.75),size_hint=(0.5,1))
        self.sts_box.add_widget(self.sts_label)
        
        self.sts = StartTimeMDSlider()
        self.sts.background_color=(0,0,0,0)
        self.sts.color=(1,1,1,0.75)
        self.sts.orientation='horizontal'
        self.sts.size_hint=(1,1)
        self.sts.step=0.5
        self.sts.bind(value=self.adjust_start_time)
        self.sts.bind(active=self.on_active)
        self.sts_box.add_widget(self.sts)
        
        self.sts_label2 = Label(text="%5.1f GST"%(self.sts.value),color=(1,1,1,0.75),size_hint=(0.5,1))
        self.sts_box.add_widget(self.sts_label2)

        
        self.ots_box = BoxLayout()
        self.ots_box.orientation='horizontal'
        self.ots_label = Label(text='Duration:',color=(1,1,1,0.75),size_hint=(0.5,1))
        self.ots_box.add_widget(self.ots_label)
        
        self.ots = ObsTimeMDSlider()
        self.ots.background_color=(0,0,0,0)
        self.ots.color=(1,1,1,0.75)
        self.ots.orientation='horizontal'
        self.ots.size_hint=(1,1)
        self.ots.step=0.5
        self.ots.bind(value=self.adjust_obs_time)
        self.ots.bind(active=self.on_active)
        self.ots_box.add_widget(self.ots)

        self.ots_label2 = Label(text="%5.1f h"%(self.ots.value),color=(1,1,1,0.75),size_hint=(0.5,1))
        self.ots_box.add_widget(self.ots_label2)

        if (__main_perf__) :
            print("--- %15.8g --- ObsTimeSliders.__init__ done"%(time.perf_counter()))
        
    
    def toggle_state(self) :
        if (self.is_open) :
            self.is_open = False
            self.clear_widgets()
            self.top_menu.toggle_state()
        else :
            self.is_open = True
            self.top_menu.toggle_state()
            Clock.schedule_once(lambda x: self.add_widget(self.sts_box), self.top_menu.expand_time)
            Clock.schedule_once(lambda x: self.add_widget(self.ots_box), self.top_menu.expand_time)

    def refresh(self) :
        self.sts.value = _time_range[0]
        self.ots.value = _time_range[1]-_time_range[0]

    def on_active(self,widget,active) :
        if active :
            self.plot.freeze_plot()
        else :
            self.plot.unfreeze_plot()
            
    def adjust_start_time(self,widget,val) :
        self.plot.set_start_time(val)
        self.sts_label2.text = "%5.1f GST"%(val)
        
    def adjust_obs_time(self,widget,val) :
        self.plot.set_obs_time(val)
        self.ots_label2.text = "%5.1f h"%(val)


class StartTimeMDSlider(FancyMDSlider):

    def __init__(self,**kwargs):
        super().__init__(**kwargs)

        self.min = 0
        self.max = 24
        self.value = 0
        self.show_off = False

    def hint_box_text(self,value) :
        return "%5.1f GST"%(value)

    def hint_box_size(self) :
        return (dp(60),dp(28))

    
class ObsTimeMDSlider(FancyMDSlider):
    
    def __init__(self,**kwargs):
        super().__init__(**kwargs)

        self.min = 0.5
        self.max = 24
        self.value = 24
        self.show_off = False

    def hint_box_text(self,value) :
        return "%5.1f h"%(value)

    def hint_box_size(self) :
        return (dp(50),dp(28))


class DiameterMenu(DynamicBoxLayout) :
    plot = ObjectProperty(None)
    ddm_id = ObjectProperty(None)
    def __init__(self,**kwargs) :
        super().__init__(**kwargs)

    def refresh(self) :

        if __main_debug__ :
            print("DiameterMenu.refresh",self.plot)
        
        self.ddm_id.refresh()
        
    
class DiameterSliders(BoxLayout) :
    plot = ObjectProperty(None)
    top_menu = ObjectProperty(None)
    is_open = BooleanProperty(False)
    def __init__(self,**kwargs) :
        if (__main_perf__) :
            print("--- %15.8g --- DiameterSliders.__init__ start"%(time.perf_counter()))

        super().__init__(**kwargs)
        self.orientation = 'vertical'

        self.dms_box = BoxLayout()
        self.dms_box.orientation='horizontal'
        self.dms_label = Label(text='Diameter:',color=(1,1,1,0.75),size_hint=(0.5,1))
        self.dms_box.add_widget(self.dms_label)
        
        self.dms = DiameterMDSlider()
        self.dms.background_color=(0,0,0,0)
        self.dms.color=(1,1,1,0.75)
        self.dms.orientation='horizontal'
        self.dms.size_hint=(0.8,1)
        self.dms.step=0.5
        self.dms.bind(value=self.adjust_diameter)
        self.dms.bind(active=self.on_active)
        self.dms_box.add_widget(self.dms)
        
        self.dms_label2 = Label(text="%5.1f m"%(self.dms.value),color=(1,1,1,0.75),size_hint=(0.5,1))
        self.dms_box.add_widget(self.dms_label2)
        
        self.sns_box = BoxLayout()
        self.sns_box.orientation='horizontal'
        # self.sns_label = Label(text='S/N Limit:',color=(1,1,1,0.75),size_hint=(0.5,1))
        self.sns_label = Label(text='Bandwidth:',color=(1,1,1,0.75),size_hint=(0.5,1))
        self.sns_box.add_widget(self.sns_label)
        
        self.sns = SNRMDSlider()
        self.sns.background_color=(0,0,0,0)
        self.sns.color=(1,1,1,0.75)
        self.sns.orientation='horizontal'
        self.sns.size_hint=(0.8,1)
        #self.sns.step=0.25
        self.sns.bind(value=self.adjust_snrcut)
        self.sns.bind(active=self.on_active)
        self.sns_box.add_widget(self.sns)
        
        #self.sns_label2 = Label(text="%5.1f"%(10**self.sns.value),color=(1,1,1,0.75),size_hint=(0.5,1))
        self.sns_label2 = Label(text="%g GHz"%(self.sns.bandwidth_value()),color=(1,1,1,0.75),size_hint=(0.5,1))
        
        self.sns_box.add_widget(self.sns_label2)

        if (__main_perf__) :
            print("--- %15.8g --- DiameterSliders.__init__ done"%(time.perf_counter()))
    
    def toggle_state(self) :
        if (self.is_open) :
            self.is_open = False
            self.clear_widgets()
            self.top_menu.toggle_state()
        else :
            self.is_open = True
            self.top_menu.toggle_state()
            Clock.schedule_once(lambda x: self.add_widget(self.dms_box), self.top_menu.expand_time)
            Clock.schedule_once(lambda x: self.add_widget(self.sns_box), self.top_menu.expand_time)

    def refresh(self) :
        global _ngeht_diameter_setting, _snr_cut_setting
        self.dms.value = _ngeht_diameter_setting
        self.sns.value = _snr_cut_setting

    def on_active(self,widget,active) :
        if active :
            self.plot.freeze_plot()
        else :
            self.plot.unfreeze_plot()
            
    def adjust_diameter(self,widget,val) :
        global _ngeht_diameter_setting
        _ngeht_diameter_setting = val
        self.plot.set_ngeht_diameter(val)
        self.dms_label2.text = "%5.1f m"%(val)
        
    def adjust_snrcut(self,widget,val) :
        global _snr_cut_setting
        _snr_cut_setting = val
        if self.sns._is_off :
            self.plot.set_snr_cut(None)
            self.sns_label2.text = "None"
        else :
            # self.plot.set_snr_cut(10**val)
            # self.sns_label2.text = "%5.1f"%(10**val)
            self.plot.set_snr_cut(self.sns.snr_value())
            self.sns_label2.text = "%g GHz"%(self.sns.bandwidth_value())
        

class DiameterMDSlider(FancyMDSlider):

    def __init__(self,**kwargs):
        super().__init__(**kwargs)

        self.min = 3
        self.max = 15
        self.value = 6
        self.show_off = False

    def hint_box_text(self,value) :
        return "%5.1f m"%(value)

    def hint_box_size(self) :
        return (dp(50),dp(28))

# # Set the SNR directly  
# class SNRMDSlider(FancyMDSlider):
    
#     def __init__(self,**kwargs):
#         super().__init__(**kwargs)

#         self.min = 0
#         self.max = 3
#         self.value = 2
#         self.show_off = True

#     def hint_box_text(self,value) :
#         return "%5.1f"%(10**value)

#     def hint_box_size(self) :
#         return (dp(50),dp(28))

# Use the bandwidth to set the SNR    
class SNRMDSlider(FancyMDSlider):

    
    def __init__(self,**kwargs):
        self.bandwidth_list = [4, 8, 12, 16]

        super().__init__(**kwargs)

        self.min = 0 # 4 GHz
        self.max = len(self.bandwidth_list)-1 # 16 GHz
        self.value = 1
        self.step = 1
        self.show_off = False

        
    def hint_box_text(self,value) :
        return "%g GHz"%(self.bandwidth_list[int(value)])

    def hint_box_size(self) :
        return (dp(50),dp(28))

    def bandwidth_value(self) :
        return self.bandwidth_list[int(self.value)]
    
    def snr_value(self) :
        return ( 7 * np.sqrt(8.0/self.bandwidth_list[int(self.value)]) )

            
        
            
class TargetSelectionMap(BoxLayout) :


    # smc = skymap_plot.StarMapCanvas()
    # ismp = skymap_plot.InteractiveSkyMapPlot()
    # tss = ObjectProperty(None)

    fps = NumericProperty(30)
    
    def __init__(self,**kwargs) :
        if (__main_perf__) :
            print("--- %15.8g --- TargetSelectionMap.__init__ start"%(time.perf_counter()))

        self.smc = skymap_plot.StarMapCanvas()
        self.ismp = skymap_plot.InteractiveSkyMapPlot()
            
        global _source_RA, source_Dec
        
        super().__init__(**kwargs)

        self.add_widget(self.ismp)
        self.add_widget(self.smc)


        self.tbox = BoxLayout(orientation='vertical',size_hint=(None,None),width=dp(150),height=sp(100)) #,dp(200))) #,pos=(dp(100),dp(100)))
        # self.tbox = BoxLayout(orientation='vertical',size_hint=(None,None),size=(dp(50),dp(90)))
        
        self.targets = {}        
        self.targets['Sgr A*']={'RA':self.RA_hr(17,45,40.049),'Dec':self.Dec_deg(-29,0,28.118)}
        self.targets['M87']={'RA':self.RA_hr(12,30,49.42338),'Dec':self.Dec_deg(12,23,28.0439)}
        self.targets['M31']={'RA':self.RA_hr(0,42,44.3),'Dec':self.Dec_deg(41,16,9)}
        self.targets['Cen A']={'RA':self.RA_hr(13,25,27.6),'Dec':self.Dec_deg(-43,1,9)}
        self.targets['OJ 287']={'RA':self.RA_hr(8,54,48.9),'Dec':self.Dec_deg(20,6,31)}
        self.targets['3C 279']={'RA':self.RA_hr(12,56,11.1),'Dec':self.Dec_deg(-5,47,22)}
        # self.targets['Mkn 421']={'RA':self.RA_hr(11,4,27.314),'Dec':self.Dec_deg(38,12,31.80)}
        # self.targets['BL Lac']={'RA':self.RA_hr(22,2,43.3),'Dec':self.Dec_deg(42,16,40)}
        # self.targets['M81']={'RA':self.RA_hr(9,55,33.2),'Dec':self.Dec_deg(69,3,55)}
        # self.targets['LMC']={'RA':self.RA_hr(5,23,34.5),'Dec':self.Dec_deg(-69,45,22)}
        # self.targets['SMC']={'RA':self.RA_hr(0,52,44.8),'Dec':self.Dec_deg(-72,49,43)}

        self.targets['--- Select ---']={'RA':None,'Dec':None}

        
        if (__main_debug__) :
            for s in self.targets.keys() :
                if (s!='--- Select ---') :
                    print("%10s %15.8g %15.8g"%(s,self.targets[s]['RA'],self.targets[s]['Dec']))
        
        self.tss = skymap_plot.TargetSelectionSpinner(self.targets)
        self.tss.size_hint = (1,1)
        self.tss.background_color = (1,1,1,0.1)
        self.tss.color = (1,0.75,0.25,1)
        self.tss.bind(text=self.select_target)
        self.tbox.add_widget(self.tss)
        self.ra_label = MDLabel(text=" RA: ",size_hint=(1,1))#,color=(1,1,1))
        self.dec_label = MDLabel(text="Dec: ",size_hint=(1,1))#,color=(1,1,1))
        self.tbox.add_widget(self.ra_label)
        self.tbox.add_widget(self.dec_label)

        self.add_widget(self.tbox)
        
        self.pixel_offset = (0,0)

        # Generate some default resizing behaviors
        self.bind(height=self.resize)
        self.bind(width=self.resize)

        self.animation_RA_start = 0
        self.animation_Dec_start = 0
        self.animation_total_time = 1.0
        self.animation_type = 'cubic'


        # Select a target
        self.select_target(self,list(self.targets.keys())[0])
        self.set_map_center(_source_RA,_source_Dec)

        
        if __main_debug__ :
            print("mp.__init__: finished")

        if (__main_perf__) :
            print("--- %15.8g --- TargetSelectionMap.__init__ done"%(time.perf_counter()))

            
    def select_target(self,widget,value) :
        if (__main_debug__) :
            print("Selecting target:",widget,value,self.tss.text)
        global _source_RA, _source_Dec
        if (self.tss.text!="--- Select ---") :
            # print("====== Setting to",self.tss.text)
            _source_RA = self.targets[self.tss.text]['RA']
            _source_Dec = self.targets[self.tss.text]['Dec']
            # print("====== RA,Dec",_source_RA,_source_Dec)
        self.ra_label.text = " RA: "+self.hr_to_str(_source_RA)
        self.dec_label.text = "Dec: "+self.deg_to_str(_source_Dec)
        # print("====== RA,Dec 2",_source_RA,_source_Dec)
        # print("====== RA,Dec lbls",self.ra_label.text,self.dec_label.text)
        self.smc.plot_targets(self.targets,self.ismp.rect,_source_RA,_source_Dec)
        if (self.tss.text!="--- Select ---") :
            self.animate_to_target(0.5)


    def set_target(self,widget,value) :
        if (__main_debug__) :
            print("Selecting target:",widget,value,self.tss.text)
        global _source_RA, _source_Dec
        if (self.tss.text!="--- Select ---") :
            # print("====== Setting to",self.tss.text)
            _source_RA = self.targets[self.tss.text]['RA']
            _source_Dec = self.targets[self.tss.text]['Dec']
            # print("====== RA,Dec",_source_RA,_source_Dec)
        self.ra_label.text = " RA: "+self.hr_to_str(_source_RA)
        self.dec_label.text = "Dec: "+self.deg_to_str(_source_Dec)
        # print("====== RA,Dec 2",_source_RA,_source_Dec)
        # print("====== RA,Dec lbls",self.ra_label.text,self.dec_label.text)
        self.smc.plot_targets(self.targets,self.ismp.rect,_source_RA,_source_Dec)
        self.set_map_center(_source_RA,_source_Dec)
        #self.animate_to_target(0.5)
        
        
    def RA_hr(self,hh,mm,ss) :
        return hh+mm/60.0+ss/3600.
        
    def Dec_deg(self,deg,arcmin,arcsec) :
        return (np.sign(deg)*(np.abs(deg)+arcmin/60.0+arcsec/3600.))

    def hr_to_str(self,RA) :
        hh = int(RA)
        mm = int((RA-hh)*60.0)
        ss = ((RA-hh)*60.0-mm)*60.0
        return ("%02ih %02im %02.0fs"%(hh,mm,ss))
        
    def deg_to_str(self,Dec) :
        if (Dec<0) :
            ns = '-'
        else :
            ns = '+'
        Dec = np.abs(Dec)
        dg = int(Dec)
        mm = int((Dec-dg)*60.0)
        ss = ((Dec-dg)*60.0-mm)*60.0
        return ("%1s%02i\u00B0 %02i\' %02.0f\""%(ns,dg,mm,ss))

            
    def update(self,datadict,statdict) :
        self.ismp.update()
        self.smc.plot_targets(self.targets,self.ismp.rect,_source_RA,_source_Dec)

    def replot(self) :
        self.ismp.replot()
        self.smc.plot_targets(self.targets,self.ismp.rect,_source_RA,_source_Dec)

    def on_touch_move(self,touch) :
        #if (not self.plot_frozen) :
        self.pixel_offset = ( self.pixel_offset[0] + touch.dpos[0], self.pixel_offset[1] + touch.dpos[1] )
        self.ismp.on_touch_move(touch)
        self.smc.plot_targets(self.targets,self.ismp.rect,_source_RA,_source_Dec)
        if __main_debug__ :
            print("TargetSelectionMap.on_touch_move(): replotting")

    def on_touch_down(self,touch) :

        global _source_RA, _source_Dec

        # print("touch coords:",self.smc.px_to_coords(touch.pos[0],touch.pos[1],self.ismp.rect))

        # Do the normal stuff for the map, whatever that is
        self.ismp.on_touch_down(touch)

        # Catch the map centering
        if (touch.is_double_tap) :
            self.set_map_center(_source_RA,_source_Dec)

        # Pass to the spinner menu to choose a source
        self.tss.on_touch_down(touch)

        # Make a selection/set the target
        if (touch.is_touch) :
            if (touch.pos[1]<self.pos[1]+self.height and self.tss.text=="--- Select ---") :

                snap_source = None
                for s in self.targets.keys() :
                    if (s!="--- Select ---") :
                        xpx_src,ypx_src = self.smc.coords_to_px(self.targets[s]['RA'],self.targets[s]['Dec'],self.ismp.rect)
                        dxpx = (touch.pos[0] - xpx_src + 0.5*self.ismp.rect.size[0])%self.ismp.rect.size[0] - 0.5*self.ismp.rect.size[0]
                        dypx = (touch.pos[1] - ypx_src)
                        if ( dxpx**2 + dypx**2 <= dp(15)**2 ) :
                            snap_source = s
                            
                if (snap_source is None) :
                    RA,Dec = self.smc.px_to_coords(touch.pos[0],touch.pos[1],self.ismp.rect)
                    _source_RA = RA
                    _source_Dec = Dec
                
                    self.ra_label.text = " RA: "+self.hr_to_str(_source_RA)
                    self.dec_label.text = "Dec: "+self.deg_to_str(_source_Dec)
                    self.smc.plot_targets(self.targets,self.ismp.rect,_source_RA,_source_Dec)
                else :
                    self.tss.text = snap_source
                    self.select_target(self,snap_source)
        
        
    def animate_to_target(self,total_time) :
        self.animation_RA_start, self.animation_Dec_start = self.ismp.get_coord_center()
        if __main_debug__ :
            print("TargetSelectionMap.animate_to_target: 1 --",self.animation_RA_start, self.animation_Dec_start)
        # Get closest branch to new RA
        self.animation_RA_start = (self.animation_RA_start-_source_RA + 12)%24 - 12 + _source_RA
        if __main_debug__ :
            print("TargetSelectionMap.animate_to_target: 2 --",self.animation_RA_start, self.animation_Dec_start)
        self.animation_total_time = total_time        
        for dt in np.linspace(0,total_time,int(total_time*self.fps)) :
            Clock.schedule_once( self.animate_map_center , dt)

    def animate_map_center(self,dt) :
        ds = self.animation_model(dt/self.animation_total_time)
        RA = ds*_source_RA + (1.0-ds)*self.animation_RA_start
        Dec = ds*_source_Dec + (1.0-ds)*self.animation_Dec_start
        self.set_map_center(RA,Dec)

    def animation_model(self, x) :
        if (self.animation_type=='cubic') :
            return 6.0*(0.25*x - 0.3333333333*(x-0.5)**3 - 0.041666666667)
    
        else :
            raise ValueError("animation model type not defined!")
        
    def set_map_center(self,RA,Dec) :
        if (self.size[0]==0 or self.size[1]==0) :
            return
        self.ismp.set_coord_center(RA,Dec)
        self.smc.plot_targets(self.targets,self.ismp.rect,_source_RA,_source_Dec)

    
        
    def zoom_in(self) :
        self.ismp.zoom_in()
        self.smc.plot_targets(self.targets,self.ismp.rect,_source_RA,_source_Dec)

    def zoom_out(self) :
        self.ismp.zoom_out()
        self.smc.plot_targets(self.targets,self.ismp.rect,_source_RA,_source_Dec)

    def resize(self,widget,newsize) :
        self.ismp.resize(widget,newsize)
        self.smc.plot_targets(self.targets,self.ismp.rect,_source_RA,_source_Dec)

        # Hack to fix the plot resize on initialization
        # if (self.mp.rect.size[0]==0 or self.mp.rect.size[1]==0) :
        #     Clock.schedule_once(lambda x : self.replot(), 0.1)
        # Clock.schedule_once(lambda x : self.smc.plot_targets(self.targets,self.ismp.rect,_source_RA,_source_Dec), 0.1)
        Clock.schedule_once(lambda x : self.set_target(self,self.tss.text), 0.1)


class Abbrv_DataSetSelectionPage(BoxLayout) :

    # path_info = StringProperty("")
    
    def __init__(self,**kwargs) :
        if (__main_perf__) :
            print("--- %15.8g --- Abbrv_DataSetSelectionPage.__init__ start"%(time.perf_counter()))

        super().__init__(**kwargs)
        
        self.orientation = "vertical"


        self.source_size = 500.0
        self.source_flux = 1.0
        self.observation_frequency = 230.


        
        self.ic = data.ImageCarousel()
        self.targets = [{'RA':None,'Dec':None}]
        self.ic.add_image([path.abspath(path.join(path.dirname(__file__),"source_images/quickstart_M87_230.png")),
                           path.abspath(path.join(path.dirname(__file__),"source_images/quickstart_M87_230.png")),
                           path.abspath(path.join(path.dirname(__file__),"source_images/quickstart_M87_345.png")),
                           path.abspath(path.join(path.dirname(__file__),"source_images/quickstart_M87_345.png")),
                           path.abspath(path.join(path.dirname(__file__),"source_images/quickstart_M87_345.png"))],
                          [path.abspath(path.join(path.dirname(__file__),"source_images/GRRT_IMAGE_data1400_freq230.npy")),
                           path.abspath(path.join(path.dirname(__file__),"source_images/GRRT_IMAGE_data1400_freq230.npy")),
                           path.abspath(path.join(path.dirname(__file__),"source_images/GRRT_IMAGE_data1400_freq345.npy")),
                           path.abspath(path.join(path.dirname(__file__),"source_images/GRRT_IMAGE_data1400_freq345.npy")),
                           path.abspath(path.join(path.dirname(__file__),"source_images/GRRT_IMAGE_data1400_freq345.npy"))],
                          "Simulated jet in Messier 87. (Credit: A. Chael)",
                          False)
        # M87
        self.targets.append({'RA':self.RA_hr(12,30,49.42338),'Dec':self.Dec_deg(12,23,28.0439)})
        
        self.ic.add_image([path.abspath(path.join(path.dirname(__file__),"source_images/quickstart_SGRA_230.png")),
                           path.abspath(path.join(path.dirname(__file__),"source_images/quickstart_SGRA_230.png")),
                           path.abspath(path.join(path.dirname(__file__),"source_images/quickstart_SGRA_345.png")),
                           path.abspath(path.join(path.dirname(__file__),"source_images/quickstart_SGRA_345.png")),
                           path.abspath(path.join(path.dirname(__file__),"source_images/quickstart_SGRA_345.png"))],
                          [path.abspath(path.join(path.dirname(__file__),"source_images/fromm230_scat.npy")),
                           path.abspath(path.join(path.dirname(__file__),"source_images/fromm230_scat.npy")),
                           path.abspath(path.join(path.dirname(__file__),"source_images/fromm345_scat.npy")),
                           path.abspath(path.join(path.dirname(__file__),"source_images/fromm345_scat.npy")),
                           path.abspath(path.join(path.dirname(__file__),"source_images/fromm345_scat.npy"))],
                          "Simulated accretion flow at the Galactic center! (Credit: C. Fromm)",
                          False)
        # Sgr A
        self.targets.append({'RA':self.RA_hr(17,45,40.049),'Dec':self.Dec_deg(-29,0,28.118)})

        # self.ic.add_image([path.abspath(path.join(path.dirname(__file__),"source_images/riaf_freq_8.6e+10_0003.png")),
        #                    path.abspath(path.join(path.dirname(__file__),"source_images/riaf_freq_2.3e+11_0003.png")),
        #                    path.abspath(path.join(path.dirname(__file__),"source_images/riaf_freq_3.45e+11_0003.png")),
        #                    path.abspath(path.join(path.dirname(__file__),"source_images/riaf_freq_4.5e+11_0003.png")),
        #                    path.abspath(path.join(path.dirname(__file__),"source_images/riaf_freq_6.9e+11_0003.png"))],
        #                   [path.abspath(path.join(path.dirname(__file__),"source_images/riaf_freq_8.6e+10_0003.npy")),
        #                    path.abspath(path.join(path.dirname(__file__),"source_images/riaf_freq_2.3e+11_0003.npy")),
        #                    path.abspath(path.join(path.dirname(__file__),"source_images/riaf_freq_3.45e+11_0003.npy")),
        #                    path.abspath(path.join(path.dirname(__file__),"source_images/riaf_freq_4.5e+11_0003.npy")),
        #                    path.abspath(path.join(path.dirname(__file__),"source_images/riaf_freq_6.9e+11_0003.npy"))],
        #                   "Simulated accretion disk viewed from 70 degrees. (Credit: P. Tiede)",
        #                   False)

        # self.ic.add_image([path.abspath(path.join(path.dirname(__file__),"source_images/riaf_freq_8.6e+10_0006.png")),
        #                    path.abspath(path.join(path.dirname(__file__),"source_images/riaf_freq_2.3e+11_0006.png")),
        #                    path.abspath(path.join(path.dirname(__file__),"source_images/riaf_freq_3.45e+11_0006.png")),
        #                    path.abspath(path.join(path.dirname(__file__),"source_images/riaf_freq_4.5e+11_0006.png")),
        #                    path.abspath(path.join(path.dirname(__file__),"source_images/riaf_freq_6.9e+11_0006.png"))],
        #                   [path.abspath(path.join(path.dirname(__file__),"source_images/riaf_freq_8.6e+10_0006.npy")),
        #                    path.abspath(path.join(path.dirname(__file__),"source_images/riaf_freq_2.3e+11_0006.npy")),
        #                    path.abspath(path.join(path.dirname(__file__),"source_images/riaf_freq_3.45e+11_0006.npy")),
        #                    path.abspath(path.join(path.dirname(__file__),"source_images/riaf_freq_4.5e+11_0006.npy")),
        #                    path.abspath(path.join(path.dirname(__file__),"source_images/riaf_freq_6.9e+11_0006.npy"))],
        #                   "Simulated accretion disk viewed from 50 degrees. (Credit: P. Tiede)",
        #                   False)        

        self.ic.add_image(path.abspath(path.join(path.dirname(__file__),"source_images/Einstein2.png")),
                          path.abspath(path.join(path.dirname(__file__),"source_images/Einstein2.png")),
                          "The face of gravity in Huchra's lens.",
                          True)
        # Location of the Einstein cross
        self.targets.append({'RA':self.RA_hr(22,40,30.3),'Dec':self.Dec_deg(3,21,31)})
                            
        self.ic.add_image(path.abspath(path.join(path.dirname(__file__),"source_images/toy_story_aliens.png")),
                          path.abspath(path.join(path.dirname(__file__),"source_images/toy_story_aliens.png")),
                          "First contact from the Andromeda Galaxy!",
                          True)
        # M31!
        self.targets.append({'RA':self.RA_hr(0,42,44.3),'Dec':self.Dec_deg(41,16,9)})

        self.add_widget(self.ic)

        # self.dss = data.DataSelectionSliders()
        # self.dss.size_hint = 1,0.5
        # self.dss.its.active=True
        # self.dss.its.disabled = True
        
        # self.add_widget(self.dss)

        self.argument_hash = None
        self.ic.index = 1

        global _source_RA,_source_Dec,_datadict
        if __generate_fast_start_data__ :
            print("Abbrv_DataSetSelectionPage: Generating fast start data")
            self.produce_selected_data_set()
            np.save("fast_start_data/Abbrv_DataSetSelectionPage.npy",[self.argument_hash,_source_RA,_source_Dec,_datadict])
        else :
            self.argument_hash,_source_RA,_source_Dec,_datadict = np.load("fast_start_data/Abbrv_DataSetSelectionPage.npy",allow_pickle=True)
            # self.produce_selected_data_set()
            if (__main_debug__) :
                print("Abbrv_DataSetSelectionPage: Reloaded fast start data")
                print("   hash:",self.argument_hash)        

        self.file_manager_obj = MDFileManager(
            select_path=self.select_path,
            exit_manager=self.exit_manager,
            preview=True,
            ext=['png','jpg','jpeg','gif']
        )
        self.file_manager_obj.md_bg_color = (0.25,0.25,0.25,1)

        self.ic.add_btn.bind(on_release=self.open_file_manager)

        self.box = BoxLayout(size_hint=(1,0.5))

        # Add the observation frequency slider
        self.ofs_box = BoxLayout()
        self.ofs_box.orientation='horizontal'
        # self.ofs_label = Label(text='Obs. Freq.:',color=(1,1,1,0.75),size_hint=(0.5,1))
        self.ofs_label = MDLabel(text='Obs. Freq.:',halign='center',size_hint=(0.5,1))
        self.ofs_box.add_widget(self.ofs_label)        
        self.ofs = data.ObsFrequencyMDSlider()
        self.ofs.observation_frequency_list = [86, 230, 345]
        self.ofs.max = 2
        self.ofs.value = 1
        self.ofs.background_color=(0,0,0,0)
        # self.ofs.color=(1,1,1,0.75)
        self.ofs.set_color=False
        self.ofs.orientation='horizontal'
        self.ofs.size_hint=(0.8,1)
        self.ofs.bind(value=self.adjust_observation_frequency) #
        self.ofs_box.add_widget(self.ofs)
        self.ofs_label2 = MDLabel(text="%3g GHz"%(self.ofs.observation_frequency()),halign='center',size_hint=(0.5,1))
        self.ofs_box.add_widget(self.ofs_label2)

        self.box.add_widget(self.ofs_box)
        self.add_widget(self.box)
        self.ofs.bind(value=self.ic.set_frequency)
        self.observation_frequency = self.ofs.observation_frequency()

        if (__main_perf__) :
            print("--- %15.8g --- Abbrv_DataSetSelectionPage.__init__ done"%(time.perf_counter()))
        
        
    def adjust_observation_frequency(self,widget,val) :
        self.observation_frequency = self.ofs.observation_frequency()
        self.ofs_label2.text = self.ofs.hint_box_text(0)
        if (__main_debug__) :
            print("DataSelectionSliders.adjust_observation_frequency:",self.observation_frequency,val,self.ofs_label2.text)
        
    def RA_hr(self,hh,mm,ss) :
        return hh+mm/60.0+ss/3600.
        
    def Dec_deg(self,deg,arcmin,arcsec) :
        return (np.sign(deg)*(np.abs(deg)+arcmin/60.0+arcsec/3600.))
        
    def select_path(self,path) :
        MainApp.get_running_app().save_path(plP(path).parent)
        self.ic.add_image(path,path,path,True)
        self.targets.append({'RA':self.RA_hr(17,45,40.049),'Dec':self.Dec_deg(-29,0,28.118)})
        self.exit_manager(0)
        
    def open_file_manager(self,widget) :
        topdir = MainApp.get_running_app().read_path()
        self.file_manager_obj.show(topdir)

    def exit_manager(self,value) :
        if (value==1) : # a valid file wasn't selected, return to screen
            self.ic.index = 0
        else :
            self.ic.index = -1 # Set to value just added
            
        self.file_manager_obj.close()

    def on_touch_move(self,touch) :
        self.ic.on_touch_move(touch)
        self.box.on_touch_move(touch)
        Clock.schedule_once(lambda x: self.on_selection(), self.ic.anim_move_duration+0.1)
        
    def on_selection(self) :
        if (__main_debug__) :
            print("Setting taper switch to active?",self.ic.taperable_list[self.ic.index])
        # self.dss.its.disabled = not self.ic.taperable_list[self.ic.index]
        if (__main_debug__) :
            print("Setting taper switch to active?",self.ic.taperable_list[self.ic.index])

    def selection_check(self) :
        if (self.ic.index==0) :
            if (__main_debug__) :
                print("Bad selection!  Setting to index 1.")
            self.ic.load_slide(self.ic.slides[1])
            return False
        return True

    def check_data_hash(self) :
        _source_RA = self.targets[self.ic.index]['RA']
        _source_Dec = self.targets[self.ic.index]['Dec']
        new_argument_hash = hashlib.md5(bytes(str(self.ic.selected_data_file())+str(_statdict_maximum) + str(self.observation_frequency) + str(_source_RA) + str(_source_Dec) + str(self.source_size) + str(self.source_flux) + str(self.ic.taperable_list[self.ic.index]),'utf-8')).hexdigest()
        if ( new_argument_hash == self.argument_hash ) :
            return False
        return True


    def produce_selected_data_set(self) :
        _source_RA = self.targets[self.ic.index]['RA']
        _source_Dec = self.targets[self.ic.index]['Dec']
        if (__main_debug__) :
            print("DSSP.produce_selected_data_set:",self.ic.selected_data_file(),self.observation_frequency,_source_RA,_source_Dec,self.source_size,self.source_flux)
        new_argument_hash = hashlib.md5(bytes(str(self.ic.selected_data_file())+str(_statdict_maximum) + str(self.observation_frequency) + str(_source_RA) + str(_source_Dec) + str(self.source_size) + str(self.source_flux) + str(self.ic.taperable_list[self.ic.index]),'utf-8')).hexdigest()
        if (__main_debug__) :
            print("New data md5 hash:",new_argument_hash)
            print("Old data md5 hash:",self.argument_hash)
        if ( new_argument_hash == self.argument_hash ) :
            return
        self.argument_hash = new_argument_hash
            
        global _datadict
        _datadict = data.generate_data_from_file( self.ic.selected_data_file(), \
                                                  _statdict_maximum, \
                                                  freq=self.observation_frequency, \
                                                  ra=_source_RA,dec=_source_Dec, \
                                                  scale=self.source_size, \
                                                  total_flux=self.source_flux, \
                                                  taper_image=self.ic.taperable_list[self.ic.index])
            

        
class DataSetSelectionPage(BoxLayout) :

    # path_info = StringProperty("")
    
    def __init__(self,**kwargs) :
        if (__main_perf__) :
            print("--- %15.8g --- DataSetSelectionPage.__init__ start"%(time.perf_counter()))
        super().__init__(**kwargs)
        
        self.orientation = "vertical"
        
        self.ic = data.ImageCarousel()

        self.ic.add_image([path.abspath(path.join(path.dirname(__file__),"source_images/M87_230.png")),
                           path.abspath(path.join(path.dirname(__file__),"source_images/M87_230.png")),
                           path.abspath(path.join(path.dirname(__file__),"source_images/M87_345.png")),
                           path.abspath(path.join(path.dirname(__file__),"source_images/M87_345.png")),
                           path.abspath(path.join(path.dirname(__file__),"source_images/M87_345.png"))],
                          [path.abspath(path.join(path.dirname(__file__),"source_images/GRRT_IMAGE_data1400_freq230.npy")),
                           path.abspath(path.join(path.dirname(__file__),"source_images/GRRT_IMAGE_data1400_freq230.npy")),
                           path.abspath(path.join(path.dirname(__file__),"source_images/GRRT_IMAGE_data1400_freq345.npy")),
                           path.abspath(path.join(path.dirname(__file__),"source_images/GRRT_IMAGE_data1400_freq345.npy")),
                           path.abspath(path.join(path.dirname(__file__),"source_images/GRRT_IMAGE_data1400_freq345.npy"))],
                          "Simulated jet appropriate for M87. (Credit: A. Chael)",
                          False)
        # self.ic.add_image(path.abspath(path.join(path.dirname(__file__),"source_images/M87_230.png")),
        #                   path.abspath(path.join(path.dirname(__file__),"source_images/GRRT_IMAGE_data1400_freq230.npy")),
        #                   "Simulated jet at 230 GHz.",
        #                   False)
        # self.ic.add_image(path.abspath(path.join(path.dirname(__file__),"source_images/M87_345.png")),
        #                   path.abspath(path.join(path.dirname(__file__),"source_images/GRRT_IMAGE_data1400_freq345.npy")),
        #                   "Simulated jet at 345 GHz.",
        #                   False)
        self.ic.add_image([path.abspath(path.join(path.dirname(__file__),"source_images/SGRA_230.png")),
                           path.abspath(path.join(path.dirname(__file__),"source_images/SGRA_230.png")),
                           path.abspath(path.join(path.dirname(__file__),"source_images/SGRA_345.png")),
                           path.abspath(path.join(path.dirname(__file__),"source_images/SGRA_345.png")),
                           path.abspath(path.join(path.dirname(__file__),"source_images/SGRA_345.png"))],
                          [path.abspath(path.join(path.dirname(__file__),"source_images/fromm230_scat.npy")),
                           path.abspath(path.join(path.dirname(__file__),"source_images/fromm230_scat.npy")),
                           path.abspath(path.join(path.dirname(__file__),"source_images/fromm345_scat.npy")),
                           path.abspath(path.join(path.dirname(__file__),"source_images/fromm345_scat.npy")),
                           path.abspath(path.join(path.dirname(__file__),"source_images/fromm345_scat.npy"))],
                          "Simulated accretion disk, scattered by the Galactic disk. (Credit: C. Fromm)",
                          False)
        # self.ic.add_image(path.abspath(path.join(path.dirname(__file__),"source_images/SGRA_230.png")),
        #                   path.abspath(path.join(path.dirname(__file__),"source_images/fromm230_scat.npy")),
        #                   "Simulated RIAF at 230 GHz.",
        #                   False)
        # self.ic.add_image(path.abspath(path.join(path.dirname(__file__),"source_images/SGRA_345.png")),
        #                   path.abspath(path.join(path.dirname(__file__),"source_images/fromm345_scat.npy")),
        #                   "Simulated RIAF at 345 GHz.",
        #                   False)
        self.ic.add_image([path.abspath(path.join(path.dirname(__file__),"source_images/riaf_freq_8.6e+10_0003.png")),
                           path.abspath(path.join(path.dirname(__file__),"source_images/riaf_freq_2.3e+11_0003.png")),
                           path.abspath(path.join(path.dirname(__file__),"source_images/riaf_freq_3.45e+11_0003.png")),
                           path.abspath(path.join(path.dirname(__file__),"source_images/riaf_freq_4.5e+11_0003.png")),
                           path.abspath(path.join(path.dirname(__file__),"source_images/riaf_freq_6.9e+11_0003.png"))],
                          [path.abspath(path.join(path.dirname(__file__),"source_images/riaf_freq_8.6e+10_0003.npy")),
                           path.abspath(path.join(path.dirname(__file__),"source_images/riaf_freq_2.3e+11_0003.npy")),
                           path.abspath(path.join(path.dirname(__file__),"source_images/riaf_freq_3.45e+11_0003.npy")),
                           path.abspath(path.join(path.dirname(__file__),"source_images/riaf_freq_4.5e+11_0003.npy")),
                           path.abspath(path.join(path.dirname(__file__),"source_images/riaf_freq_6.9e+11_0003.npy"))],
                          "Simulated accretion disk viewed from 70 degrees. (Credit: P. Tiede)",
                          False)
        self.ic.add_image([path.abspath(path.join(path.dirname(__file__),"source_images/riaf_freq_8.6e+10_0006.png")),
                           path.abspath(path.join(path.dirname(__file__),"source_images/riaf_freq_2.3e+11_0006.png")),
                           path.abspath(path.join(path.dirname(__file__),"source_images/riaf_freq_3.45e+11_0006.png")),
                           path.abspath(path.join(path.dirname(__file__),"source_images/riaf_freq_4.5e+11_0006.png")),
                           path.abspath(path.join(path.dirname(__file__),"source_images/riaf_freq_6.9e+11_0006.png"))],
                          [path.abspath(path.join(path.dirname(__file__),"source_images/riaf_freq_8.6e+10_0006.npy")),
                           path.abspath(path.join(path.dirname(__file__),"source_images/riaf_freq_2.3e+11_0006.npy")),
                           path.abspath(path.join(path.dirname(__file__),"source_images/riaf_freq_3.45e+11_0006.npy")),
                           path.abspath(path.join(path.dirname(__file__),"source_images/riaf_freq_4.5e+11_0006.npy")),
                           path.abspath(path.join(path.dirname(__file__),"source_images/riaf_freq_6.9e+11_0006.npy"))],
                          "Simulated accretion disk viewed from 50 degrees. (Credit: P. Tiede)",
                          False)        
        self.ic.add_image(path.abspath(path.join(path.dirname(__file__),"source_images/Einstein2.png")),
                          path.abspath(path.join(path.dirname(__file__),"source_images/Einstein2.png")),
                          "The face of gravity.",
                          True)
        self.ic.add_image(path.abspath(path.join(path.dirname(__file__),"source_images/toy_story_aliens.png")),
                          path.abspath(path.join(path.dirname(__file__),"source_images/toy_story_aliens.png")),
                          "First contact!",
                          True)
        # self.ic.add_image(path.abspath(path.join(path.dirname(__file__),"images/image_file_icon.png")),
        #                   None,
        #                   "Choose a file of your own!")

        self.add_widget(self.ic)

        self.dss = data.DataSelectionSliders()
        self.dss.size_hint = 1,0.5
        self.dss.its.active=True
        self.dss.its.disabled = True
        
        self.add_widget(self.dss)

        self.argument_hash = None
        self.ic.index = 1

        global _source_RA,_source_Dec,_datadict
        if __generate_fast_start_data__ :
            print("DataSetSelectionPage: Generating fast start data")
            self.produce_selected_data_set()
            np.save("fast_start_data/DataSetSelectionPage.npy",[self.argument_hash,_source_RA,_source_Dec,_datadict])
        else :
            self.argument_hash,_source_RA,_source_Dec,_datadict = np.load("fast_start_data/DataSetSelectionPage.npy",allow_pickle=True)
            # self.produce_selected_data_set()
            if (__main_debug__) :
                print("DataSetSelectionPage: Reloaded fast start data")
                print("   hash:",self.argument_hash)        

        self.file_manager_obj = MDFileManager(
            select_path=self.select_path,
            exit_manager=self.exit_manager,
            preview=True,
            ext=['png','jpg','jpeg','gif']
        )
        self.file_manager_obj.md_bg_color = (0.25,0.25,0.25,1)
        # self.file_manager_obj.toolbar.specific_text_color = (0.77,0.55,0.17,1)

        self.ic.add_btn.bind(on_release=self.open_file_manager)

        self.dss.ofs.bind(value=self.ic.set_frequency)

        if (__main_perf__) :
            print("--- %15.8g --- DataSetSelectionPage.__init__ done"%(time.perf_counter()))

        
    def select_path(self,path) :
        MainApp.get_running_app().save_path(plP(path).parent)
        self.ic.add_image(path,path,path,True)
        self.dss.its.disabled = False
        self.exit_manager(0)
        
    def open_file_manager(self,widget) :
        topdir = MainApp.get_running_app().read_path()
        self.file_manager_obj.show(topdir)

    def exit_manager(self,value) :
        if (value==1) : # a valid file wasn't selected, return to screen
            self.ic.index = 0
        else :
            self.ic.index = -1 # Set to value just added
            
        self.file_manager_obj.close()

    def on_touch_move(self,touch) :
        self.ic.on_touch_move(touch)
        self.dss.on_touch_move(touch)
        Clock.schedule_once(lambda x: self.on_selection(), self.ic.anim_move_duration+0.1)
        
    def on_selection(self) :
        if (__main_debug__) :
            print("Setting taper switch to active?",self.ic.taperable_list[self.ic.index])
        self.dss.its.disabled = not self.ic.taperable_list[self.ic.index]
        if (__main_debug__) :
            print("Setting taper switch to active?",self.ic.taperable_list[self.ic.index])

    def selection_check(self) :
        if (self.ic.index==0) :
            if (__main_debug__) :
                print("Bad selection!  Setting to index 1.")
            self.ic.load_slide(self.ic.slides[1])
            return False
        return True

    def check_data_hash(self) :
        new_argument_hash = hashlib.md5(bytes(str(self.ic.selected_data_file())+str(_statdict_maximum) + str(self.dss.observation_frequency_list()) + str(_source_RA) + str(_source_Dec) + str(self.dss.source_size) + str(self.dss.source_flux) + str(self.dss.its.active and not self.dss.its.disabled),'utf-8')).hexdigest()
        if ( new_argument_hash == self.argument_hash ) :
            return False
        return True
    
    def produce_selected_data_set(self) :
        if (__main_debug__) :
            print("DSSP.produce_selected_data_set:",self.ic.selected_data_file(),self.dss.observation_frequency_list(),_source_RA,_source_Dec,self.dss.source_size,self.dss.source_flux)

        new_argument_hash = hashlib.md5(bytes(str(self.ic.selected_data_file())+str(_statdict_maximum) + str(self.dss.observation_frequency_list()) + str(_source_RA) + str(_source_Dec) + str(self.dss.source_size) + str(self.dss.source_flux) + str(self.dss.its.active and not self.dss.its.disabled),'utf-8')).hexdigest()
        if (__main_debug__) :
            print("New data md5 hash:",new_argument_hash)
            print("Old data md5 hash:",self.argument_hash)
        if ( new_argument_hash == self.argument_hash ) :
            return
        self.argument_hash = new_argument_hash
        
        global _datadict
        _datadict = data.generate_data_from_file( self.ic.selected_data_file(), \
                                                  _statdict_maximum, \
                                                  # freq=self.dss.observation_frequency, \
                                                  freq=self.dss.observation_frequency_list(), \
                                                  ra=_source_RA,dec=_source_Dec, \
                                                  scale=self.dss.source_size, \
                                                  total_flux=self.dss.source_flux, \
                                                  taper_image=(self.dss.its.active and not self.dss.its.disabled))
            

class LogoBackground(FloatLayout) :

    background_color = ListProperty(None)
    highlight_color = ListProperty(None)
    logo_color = ListProperty(None)
    logo_size = NumericProperty(None)
    logo_offset = ListProperty(None,size=2)
    highlight_offset = ListProperty(None,size=2)
    
    def __init__(self,**kwargs) :
        if (__main_perf__) :
            print("--- %15.8g --- LogoBackground.__init__ start"%(time.perf_counter()))
        super().__init__(**kwargs)
        self.bind(height=self.resize)
        self.bind(width=self.resize)

        # Generate the circle details
        self.radius_list = np.array([1.0, 0.80, 0.69, 0.53, 0.41, 0.24])
        self.phi0_list = np.array([0, 90, 180, 240, 30, 180, 180])
        self.total_phi0_list = (self.phi0_list[1:]-self.phi0_list[:-1]+360.0)%360.0 + 360.0
        self.dx_list = np.zeros(len(self.radius_list))
        self.dy_list = np.zeros(len(self.radius_list))
        for j in range(1,len(self.radius_list)) :
            self.dx_list[j] = (self.radius_list[j]-self.radius_list[j-1]) * np.sin(self.phi0_list[j]*np.pi/180.0) + self.dx_list[j-1]
            self.dy_list[j] = (self.radius_list[j]-self.radius_list[j-1]) * np.cos(self.phi0_list[j]*np.pi/180.0) + self.dy_list[j-1]

        self.dx_list = -self.dx_list
        self.dy_list = -self.dy_list
            
        self.background_color = (0.25,0.25,0.25,1)
        self.highlight_color = (0.35,0.35,0.35,1)
        self.logo_color = (0.14,0.14,0.14,1)
        self.logo_offset = (75,45)
        self.logo_size = 75
        self.logo_thickness = dp(6)
        self.highlight_offset = (-0.2*dp(6),0.2*dp(6))

        if (__main_perf__) :
            print("--- %15.8g --- LogoBackground.__init__ done"%(time.perf_counter()))
        
    
    def redraw_background(self) :

        self.canvas.clear()
        
        with self.canvas :
            
            Color(self.background_color[0],self.background_color[1],self.background_color[2],self.background_color[3])
            Rectangle(size=self.size)
            
            Xc = self.logo_offset[0] + self.highlight_offset[0]
            Yc = self.logo_offset[1] + self.highlight_offset[1]
            Color(self.highlight_color[0],self.highlight_color[1],self.highlight_color[2],self.highlight_color[3])
            for j in range(len(self.radius_list)) :
                xc = self.dx_list[j]*self.logo_size + Xc
                yc = self.dy_list[j]*self.logo_size + Yc
                rc = self.radius_list[j]*self.logo_size
                Line(circle=(xc,yc,rc),close=True,width=self.logo_thickness)

            Xc = Xc - self.highlight_offset[0]
            Yc = Yc - self.highlight_offset[1]
            Color(self.logo_color[0],self.logo_color[1],self.logo_color[2],self.logo_color[3])
            for j in range(len(self.radius_list)) :
                xc = self.dx_list[j]*self.logo_size + Xc
                yc = self.dy_list[j]*self.logo_size + Yc
                rc = self.radius_list[j]*self.logo_size
                Line(circle=(xc,yc,rc),close=True,width=self.logo_thickness)
                

    def resize(self,widget,newsize) :
        self.redraw_background()

class SpecificationCategory(BoxLayout) :
    title = StringProperty("")
    padding = [dp(20),dp(0),dp(20),dp(20)]
    content_height = NumericProperty(0)
    
class SpecificationItem(BoxLayout) :
    name = StringProperty("")
    value = StringProperty("")
            
class SpecificationsPage(BoxLayout) :

    est_cost = StringProperty("$200M")
    est_capex = StringProperty("$200M")
    est_opex = StringProperty("$0.75M/yr")
    est_datex = StringProperty("$0.75M/yr")
    stations = NumericProperty(0)
    new_stations = NumericProperty(0)
    ngeht_stations = NumericProperty(0)
    bandwidth = NumericProperty(8)
    data_rate = NumericProperty(10)
    number_of_baselines_total = NumericProperty(0)
    number_of_baselines_in_timerange = NumericProperty(0)
    number_of_baselines_above_snrcut = NumericProperty(0)
    number_of_visibilities_total = NumericProperty(0)
    number_of_visibilities_in_timerange = NumericProperty(0)
    number_of_visibilities_above_snrcut = NumericProperty(0)

    est_baseline_sensitivity = StringProperty("0 mJy")
    est_point_source_sensitivity = StringProperty("0 mJy")
    est_angular_resolution = StringProperty("0 uas")
    est_field_of_view = StringProperty("0 mas")
    est_image_dynamic_range = StringProperty("0")
    est_snapshot_dynamic_range = StringProperty("0")
    
    ngeht_diameter = NumericProperty(_ngeht_diameter)
    time_range = ListProperty(_time_range,size=2)
    snr_cut = NumericProperty(_snr_cut)
    source_RA = StringProperty("--")
    source_Dec = StringProperty("--")


    
    def generate_specs(self) :
        self.get_station_counts()
        self.get_data_rate()
        self.get_data_statistics()
        self.get_array_parameters()
        #
        self.estimate_cost()
        #
        self.estimate_performance()
        
        
    def estimate_cost(self) :
        capex,opex = ngeht_array.cost_model(_statdict,_ngeht_diameter,opex_exclude=list(_stationdicts['EHT 2022'].keys()))
        tot = capex + opex*10
        self.est_cost = "$%.1fM"%(int(tot*10+0.5)/10.0)
        self.est_capex = "$%.1fM"%(int(capex*10+0.5)/10.0)
        self.est_opex = "$%.1fM/yr"%(int(opex*10.0+0.5)/10.0)
        self.est_datex = "TBD"
        # self.est_datex = "$1M/yr"
        
    def get_station_counts(self) :
        n = 0
        nnew = 0
        nngeht = 0
        for s in _statdict.keys() :
            # print("Station:",s)
            if (_statdict[s]['on']) :
                n += 1
                if (not s in _existing_station_list) :
                    nnew += 1
                    # print("-> new station?",s)
                    # if (not s in ['GB']) :
                    #     nngeht += 1
                    #     print("--> ngEHT station?",s)
        self.stations = n
        self.new_stations = nnew
        self.ngeht_stations = nngeht
        
    def get_data_rate(self) :
        # 2 pol * nyquist * 2 bit * n stations
        self.data_rate = 2 * 2*self.bandwidth*1e9 * 2 * self.stations / 1e12

    def get_data_statistics(self) :
        
        # Exclude stations not in array
        stations = list(np.unique(np.array(list(_statdict.keys()))))
        keep = np.array([ (_datadict['s1'][j] in stations) and (_datadict['s2'][j] in stations) for j in range(len(_datadict['s1'])) ])
        ddtmp = {}
        for key in ['u','v','V','s1','s2','t','err'] :
            ddtmp[key] = _datadict[key][keep]
        keep = np.array([ _statdict[ddtmp['s1'][j]]['on'] and _statdict[ddtmp['s2'][j]]['on'] for j in range(len(ddtmp['s1'])) ])
        for key in ['u','v','V','s1','s2','t','err'] :
            ddtmp[key] = ddtmp[key][keep]

        # Get the number of unique baselines
        self.number_of_baselines_total = 0
        #stations = list(np.unique(np.append(_datadict['s1'],_datadict['s2'])))
        for k,s1 in enumerate(stations) :
            for s2 in stations[(k+1):] :
                # print("Baseline count:",self.number_of_baselines_total,s1,s2,np.any((ddtmp['s1']==s1)*(ddtmp['s2']==s2)))
                if ( np.any((ddtmp['s1']==s1)*(ddtmp['s2']==s2)) ) :
                    self.number_of_baselines_total += 1

        self.number_of_visibilities_total = ddtmp['V'].size//2
                    
        # Keep baselines above SNR cut
        keep = (ddtmp['t']>=_time_range[0])*(ddtmp['t']<_time_range[1])
        ddtmp2 = {'u':np.array([]),'v':np.array([]),'V':np.array([]),'s1':np.array([]),'s2':np.array([]),'t':np.array([]),'err':np.array([])}
        for key in ['u','v','V','s1','s2','t','err'] :
            ddtmp2[key] = ddtmp[key][keep]

        # Get the number of unique baselines
        self.number_of_baselines_in_timerange = 0
        #stations = list(np.unique(np.append(_datadict['s1'],_datadict['s2'])))
        for k,s1 in enumerate(stations) :
            for s2 in stations[(k+1):] :
                # print("  time -- Baseline count:",self.number_of_baselines_in_timerange,s1,s2,np.any((ddtmp['s1']==s1)*(ddtmp['s2']==s2)))
                if ( np.any((ddtmp2['s1']==s1)*(ddtmp2['s2']==s2)) ) :
                    self.number_of_baselines_in_timerange += 1

        self.number_of_visibilities_in_timerange = ddtmp2['V'].size//2

        # Cut points with S/N less than the specified minimum value
        if ((_snr_cut is None) or (_snr_cut==0)) :
            self.number_of_baselines_above_snrcut = self.number_of_baselines_in_timerange
            self.number_of_visibilities_above_snrcut = self.number_of_visibilities_in_timerange
        else :
            # Get a list of error adjustments based on stations
            diameter_correction_factor = {}
            for s in stations :
                if (_statdict[s]['exists']) :
                    diameter_correction_factor[s] = 1.0
                else :
                    diameter_correction_factor[s] = _statdict[s]['diameter']/_ngeht_diameter
            keep = np.array([ np.abs(ddtmp2['V'][j])/(ddtmp2['err'][j].real * diameter_correction_factor[ddtmp2['s1'][j]] * diameter_correction_factor[ddtmp2['s2'][j]]) > _snr_cut for j in range(len(ddtmp2['s1'])) ])
            ddtmp = {'u':np.array([]),'v':np.array([]),'V':np.array([]),'s1':np.array([]),'s2':np.array([]),'t':np.array([]),'err':np.array([])}
            for key in ['u','v','V','s1','s2','t','err'] :
                ddtmp[key] = ddtmp2[key][keep]

                
            # Get the number of unique baselines
            self.number_of_baselines_above_snrcut = 0
            stations = list(np.unique(np.append(_datadict['s1'],_datadict['s2'])))
            for k,s1 in enumerate(stations) :
                for s2 in stations[(k+1):] :
                    # print("  snrcut -- Baseline count:",self.number_of_baselines_above_snrcut,s1,s2,np.any((ddtmp['s1']==s1)*(ddtmp['s2']==s2)))
                    if ( np.any((ddtmp['s1']==s1)*(ddtmp['s2']==s2)) ) :
                        self.number_of_baselines_above_snrcut += 1

            self.number_of_visibilities_above_snrcut = ddtmp['V'].size//2
                
    def get_array_parameters(self) :
        self.ngeht_diameter = _ngeht_diameter
        self.time_range = _time_range
        self.snr_cut = float(_snr_cut)
        self.source_RA = self.hr_to_str(_source_RA)
        self.source_Dec = self.deg_to_str(_source_Dec)


    def sig_fig(self,val,n) :
        mag = 10**(int(np.log10(val)-n+1))
        return int(val/mag+0.5)*mag
        

    def estimate_performance(self) :

        # Uses data that has been chosen.

        # Cut points with S/N less than the specified minimum value
        stations = list(np.unique(np.array(list(_statdict.keys()))))
        if (not _snr_cut is None) and _snr_cut>0 :
            # Get a list of error adjustments based on stations
            diameter_correction_factor = {}
            for s in stations :
                if (_statdict[s]['exists']) :
                    diameter_correction_factor[s] = 1.0
                else :
                    diameter_correction_factor[s] = _statdict[s]['diameter']/_ngeht_diameter
        else :
            diameter_correction_factor = {}
            for s in stations :
                diameter_correction_factor[s] = 1.0

                
        # Get the max sensitivities on various baselines
        on_station_list = []
        ngEHT_station_list = []
        for s in _statdict.keys() :
            if (_statdict[s]['on']) :
                on_station_list.append(s)
                if (_statdict[s]['exists']==False) :
                    ngEHT_station_list.append(s)
        err_list_all = []
        err_list_ngeht = []
        for j in range(len(_datadict['s1'])) :
            if ( (_datadict['s1'][j] in on_station_list) and (_datadict['s2'][j] in on_station_list) ) :
                err_list_all.append( _datadict['err'][j].real * diameter_correction_factor[_datadict['s1'][j]] * diameter_correction_factor[_datadict['s2'][j]] )
            if ( (_datadict['s1'][j] in on_station_list) and (_datadict['s2'][j] in ngEHT_station_list) ) :
                err_list_ngeht.append( _datadict['err'][j].real * diameter_correction_factor[_datadict['s1'][j]] * diameter_correction_factor[_datadict['s2'][j]] )
        err_list_all = np.array(err_list_all)
        err_list_ngeht = np.array(err_list_ngeht)

        # Get the sensitivity from the most sensitive element of the current arrary to an ngEHT station        
        if (len(err_list_ngeht)==0) :
            self.est_baseline_sensitivity = "N/A"
        else :
            err_anchor = np.min(err_list_ngeht)
            # print("err anchor:",err_anchor)
            baseline_sensitivity = 7 * np.real(err_anchor) * 1e3
            self.est_baseline_sensitivity = "%2g mJy"%(self.sig_fig(baseline_sensitivity,2))

        # Get the sensitivity between two most sensitive elements of the current array            
        if (len(err_list_all)==0) :
            self.est_point_source_sensitivity = "N/A"
        else :
            err_max = np.min(err_list_all)
            # print("err anchor:",err_max)
            point_source_sensitivity = 7 * np.real(err_max) * 1e3
            self.est_point_source_sensitivity = "%2g mJy"%(self.sig_fig(point_source_sensitivity,2))
            
        
        # # Get the sensitivity from the most sensitive element of the current arrary to an ngEHT station
        # on_station_list = []
        # on_station_sefd = []
        # for s in _statdict.keys() :
        #     if (_statdict[s]['on']) :
        #         on_station_list.append(s)
        #         on_station_sefd.append(_statdict[s]['sefd'][0] * diameter_correction_factor[s])
        # on_station_list = np.array(on_station_list)
        # on_station_sefd = np.array(on_station_sefd)
        # on_station_list = on_station_list[np.argsort(on_station_sefd)]
        # on_station_sefd = on_station_sefd[np.argsort(on_station_sefd)]

        # anchor_station = on_station_list[0]
        # prototype_station = 'BA'
        # print("Anchor station:",anchor_station)
        # if ( not prototype_station in _statdict.keys() ) : # not an ngEHT array
        #     self.est_baseline_sensitivity = "N/A"
        # else :
        #     err_anchor = _datadict['err'][(_datadict['s1']==anchor_station)*(_datadict['s2']==prototype_station)].real * diameter_correction_factor[anchor_station]*diameter_correction_factor[prototype_station]
        #     print("err anchor:",err_anchor)
        #     baseline_sensitivity = 7 * np.max(err_anchor) * 1e3
        #     self.est_baseline_sensitivity = "%2g mJy"%(self.sig_fig(baseline_sensitivity,2))

        # # Get the sensitivity between two most sensitive elements of the current array
        # err_max = _datadict['err'][(_datadict['s1']==anchor_station)*(_datadict['s2']==on_station_list[1])].real * diameter_correction_factor[anchor_station]*diameter_correction_factor[prototype_station] 
        # point_source_sensitivity = 7 * np.max(err_max) * 1e3
        # self.est_point_source_sensitivity = "%2g mJy"%(self.sig_fig(point_source_sensitivity,2))
        
        # Exclude stations not in current array
        keep = np.array([ (_datadict['s1'][j] in stations) and (_datadict['s2'][j] in stations) for j in range(len(_datadict['s1'])) ])
        ddtmp = {}
        for key in ['u','v','V','s1','s2','t','err'] :
            ddtmp[key] = _datadict[key][keep]
        keep = np.array([ _statdict[ddtmp['s1'][j]]['on'] and _statdict[ddtmp['s2'][j]]['on'] for j in range(len(ddtmp['s1'])) ])
        for key in ['u','v','V','s1','s2','t','err'] :
            ddtmp[key] = ddtmp[key][keep]
            
        # Cut points with S/N less than the specified minimum value
        if (not _snr_cut is None) and _snr_cut>0 :
            ddtmp2 = copy.deepcopy(ddtmp)
            
            # Baseline-by-baseline filtering
            # keep = np.array([ np.abs(ddtmp2['V'][j])/(ddtmp2['err'][j].real * diameter_correction_factor[ddtmp2['s1'][j]] * diameter_correction_factor[ddtmp2['s2'][j]]) > _snr_cut for j in range(len(ddtmp2['s1'])) ])

            # Ad hoc phasing
            keep = np.array([True]*len(ddtmp2['s1']))
            jtot = np.arange(ddtmp2['t'].size)
            for tscan in np.unique(ddtmp2['t']) :
                inscan = (ddtmp2['t']==tscan)
                s1_scan = ddtmp2['s1'][inscan]
                s2_scan = ddtmp2['s2'][inscan]
                snr_scan = np.array([ np.abs(ddtmp2['V'][inscan][j])/( ddtmp2['err'][inscan][j].real * diameter_correction_factor[s1_scan[j]] * diameter_correction_factor[s2_scan[j]] ) for j in range(len(s1_scan)) ])
                detection_station_list = []
                for ss in np.unique(np.append(s1_scan,s2_scan)) :
                    snr_scan_ss = np.append(snr_scan[s1_scan==ss],snr_scan[s2_scan==ss])
                    if np.any(snr_scan_ss > _snr_cut ) :
                        detection_station_list.append(ss)
                keep[jtot[inscan]] = np.array([ (s1_scan[k] in detection_station_list) and (s2_scan[k] in detection_station_list) for k in range(len(s1_scan)) ])

            ddtmp = {'u':np.array([]),'v':np.array([]),'V':np.array([]),'s1':np.array([]),'s2':np.array([]),'t':np.array([]),'err':np.array([])}
            for key in ['u','v','V','s1','s2','t','err'] :
                ddtmp[key] = ddtmp2[key][keep]


        # Get the angular resolution
        uvmax = np.sqrt(np.max( ddtmp['u']**2 + ddtmp['v']**2 ))*1e9
        angular_resolution = 1.0/uvmax * 180.*3600e6/np.pi

        # Get the fov (shortest non-intrasite baseline)
        ddtmp2 = {'u':np.array([]),'v':np.array([]),'V':np.array([]),'s1':np.array([]),'s2':np.array([]),'t':np.array([]),'err':np.array([])}
        keep = np.array([True]*ddtmp['V'].size)
        for baseline in [['AA','AP'],['SM','JC']] :
            # print("Removing baseline",baseline[0],baseline[1])
            isbaseline = (ddtmp['s1']==baseline[0])*(ddtmp['s2']==baseline[1]) + (ddtmp['s2']==baseline[0])*(ddtmp['s1']==baseline[1])
            keep = keep*(isbaseline==False)
            
        # for j in np.arange(ddtmp['V'].size) :
        #     print(ddtmp['s1'][j],ddtmp['s2'][j],keep[j])
            
        for key in ['u','v','V','s1','s2','t','err'] :
            ddtmp2[key] = ddtmp[key][keep]
        uvmin = np.sqrt(np.min( ddtmp2['u']**2 + ddtmp2['v']**2 )) * 1e9
        imin = np.argmin( ddtmp2['u']**2 + ddtmp2['v']**2 )
        field_of_view = 1.0/uvmin * 180.*3600e3/np.pi 

        # print("angular resolution:",angular_resolution)
        # print("field of view:",field_of_view,ddtmp2['s1'][imin],ddtmp2['s2'][imin])
        
        # self.est_angular_resolution =  "%0.1f uas"%(int(angular_resolution*10+0.5)/10.0)
        # self.est_field_of_view =  "%0.1f mas"%(int(field_of_view*10+0.5)/10.0)

        self.est_angular_resolution =  "%g \u03BCas"%(self.sig_fig(angular_resolution,1))

        if (field_of_view>=1) :
            self.est_field_of_view =  "%g mas"%(self.sig_fig(field_of_view,1))
        else :
            self.est_field_of_view =  "%g \u03BCas"%(self.sig_fig(field_of_view*1e3,1))

        
        ### Generate the image
        img = cheap_image.InteractiveImageReconstructionPlot()
        # Image dynamic range
        x,y,I = img.reconstruct_image(_datadict,_statdict,snr_cut=_snr_cut,ngeht_diameter=_ngeht_diameter)
        image_dynamic_range = img.estimate_dynamic_range(x,y,I)
        if (not I is None) :
            image_dynamic_range = img.estimate_dynamic_range(x,y,I)
            self.est_image_dynamic_range = "%g"%(self.sig_fig(image_dynamic_range,1))
        else :
            image_dynamic_range = np.nan
            self.est_image_dynamic_range = "N/A"
        # Snapshot dynamic range
        tscans = np.unique(ddtmp['t'])
        Nscans = []
        Iscans = []
        for ts in tscans :
            inscan = (ddtmp['t']==ts)
            uscan = ddtmp['u'][inscan]
            vscan = ddtmp['v'][inscan]
            Nscans.append(uscan.size)
            mu2 = np.mean(uscan**2)
            mv2 = np.mean(vscan**2)
            muv = np.mean(uscan*vscan)
            Iscans.append( 1.0 - np.sqrt( (mu2-mv2)**2 + 4.0*muv**2 )/(mu2+mv2) )
        Nscans = np.array(Nscans)
        Iscans = np.array(Iscans)
        Nscans_max = np.max(Nscans)
        tscans = tscans[Nscans==Nscans_max]
        Iscans = Iscans[Nscans==Nscans_max]
        Nscans = Nscans[Nscans==Nscans_max]
        tscan_max = tscans[np.argmax(Iscans)]

        if (np.max(Iscans)<0.1) :
            x,y,I = None,None,None
        else :
            x,y,I = img.reconstruct_image(_datadict,_statdict,time_range=[tscan_max-0.03,tscan_max+0.03],snr_cut=_snr_cut,ngeht_diameter=_ngeht_diameter)
        if (not I is None) :
            snapshot_dynamic_range = img.estimate_dynamic_range(x,y,I)
            self.est_snapshot_dynamic_range = "%g"%(self.sig_fig(snapshot_dynamic_range,1))
        else :
            snapshot_dynamic_range = np.nan
            self.est_snapshot_dynamic_range = "N/A"

        # print("image dynamic range:",image_dynamic_range,int(np.log10(image_dynamic_range)))
        # print("snapshot dynamic range:",snapshot_dynamic_range)

        # self.est_image_dynamic_range = "%g"%(int(image_dynamic_range/10**(int(np.log10(image_dynamic_range))))*10**(int(np.log10(image_dynamic_range))))
        # self.est_snapshot_dynamic_range = "%g"%(int(snapshot_dynamic_range/10**(int(np.log10(snapshot_dynamic_range))))*10**(int(np.log10(snapshot_dynamic_range))))

        #self.est_image_dynamic_range = "%g"%(self.sig_fig(image_dynamic_range,1))
        #self.est_snapshot_dynamic_range = "%g"%(self.sig_fig(snapshot_dynamic_range,1))
        
    def hr_to_str(self,RA) :
        hh = int(RA)
        mm = int((RA-hh)*60.0)
        ss = ((RA-hh)*60.0-mm)*60.0
        return ("%02ih %02im %02.0fs"%(hh,mm,ss))
        
    def deg_to_str(self,Dec) :
        if (Dec<0) :
            ns = '-'
        else :
            ns = '+'
        Dec = np.abs(Dec)
        dg = int(Dec)
        mm = int((Dec-dg)*60.0)
        ss = ((Dec-dg)*60.0-mm)*60.0
        return ("%1s%02i\u00B0 %02i\' %02.0f\""%(ns,dg,mm,ss))

        
        
class InteractiveReconstructionPlot(FloatLayout) :
    ddm_id = ObjectProperty(None)
    otm_id = ObjectProperty(None)
    menu_id = ObjectProperty(None)
    plot_id = ObjectProperty(None)

class Abbrv_InteractiveReconstructionPlot(FloatLayout) :
    menu_id = ObjectProperty(None)
    plot_id = ObjectProperty(None)
    
class InteractiveBaselinesPlot(FloatLayout) :
    ddm_id = ObjectProperty(None)
    otm_id = ObjectProperty(None)
    menu_id = ObjectProperty(None)
    plot_id = ObjectProperty(None)

class InteractiveMapsPlot(FloatLayout) :
    ddm_id = ObjectProperty(None)
    otm_id = ObjectProperty(None)
    menu_id = ObjectProperty(None)
    plot_id = ObjectProperty(None)

class Abbrv_InteractiveMapsPlot(FloatLayout) :
    menu_id = ObjectProperty(None)
    plot_id = ObjectProperty(None)

    
class ImageButton(CircularRippleBehavior, ButtonBehavior, Image):
    def __init__(self, **kwargs):
        self.ripple_scale = 0.85
        super().__init__(**kwargs)

    def delayed_switch_to_imaging(self,delay=0) :
        Clock.schedule_once(self.switch_to_imaging, delay)
        
    def switch_to_imaging(self,val):
        sm = ngEHTApp.get_running_app().root
        sm.transition = FadeTransition()
        # sm.current = "screen0"
        sm.current = "targets"
        sm.transition = SlideTransition()

    

# class LoadingScreen(Screen):
#     def __init__(self,**kwargs) :
#         super().__init__(**kwargs)


# class LoadingStartUp(object):

#     app = None
#     def __init__(self, app):
#         self.app = app
#         return

#     def loadButtonImages(self):
#         print("Loading screen stuff ...")
#         self.app.root.ids.lpw.clock_run(5)

#     def finish(self) :
#         self.app.root.ids.lpw.complete()
#         Clock.schedule_once( lambda x : self.switch(), 2 )
#         return
    
#     def switch(self) :
#         self.app.root.current = "main_app_screen"

class CustomSnackbar(BaseSnackbar):
    text = StringProperty(None)
    icon = StringProperty(None)
    text_color = ListProperty(None)
    font_size = NumericProperty("15sp")


# class MenuItem(OneLineIconListItem):
#     icon = StringProperty("cog")

    
class MainApp(MDApp):

    transition_delay = NumericProperty(0.0)

    app_mode = StringProperty('quickstart')
    theme_style = StringProperty("Dark")
    map_color = BooleanProperty(False)
    show_contours = BooleanProperty(True)

    # LoadingStartUp = None
            
    def build(self):
        if (__main_perf__) :
            print("--- %15.8g --- MainApp.build start"%(time.perf_counter()))
            
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.colors["Dark"]["Background"] = "404040"
        self.theme_cls.colors["Light"]["Background"] = "d0d0d0"
        self.theme_cls.primary_palette = "Orange"
        self.theme_cls.accent_palette = "Gray"
        Window.bind(on_keyboard=self.key_input)
        
        Loader.loading_image = "images/load_image.png"
        
        app = Builder.load_file("ngeht.kv")

        # Clock.schedule_once(lambda x: self.on_start_finish(), 0.5)
        
        if (__main_perf__) :
            print("--- %15.8g --- MainApp.build done"%(time.perf_counter()))

        # Set some defaults for the snackbar
        self.snackbar = CustomSnackbar(icon=path.abspath(path.join(path.dirname(__file__),"images/ngeht_medallion_gold_on_white.png")),
                                       text="",
                                       text_color=self.theme_cls.primary_color,
                                       snackbar_x="10dp",snackbar_y="10dp",
                                       size_hint_x=(Window.width-(dp(10)*2))/Window.width,
                                       font_size="20sp",
                                       # bg_color=(0,0,0,0.75),
                                       bg_color=(0.14,0.14,0.14,0.5),
                                       radius=[0,20,0,20])


        Clock.schedule_once(lambda x : self.read_setting('app_mode'),0.1)
        Clock.schedule_once(lambda x : self.read_setting('app_theme'),0.1)
        Clock.schedule_once(lambda x : self.read_setting('map_color'),0.1)
        Clock.schedule_once(lambda x : self.read_setting('contours'),0.1)
        

        # ####
        # # Create the options menu
        # menu_items = []
        # #menu_items.append({'viewclass':'ItemDrawer','text':"Settings",'icon':"cog",'height':dp(50),text_color:(1,0,0,1),"on_release": lambda x=f"Settings": self.menu_callback(x)})
        # menu_list = ["Splash Screen","Reconstructions","News","ngEHT","About"]
        # # menu_items = [{ 'viewclass':'MenuItem', 'icon':'cog', 'text':f"{menu_list[i]}", "height": dp(40), "on_release": lambda x=f"{menu_list[i]}": self.menu_callback(x), 'text_color':(1,1,1,1), 'theme_text_color':"Custom",} for i in range(len(menu_list)) ]
        # menu_items = [{ 'viewclass':'MenuItem', 'icon':'cog', 'text':f"{menu_list[i]}", "height": dp(50), "on_release": lambda x=f"{menu_list[i]}": self.menu_callback(x),} for i in range(len(menu_list)) ]
        # # menu_items = [{ 'viewclass':'OneLineIconListItem', 'icon':'cog', 'text':f"{menu_list[i]}", "height": dp(40), "on_release": lambda x=f"{menu_list[i]}": self.menu_callback(x), 'text_color':(1,1,1,1), 'theme_text_color':"Custom",} for i in range(len(menu_list)) ]
        # self.menu = MDDropdownMenu(items=menu_items,width_mult=4) #,background_color=(0.7,0.7,0.7,0.5))
        
        return app

    # def on_start(self) :
    #     print("Starting!!!")
    #     #self.sm_master.lpw.clock_run(5)
    #     # MainApp.get_running_app().root.ids.lpw.clock_run(10)
    #     self.LoadingStartUp = LoadingStartUp(self)
    #     Clock.schedule_once(lambda x : self.LoadingStartUp.loadButtonImages(),5)
    #     Clock.schedule_once(lambda x : self.LoadingStartUp.finish(),12.5)
            
    # def on_start_finish(self) :
    #     self.root.ids.sm_master.splash.lpw.complete()
    #     self.root.ids.sm_master.current = "main_app_screen"
        
        
    
    def set_theme(self,dark) :
        if (dark) :
            self.theme_cls.theme_style="Dark"
            self.theme_cls.accent_light_hue = '200'
            self.theme_cls.accent_dark_hue = '700'
        else :
            self.theme_cls.theme_style="Light"
            self.theme_cls.accent_light_hue = '200'
            self.theme_cls.accent_dark_hue = '400'

        root = MainApp.get_running_app().root.ids.logo_background.redraw_background()
        self.theme_style = self.theme_cls.theme_style
        self.save_setting('app_theme')


    def set_map_color(self,natural) :
        root = MainApp.get_running_app().root
        root.ids.qs_map.plot_id.mp.set_map_true_color(natural)
        root.ids.ex_map.plot_id.mp.set_map_true_color(natural)
        self.map_color = natural
        self.save_setting('map_color')
        
    def set_show_contours(self,show) :
        root = MainApp.get_running_app().root
        root.ids.ex_img.plot_id.show_contours = show
        self.show_contours = show
        self.save_setting('contours')
        
        
    # def callback(self,button) :
    #     self.menu.caller = button
    #     self.menu.open()

    # def menu_callback(self,text) :
    #     self.menu.dismiss()
    #     print("Menu text:",text)
        
    #     # if (text=="Splash Screen") :
    #     #     self.set_splash_screen()
    #     # elif (text=="Reconstructions") :
    #     #     self.set_target_screen()
    #     # elif (text=="News") :
    #     #     self.set_news_screen()
    #     # elif (text=="ngEHT") :
    #     #     import webbrowser
    #     #     webbrowser.open("http://www.ngeht.org/science")
    #     # elif (text=="About") :
    #     #     self.set_about_screen()
    #     # else :
    #     #     print("WTF BBQ!?!?!")        
    
    def twitter_follow(self) :
        import webbrowser
        webbrowser.open("http://www.twitter.com")
        print("Insert twitter follow link")
    
    def facebook_follow(self) :
        import webbrowser
        webbrowser.open("http://www.facebook.com")
        print("Insert facebook follow link")

    def instagram_follow(self) :
        import webbrowser
        webbrowser.open("http://www.instagram.com")
        print("Insert instagram follow link")

    def youtube_follow(self) :
        import webbrowser
        webbrowser.open("https://www.youtube.com/channel/UCJeDtgEqIM6DCS-4lDpMnLw/featured")
        print("Insert YouTube follow link")

    def website_link(self,page="") :
        import webbrowser
        webbrowser.open("http://www.ngeht.org/"+page)

    def null_func(self) :
        pass


    def key_input(self, window, key, scancode, codepoint, modifier):
        if key == 27:
            return True  # override the default behaviour
        else:           # the key now does nothing
            return False

    def set_quickstart_transition_delay(self):
        if (MainApp.get_running_app().root.ids.qs_data.selection_check()) :
            self.transition_delay = 0.5 # Close the tray and raise snackbars
        else :
            self.transition_delay = 1.5

    def quickstart_snackbar_checks(self,procs="all"):
        root = MainApp.get_running_app().root
        making_data = False
        making_image = False
        if (procs in ["data","all"]) :
            making_data = root.ids.qs_data.check_data_hash()
        if (procs in ["image","all"]) :
            making_image = root.ids.qs_img.plot_id.check_image_hash() or making_data
        msg = ""
        if (making_data and making_image) :
            msg = "Observing & imaging ..."
        elif (making_data) :
            msg = "Observing ..."
        elif (making_image) :
            msg = "Imaging ..."

        if (msg!="") :
            self.transition_delay = max(0.65,self.transition_delay)
            # self.snackbar.text="[color="+get_hex_from_color(self.theme_cls.primary_color)+"]"+msg+"[/color]"
            self.snackbar.text=msg
            self.snackbar.size_hint_x=(Window.width-(dp(10)*2))/Window.width
            self.snackbar.open()

    def transition_to_quickstart_source(self,qs_nav_drawer):
        root = MainApp.get_running_app().root
        root.ids.screen_manager.current = "quickstart_source"
        qs_nav_drawer.active_screen = "quickstart_source"
        self.snackbar.dismiss()
            
    def transition_to_quickstart_array(self,qs_nav_drawer):
        root = MainApp.get_running_app().root
        root.ids.screen_manager.current = "quickstart_array"
        qs_nav_drawer.active_screen = "quickstart_array"
        # root.ids.qs_data.produce_selected_data_set()
        root.ids.qs_map.menu_id.refresh()
        root.ids.qs_map.plot_id.replot()
        self.snackbar.dismiss()
        
    def transition_to_quickstart_image(self,qs_nav_drawer):
        root = MainApp.get_running_app().root
        root.ids.qs_data.produce_selected_data_set()
        root.ids.screen_manager.current = "quickstart_image"
        qs_nav_drawer.active_screen = "quickstart_image"
        root.ids.qs_img.menu_id.refresh()
        root.ids.qs_img.plot_id.replot()
        self.snackbar.dismiss()

        
    def set_expert_transition_delay(self):
        if (MainApp.get_running_app().root.ids.ex_data.selection_check()) :
            self.transition_delay = 0.35 # Close the tray and raise snackbars
        else :
            self.transition_delay = 1.5

    def expert_snackbar_checks(self,procs="all"):
        root = MainApp.get_running_app().root
        making_data = False
        making_image = False
        if (procs in ["data","all"]) :
            making_data = root.ids.ex_data.check_data_hash()
        if (procs in ["image","all"]) :
            making_image = root.ids.ex_img.plot_id.check_image_hash() or making_data
        msg = ""
        if (making_data and making_image) :
            msg = "Observing & imaging ..."
        elif (making_data) :
            msg = "Observing ..."
        elif (making_image) :
            msg = "Imaging ..."

        if (msg!="") :
            self.transition_delay = max(0.65,self.transition_delay)
            # self.snackbar.text="[color="+get_hex_from_color(self.theme_cls.primary_color)+"]"+msg+"[/color]"
            self.snackbar.text=msg
            self.snackbar.size_hint_x=(Window.width-(dp(10)*2))/Window.width
            self.snackbar.open()
        
    def transition_to_expert_target(self,qs_nav_drawer):
        root = MainApp.get_running_app().root
        root.ids.screen_manager.current = "expert_target"
        qs_nav_drawer.active_screen = "expert_target"
        self.snackbar.dismiss()

    def transition_to_expert_source(self,qs_nav_drawer):
        root = MainApp.get_running_app().root
        root.ids.screen_manager.current = "expert_source"
        qs_nav_drawer.active_screen = "expert_source"
        self.snackbar.dismiss()

    def transition_to_expert_array(self,ex_nav_drawer):
        root = MainApp.get_running_app().root
        root.ids.screen_manager.current = "expert_array"
        ex_nav_drawer.active_screen = "expert_array"
        root.ids.ex_map.ddm_id.refresh()
        root.ids.ex_map.otm_id.refresh()
        root.ids.ex_map.menu_id.refresh()
        root.ids.ex_map.plot_id.replot()
        self.snackbar.dismiss()
        
    def transition_to_expert_baselines(self,ex_nav_drawer):
        root = MainApp.get_running_app().root
        root.ids.ex_data.produce_selected_data_set()
        root.ids.screen_manager.current = "expert_baselines"
        ex_nav_drawer.active_screen = "expert_baselines"
        root.ids.ex_uv.ddm_id.refresh()
        root.ids.ex_uv.otm_id.refresh()
        root.ids.ex_uv.menu_id.refresh()
        root.ids.ex_uv.plot_id.replot()
        self.snackbar.dismiss()
        
    def transition_to_expert_image(self,ex_nav_drawer):
        root = MainApp.get_running_app().root
        root.ids.ex_data.produce_selected_data_set()
        root.ids.screen_manager.current = "expert_image"
        ex_nav_drawer.active_screen = "expert_image"
        root.ids.ex_img.ddm_id.refresh()
        root.ids.ex_img.otm_id.refresh()
        root.ids.ex_img.menu_id.refresh()
        root.ids.ex_img.plot_id.replot()
        self.snackbar.dismiss()

    def transition_to_expert_specs(self,ex_nav_drawer):
        root = MainApp.get_running_app().root
        root.ids.ex_data.produce_selected_data_set()
        root.ids.ex_specs.generate_specs()
        root.ids.screen_manager.current = "expert_specs"
        ex_nav_drawer.active_screen = "expert_specs"
        self.snackbar.dismiss()



    def transition_to_settings(self,nav_drawer):
        root = MainApp.get_running_app().root
        root.ids.screen_manager.current = "settings"
        nav_drawer.active_screen = "settings"
        self.snackbar.dismiss()

    def transition_to_about(self,nav_drawer):
        root = MainApp.get_running_app().root
        root.ids.screen_manager.current = "about"
        nav_drawer.active_screen = "about"
        self.snackbar.dismiss()

    def version(self) :
        return __version__

    def save_path(self,file_path) :
        try :
            with open(path.abspath(path.join(path.dirname(__file__),"settings/last_path.txt")),'w') as f :
                f.write(str(file_path))
        except:
            print("ERROR: Could not save path")

    def read_path(self) :
        try :
            with open(path.abspath(path.join(path.dirname(__file__),"settings/last_path.txt")),'r') as f :
                topdir = f.readline()
        except :
            topdir=""

        if (topdir=="") :
            home = str(plP.home())
            if (home!='/data') :
                topdir = home
            else :
                topdir = '/'

        if (__main_debug__) :
            print("Set",topdir)

        return topdir

    def save_setting_to_file(self,setting_file_name,setting_value) :
        try:
            with open(path.abspath(path.join(path.dirname(__file__),"settings/"+setting_file_name)),'w') as f :
                f.write(str(setting_value))
            if (__main_debug__) :
                print("Saved setting",setting_file_name,"as",setting_value)
        except:
            print("ERROR: Unable to save setting ...")

    def save_setting(self,setting_name) :
        if (setting_name=='app_mode') :
            self.save_setting_to_file("app_mode.txt",self.app_mode)
        elif (setting_name=='app_theme') : 
            self.save_setting_to_file("app_theme.txt",self.theme_cls.theme_style)
        elif (setting_name=='map_color') : 
            self.save_setting_to_file("map_color.txt",self.map_color)
        elif (setting_name=='contours') : 
            self.save_setting_to_file("contours.txt",self.show_contours)
        else :
            print("ERROR: Unrecognized setting",setting_name)

    def read_string_setting_from_file(self,setting_file_name,acceptable_values) :
            try: 
                with open(path.abspath(path.join(path.dirname(__file__),"settings/"+setting_file_name)),'r') as f :
                    value = str(f.readline())
            except :
                value = None
            if (__main_debug__) :
                print("Read string setting",setting_file_name,acceptable_values,value)
            if (not value in acceptable_values) :
                value = acceptable_values[0]
            return value

    def read_boolean_setting_from_file(self,setting_file_name,default_value) :
            try: 
                with open(path.abspath(path.join(path.dirname(__file__),"settings/"+setting_file_name)),'r') as f :
                    value = (f.readline()=="True")
            except :
                value = None
            if (__main_debug__) :
                print("Read bool setting %s [%s] %s"%(setting_file_name,str(default_value),str(value)))
            if (not value in [True,False]) :
                value = default_value
            return value

    def read_setting(self,setting_name) :
        if (setting_name=='app_mode') :
            app_mode = self.read_string_setting_from_file("app_mode.txt",["quickstart","expert"])
            self.get_running_app().root.ids.content_drawer.set_nav_drawer_list(app_mode=='expert')
        elif (setting_name=='app_theme') :
            theme = self.read_string_setting_from_file("app_theme.txt",["Dark","Light"])
            self.set_theme(theme=="Dark")
        elif (setting_name=='map_color') :
            map_color = self.read_boolean_setting_from_file("map_color.txt",False)
            self.set_map_color(map_color)
        elif (setting_name=='contours') :
            show_contours = self.read_boolean_setting_from_file("contours.txt",True)
            self.set_show_contours(show_contours)
        else :
            print("ERROR: Unrecognized setting",setting_name)
        if (__main_debug__) :
            print("Read setting",setting_name,":",self.app_mode,self.theme_style,self.map_color,self.show_contours)

    def restore_default_settings(self):
        self.get_running_app().root.ids.content_drawer.set_nav_drawer_list(False)
        self.set_theme(True)
        self.set_map_color(False)
        self.set_show_contours(True)
        self.save_path("")
    # def transition_to_expert_settings(self,ex_nav_drawer):
    #     root = MainApp.get_running_app().root
    #     root.ids.ex_data.produce_selected_data_set()
    #     root.ids.screen_manager.current = "settings"
    #     ex_nav_drawer.active_screen = "settings"
    #     self.snackbar.dismiss()

    # def transition_to_expert_about(self,ex_nav_drawer):
    #     root = MainApp.get_running_app().root
    #     root.ids.ex_data.produce_selected_data_set()
    #     root.ids.screen_manager.current = "about"
    #     ex_nav_drawer.active_screen = "about"
    #     self.snackbar.dismiss()
        
        
if __name__ == '__main__' :
    MainApp().run()

    
