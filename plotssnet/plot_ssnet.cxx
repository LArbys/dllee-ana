#include <iostream>
#include <string>

#include "TFile.h"
#include "TH1D.h"

#include "DataFormat/IOManager.h"
#include "DataFormat/EventImage2D.h"



int main( int nargs, char** argv ) {

  std::string ssnet_input  = argv[1];
  std::string supera_input = argv[2];
  std::string out = argv[3];

  larcv::IOManager io(larcv::IOManager::kREAD);
  io.add_in_file( ssnet_input );
  io.add_in_file( supera_input );
  io.initialize();

  TFile tfile(out.c_str(),"new");
  
  // histograms of score values!
  std::vector< TH1D* > hshower_v(3,0);
  std::vector< TH1D* > htrack_v(3,0);
  std::vector< TH1D* > hfracshower_v(3,0);
  for (int i=0; i<3; i++) {
    char histname[50];
    sprintf(histname,"hshower_p%d",i);
    hshower_v[i] = new TH1D(histname,"",100,0,1.0);
    
    char trackname[50];
    sprintf(trackname,"htrack_p%d",i);
    htrack_v[i]  = new TH1D(trackname,"",100,0,1.0);

    char fracname[50];
    sprintf(fracname,"hfracshower_p%d",i);
    hfracshower_v[i] = new TH1D(fracname,"",100,0,1.0);
  }

  int nentries = io.get_n_entries();
  
  for (int ientry=0; ientry<nentries; ientry++) {
    io.read_entry(ientry);
    
    std::cout << "Entry " << ientry << std::endl;
    
    larcv::EventImage2D* ev_ssnetout_planes[3];
    for (int p=0; p<3; p++) {
      char branchname[20];
      sprintf( branchname, "uburn_plane%d", p );
      ev_ssnetout_planes[p] = (larcv::EventImage2D*)io.get_data( larcv::kProductImage2D, branchname );
    }
    larcv::EventImage2D* ev_img = (larcv::EventImage2D*)io.get_data( larcv::kProductImage2D, "wire" );
    
    for (int p=0; p<3; p++) {
      if ( ev_ssnetout_planes[p]->Image2DArray().size()==0 )
	continue;
      const larcv::Image2D& showerimg = ev_ssnetout_planes[p]->Image2DArray()[0];
      const larcv::Image2D& trackimg  = ev_ssnetout_planes[p]->Image2DArray()[1];
      const larcv::Image2D& adcimg    = ev_img->Image2DArray()[p];
      const larcv::ImageMeta& meta    = showerimg.meta();

      float nshower = 0;
      float nabovethresh = 0.;

      for (int r=0; r<(int)meta.rows(); r++) {
	for ( int c=0; c<(int)meta.cols(); c++) {
	  
	  try {
	    int t = meta.pos_y( r );
	    int w = meta.pos_x( c );
	    float val = adcimg.pixel( adcimg.meta().row(t), adcimg.meta().col(w) );
	    if (val>10.0) {
	      nabovethresh += 1.0;
	      hshower_v[p]->Fill( showerimg.pixel(r,c) );
	      htrack_v[p]->Fill( trackimg.pixel(r,c) );
	      if ( showerimg.pixel(r,c)>0.5 )
		nshower += 1.0;
	    }
	  }
	  catch (...) {
	    std::cout << "error acessing (" << r << "," << c << ")" << std::endl;
	  }
	}
      }//end of row loop
      
      if ( nabovethresh>0 )
	hfracshower_v[p]->Fill( nshower/nabovethresh );
      
    }//end of plane loop
  }//end of entry loop
  
  tfile.Write();
  
  return 0;
}
