from kivy.uix.boxlayout import BoxLayout
from kivy.uix.carousel import Carousel
from kivy.uix.image import AsyncImage
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.metrics import dp, sp
from kivy.properties import StringProperty, NumericProperty
from fancy_mdslider import FancyMDSlider
# from kivymd.uix.selectioncontrol import MDSwitch
from fancy_mdswitch import FancyMDSwitch
# from fancy_mdslider2 import Slider2

from kivy.uix.behaviors.touchripple import TouchRippleButtonBehavior
from kivy.uix.behaviors.button import ButtonBehavior

from kivymd.uix.label import MDLabel
from kivymd.app import MDApp

import os
import numpy as np
import matplotlib.image as mi

__data_debug__ = False


#########
# To read in data to get the 
def read_themis_data_file(v_file_name) :

    # Read in Themis-style data, which is simple and compact
    data = np.loadtxt(v_file_name,usecols=[5,6,7,8,9,10,3])
    baselines = np.loadtxt(v_file_name,usecols=[4],dtype=str)
    s1 = np.array([x[:2] for x in baselines])
    s2 = np.array([x[2:] for x in baselines])
    u = data[:,0]/1e3
    v = data[:,1]/1e3
    V = data[:,2] + 1.0j*data[:,4]
    err = data[:,3] + 1.0j*data[:,5]
    t = data[:,6]
    
    # Make conjugate points
    u = np.append(u,-u)
    v = np.append(v,-v)
    V = np.append(V,np.conj(V))
    err = np.append(err,err)
    t = np.append(t,t)
    s1d = np.append(s1,s2)
    s2d = np.append(s2,s1)
    
    return {'u':u,'v':v,'V':V,'s1':s1d,'s2':s2d,'t':t,'err':err}

#########
# Binlinear interpolation
def bilinear(x1d,y1d,f,X,Y,indexing='xy') :

    xfac = 1.0/(x1d[-1]-x1d[0])
    yfac = 1.0/(y1d[-1]-y1d[0])
    ifac = (len(x1d)-1)*xfac
    jfac = (len(y1d)-1)*yfac

    i = np.minimum(len(x1d)-2,np.maximum(0,((X-x1d[0])*ifac)).astype(int))
    j = np.minimum(len(y1d)-2,np.maximum(0,((Y-y1d[0])*jfac)).astype(int))

    wx = (X-x1d[i])/(x1d[1]-x1d[0])
    wy = (Y-y1d[j])/(y1d[1]-y1d[0])

    if (indexing=='ij') :
        F = (1.0-wx)*(1.0-wy)*f[i,j] + (1.0-wx)*wy*f[i,j+1] + wx*(1.0-wy)*f[i+1,j] + wx*wy*f[i+1,j+1]
    elif (indexing=='xy') :
        F = (1.0-wx)*(1.0-wy)*f[j,i] + (1.0-wx)*wy*f[j+1,i] + wx*(1.0-wy)*f[j,i+1] + wx*wy*f[j+1,i+1]
    else :
        print("ERROR: %s is not a valid indexing value."%(indexing))
        
    return F


def nearest_neighbor(X,xp,yp) :
    return yp[np.argmin(np.abs(X-xp))]
    

#########
# To generate data from a station dictionary and image
def generate_data(freq,ra,dec,imgx,imgy,imgI,statdict,integration_time=None,scan_time=600,min_elev=15,bandwidth=8.0,day=80) :

    #print("generate_data frequence is:",freq)
    
    if isinstance(freq,list) :
        return generate_data_multi_frequency(freq,ra,dec,imgx,imgy,imgI,statdict,integration_time=None,scan_time=600,min_elev=15,bandwidth=8.0,day=80)
    else :
        return generate_data_single_frequency(freq,ra,dec,imgx,imgy,imgI,statdict,integration_time=None,scan_time=600,min_elev=15,bandwidth=8.0,day=80)


#########
# To generate data from a station dictionary and image
def generate_data_multi_frequency(freq_list,ra,dec,imgx,imgy,imgI,statdict,integration_time=None,scan_time=600,min_elev=15,bandwidth=8.0,day=80) :
    # Takes:
    #  list of freq in GHz
    #  ra in hr
    #  dec in deg
    #  x in uas
    #  y in uas
    #  I in Jy
    #  statdict as specified in ngeht_array.py
    #  integration_time in s
    #  scan_time in s
    #  minimum elevation in deg
    #  bandwidth in GHz
    #  day of year

    ################################################################
    # Generate observation map
    #
    uas2rad = np.pi/180.0/3600e6
    V0 = np.fft.fftshift(np.fft.fft2(np.pad(imgI,pad_width=((0,imgI.shape[0]),(0,imgI.shape[1])))))
    # u01d = -np.fft.fftshift(np.fft.fftfreq(2*imgx.shape[0],d=(imgx[1,1]-imgx[0,0])*uas2rad)/1e9)
    # v01d = -np.fft.fftshift(np.fft.fftfreq(2*imgy.shape[1],d=(imgy[1,1]-imgy[0,0])*uas2rad)/1e9)
    u01d = -np.fft.fftshift(np.fft.fftfreq(2*imgx.shape[1],d=(imgx[1,1]-imgx[0,0])*uas2rad)/1e9)
    v01d = -np.fft.fftshift(np.fft.fftfreq(2*imgy.shape[0],d=(imgy[1,1]-imgy[0,0])*uas2rad)/1e9)

    if (__data_debug__) :
        print("Finished FFTs")

    # Phase center the image
    xc = 0.5*(imgx[-1,-1]-imgx[0,0])*uas2rad*1e9
    yc = 0.5*(imgy[-1,-1]-imgy[0,0])*uas2rad*1e9
    # u0,v0 = np.meshgrid(u01d,v01d,indexing='ij')
    # u0,v0 = np.meshgrid(v01d,u01d,indexing='xy')
    u0,v0 = np.meshgrid(u01d,v01d)
    V0 = V0*np.exp(-2.0j*np.pi*(u0*xc+v0*yc))

    # import matplotlib.pyplot as plt
    # plt.figure()
    # plt.imshow(imgI)
    # plt.figure()
    # plt.imshow(V0.real)
    # plt.figure()
    # plt.imshow(np.abs(V0))
    # # plt.figure()
    # # plt.pcolor(u0,v0,np.abs(V0))
    # plt.show()

    
    if (__data_debug__) :
        print("Phase centered visibilities")

        
    
    s1 = []
    s2 = []
    u = []
    v = []
    V = []
    err = []
    t = []

    for freq in freq_list :
    
        if (integration_time is None) :
            integration_time = 30 * (86/freq)
    
        one_over_lambda = freq*1e9 / 2.998e8 / 1e9
            
        thermal_error_factor = 1.0/np.sqrt( 0.8*2*bandwidth*1e9*integration_time ) # * np.sqrt(integration_time/scan_time)

    
        min_cos_zenith = np.cos( (90-min_elev)*np.pi/180.0 )

        if (__data_debug__) :
            print("Minimum cos(zenith):",min_cos_zenith)

        usub = []
        vsub = []

            
        ################################################################
        # Generate observation map
        #
        for obstime in np.arange(0,24.0,scan_time/3600.0) :

            csph = -np.cos((ra-obstime-(day-80)*24/365.25)*np.pi/12.)
            snph = -np.sin((ra-obstime-(day-80)*24/365.25)*np.pi/12.)
            csth = np.sin(dec*np.pi/180.0)
            snth = np.cos(dec*np.pi/180.0)

            X = csph*snth
            Y = snph*snth
            Z = csth
            for k,stat1 in enumerate(statdict.keys()) :
                x,y,z = statdict[stat1]['loc']
                csze1 = (x*X+y*Y+z*Z)/np.sqrt(x*x+y*y+z*z)
                if (csze1>=min_cos_zenith) :
                    x1 = csth*(csph*x+snph*y) - snth*z
                    y1 = -snph*x + csph*y
                    # z1 = snth*(csph*x+snph*y) + csth*z
                    for stat2 in list(statdict.keys())[(k+1):] :
                        x,y,z = statdict[stat2]['loc']
                        csze2 = (x*X+y*Y+z*Z)/np.sqrt(x*x+y*y+z*z)
                        if (csze2>=min_cos_zenith) :
                            x2 = csth*(csph*x+snph*y) - snth*z
                            y2 = -snph*x + csph*y
                            # z2 = snth*(csph*x+snph*y) + csth*z

                            usub.append( (y1-y2) * one_over_lambda )
                            vsub.append( -(x1-x2) * one_over_lambda )
                            u.append( (y1-y2) * one_over_lambda )
                            v.append( -(x1-x2) * one_over_lambda )
                            t.append( obstime )

                            s1.append( stat1 )
                            s2.append( stat2 )

                            sefd1 = nearest_neighbor(freq,statdict[stat1]['sefd_freq'],statdict[stat1]['sefd'])
                            sefd2 = nearest_neighbor(freq,statdict[stat1]['sefd_freq'],statdict[stat2]['sefd'])

                            err.append( np.sqrt( sefd1*sefd2 ) * thermal_error_factor )


        # Interpolate to the data points
        # V = bilinear(u01d,v01d,V0,u,v)
        V.extend(list(bilinear(u01d,v01d,V0,usub,vsub)))
    

        if (__data_debug__) :
            print("Interpolated to the truth")

            
                            
    u = np.array(u)
    v = np.array(v)
    t = np.array(t)
    s1 = np.array(s1)
    s2 = np.array(s2)
    err = np.array(err)
    V = np.array(V)

    if (__data_debug__) :
        print("Generated baseline map")

    # Make conjugate points
    u = np.append(u,-u)
    v = np.append(v,-v)
    V = np.append(V,np.conj(V))
    err = np.append(err,err)
    t = np.append(t,t)
    s1d = np.append(s1,s2)
    s2d = np.append(s2,s1)

    if (__data_debug__) :
        print("Made conjugates, all done!  Number of data points:",len(u))

    
    return {'u':u,'v':v,'V':V,'s1':s1d,'s2':s2d,'t':t,'err':(1.0+1.0j)*err}
    
        
#########
# To generate data from a station dictionary and image
def generate_data_single_frequency(freq,ra,dec,imgx,imgy,imgI,statdict,integration_time=None,scan_time=600,min_elev=15,bandwidth=8.0,day=80) :
    # Takes:
    #  freq in GHz
    #  ra in hr
    #  dec in deg
    #  x in uas
    #  y in uas
    #  I in Jy
    #  statdict as specified in ngeht_array.py
    #  integration_time in s
    #  scan_time in s
    #  minimum elevation in deg
    #  bandwidth in GHz
    #  day of year
    
    s1 = []
    s2 = []
    u = []
    v = []
    V = []
    err = []
    t = []

    if (integration_time is None) :
        integration_time = 30 * (86/freq)
    
    one_over_lambda = freq*1e9 / 2.998e8 / 1e9

    thermal_error_factor = 1.0/np.sqrt( 0.8*2*bandwidth*1e9*integration_time ) # * np.sqrt(integration_time/scan_time)

    
    min_cos_zenith = np.cos( (90-min_elev)*np.pi/180.0 )

    if (__data_debug__) :
        print("Minimum cos(zenith):",min_cos_zenith)
    
    ################################################################
    # Generate observation map
    #
    for obstime in np.arange(0,24.0,scan_time/3600.0) :

        csph = -np.cos((ra-obstime-(day-80)*24/365.25)*np.pi/12.)
        snph = -np.sin((ra-obstime-(day-80)*24/365.25)*np.pi/12.)
        csth = np.sin(dec*np.pi/180.0)
        snth = np.cos(dec*np.pi/180.0)
        
        X = csph*snth
        Y = snph*snth
        Z = csth
        for k,stat1 in enumerate(statdict.keys()) :
            x,y,z = statdict[stat1]['loc']
            csze1 = (x*X+y*Y+z*Z)/np.sqrt(x*x+y*y+z*z)
            if (csze1>=min_cos_zenith) :
                x1 = csth*(csph*x+snph*y) - snth*z
                y1 = -snph*x + csph*y
                # z1 = snth*(csph*x+snph*y) + csth*z
                for stat2 in list(statdict.keys())[(k+1):] :
                    x,y,z = statdict[stat2]['loc']
                    csze2 = (x*X+y*Y+z*Z)/np.sqrt(x*x+y*y+z*z)
                    if (csze2>=min_cos_zenith) :
                        x2 = csth*(csph*x+snph*y) - snth*z
                        y2 = -snph*x + csph*y
                        # z2 = snth*(csph*x+snph*y) + csth*z
                        
                        u.append( (y1-y2) * one_over_lambda )
                        v.append( -(x1-x2) * one_over_lambda )
                        t.append( obstime )

                        s1.append( stat1 )
                        s2.append( stat2 )

                        sefd1 = nearest_neighbor(freq,statdict[stat1]['sefd_freq'],statdict[stat1]['sefd'])
                        sefd2 = nearest_neighbor(freq,statdict[stat1]['sefd_freq'],statdict[stat2]['sefd'])

                        err.append( np.sqrt( sefd1*sefd2 ) * thermal_error_factor )
                        
    u = np.array(u)
    v = np.array(v)
    t = np.array(t)
    s1 = np.array(s1)
    s2 = np.array(s2)
    err = np.array(err)

    if (__data_debug__) :
        print("Generated baseline map")

    ################################################################
    # Generate observation map
    #
    uas2rad = np.pi/180.0/3600e6
    V0 = np.fft.fftshift(np.fft.fft2(np.pad(imgI,pad_width=((0,imgI.shape[0]),(0,imgI.shape[1])))))
    # u01d = -np.fft.fftshift(np.fft.fftfreq(2*imgx.shape[0],d=(imgx[1,1]-imgx[0,0])*uas2rad)/1e9)
    # v01d = -np.fft.fftshift(np.fft.fftfreq(2*imgy.shape[1],d=(imgy[1,1]-imgy[0,0])*uas2rad)/1e9)
    u01d = -np.fft.fftshift(np.fft.fftfreq(2*imgx.shape[1],d=(imgx[1,1]-imgx[0,0])*uas2rad)/1e9)
    v01d = -np.fft.fftshift(np.fft.fftfreq(2*imgy.shape[0],d=(imgy[1,1]-imgy[0,0])*uas2rad)/1e9)

    if (__data_debug__) :
        print("Finished FFTs")

    
    # Phase center the image
    xc = 0.5*(imgx[-1,-1]-imgx[0,0])*uas2rad*1e9
    yc = 0.5*(imgy[-1,-1]-imgy[0,0])*uas2rad*1e9
    # u0,v0 = np.meshgrid(u01d,v01d,indexing='ij')
    # u0,v0 = np.meshgrid(v01d,u01d,indexing='xy')
    u0,v0 = np.meshgrid(u01d,v01d)
    V0 = V0*np.exp(-2.0j*np.pi*(u0*xc+v0*yc))

    # import matplotlib.pyplot as plt
    # plt.figure()
    # plt.imshow(imgI)
    # plt.figure()
    # plt.imshow(V0.real)
    # plt.figure()
    # plt.imshow(np.abs(V0))
    # # plt.figure()
    # # plt.pcolor(u0,v0,np.abs(V0))
    # plt.show()

    
    if (__data_debug__) :
        print("Phase centered visibilities")
    
    # Interpolate to the data points
    V = bilinear(u01d,v01d,V0,u,v)

    if (__data_debug__) :
        print("Interpolated to the truth")

    # Make conjugate points
    u = np.append(u,-u)
    v = np.append(v,-v)
    V = np.append(V,np.conj(V))
    err = np.append(err,err)
    t = np.append(t,t)
    s1d = np.append(s1,s2)
    s2d = np.append(s2,s1)

    if (__data_debug__) :
        print("Made conjugates, all done!  Number of data points:",len(u))

    
    return {'u':u,'v':v,'V':V,'s1':s1d,'s2':s2d,'t':t,'err':(1.0+1.0j)*err}

                        
                        
def generate_data_from_file(file_name,statdict,freq=230,ra=17.7611225,dec=-29.007810,scale=500.0,total_flux=None,taper_image=False,**kwargs) :

    if (__data_debug__) :
        print("generate_data_from_file:",file_name,freq,ra,dec,scale,total_flux)
    
    ext = os.path.splitext(file_name)[1]

    if (__data_debug__) :
        print("Started in generate_data_from_file, I think this is a %s file."%(ext))
    
    if ( ext=='.dat' ) :
        return read_themis_data_file(file_name)  # No kwargs

    elif ( ext=='.npy' ) :

        [img_total_flux,xdim,ydim,psize,drf,ii] = np.load(file_name,allow_pickle=True)
        I = 10**(ii.reshape(xdim,ydim)/256.0 * drf - drf)
        if (total_flux is None) :
            total_flux = img_total_flux
        I = I * total_flux/np.sum(I)
        I = np.flipud(np.fliplr(I)) 
        # I = np.transpose(np.flipud(np.fliplr(I)))
        # x,y = np.meshgrid(np.arange(0,I.shape[0]),np.arange(0,I.shape[1]),indexing='ij')
        # x,y = np.meshgrid(np.arange(0,I.shape[1]),np.arange(0,I.shape[0]),indexing='ij')
        x,y = np.meshgrid(np.arange(0,I.shape[1]),np.arange(0,I.shape[0]))
        x = (x-0.5*I.shape[1])*psize * (scale/500.0)
        y = (y-0.5*I.shape[0])*psize * (scale/500.0)

        # print("Shapes:",x.shape,y.shape,I.shape)
        # print("x:",x[:5,0],x[:,0].shape)
        # print("y:",y[0,:5],y[0,:].shape)
        # import matplotlib.pyplot as plt
        # plt.pcolor(x,y,np.log10(I/np.max(I)),vmax=0,vmin=-4,cmap='afmhot')
        # plt.show()

        if (__data_debug__) :
            print("Finished npy read:",x.shape,y.shape,I.shape,x[0,0],x[-1,-1],y[0,0],y[-1,-1],np.max(I))
            
        return generate_data(freq,ra,dec,x,y,I,statdict,**kwargs)
    
    elif ( ext.lower() in ['.jpg','.jpeg','.png','.gif'] ) :

        img = mi.imread(file_name)

        if (__data_debug__) :
            print("Read",file_name,img.shape)        

        if (len(img.shape)==2) : # BW img
            I = img
        elif (len(img.shape)==3) : # Color img
            if (img.shape[2]==3) : # rgb
                I = np.sqrt( (img[:,:,0].astype(float))**2 + (img[:,:,1].astype(float))**2 + (img[:,:,2].astype(float))**2 )
            elif (img.shape[2]==4) : # rgba
                I = np.sqrt( (img[:,:,0].astype(float))**2 + (img[:,:,1].astype(float))**2 + (img[:,:,2].astype(float))**2 ) * (img[:,:,3].astype(float))
        else :
            print("ERROR: Unknown image type in file %s"%(file_name))
            return None




        # Taper image
        if (taper_image) :
            i,j = np.meshgrid(np.linspace(0,1,I.shape[1]),np.linspace(0,1,I.shape[0]))

            # Hann window
            hi = (np.sin(np.pi*i))**2
            hj = (np.sin(np.pi*j))**2

            # Blackman window
            # hi = 0.42 - 0.5*np.cos(2*np.pi*i) + 0.08*np.cos(4*np.pi*i)
            # hj = 0.42 - 0.5*np.cos(2*np.pi*j) + 0.08*np.cos(4*np.pi*j)
            
            taper_func = hi*hj
            I = I * taper_func**2

            # import matplotlib.pyplot as plt            
            # plt.figure()
            # plt.imshow(I)
            # plt.show()

        else :
            # Edge smoothing (which we do no matter what)
            px_smooth = 0.05
            i,j = np.meshgrid(np.linspace(0,1,I.shape[1]),np.linspace(0,1,I.shape[0]))
            hi = np.sin(0.5*np.pi*i/px_smooth)*(i<px_smooth) + 1.0*(i>=px_smooth)*(i<=1.0-px_smooth) + np.sin(0.5*np.pi*(1-i)/px_smooth)*(1-i<px_smooth)
            hj = np.sin(0.5*np.pi*j/px_smooth)*(j<px_smooth) + 1.0*(j>=px_smooth)*(j<=1.0-px_smooth) + np.sin(0.5*np.pi*(1-j)/px_smooth)*(1-j<px_smooth)

            taper_func = hi*hj
            I = I * taper_func
            
            # import matplotlib.pyplot as plt
            # plt.figure()
            # plt.pcolor(i,j,taper_func,cmap='afmhot')
            # plt.figure()
            # plt.pcolor(i,j,I,cmap='afmhot')
            # plt.show()
        
            
        # drf = 1
        # I = 1 * I / np.max(I)
        #I = I**2

        if (scale<1000.0) :
            if (__data_debug__) :
                print("Plot too small in x-direction:",scale)
            dim = min(I.shape[1]+128,int(np.ceil(1000.0/scale * I.shape[1])))
            mpad = (dim-I.shape[1])//2
            ppad = (dim-I.shape[1])-mpad
            if (__data_debug__) :
                print("  new dim, mpad, ppad:",dim,mpad,ppad)
            scale = float(dim)/I.shape[1] * scale
            if (__data_debug__) :
                print("  new scale:",scale)
            I = np.pad(I,pad_width=((0,0),(mpad,ppad)))

        if (__data_debug__) :
            print("Shape after x-dim check:",I.shape)
            
        if (scale*I.shape[0]/I.shape[1]<1000.0) :
            if (__data_debug__) :
                print("Plot too small in y-direction:",scale)
            dim = min(I.shape[1]+128,int(np.ceil(1000.0/scale * I.shape[1])))
            mpad = (dim-I.shape[0])//2
            ppad = (dim-I.shape[0])-mpad
            if (__data_debug__) :
                print("  new dim, mpad, ppad:",dim,mpad,ppad)
            I = np.pad(I,pad_width=((mpad,ppad),(0,0)))

        if (__data_debug__) :
            print("Shape after y-dim check:",I.shape)

        # if (I.shape[0]<1024 or I.shape[1]<1024) :
        #     x_mpad = (1024-I.shape[0])//2
        #     x_ppad = 1024-I.shape[0]-x_mpad
        #     y_mpad = (1024-I.shape[1])//2
        #     y_ppad = 1024-I.shape[1]-y_mpad
        #     scale = 1024./I.shape[0] * scale
        #     I = np.pad(I,pad_width=((x_mpad,x_ppad),(y_mpad,y_ppad)))
        # print("Shape after size check:",I.shape)

        

        
        if (__data_debug__) :
            print("Set intensity array",I.shape,np.max(I),np.min(I))
        if (total_flux is None) :
            total_flux = 1.0
        I = I * total_flux / np.sum(I)
        I = np.flipud(np.fliplr(I))
        # x,y = np.meshgrid(np.arange(0,I.shape[0]),np.arange(0,I.shape[1]),indexing='ij')
        # x = (x-0.5*I.shape[0])*scale/I.shape[0]
        # y = (y-0.5*I.shape[1])*scale/I.shape[0]

        x,y = np.meshgrid(np.arange(0,I.shape[1]),np.arange(0,I.shape[0]))
        x = (x-0.5*I.shape[1])*scale/I.shape[1]
        y = (y-0.5*I.shape[0])*scale/I.shape[1]


        I = I + 0.1*np.max(I)*np.exp(-(x**2+y**2)/(2.0*200.0**2) )
        # I = 0.1*np.max(I)*np.exp(-(x**2+y**2)/(2.0*200.0**2) )


        # Crop image to 1024x1024 on -0.5 mas to 0.5 mas
        x2,y2 = np.meshgrid(-np.linspace(-500,500,1024),np.linspace(-500,500,1024))
        I2 = bilinear(x[0,:],y[:,0],I,x2,y2)

        
        if (__data_debug__) :
            print("Shapes:",x2.shape,y2.shape,I2.shape)
            print("x2:",x2[:5,0],x2[:,0].shape)
            print("y2:",y2[0,:5],y2[0,:].shape)

        # import matplotlib.pyplot as plt
        # # plt.figure()
        # # plt.pcolor(x,y,I,cmap='afmhot')
        # plt.figure()
        # plt.pcolor(x2,y2,I2,cmap='afmhot')
        # plt.show()
        
        if (__data_debug__) :
            print("Finished %s read."%(ext))        

        return generate_data(freq,ra,dec,x2,y2,I2,statdict,**kwargs)

        
class FileImageButton(ButtonBehavior,Image) :
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.default_image_source = "./images/image_file_icon.png"
        self.pressed_image_source = "./images/image_file_icon_pressed.png"

        self.source = self.default_image_source
        self.allow_stretch = True
        
        self.bind(on_press=self.press)
        self.bind(on_release=self.release)

    def press(self,widget) :
        self.source = self.pressed_image_source

    def release(self,widget) :
        self.source = self.default_image_source
        
    
class ImageCarousel(Carousel) :

    slide_index = NumericProperty(None)
    slide_caption = StringProperty(None)
    
    def __init__(self,**kwargs) :
        super().__init__(**kwargs)

        self.direction = 'right'
        self.loop = True
        self.image_file_list = []
        self.data_file_list = []
        self.taperable_list = []

        box = BoxLayout()
        box.orientation = "vertical"
        self.add_btn = FileImageButton()
        # lbl = MDLabel(text="Add custom image!",halign='center',size_hint=(1,None),height=sp(24),font_size=sp(12))
        lbl = MDLabel(text="Add custom image!",halign='center',size_hint=(1,None),height=sp(24),font_style='Caption',font_size=sp(10))
        box.add_widget(self.add_btn)
        box.add_widget(lbl)
        self.add_widget(box)
        self.image_file_list.append("")
        self.data_file_list.append("")
        self.taperable_list.append(False)

        # Expects image for each frequency
        self.frequency_index = 1
        self.frequency_list = np.array([86,230,345,480,690])
        
    def add_image(self,image_file,data_file,caption="",taperable=True) :

        if (not isinstance(image_file,list)) :
            image_file = [image_file,image_file,image_file,image_file,image_file]
            data_file = [data_file,data_file,data_file,data_file,data_file]
            
        
        img_file = image_file[self.frequency_index]
        
        box = BoxLayout()
        box.orientation = "vertical"
        image = AsyncImage(source=img_file, allow_stretch=True)
        # image = Image(source=img_file, allow_stretch=True)
        lbl = MDLabel(text=caption,halign='center',size_hint=(1,None),height=sp(24),font_size=sp(12))
        box.add_widget(image)
        box.add_widget(lbl)
        self.add_widget(box)

        self.image_file_list.append(image_file)
        self.data_file_list.append(data_file)
        self.taperable_list.append(taperable)
        
    def selected_data_file(self) :
        return self.data_file_list[max(1,self.index)][self.frequency_index]

    def set_frequency(self,widget,val) :
        self.frequency_index = int(val)
        if (__data_debug__) :
            print("ImageCarousel.set_frequency:",self.frequency_index,val,self.frequency_list)
        for j,w in enumerate(self.slides) :
            if (j>0) :
                w.children[1].source = self.image_file_list[j][self.frequency_index]
            
        
class DataSelectionSliders(BoxLayout) :

    source_size = NumericProperty(None)
    source_flux = NumericProperty(None)
    observation_frequency = NumericProperty(None)
    minimum_observation_frequency = NumericProperty(None)
    
    def __init__(self,**kwargs) :
        super().__init__(**kwargs)
        self.orientation = 'vertical'

        # Add the taper switch
        self.its_box = BoxLayout()
        self.its_box.orientation='horizontal'
        self.its_label = MDLabel(text='Taper image',halign='center')
        self.its_box.add_widget(self.its_label)
        self.its_box_box = BoxLayout()
        self.its = FancyMDSwitch(pos_hint={'center_x':0.5,'center_y':0.5})
        self.its._thumb_color_down = (1,0.75,0.25,1)
        self.its_box_box.add_widget(self.its)
        self.its_box.add_widget(self.its_box_box)

        self.imws_label = MDLabel(text='Multi-freq.',halign='center')
        self.its_box.add_widget(self.imws_label)
        self.imws_box_box = BoxLayout()
        self.imws = FancyMDSwitch(pos_hint={'center_x':0.5,'center_y':0.5})
        self.imws._thumb_color_down = (1,0.75,0.25,1)
        self.imws_box_box.add_widget(self.imws)
        self.imws.bind(active=self.cycle_multi_wavelength)
        self.its_box.add_widget(self.imws_box_box)
        
        # Add the source size slider
        self.sss_box = BoxLayout()
        self.sss_box.orientation='horizontal'
        self.sss_label = MDLabel(text='Size:',halign='center',size_hint=(0.5,1))
        self.sss_box.add_widget(self.sss_label)
        
        self.sss = SourceSizeMDSlider()
        self.sss.background_color=(0,0,0,0)
        self.sss.set_color=False
        self.sss.orientation='horizontal'
        self.sss.size_hint=(0.8,1)
        self.sss.bind(value=self.adjust_source_size)
        self.sss_box.add_widget(self.sss)
        
        self.sss_label2 = MDLabel(text=("%3g \u03BCas")%(self.sss.source_size()),halign='center',size_hint=(0.5,1))
        self.sss_box.add_widget(self.sss_label2)

        
        # Add the source flux slider
        self.sfs_box = BoxLayout()
        self.sfs_box.orientation='horizontal'
        self.sfs_label = MDLabel(text='Total Flux:',halign='center',size_hint=(0.5,1))
        self.sfs_box.add_widget(self.sfs_label)
        
        self.sfs = FluxMDSlider()
        self.sfs.background_color=(0,0,0,0)
        self.sfs.set_color=False        
        self.sfs.orientation='horizontal'
        self.sfs.size_hint=(0.8,1)
        self.sfs.bind(value=self.adjust_source_flux) #
        self.sfs_box.add_widget(self.sfs)
        self.sfs_label2 = MDLabel(text="%5.1f Jy"%(self.sfs.flux()),halign='center',size_hint=(0.5,1))
        self.sfs_box.add_widget(self.sfs_label2)

        
        # Add the observation frequency slider
        self.ofs_box = BoxLayout()
        self.ofs_box.orientation='horizontal'
        self.ofs_label = MDLabel(text='Obs. Freq.:',halign='center',size_hint=(0.5,1))
        self.ofs_box.add_widget(self.ofs_label)
        
        self.ofs = ObsFrequencyMDSlider()
        self.ofs.background_color=(0,0,0,0)
        self.ofs.set_color=False
        self.ofs.orientation='horizontal'
        self.ofs.size_hint=(0.8,1)
        self.ofs.bind(value=self.adjust_observation_frequency) #
        self.ofs_box.add_widget(self.ofs)
        self.ofs_label2 = MDLabel(text="%3g GHz"%(self.ofs.observation_frequency()),halign='center',size_hint=(0.5,1))
        self.ofs_box.add_widget(self.ofs_label2)


        # Add the observation frequency slider
        self.mofs_box = BoxLayout()
        self.mofs_box.orientation='horizontal'
        self.mofs_label = MDLabel(text='Min. Freq.:',halign='center',size_hint=(0.5,1))
        self.mofs_box.add_widget(self.mofs_label)
        
        self.mofs = ObsFrequencyMDSlider()
        self.mofs.background_color=(0,0,0,0)
        self.mofs.set_color=False
        self.mofs.orientation='horizontal'
        self.mofs.size_hint=(0.8,1)
        self.mofs.bind(value=self.adjust_minimum_observation_frequency) #
        self.mofs_box.add_widget(self.mofs)
        self.mofs_label2 = MDLabel(text="%3g GHz"%(self.mofs.observation_frequency()),halign='center',size_hint=(0.5,1))
        self.mofs_box.add_widget(self.mofs_label2)
        
        self.source_size = self.sss.source_size()
        self.source_flux = self.sfs.flux()
        self.observation_frequency = self.ofs.observation_frequency()
        self.minimum_observation_frequency = self.mofs.observation_frequency()

        self.add_widget(self.its_box)        
        self.add_widget(self.sss_box)
        self.add_widget(self.sfs_box)
        self.add_widget(self.ofs_box)
        #self.add_widget(self.mofs_box)

    def cycle_multi_wavelength(self,widget,active) :
        if (active) :
            self.clear_widgets()
            self.add_widget(self.its_box)        
            self.add_widget(self.sss_box)
            self.add_widget(self.sfs_box)
            self.add_widget(self.ofs_box)
            self.add_widget(self.mofs_box)
            self.ofs_label.text='Max. Freq.'
        else :
            self.clear_widgets()
            self.add_widget(self.its_box)        
            self.add_widget(self.sss_box)
            self.add_widget(self.sfs_box)
            self.add_widget(self.ofs_box)
            self.ofs_label.text='Obs. Freq.'
            self.minimum_observation_frequency = self.observation_frequency
            self.mofs.value = self.ofs.value
        
    def adjust_source_size(self,widget,val) :
        self.source_size = self.sss.source_size()
        self.sss_label2.text = self.sss.hint_box_text(0)

    def adjust_source_flux(self,widget,val) :
        self.source_flux = self.sfs.flux()
        self.sfs_label2.text = self.sfs.hint_box_text(0)

    def adjust_observation_frequency(self,widget,val) :
        self.observation_frequency = self.ofs.observation_frequency()
        self.ofs_label2.text = self.ofs.hint_box_text(0)
        self.mofs.value = min(self.mofs.value,self.ofs.value)
        if (self.imws.active==False) :
            self.mofs.value = self.ofs.value
            self.minimum_observation_frequency = self.mofs.observation_frequency()
        #print("Freq. range:",[self.mofs.observation_frequency(),self.ofs.observation_frequency()])
        if (__data_debug__) :
            print("DataSelectionSliders.adjust_observation_frequency:",self.observation_frequency,val,self.ofs_label2.text)

    def adjust_minimum_observation_frequency(self,widget,val) :
        self.minimum_observation_frequency = min(self.ofs.observation_frequency(),self.mofs.observation_frequency())
        self.mofs.value = min(self.mofs.value,self.ofs.value)
        self.mofs_label2.text = self.mofs.hint_box_text(0)
        if (__data_debug__) :
            print("DataSelectionSliders.adjust_observation_frequency:",self.minimum_observation_frequency,val,self.mofs_label2.text)


    def observation_frequency_list(self) :
        freq_list = []
        for i in range(int(self.mofs.value),int(self.ofs.value+1)) :
            freq_list.append(self.ofs.observation_frequency_list[i])
        #print("freq list:",freq_list)
        return freq_list
        
class ObsFrequencyMDSlider(FancyMDSlider):

    def __init__(self,**kwargs):
        self.observation_frequency_list = [ 86, 230, 345, 480, 690 ]
        super().__init__(**kwargs)
        self.min = 0
        self.max = len(self.observation_frequency_list)-1
        self.value = 1
        self.step = 1
        self.show_off = False

    def observation_frequency(self) :
        return self.observation_frequency_list[int(self.value)]
        
    def hint_box_text(self,value) :
        return "%3g GHz"%(self.observation_frequency())

    def hint_box_size(self) :
        return (dp(50),dp(28))            

    
class SourceSizeMDSlider(FancyMDSlider):
    
    def __init__(self,**kwargs):
        super().__init__(**kwargs)

        self.min = 50
        self.max = 1000
        self.value = 500
        self.step = 50
        self.show_off = False

    def source_size(self) :
        return self.value
        
    def hint_box_text(self,value) :
        return ("%5g \u03BCas")%(self.source_size())

    def hint_box_size(self) :
        return (dp(50),dp(28))
    
    
class FluxMDSlider(FancyMDSlider):
    
    def __init__(self,**kwargs):
        super().__init__(**kwargs)

        self.min = -2
        self.max = 1
        self.value = 0
        self.step = 0.25
        self.show_off = True

    def flux(self) :
        return 10**self.value
        
    def hint_box_text(self,value) :
        f = self.flux()
        if (f<1e-4) :
            return "%5.2f \03BCJy"%(1e6*f)
        elif (f<1e-1):
            return "%5.2f mJy"%(1e3*f)
        elif (f<1e2) :
            return "%5.2f Jy"%(f)
        else :
            return "%5.2f kJy"%(1e-3*f)

    def hint_box_size(self) :
        return (dp(60),dp(28))
