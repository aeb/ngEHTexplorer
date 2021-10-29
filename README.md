# ngEHTexplorer
An interactive tool with which to explore the possible imaging performance of candidate ngEHT architectures.

- [Summary Description](#Summary-Description)
- [Getting Started](#Getting-Started)
- [Feature Tour](#Feature-Tour)




## Summary Description
ngEHTexplorer is an interactive "app" that enables you to explore the impact of different ngEHT architecture choices on image reconstructions.  It is possible to investigate:
- performance of different arrays (incl. add/remove stations)
- imaging at multiple frequecies (incl. simultaneous multi-freq.)
- the impact of receiver bandwidth
- the impact of ngEHT dish size
- performance over different observation times and duration
- performance for different target sky positions
- performancce on various source images (incl. your own!)

and combinations thereof.

## Getting Started
To run ngEHTexplorer on Mac OSX, Linux, or other POSIX systems:
1. Clone the ngEHTexplorer github repository:
> $ git clone https://github.com/aeb/ngEHTexplorer.git
2. Descend into the ngEHTexplorer directory:
> $ cd ngEHTexplorer
3. Run the executable:
> $ ./ngEHTexplorer

To run ngEHTexplorerr on Windows you may need to run the python script manually:
1. Clone the ngEHTexplorer github repository:
> $ git clone https://github.com/aeb/ngEHTexplorer.git
2. Descend into the ngEHTexplorer/src directory:
> $ cd ngEHTexplorer/src
3. Run the executable:
> $ python3 main.py

You may need to edit the top of ngEHTexplorer to set the executables for your python3 and pip3 installations.



## Requirements
ngEHTexplorer is built with Python.  To run ngEHTexplorer requries:
- Python3 (3.7-9; some conflicts with 3.10 have been reported)
- kivy
- kivymd
- matplotlib
- numpy

You can normally install these (locally) with pip:
> $ pip3 install --upgrade kivy kivymd matplotlib numpy --user


## Feature Tour
Upon starting ngEHTexplorer, you should see a source selection screen:

<p align="center">
   <img src="docs/quickstart_selection_screen.png" alt="quickstart selection screen" width="256" class="center"/>  &emsp; <img src="docs/quickstart_navigation_drawer.png" alt="quickstart navigation drawer" width="256" class="center"/>
</p>

The navigation drawer (circled above) is the primary way to move through the various features of the application.  The application will intially be in "Quickstart" mode, which has a reduced set of features.  To enter "Expert mode", open the navigation drawer and select the switch at the top (circled below).

<p align="center">
   <img src="docs/quickstart_navigation_drawer_qsex.png" alt="quickstart navigation drawer" width="256" class="center"/>  &emsp; <img src="docs/expert_navigation_drawer.png" alt="expert navigation drawer" width="256" class="center"/>
</p>

From the navigation drawer a variety of screens may be selected.  We begin with the Target screen, which permits selecting the sky position of interest.  Sky positions of a number of specific sources are listed in the menu in the lower-right (currently set to "Sgr A*").  Among these choices is "--Select--", which permits the selection of arbitrary sky positions with the mouse.  The sky map can be scrolled (mouse) and zoomed (+/-) in the normal way.

<p align="center">
   <img src="docs/expert_navigation_drawer_tg.png" alt="expert navigation drawer" width="256" class="center"/>  &emsp; <img src="docs/expert_target_selection.png" alt="expert target selection" width="256" class="center"/>
</p>

The Source screen permits selecting among various source images, including your own.  Options include the source image itself (dragging left/right on the image), the angular size of the image, total flux in the image, and observation frequency.  

<p align="center">
   <img src="docs/expert_navigation_drawer_src.png" alt="expert navigation drawer" width="256" class="center"/>  &emsp; <img src="docs/expert_source_selection.png" alt="expert source selection" width="256" class="center"/>
</p>

It is possible to simulate multi-frequency observations, i.e., observations in which multiple frequencies are reconstructed simultaneously (assuming perfect phase transfer).  To do this, select the "Multi-freq." switch, and set the maximum and minimum frequency (e.g., 345 GHz and 86 GHz).

<p align="center">
   <img src="docs/expert_source_selection_multifreq.png" alt="multi-frequency option" width="256" class="center"/>  &emsp; <img src="docs/expert_source_selection_multifreq2.png" alt="multi-frequency range selection" width="256" class="center"/>
</p>

The Array screen provides a visualization of the global position of array stations.  The map can be scrolled (mouse) and zoomed (+/-) in the normal way.

<p align="center">
   <img src="docs/expert_navigation_drawer_arr.png" alt="expert navigation drawer" width="256" class="center"/> &emsp; <img src="docs/expert_array.png" alt="multi-frequency range selection" width="256" class="center"/>
</p>

Different arrays can be selected (also on the Baselines and Image screeens) by selecting the array name.  Selecting "ngEHT+" allows the addition of arbitrary new array locations.

<p align="center">
   <img src="docs/expert_array_mn.png" alt="expert array menu" width="256" class="center"/> &emsp; <img src="docs/expert_array_menu_sel.png" alt="expert menu selection" width="256" class="center"/> &emsp; <img src="docs/expert_array2.png" alt="expert menu selected ngEHT 6" width="256" class="center"/>
</p>

The Baselines screen provides a visualization of the "uv coverage" of the selected array.  A number of submenus can be opened, permitting the selection/deselection of individual stations, observation time ranges, ngEHT antenna diameters, and bandwidths.  The current screen will be updated automatically as these options are adjusted, which makes it possible to explore the dependence of these parameters in real time.  The plot can be scrolled (mouse) and zoomed (+/-) in the normal way.

<p align="center">
   <img src="docs/expert_navigation_drawer_bsl.png" alt="expert navigation drawer" width="256" class="center"/> &emsp; <img src="docs/expert_baselines.png" alt="expert baselines screen" width="256" class="center"/> &emsp; <img src="docs/expert_baseline_menu2.png" alt="expert menu options" width="256" class="center"/>
</p>

The Image screen presents the image reconstructed (in real time) from the simulated ngEHT data generated from the selected target location, source image, and array configuration.  The colormap shows the image with a linear transfer function; contours indicate a logarithmic transfer function with thick contours denoting factors of 10 below the maximum brightness.  The image can be scrolled (mouse) and zoomed (+/-) in the normal way.

<p align="center">
   <img src="docs/expert_navigation_drawer_img.png" alt="expert navigation drawer" width="256" class="center"/> &emsp; <img src="docs/expert_image.png" alt="expert image screen" width="256" class="center"/>
</p>


The Specifications screen presents various statistics associated with the array, simulated data sets, and reconstruction, including array performance metrics.  These are updated as the options on the other screens are modified.

<p align="center">
   <img src="docs/expert_navigation_drawer_spec.png" alt="expert navigation drawer" width="256" class="center"/> &emsp; <img src="docs/expert_specs.png" alt="expert specifications screen" width="256" class="center"/>
</p>


Finally, various settings can be found on the Settings screen and information about the ngEHT and the development team can be found on the About screen.

Happy exploring!

