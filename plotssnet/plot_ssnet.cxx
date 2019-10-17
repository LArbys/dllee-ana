#include <iostream>
#include <string>
#include <fstream>

#include "TFile.h"
#include "TH1D.h"
#include "TH2D.h"
#include "TStyle.h"

#include "larcv/core/DataFormat/IOManager.h"
#include "larcv/core/DataFormat/EventImage2D.h"

int main( int nargs, char** argv ) {

  gStyle->SetOptStat(0);

  std::string ssnet_input  = argv[1];
  std::string supera_input = argv[2];
  std::string out = argv[3];

  std::vector<float> scale_factors(3,1.0);

  // mcc9mc [deprecated]
  // scale_factors[0] = 0.81132;
  // scale_factors[1] = 0.79630;
  // scale_factors[2] = 0.80328;

  bool save_event_vis = false;

  char filename[5000];

  // SUPERA IO: tick-backward
  larcv::IOManager io(larcv::IOManager::kREAD,"supera",larcv::IOManager::kTickBackward);
  std::ifstream superin( supera_input.c_str() );
  while (!superin.eof() && superin.good()) {
    superin >> filename;
    std::string sfilename = filename;
    std::cout << "loading supera file: " << sfilename << std::endl;
    if (sfilename!="") {
      io.add_in_file( sfilename );
    }
  }
  io.initialize();

  // SPARSE SSNET: tick-forward
  larcv::IOManager io_ssnet(larcv::IOManager::kREAD,"ssnet",larcv::IOManager::kTickForward);
  std::ifstream ssnetin( ssnet_input.c_str() );
  while (!ssnetin.eof() && ssnetin.good()) {
    ssnetin >> filename;
    std::string sfilename = filename;
    std::cout << "loading ssnet file: " << sfilename << std::endl;
    if (sfilename!="") {
      io_ssnet.add_in_file( sfilename );
    }
  }
  io_ssnet.initialize();

  TFile tfile(out.c_str(),"new");
  
  // histograms of score values!
  // [shower score, track score, fracshower]
  std::vector< TH1D* > hshower_v(3,0);
  std::vector< TH1D* > htrack_v(3,0);
  std::vector< TH1D* > hfracshower_v(3,0);
  for (int i=0; i<3; i++) {
    char histname[50];
    sprintf(histname,"hshowerscore_p%d",i);
    hshower_v[i] = new TH1D(histname,"",100,0,1.0);
    
    char trackname[50];
    sprintf(trackname,"htrackscore_p%d",i);
    htrack_v[i]  = new TH1D(trackname,"",100,0,1.0);

    char fracname[50];
    sprintf(fracname,"hfracshower_p%d",i);
    hfracshower_v[i] = new TH1D(fracname,"",100,0,1.0);
  }

  // adc histograms -- to help compare
  std::vector< TH1D* > hadc_v(3,0);
  for ( int i=0; i<3; i++ ) {
    char histname[50];
    sprintf(histname,"hadc_p%d",i);
    hadc_v[i] = new TH1D(histname,"",1000,0,200.0);
  }

  // 2d hists -- why not
  std::vector< TH2D* > hshower_adc_v(3,0);
  for ( int i=0; i<3; i++ ) {
    char histname[50];
    sprintf(histname,"hshowerscore_v_adc_p%d",i);
    hshower_adc_v[i] = new TH2D(histname,"",200,0,200.0,200,0,1.0);
  }

  int nentries = io.get_n_entries();
  
  for (int ientry=0; ientry<nentries; ientry++) {
    io.read_entry(ientry);
    io_ssnet.read_entry(ientry);
    
    std::cout << "Entry " << ientry << std::endl;

    larcv::EventImage2D* ev_ssnetout_planes[3];
    for (int p=0; p<3; p++) {
      char branchname[20];
      sprintf( branchname, "uburn_plane%d", p );
      std::cout << "  get " << branchname << std::endl;
      ev_ssnetout_planes[p] = (larcv::EventImage2D*)io_ssnet.get_data( larcv::kProductImage2D, branchname );
    }
    std::cout << "  get wire image" << std::endl;
    larcv::EventImage2D* ev_img = (larcv::EventImage2D*)io.get_data( larcv::kProductImage2D, "wire" );

    // check events are aligned
    if ( io.event_id().run()!=io_ssnet.event_id().run() 
	 || io.event_id().run()!=io_ssnet.event_id().run() 
	 || io.event_id().run()!=io_ssnet.event_id().run() ) {
      throw std::runtime_error("entries from ssnet and supera do not agree in (run,subrun,event) index");
    }
    
    for (int p=0; p<3; p++) {
      if ( ev_ssnetout_planes[p]->Image2DArray().size()==0 )
	continue;
      const larcv::Image2D& showerimg = ev_ssnetout_planes[p]->Image2DArray()[0];
      const larcv::Image2D& trackimg  = ev_ssnetout_planes[p]->Image2DArray()[1];
      const larcv::Image2D& adcimg    = ev_img->Image2DArray()[p];
      const larcv::ImageMeta& meta    = showerimg.meta();

      TH2D* h2score = nullptr;
      TH2D* h2adc   = nullptr;
      if ( save_event_vis ) {
	char name[100];
	sprintf(name, "h2score_%d_p%d", ientry, p );
	h2score = new TH2D( name, "Score hits above threshod", 
			    meta.cols(), meta.min_x(), meta.max_x(), 
			    meta.rows(), meta.min_y(), meta.max_y() );
	sprintf(name, "h2adc_%d_p%d", ientry, p );
	h2adc   = new TH2D( name, "ADC values above threshold", 
			    meta.cols(), meta.min_x(), meta.max_x(),
			    meta.rows(), meta.min_y(), meta.max_y() );

      }
      
      float nshower = 0;
      float nabovethresh = 0.;

      for (int r=0; r<(int)meta.rows(); r++) {
	for ( int c=0; c<(int)meta.cols(); c++) {

	  int t = meta.pos_y( r );
	  int w = meta.pos_x( c );
	  float val = adcimg.pixel( adcimg.meta().row(t), adcimg.meta().col(w) )*scale_factors[p];
	  if (val>10.0) {
	    nabovethresh += 1.0;
	    hshower_v[p]->Fill( showerimg.pixel(r,c) );
	    htrack_v[p]->Fill(  trackimg.pixel(r,c) );
	    if ( showerimg.pixel(r,c)>0.5 )
	      nshower += 1.0;
	    if ( save_event_vis ) {
	      h2score->SetBinContent( c+1, r+1, showerimg.pixel(r,c) );
	      h2adc->SetBinContent( c+1, r+1, val );
	    }
	    hshower_adc_v[p]->Fill( val, showerimg.pixel(r,c) );
	  }
	  if ( val>0 )
	    hadc_v[p]->Fill( val );

	  // if ( save_event_vis ) {
	  //   h2score->SetBinContent( c+1, r+1, showerimg.pixel(r,c) );
	  // }

	}
      }//end of row loop
      
      if ( nabovethresh>0 ) {
	hfracshower_v[p]->Fill( nshower/nabovethresh );
      }
      

      tfile.cd();
      if ( save_event_vis && nshower<=1.0 ) {
	std::cout << "entry " << ientry << " p=" << p << " has nshower=" << nshower << " and nabovethresh=" << nabovethresh << std::endl;
	h2adc->Write();
	h2score->Write();
	
	delete h2adc;
	delete h2score;
      }

    }//end of plane loop
  }//end of entry loop
  
  tfile.Write();
  
  return 0;
}
