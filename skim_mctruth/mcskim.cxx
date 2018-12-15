#include <iostream>

// ROOT
#include "TFile.h"
#include "TTree.h"

// larlite
#include "DataFormat/storage_manager.h"
#include "DataFormat/mctruth.h"
#include "DataFormat/mctrack.h"
#include "DataFormat/mcshower.h"
#include "LArUtil/LArProperties.h"


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
  float tick;
  float nuE;
  int nupdg;
  int l1p1; // is 1-l, 1-p final state
  int nlepton_abovethresh = 0;
  int nlepton = 0;
  int nproton_abovethresh = 0;
  int nproton = 0;
  int nother_abovethresh = 0;
  float maxleptonKEmev;
  float maxprotonKEmev;
  int mode = 0;
  int ccnc = 0;
  int nuancecode = 0;
  float q2;
  
  tskim.Branch("run",&run,"run/I");
  tskim.Branch("subrun",&subrun,"subrun/I");
  tskim.Branch("event",&event,"event/I");
  tskim.Branch("ccnc",&ccnc,"ccnc/I");
  tskim.Branch("mode",&mode,"mode/I");
  tskim.Branch("nuancecode",&nuancecode,"nuancecode/I");
  tskim.Branch("nupdg",&nupdg,"nupdg/I");
  tskim.Branch("nlepton", &nlepton, "nlepton/I");
  tskim.Branch("nproton", &nproton, "nproton/I");
  
  tskim.Branch("nlepton_abovethresh", &nlepton_abovethresh, "nlepton_abovethresh/I");
  tskim.Branch("nproton_abovethresh", &nproton_abovethresh, "nproton_abovethresh/I");
  tskim.Branch("nother_abovethresh",  &nother_abovethresh,  "nother_abovethresh/I");
  tskim.Branch("l1p1", &l1p1, "l1p1/I" );
  tskim.Branch("x",&x,"x/F");
  tskim.Branch("y",&y,"y/F");
  tskim.Branch("z",&z,"z/F");
  tskim.Branch("t",&t,"t/F");
  tskim.Branch("q2",&q2,"q2/F");
  tskim.Branch("maxleptonKEmev",&maxleptonKEmev,"maxleptonKEmev/F");
  tskim.Branch("maxprotonKEmev",&maxprotonKEmev,"maxprotonKEmev/F");
  tskim.Branch("nuEmev",&nuE,"nuEmev/F");


  const float driftv_cm_per_us = larutil::LArProperties::GetME()->DriftVelocity();
  
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
    bool nufilled = false;
    nlepton = 0;
    nproton = 0;
    nlepton_abovethresh = 0;
    nproton_abovethresh = 0;
    nother_abovethresh = 0;
    maxleptonKEmev = 0;
    maxprotonKEmev = 0;
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
	if ( !nufilled && mcpart.StatusCode()==0 && 
	     ( abs(mcpart.PdgCode())==12 || abs(mcpart.PdgCode())==14 || abs(mcpart.PdgCode())==16 ) ) {
	  // input neutrino
	  nupdg = mcpart.PdgCode();
	  nuE = mcpart.Trajectory().front().E()*1000.0; // save in mev
	  x =  mcpart.Trajectory().front().X();
	  y =  mcpart.Trajectory().front().Y();
	  z =  mcpart.Trajectory().front().Z();
	  t =  mcpart.Trajectory().front().T();

	  ccnc = mctruth.GetNeutrino().CCNC();
	  mode = mctruth.GetNeutrino().Mode();
	  nuancecode = mctruth.GetNeutrino().InteractionType();
	  q2   = mctruth.GetNeutrino().QSqr();
	  nufilled = true;
	}

	float ke = (mcpart.Trajectory().front().E() - mcpart.Mass())*1000.0;
	if ( mcpart.StatusCode()==1 ) {
	  // final state particles
	  float ke = (mcpart.Trajectory().front().E() - mcpart.Mass())*1000.0;
	  if ( abs(mcpart.PdgCode())==11 ) {
	    nlepton++;
	    if ( ke>35.0 )
	      nlepton_abovethresh++;
	    if ( ke>maxleptonKEmev ) {
	      maxleptonKEmev = ke;
	    }

	  }
	  else if ( abs(mcpart.PdgCode())==2212 ) {
	    nproton++;
	    if ( ke>35.0 )
	      nproton_abovethresh++;
	    if ( ke>maxprotonKEmev ) {
	      maxprotonKEmev = ke;
	    }

	  }
	  else {
	    if(ke>35.0)
	      nother_abovethresh++;
	  }
	}//end of if final state
      }//end of particle loop
    }//end of mctruth loop

    if ( nlepton_abovethresh==1 && nproton_abovethresh==1 && nother_abovethresh==0)
      l1p1 = 1;
    else
      l1p1 = 0;

    tskim.Fill();
    
  }

  tskim.Write();
  
  return 0;
};
