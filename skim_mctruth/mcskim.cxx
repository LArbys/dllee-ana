#include <iostream>

// ROOT
#include "TFile.h"
#include "TTree.h"

// larlite
#include "DataFormat/storage_manager.h"
#include "DataFormat/mctruth.h"
#include "DataFormat/mctrack.h"
#include "DataFormat/mcshower.h"


int main( int nargs, char** argv ) {

  std::string input_mcinfo = argv[1];
  std::string output_skim  = argv[2];

  larlite::storage_manager io( larlite::storage_manager::kREAD );
  io.add_in_filename( input_mcinfo );
  io.open();

  TFile rskim( output_skim.c_str(), "recreate" );
  TTree tskim("mcskim","Skimmed MC information");
  int run,subrun,event;
  float x,y,z,t;
  float nuE;
  int nupdg;
  int l1p1; // is 1-l, 1-p final state
  
  tskim.Branch("run",&run,"run/I");
  tskim.Branch("subrun",&subrun,"subrun/I");
  tskim.Branch("event",&event,"event/I");
  tskim.Branch("x",&x,"x/F");
  tskim.Branch("y",&y,"y/F");
  tskim.Branch("z",&z,"z/F");
  tskim.Branch("t",&t,"t/F");
  tskim.Branch("nuE",&nuE,"nuE/F");
  tskim.Branch("nupdg",&nupdg,"nupdg/I");
  tskim.Branch("l1p1", &l1p1, "l1p1/I" );
  
  for (int ientry=0; ientry<io.get_entries(); ientry++ ) {
    io.go_to(ientry);
    
    run    = io.run_id();
    subrun = io.subrun_id();
    event  = io.event_id();

    auto ev_mctruth  = (larlite::event_mctruth*) io.get_data( larlite::data::kMCTruth,  "generator" );
    auto ev_mctrack  = (larlite::event_mctrack*) io.get_data( larlite::data::kMCTrack,  "mcreco" );
    auto ev_mcshower = (larlite::event_mcshower*)io.get_data( larlite::data::kMCShower, "mcreco" );

    // we extract neutrino energy
    // neutrino pdg
    // 1l1p
    // vertex

    for ( auto const& mctruth : *ev_mctruth) {
      std::cout << "mctruth origin: " << mctruth.Origin() << std::endl;
      for ( auto const& mcpart : mctruth.GetParticles() ) {
	std::cout << "  mcpart: "
		  << " status=" << mcpart.StatusCode()
		  << " pdg=" << mcpart.PdgCode() 
		  << " E=" << mcpart.Trajectory().front().E() 
		  << " vtx=(" << mcpart.Trajectory().front().X() << "," << mcpart.Trajectory().front().Y() << "," << mcpart.Trajectory().front().Z() << ")"
		  << " t=" << mcpart.Trajectory().front().T()
		  << std::endl;
      }
    }


    
  }
  
  return 0;
};
