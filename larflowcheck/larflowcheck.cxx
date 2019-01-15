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

  std::cout << "LArFlow Check" << std::endl;
  std::string input = argv[1];
  bool make_images = true;

  larcv::IOManager io( larcv::IOManager::kREAD );
  io.add_in_file( input );
  io.initialize();

  int nentries = io.get_n_entries();
  nentries = 1;

  std::cout << "number of entries: " << nentries << std::endl;
  TApplication app( "app", &nargs, argv );

  int source_planes[6] = { 0, 0, 1, 1, 2, 2 };  
  int target_planes[6] = { 1, 2, 0, 2, 0, 1 };

  int npixels_abovethreshold[6] = {0};
  int npixels_noflow[6]         = {0};
  int npixels_flow2dead[6]      = {0};
  int npixels_flow2charge[6]    = {0}; // [10-)  
  int npixels_flow2zero[6]      = {0}; // [0]
  int npixels_flow2subthresh[6] = {0}; // (0-10)

  int npixels_belowthreshold_wflow[6] = {0};
  
  for (int ientry=0; ientry<nentries; ientry++ ) {
    io.read_entry(ientry);

    // get the event data
    auto ev_adc     = (larcv::EventImage2D*)io.get_data( larcv::kProductImage2D, "wire" );
    auto ev_larflow = (larcv::EventImage2D*)io.get_data( larcv::kProductImage2D, "larflow" );

    // make pointers and containers for visualization objects
    TCanvas* c1 = nullptr;
    TCanvas* c2 = nullptr;
    TCanvas* c3 = nullptr;
    if ( make_images ) {
      c1 = new TCanvas("c1","c1",1200,1200);
      c1->Divide( 3, 3 ); // {flow},{src,target,src->target}
      c2 = new TCanvas("c2","c2",1200,1200);
      c2->Divide( 3, 3 ); // {flow},{src,target,src->target}
      c3 = new TCanvas("c3","c3",1200,400);
      c3->Divide( 3, 1 ); // for each source plane, we histogram adc values for good and bad pixels
    }
    std::vector<TH2D*>  hsource_v;
    std::vector<TH2D*>  htarget_v;
    std::vector<TH2D*>  hflow_v;
    std::vector<TH1D*>  hadc_v;

    // loop over each (source) plane
    for ( size_t p=0; p<3; p++ ) {

      // get source plane and meta
      auto const& img  = ev_adc->Image2DArray()[p];
      auto const& meta = img.meta();

      // get target adc images
      auto const& target1 = ev_adc->Image2DArray()[ target_planes[2*p] ];
      auto const& target2 = ev_adc->Image2DArray()[ target_planes[2*p+1] ];

      // get the flow images
      auto const& flow1 = ev_larflow->Image2DArray()[2*p];
      auto const& flow2 = ev_larflow->Image2DArray()[2*p+1];
      
      // confirm the flow
      //std::cout << "plane[" << p << "] --> tar1 plane[ " << target_planes[2*p] << "]" << std::endl;
      //std::cout << "plane[" << p << "] --> tar2 plane[ " << target_planes[2*p+1] << "]" << std::endl;      

      // make image objects
      TH2D* hsource = nullptr;
      TH2D* htarget1 = nullptr;
      TH2D* htarget2 = nullptr;
      TH2D* hflow1   = nullptr;
      TH2D* hflow2   = nullptr;
      TH1D* hadc_good = nullptr;
      TH1D* hadc_wadc_noflow = nullptr;
      TH1D* hadc_noadc_wflow = nullptr;
      if ( make_images ) {
        char srcname[15];
        sprintf( srcname, "hsource%d", (int)p );
        hsource = (TH2D*)larcv::as_th2d( img, "src" ).Clone(srcname);
        hsource->Reset(); // clear so we can draw in it
        hsource->SetTitle("10:noadc/wflow 20:adc/noflow 30:wadc/wflow");
      
        char tar1name[15];
        char tar2name[15];
        sprintf( tar1name, "htarget1_p%d", (int)p );
        sprintf( tar2name, "htarget2_p%d", (int)p );
        htarget1 = (TH2D*)larcv::as_th2d( target1, "tar1" ).Clone(tar1name);
        htarget2 = (TH2D*)larcv::as_th2d( target2, "tar2" ).Clone(tar2name);
        htarget1->SetTitle("target image");
        htarget2->SetTitle("target image");        
        
        char flow1name[15];
        char flow2name[15];      
        sprintf( flow1name, "hflow1_p%d", (int)p );
        sprintf( flow2name, "hflow2_p%d", (int)p );
        hflow1 = (TH2D*)htarget1->Clone(flow1name);
        hflow2 = (TH2D*)htarget2->Clone(flow2name);
        hflow1->Reset(); // clear to draw adc flow
        hflow2->Reset(); // clear to draw adc flow
        hflow1->SetTitle("src-to-target ADC. adc=0.5 if no adc @ src");
        hflow2->SetTitle("src-to-target ADC. adc=0.5 if no adc @ src");

        char adcname1[40];
        char adcname2[40];
        char adcname3[40];
        sprintf( adcname1, "hadc_good_p%d", (int)p );
        sprintf( adcname2, "hadc_wadc_noflow_p%d", (int)p );
        sprintf( adcname3, "hadc_noadc_wflow_p%d", (int)p );
        hadc_good = new TH1D( adcname1, adcname1, 100, 0, 100 );
        hadc_wadc_noflow = new TH1D( adcname2, adcname2, 100, 0, 100 );
        hadc_noadc_wflow = new TH1D( adcname3, adcname3, 100, 0, 100 ); 
      }

      for ( int row=0; row<(int)meta.rows(); row++ ) {
        for ( int col=0; col<(int)meta.cols(); col++ ) {

          float adc    = img.pixel(row,col);
          int dflow1 = flow1.pixel(row,col);
          int dflow2 = flow2.pixel(row,col);
          int flowcol1 = col + dflow1;
          int flowcol2 = col + dflow2;

          // mistakes we need to track
          // (1) has adc, no flow
          // (2) no adc,  has flow

          // mod hsource for flow1
          if ( adc<0.5 ) {
            if ( dflow1!=0 ) {
              npixels_belowthreshold_wflow[2*p]++;
              if ( make_images ) {
                hsource->SetBinContent( col+1, meta.rows()-row, 10 ); // no adc, has flow
                hadc_noadc_wflow->Fill( adc );
              }
            }
            else {
              if ( make_images )
                hsource->SetBinContent( col+1, meta.rows()-row, 0 );  // no adc, no flow (OK)
            }
            continue;
          }
          else {
            //std::cout << "[" << row << "," << col << "] adc=" << adc << std::endl;            
            if ( dflow1!=0 ) {
              if ( make_images ) {
                hsource->SetBinContent( col+1, meta.rows()-row, 30 ); // w adc, w flow
                hadc_good->Fill( adc );
              }
            }
            else {
              if ( make_images ) {
                hsource->SetBinContent( col+1, meta.rows()-row, 20 ); // w adc, no flow
                hadc_wadc_noflow->Fill(adc);
              }
            }
          }
            
          npixels_abovethreshold[2*p]++;
          npixels_abovethreshold[2*p+1]++;
          
          if ( flowcol1<0 || (flowcol1)>=meta.cols() ) {
            std::cout << "flow output of bounds src(" << row << "," << col << ") flow=" << dflow1
                      << " tar(" << row << "," << flowcol1 << ") ncols=" << meta.cols() << std::endl;
            continue;
          }
          if ( flowcol2<0 || (flowcol2)>=meta.cols() ) {
            std::cout << "flow output of bounds src(" << row << "," << col << ") flow=" << dflow2
                      << " tar(" << row << "," << flowcol2 << ") ncols=" << meta.cols() << std::endl;
            continue;
          }
          
          float flowpix1 = target1.pixel( row, flowcol1 );
          float flowpix2 = target2.pixel( row, flowcol2 );
          
          std::cout << "src[" << col << "] pix=" << adc << " flow1=" << dflow1 << " -> tar[" << flowcol1 << "] pix=" << flowpix1 << std::endl;
          std::cout << "src[" << col << "] pix=" << adc << " flow2=" << dflow2 << " -> tar[" << flowcol2 << "] pix=" << flowpix1 << std::endl;          

          if ( make_images ) {
            if ( flowpix1>=1.0 )
              hflow1->SetBinContent( flowcol1+1, meta.rows()-row,  adc ); // good
            else
              hflow1->SetBinContent( flowcol1+1, meta.rows()-row,  0.5 ); // mistake (src adc, no tar adc)
            
            if ( flowpix2>=1.0 )
              hflow2->SetBinContent( flowcol2+1, meta.rows()-row,  adc ); // good
            else
              hflow2->SetBinContent( flowcol2+1, meta.rows()-row,  0.5 ); // mistake (src adc, no tar adc)
          }

          if ( flowpix1>=1 )
            npixels_flow2charge[2*p]++;
          else if ( flowpix1<=0 )
            npixels_flow2zero[2*p]++;
          else if ( flowpix1>0 && flowpix1<1 )
            npixels_flow2subthresh[2*p]++;

          if ( flowpix2>=1 )
            npixels_flow2charge[2*p+1]++;
          else if ( flowpix2<=0 )
            npixels_flow2zero[2*p+1]++;
          else if ( flowpix2>0 && flowpix2<1 )
            npixels_flow2subthresh[2*p+1]++;
          
        }
      }//end of row loop

      if ( make_images ) {
        c1->cd( p+1 );
        hsource->Draw("colz");
        c1->cd( p+3+1 );
        htarget1->Draw("colz");
        c1->cd( p+6+1 );
        hflow1->Draw("colz");

        c2->cd( p+1 );
        hsource->Draw("colz");
        c2->cd( p+3+1 );
        htarget2->Draw("colz");
        c2->cd( p+6+1 );
        hflow2->Draw("colz");

        c3->cd(p+1);
        hadc_good->SetLineColor(kBlack);
        hadc_wadc_noflow->SetLineColor(kRed);
        hadc_noadc_wflow->SetLineColor(kBlue);
        hadc_wadc_noflow->Draw();
        hadc_noadc_wflow->Draw("same");
        hadc_good->Draw("same");
      
        hsource_v.push_back( hsource );
        htarget_v.push_back( htarget1 );
        htarget_v.push_back( htarget2 );
        hflow_v.push_back( hflow1 );
        hflow_v.push_back( hflow2 );
        hadc_v.push_back( hadc_good );
        hadc_v.push_back( hadc_wadc_noflow );
        hadc_v.push_back( hadc_noadc_wflow ); 
      }
      
    }//end of plane (3) loop

    // view, save to png, and clean
    if ( make_images ) {
      char canvname1[20];
      sprintf( canvname1, "centry%d_flow1.png", (int)ientry );
      c1->Update();
      c1->Draw();
      c1->SaveAs(canvname1);

      char canvname2[20];
      sprintf( canvname2, "centry%d_flow2.png", (int)ientry );    
      c2->Update();
      c2->Draw();
      c2->SaveAs(canvname2);

      char canvname3[40];
      sprintf( canvname3, "centry%d_adc.png", (int)ientry );
      c3->Update();
      c3->Draw();
      c3->SaveAs(canvname3);
      
      std::cout << "entry done" << std::endl;
      std::cout << "[enter] to continue" << std::endl;
      std::cin.get();

    
      for ( auto& hsrc : hsource_v )
        delete hsrc;
      hsource_v.clear();
      for ( auto& htar : htarget_v )
        delete htar;
      htarget_v.clear();
      for ( auto& hflow : hflow_v )
        delete hflow;
      hflow_v.clear();
      for ( auto& hadc : hadc_v )
        delete hadc;
      hadc_v.clear();

      delete c1;
      delete c2;
      delete c3;
    }//if make_images
    
  }//end of entry loop

  std::cout << "summary" << std::endl;
  for ( size_t i=0; i<6; i++ ) {
    std::cout << "flow[" << i << "] ----------------" << std::endl;
    std::cout << "num abovethresh source pixels: " << npixels_abovethreshold[i] << std::endl;
    std::cout << "num flow to charge: "  << npixels_flow2charge[i] << " (" << float(npixels_flow2charge[i])/float(npixels_abovethreshold[i]) << ")" << std::endl;
    std::cout << "num flow to zero: "    << npixels_flow2zero[i] << " (" << float(npixels_flow2zero[i])/float(npixels_abovethreshold[i]) << ")" << std::endl;
    std::cout << "num flow to sub-thresh: " << npixels_flow2subthresh[i] << " (" << float(npixels_flow2subthresh[i])/float(npixels_abovethreshold[i]) << ")" << std::endl;
    std::cout << "num with no-flow: " << npixels_noflow[i] << " (" << float(npixels_noflow[i])/float(npixels_abovethreshold[i]) << ")" << std::endl;
  }
  
  
  return 0;
}
