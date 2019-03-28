#include <iostream>

// ROOT
#include "TFile.h"
#include "TTree.h"
#include "TH2D.h"
#include "TCanvas.h"
#include "TStyle.h"
#include "TGraph.h"

// larlite
#include "DataFormat/storage_manager.h"
#include "DataFormat/hit.h"
#include "LArUtil/LArProperties.h"

// larcv
#include "larcv/core/DataFormat/IOManager.h"
#include "larcv/core/DataFormat/EventImage2D.h"

/**
 * purpose of this program is to quantifying the image pixel-ADC values
 * we do this by taking reco2d gaushits, projecting the peak location of hits
 * onto the image, and recording the AC value at the peak pixel location.
 *
 * we make an adc histogram for each event, and find the peak which we record in a tree.
 * a histogram totaling over the whole file is also saved.
 * these are hadded.
 *
 */
int main( int nargs, char** argv ) {

  gStyle->SetOptStat(0);

  std::string input_larcv  = argv[1];
  std::string input_reco2d = argv[2];
  std::string output_hist  = argv[3];
  std::string mccversion   = "mcc8";
  bool make_image    = false;

  // input larcv
  larcv::IOManager iolarcv( larcv::IOManager::kREAD, "", larcv::IOManager::kTickBackward );
  iolarcv.add_in_file( input_larcv );
  iolarcv.initialize();

  larlite::storage_manager iolarlite( larlite::storage_manager::kREAD );
  iolarlite.add_in_filename( input_reco2d );
  iolarlite.open();

  TFile fout( output_hist.c_str(), "new" ); // do not rewrite

  // output is a histogram of the pixel distribution
  // not saving a tree, because presumably, the number of pixels is too large
  // maybe its not

  TTree tpix("pixamp","PixelAmpTree"); // entry per hit
  float pixamp_fromhist[3];
  int run, subrun, event;
  tpix.Branch("run",    &run,    "run/I");
  tpix.Branch("subrun", &subrun, "subrun/I");
  tpix.Branch("event",  &event,  "event/I");
  tpix.Branch("pixamp",pixamp_fromhist,"pixamp[3]/F");

  const float driftv = larutil::LArProperties::GetME()->DriftVelocity();

  TH1D* hfile[3];
  TH1D* hevent[3];
  for ( int p=0; p<3; p++ ) {
    char histname_file[100];
    sprintf(histname_file,"hpixamp_plane%d",p);
    char histname_event[100];
    sprintf(histname_event,"hpixamp_event_plane%d",p);

    hfile[p]  = new TH1D(histname_file, "",500,0,500);
    hevent[p] = new TH1D(histname_event,"",500,0,500);
  }

  int nentries = iolarcv.get_n_entries();
  for (int i=0; i<nentries; i++) {
    iolarcv.read_entry(i);
    iolarlite.go_to(i);

    std::cout << "entry " << i << std::endl;

    for ( int p=0; p<3; p++ ) hevent[p]->Reset();
    
    auto ev_hit = (larlite::event_hit*)iolarlite.get_data( larlite::data::kHit, "gaushit" );
    auto ev_img = (larcv::EventImage2D*)iolarcv.get_data( larcv::kProductImage2D, "wire" );

    std::cout << "  number of hits   = " << ev_hit->size() << std::endl;
    std::cout << "  number of images = " << ev_img->Image2DArray().size() << std::endl;

    
    // auto const& p2meta = ev_img->Image2DArray().at(2).meta();
    // TH2D* hp2 = nullptr;
    // if ( make_image ) {
    //   hp2 = new TH2D("p2","",p2meta.cols(),p2meta.min_x(),p2meta.max_x(),p2meta.rows(),p2meta.min_y(),p2meta.max_y());

    //   for (int r=0; r<p2meta.rows(); r++) {
    // 	for (int c=0; c<p2meta.cols(); c++) {
    // 	  hp2->SetBinContent( c+1, p2meta.rows()-1-r+1, ev_img->Image2DArray().at(2).pixel(r,c) );
    // 	}
    //   }
      
    //   TCanvas c("c","c",1200,600);
    //   hp2->Draw("colz");
    //   c.Update();
    //   c.SaveAs("test_nohits.png");
    // }

    // TGraph ghit( ev_hit->size() );
    // ghit.SetMarkerStyle(20);
    // ghit.SetMarkerSize(0.3);


    int ihit=0;
    for ( auto const& hit : *ev_hit ) {
      // for each hit, we get its pixel value at the peak amplitude
      int planeid = (int)hit.WireID().Plane;
      int wireid  = (int)hit.WireID().Wire;

      int   hitamp  = hit.PeakAmplitude();
      float peak_us = hit.PeakTime(); // usec from trigger?
      float tick    = peak_us;
      if ( mccversion=="mcc9" )
	tick += 4800;
      else if ( mccversion=="mcc8" )
	tick += 2400;

      
      auto const& img = ev_img->Image2DArray().at( planeid );
      auto const& meta = img.meta();
      //std::cout << "planeid=" << planeid << " peak_us=" << peak_us << " -> tick=" << tick << " meta=[" << meta.min_y() << "," << meta.max_y() << ")" << std::endl;
      
      if ( tick <= meta.min_y() || tick >=meta.max_y() )
	continue;
      
      int row = meta.row( tick );
      int col = meta.col( wireid );
      float pixamp = img.pixel( row, col );

      // if ( make_image ) {
      // 	if ( planeid==2 ) {
      // 	  ghit.SetPoint( ihit, wireid, tick );
      // 	  ihit++;
      // 	}
      // }
      
      hevent[planeid]->Fill(pixamp);
      hfile[planeid]->Fill(pixamp);
      
    }

    // if ( make_image )
    //   ghit.Set(ihit);
    // if ( make_image ) {
    //   TCanvas c("c","c",1200,600);
    //   hp2->Draw("colz");
    //   ghit.Draw("P");
    //   c.Update();
    //   c.SaveAs("test.png");
    //   delete hp2;
    //   break;
    // }

    // get max bin amp
    for ( int p=0; p<3; p++ ) {
      pixamp_fromhist[p] = hevent[p]->GetBinCenter( hevent[p]->GetMaximumBin() );
    }
    
    run    = iolarcv.event_id().run();
    subrun = iolarcv.event_id().subrun();
    event  = iolarcv.event_id().event();

    tpix.Fill();

  }//end of entry loop
  for ( int p=0; p<3; p++ ) {
    delete hevent[p];
    hfile[p]->Write();
  }
  tpix.Write();

  fout.Close();

  
  return 0;
}
