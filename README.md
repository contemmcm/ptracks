# ptracks
Python track generator for air traffic control 

## Install (Ubuntu 12.04 and 14.04)


### Requirements

 * git
 * mpi4py
 * qt4

```
sudo apt-get install git python-mpi4py python-qt4
```

### Download

Please download the latest version from git-hub:

```
git clone https://github.com/contemmcm/ptracks.git
```

### Installation


```
cd ptracks
sudo ./install
sudo update-rc.d ptracks-net defaults
```

### Quick Start

Initialize the simulation and specify the exercise to execute. In the example below, the exercise SBBR is used:

```
service ptracks start DEMO1970
```

Open a browser and go to http://localhost:61000/ to see the web interface of the simulation.

Then, to change the course of any aircraft in the simulation, just execute:

```
ptracks-pilot
```

To stop the simulation, just execute

```
service ptracks stop
```
