CXX=g++
FMWK_HEADERS = LinkDef.h
HEADERS = $(filter-out $(FMWKHEADERS), $(wildcard *.h))

INCFLAGS = -g -I. -fPIC
INCFLAGS += $(shell larlite-config --includes)
INCFLAGS += $(shell larcv-config --includes)
INCFLAGS += `root-config --cflags`
INCFLAGS += -DUSE_OPENCV=1

LDFLAGS += $(shell larcv-config --libs)
LDFLAGS += $(shell larlitecv-config --libs)
LDFLAGS += $(shell larlite-config --libs)
LDFLAGS += `root-config --ldflags --libs`

LIB=libLArFlowCheck.so
BINARIES = larflowcheck
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

%: %.cxx $(LIB)
	$(CXX) $(INCFLAGS) -o $@ $@.cxx $(LIB) $(LDFLAGS)

clean:
	@rm -f $(BINARIES) *.o $(LIB)
