CXX=g++

CXXFLAGS = -g -fPIC
INCLUDES =`root-config --cflags`
INCLUDES += `larcv-config --includes`
INCLUDES += `larlite-config --includes`

LIBS = `root-config --libs`
LIBS += `larlite-config --libs`
LIBS += `larcv-config --libs`

all: run_pixscale_ana

run_pixscale_ana: run_pixscale_ana.cxx
	$(CXX) $(CXXFLAGS) $(INCLUDES) $^ -o run_pixscale_ana $(LIBS)

