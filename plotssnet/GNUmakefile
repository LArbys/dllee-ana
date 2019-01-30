
all: plot_ssnet

clean:
	rm -f *.o *.so plot_ssnet

plot_ssnet: plot_ssnet.cxx
	g++ -fPIC -std=c++11 `root-config --cflags` -I`larcv-config --incdir` -c plot_ssnet.cxx -o plot_ssnet.o
	g++ `root-config --ldflags` -o plot_ssnet plot_ssnet.o `larcv-config --libs` `root-config --libs`