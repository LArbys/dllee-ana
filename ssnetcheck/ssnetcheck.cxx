#include <iostream>
#include <string>

#include "DataFormat/IOManager.h"
#include "DataFormat/EventImage2D.h"
#include "ROOTUtil/ROOTUtil.h"

#include "TApplication.h"
#include "TCanvas.h"
#include "TH1D.h"
#include "TH2D.h"
#include "TStyle.h"

int main( int nargs, char** argv ) {

  gStyle->SetOptStat(0);

  std::cout << "SSNet Check" << std::endl;
  std::vector<std::string> input_v;
  for ( int i=1; i<nargs; i++ )
    input_v.push_back( std::string(argv[i]) );
  bool make_images = true;

  larcv::IOManager io( larcv::IOManager::kREAD );
  for ( auto const& input : input_v )
    io.add_in_file( input );
  io.initialize();

  int nentries = io.get_n_entries();
  nentries = 1;

  std::cout << "number of entries: " << nentries << std::endl;
  TApplication app( "app", &nargs, argv );
  
  struct SSNetMetric_t {
    int abovethresh[3];         // all above threshold
    int abovethresh_correct[3]; // w/ label    
    int abovethresh_nolabel[3];
    int belowthresh[3];    
    int belowthresh_wlabel[3];
    int belowthresh_correct[3]; // no label
    SSNetMetric_t() {
      memset(abovethresh,        0,sizeof(int)*3);
      memset(abovethresh_correct,0,sizeof(int)*3);      
      memset(abovethresh_nolabel,0,sizeof(int)*3);

      memset(belowthresh,        0,sizeof(int)*3);      
      memset(belowthresh_wlabel, 0,sizeof(int)*3);
      memset(belowthresh_correct,0,sizeof(int)*3);      
    };
  };
  
  SSNetMetric_t ssnetpix;



  for (int ientry=0; ientry<nentries; ientry++ ) {
    io.read_entry(ientry);

    // get the event data
    auto ev_adc     = (larcv::EventImage2D*)io.get_data( larcv::kProductImage2D, "wire" );
    auto ev_segment = (larcv::EventImage2D*)io.get_data( larcv::kProductImage2D, "segment" );

    // make pointers and containers for visualization objects
    TCanvas* c1 = nullptr;
    if ( make_images ) {
      c1 = new TCanvas("c1","c1",1200,800);
      c1->Divide( 3, 2 );
    }
    // images: for each plane
    std::vector<TH1D*>  hadc_v;    
    std::vector<TH2D*>  hcheck_v;

    // loop over each plane
    for ( size_t p=0; p<3; p++ ) {

      // get adc plane and meta
      auto const& img  = ev_adc->Image2DArray()[p];
      auto const& meta = img.meta();

      // get segment image and meta
      auto const& seg  = ev_segment->Image2DArray()[p];

      // make image objects
      TH2D* hadc   = nullptr;
      TH2D* hcheck = nullptr;
      if ( make_images ) {
        char adcname[40];
        sprintf( adcname, "hadc_p%d", (int)p );
        char adcname2[40];
        sprintf( adcname2, "hadc_src_p%d", (int)p );
        hadc = (TH2D*)larcv::as_th2d( img, adcname2 ).Clone( adcname );

        char checkname[40];
        sprintf( checkname, "hcheck_p%d", (int)p );
        hcheck = (TH2D*)hadc->Clone( checkname );
        hcheck->Reset();
      }

      for ( int row=0; row<(int)meta.rows(); row++ ) {
        for ( int col=0; col<(int)meta.cols(); col++ ) {

          float adc    = img.pixel(row,col);
          int   label  = seg.pixel(row,col);
          
          if ( adc<10.0 ) {
            // pixel below threshold
            ssnetpix.belowthresh[p]++;
            if ( label<=0 ) {
              ssnetpix.belowthresh_correct[p]++;
              hcheck->SetBinContent( col+1, row+1,  0.1 );
            }
            else {
              hcheck->SetBinContent( col+1, row+1, -0.1 );
            }
          }
          else {
            // pixel above threshold
            ssnetpix.abovethresh[p]++;
            if ( label<=0 ) {
              hcheck->SetBinContent( col+1, row+1, -1.0 );              
              ssnetpix.abovethresh_nolabel[p]++;
            }
            else {
              hcheck->SetBinContent( col+1, row+1,  1.0 );
              ssnetpix.abovethresh_correct[p]++;
            }
          }
        }//end of col loop
      }//end of row loop
        
      if ( make_images ) {
        c1->cd( p+1 );
        hadc->Draw("colz");
        c1->cd( p+3+1 );
        hcheck->Draw("colz");
      }      
    }//end of plane (3) loop

    // view, save to png, and clean
    if ( make_images ) {
      char canvname1[50];
      sprintf( canvname1, "centry%d_ssnetcheck.pdf", (int)ientry );
      c1->Update();
      c1->Draw();
      c1->SaveAs(canvname1);
      
      std::cout << "entry done" << std::endl;
      std::cout << "[enter] to continue" << std::endl;
      std::cin.get();

    
      for ( auto& hadc : hadc_v )
        delete hadc;
      hadc_v.clear();

      for ( auto& hcheck : hcheck_v )
        delete hcheck;
      hcheck_v.clear();

      delete c1;
    }//if make_images
    
  }//end of entry loop

  // std::cout << "summary" << std::endl;
  // for ( size_t i=0; i<6; i++ ) {
  //   std::cout << "flow[" << i << "] ----------------" << std::endl;
  //   std::cout << "num abovethresh source pixels: " << npixels_abovethreshold[i] << std::endl;
  //   std::cout << "num flow to charge: "  << npixels_flow2charge[i] << " (" << float(npixels_flow2charge[i])/float(npixels_abovethreshold[i]) << ")" << std::endl;
  //   std::cout << "num flow to zero: "    << npixels_flow2zero[i] << " (" << float(npixels_flow2zero[i])/float(npixels_abovethreshold[i]) << ")" << std::endl;
  //   std::cout << "num flow to sub-thresh: " << npixels_flow2subthresh[i] << " (" << float(npixels_flow2subthresh[i])/float(npixels_abovethreshold[i]) << ")" << std::endl;
  //   std::cout << "num with no-flow: " << npixels_noflow[i] << " (" << float(npixels_noflow[i])/float(npixels_abovethreshold[i]) << ")" << std::endl;
  //   std::cout << "num belowthresh w/ flow: " << npixels_belowthreshold_wflow[i] << std::endl;
  // }

  
  return 0;
}
