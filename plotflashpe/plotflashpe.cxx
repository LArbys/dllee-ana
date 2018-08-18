#include <iostream>
#include <vector>
#include <string>
#include <fstream>

#include "TFile.h"
#include "TTree.h"

// larcv
#include "DataFormat/IOManager.h"
#include "DataFormat/EventROI.h"
#include "Base/LArCVBaseUtilFunc.h"
#include "Base/PSet.h"

// larlite
#include "DataFormat/opflash.h"
#include "DataFormat/user_info.h"

#include "Base/DataCoordinator.h"

int main( int nargs, char** argv ) {

  std::cout << "Filter by CROI" << std::endl;

  std::string outname = "output_plotflashpe.root";
  outname  = argv[1];

  larcv::PSet cfg = larcv::CreatePSetFromFile("io.cfg");
  larcv::PSet pset = cfg.get<larcv::PSet>("IOConfig");
  std::string ssnet_flist = pset.get<std::string>("SSNetFilelist");
  std::string opreco_flist = pset.get<std::string>("OpRecoFilelist");
  
  larlitecv::DataCoordinator dataco;
  dataco.configure( "io.cfg", "IOManager", "StorageManager", "IOConfig" );
  dataco.set_filelist( ssnet_flist,  "larcv" );
  dataco.set_filelist( opreco_flist, "larlite" );
  dataco.initialize();
  std::cout << "initialized." << std::endl;

  int nentries = dataco.get_nentries("larcv");
  std::cout << "Number of entries: " << nentries << std::endl;

  TFile out(outname.c_str(), "recreate" );

  // tree for all beam opflashes
  TTree tree("flashtree", "Info for all flashes" );
  int   flashtick; //tick
  int   flashbeam; //is beamflash
  float flashpe;   //pe
  tree.Branch( "flashbeam", &flashbeam, "flashbeam/I" );
  tree.Branch( "flashtick", &flashtick, "flashtick/I" );
  tree.Branch( "flashpe", &flashpe, "flashpe/F" );

  TTree evtree("eventtree", "In-time flash + Precut info");
  int   run, subrun, event;
  int   numcroi;
  int   precutpass;
  int   intime_hasflash;
  int   intime_flashtick;
  float intime_flashpe;
  float intime_flashy;
  float intime_flashz;
  int   num_intime;
  evtree.Branch( "run",    &run,    "run/I");
  evtree.Branch( "subrun", &subrun, "subrun/I");
  evtree.Branch( "event",  &event,  "event/I");
  evtree.Branch( "numcroi", &numcroi, "numcroi/I" );
  evtree.Branch( "precutpass", &precutpass, "precutpass/I");
  evtree.Branch( "intime_hasflash",  &intime_hasflash,  "intime_hasflash/I");
  evtree.Branch( "intime_flashtick", &intime_flashtick, "intime_flashtick/I");
  evtree.Branch( "intime_flashpe", &intime_flashpe, "intime_flashpe/F");
  evtree.Branch( "intime_flashy",  &intime_flashy,  "intime_flashy/F");
  evtree.Branch( "intime_flashz",  &intime_flashz,  "intime_flashz/F");
  evtree.Branch( "num_intime",     &num_intime,     "num_intime/I" );
  
  for ( int ientry=0; ientry<nentries; ientry++ ) {
    dataco.goto_entry( ientry,  "larcv" );
    
    larcv::EventROI* ev_croimerged     = (larcv::EventROI*)       dataco.get_larcv_data(   larcv::kProductROI, "croi" );
    larlite::event_opflash* ev_opflash_beam   = (larlite::event_opflash*)dataco.get_larlite_data( larlite::data::kOpFlash,  "simpleFlashBeam" );
    larlite::event_opflash* ev_opflash_cosmic = (larlite::event_opflash*)dataco.get_larlite_data( larlite::data::kOpFlash,  "simpleFlashCosmic" );
    larlite::event_user*  ev_precut_info       = (larlite::event_user*)   dataco.get_larlite_data( larlite::data::kUserInfo, "precutresults" );
    bool hasprecut = true;
    if ( !ev_precut_info ) {
      std::cout << "No precut info" << std::endl;
      hasprecut = false;
    }

    run    = dataco.run();
    subrun = dataco.subrun();
    event  = dataco.event();

    // flash tree
    intime_hasflash = 0;
    num_intime = 0;
    intime_flashpe = -1;
    intime_flashtick = -1;
    intime_flashy = -200;
    intime_flashz = -200;
    for ( auto const& flash : *ev_opflash_beam ) {
      flashbeam = 1;
      flashtick = flash.Time()/0.015625;
      flashpe   = flash.TotalPE();
      tree.Fill();

      if ( intime_hasflash==0 && flashtick>=200 && flashtick<=350 ) { // overlay bounds
      //if ( flashtick>=180 && flashtick<=330 ) { // bnb or mc bounds
	num_intime++;
	if ( intime_hasflash==0 ) {
	  intime_hasflash  = 1;
	  intime_flashpe   = flashpe;
	  intime_flashtick = flashtick;
	  intime_flashy    = flash.YCenter();
	  intime_flashz    = flash.ZCenter();
	}
      }
    }
    for ( auto const& flash : *ev_opflash_cosmic ) {
      flashbeam = 0;
      flashtick = flash.Time()/0.015625;
      flashpe   = flash.TotalPE();
      tree.Fill();
    }

    auto const& croimerged_v  = ev_croimerged->ROIArray();
    numcroi = croimerged_v.size();

    precutpass = 0;
    if ( hasprecut )
      precutpass = ev_precut_info->front().get_int( "pass" );
    
    evtree.Fill();
  }
  
  dataco.close();

  tree.Write();
  evtree.Write();
  
  return 0;
}
