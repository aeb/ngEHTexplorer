# ngEHTexplorer
An interactive tool with which to explore the possible imaging performance of candidate ngEHT architectures.

## Welcome!
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
To run ngEHTexplorer:
1. Clone the ngEHTexplorer github repository:
> $ git clone https://github.com/aeb/ngEHTexplorer.git
2. Descend into the ngEHTexplorer directory:
> $ cd ngEHTexplorer
3. Run the executable:
> $ ./ngEHTexplorer

You may need to edit the top of ngEHTexplorer to set the executables for your python3 and pip3 installations.



## Requirements
ngEHTexplorer is built with Python.  To run ngEHTexplorer requries:
- Python3 (3.7 or later)
- kivy
- kivymd
- matplotlib
- numpy
You can normally install these (locally) with pip:
> $ pip3 install --upgrade kivy kivymd matplotlib numpy --user


## Tour
On start up, you should see the "quickstart" source selection screen:

<p align="center">
   <img src="docs/quickstart_selection_screen.png" alt="quickstart selection screen" width="256" class="center"/>
</p>

The navigation drawer (circled above) is the primary way to move through the various features of the app.  The app will intially start in "Quickstart" mode, which has a reduced set of features.  To enter "Expert mode", open the navigation drawer and select the switch at the top.

<p align="center">
   <img src="docs/quickstart_navigation_drawer.png" alt="quickstart navigation drawer" width="256" class="center"/>  <br>  <img src="docs/expert_navigation_drawer.png" alt="quickstart navigation drawer" width="256" class="center"/>
</p>


