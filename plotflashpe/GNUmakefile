CXX=g++
FMWK_HEADERS = LinkDef.h
HEADERS = $(filter-out $(FMWKHEADERS), $(wildcard *.h))

INCFLAGS = -g -I. -fPIC
INCFLAGS += $(shell larlite-config --includes)
INCFLAGS += $(shell larcv-config --includes)
#INCFLAGS += -I$(GEO2D_BASEDIR)
#INCFLAGS += -I$(LAROPENCV_BASEDIR)
#INCFLAGS += -I$(LARLITE_BASEDIR)/../
#INCFLAGS += -I$(LARLITE_BASEDIR)/UserDev
#INCFLAGS += -I$(LARLITE_BASEDIR)/UserDev/BasicTool
#INCFLAGS += -I$(LARLITE_BASEDIR)/UserDev/SelectionTool
#INCFLAGS += -I$(LARLITECV_BASEDIR)/app
INCFLAGS += $(shell larlitecv-config --includes)
INCFLAGS += -I$(LARCV_BASEDIR)/app/ann_1.1.2/include
INCFLAGS += `root-config --cflags`
INCFLAGS += -DUSE_OPENCV=1

LDFLAGS += $(shell larcv-config --libs)
LDFLAGS += $(shell larlitecv-config --libs)
LDFLAGS += $(shell larlite-config --libs)
#LDFLAGS += -lSelectionTool_OpT0FinderAna -lSelectionTool_OpT0FinderApp \
	-lSelectionTool_OpT0PhotonLibrary -lSelectionTool_OpT0FinderAlgorithms -lSelectionTool_OpT0FinderBase 
LDFLAGS += `root-config --ldflags --libs`

LIB=libPlotFlashPE.so
BINARIES = plotflashpe
BINSRCS = $(addsuffix .cxx,$(BINARIES))
SOURCES = 
OBJS = $(SOURCES:.cxx=.o)

all: $(LIB) $(BINARIES)

%.o: %.cxx %.h
	$(CXX) $(INCFLAGS) -c -o $@ $*.cxx

$(LIB): $(OBJS)
	@echo "binsrcs: $(BINSRCS)"
	@echo "objects: $(OBJS)"
	$(CXX) -shared -o $@ $^ $(LDFLAGS)

plotflashpe: plotflashpe.cxx $(LIB)
	$(CXX) $(INCFLAGS) -o $@ $@.cxx $(LIB) $(LDFLAGS)

clean:
	@rm -f $(BINARIES) *.o $(LIB)
