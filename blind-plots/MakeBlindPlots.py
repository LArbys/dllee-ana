from ROOT import TFile, TH1F
from sys import argv
import pickle
import numpy as np
from scipy.interpolate import interp1d

def PmuGivenX(mu,x):

    mu = mu.astype(float)
    pi  = np.pi
    c   = [1.,-1./12,1./288,139./51840,-571./2488320,-163879./209018880]
    
    try:
        poly = sum(c[i]/x**(i+0.5) for i in range(len(c)))
        return 1/np.sqrt(2*pi)*np.exp(x+x*np.log(mu/x)-mu)*poly
    except:
        return np.exp(-mu)
    
def GetErrors(xobs,CL=0.6827):
    
    step    = 0.01

    upperBoundary = int(max(10,xobs+5*np.sqrt(xobs)))
    r = np.arange(0.01,upperBoundary,step)  
    s    = PmuGivenX(r,xobs)*step
    PDF1 = interp1d(r,s,bounds_error=False,fill_value=0)
    PPF1 = interp1d(np.cumsum(s),r)
    
    xobs_low  = float(PPF1((1-CL)/2))
    xobs_high = float(PPF1(1-(1-CL)/2))

    return xobs_low,xobs_high

def GetShCons(evt):
    
    EU = evt.shower1_sumQ_U*0.0139 + 31.5
    EV = evt.shower1_sumQ_V*0.0143 + 35.7
    EY = evt.shower1_sumQ_Y*0.0125 + 13.8       
    
    return np.sqrt((EU-EV)**2 + (EU-EY)**2 + (EY-EV)**2)/EY



INPUT_FVV  = argv[1]
INPUT_FILE = TFile.Open(INPUT_FVV)
INPUT_TREE = INPUT_FILE.Get("dlana/FinalVertexVariables")
APPLY_BQ   = False
#Assume that the beam quality has been scraped into a pickle with format BeamQuality[(run,subrun,event)] = True/False
if APPLY_BQ:
    with open("BeamQualityFilter.pickle","wb") as handle: PassBeamQuality = pickle.load(handle)

TARGET_POT = float(argv[2])
KEEP_N     = 8#int(14*TARGET_POT / 1.0e20)
        
ChooseMe = {}
for event in INPUT_TREE:

    run = event.run
    sub = event.subrun
    evt = event.event
    vid = event.vtxid

    BDTscore = event.BDTscore_1e1p
    
    idx  = tuple((run,sub,evt))
    idxv = tuple((run,sub,evt,vid))

    if APPLY_BQ and not PassBeamQuality[idx]: continue
    if idx in ChooseMe and ChooseMe[idx] > BDTscore: continue
    ChooseMe[idx] = BDTscore

Variables = []
for event in INPUT_TREE:

    run = event.run
    sub = event.subrun
    evt = event.event
    vid = event.vtxid
    
    PassSimpleCuts  = event.PassSimpleCuts
    PassShowerReco  = event.PassShowerReco
    BDTscore        = event.BDTscore_1e1p
    pi0Mass         = event._pi0mass
    PIDmu           = event.MuonPID_int_v[2]
    PIDe            = event.EminusPID_int_v[2]
    PIDp            = event.ProtonPID_int_v[2]
    PIDgPix         = event.GammaPID_pix_v[2]
    PIDePix         = event.EminusPID_pix_v[2]
    ShrCons         = GetShCons(event)
    ElectronE       = event.Electron_Edep   
    ProtonE         = event.Proton_Edep   
    ProtonTh        = event.Proton_ThetaReco
    MaxShrFrac      = event.MaxShrFrac
    
    idx = tuple((run,sub,evt))
    if ChooseMe[idx] != BDTscore: continue
    if PassSimpleCuts == 0: continue
    if PassShowerReco == 0: continue
    if MaxShrFrac < 0.2: continue
    if ProtonE < 60 or ElectronE < 35: continue
    if pi0Mass > 50: continue
    if ProtonTh > np.pi/2: continue
    if ShrCons > 2: continue
    if ElectronE > 100 and PIDmu > 0.2: continue
    if PIDgPix / PIDePix > 2 : continue
                
    Variables.append([
        event.AlphaT_1e1p,
        event.PT_1e1p,
        event.PTRat_1e1p,
        event.Lepton_dQdx,
        event.Proton_dQdx,
        event.BjXB_1e1p,
        event.BjYB_1e1p,
        event.SphB_1e1p,
        event.Q0_1e1p,
        event.Q3_1e1p,
        event.ChargeNearTrunk,
        event.MinShrFrac,
        event.MaxShrFrac,
        event.Lepton_PhiReco,
        event.Proton_PhiReco,
        event.Proton_ThetaReco,
        event.OpenAng,
        event.Thetas,
        event.Phis,
        event.Proton_Edep,
        event.PzEnu_1e1p,
        event.Xreco,
        event.Yreco,
        event.Zreco,
        event.shower1_smallQ_Y/event.shower1_sumQ_Y,
        max(event.Proton_TrackLength,event.Lepton_TrackLength),
        PIDmu,
        PIDp,
        PIDe])

names = [
    r'$\alpha_T$',
    r'$p_T$',
    r'$p_T/p$',
    'Lepton dQ/dx',
    'Proton dQ/dx',
    'Bjorken X*',
    'Bjorken Y*',
    '2-Body Scattering Consistency',
    r'$Q_0$',
    r'$Q_3$',
    'Charge Near Vertex',
    'Proton Shower Fraction',
    'Electron Shower Fraction',
    r'Electron $\phi$',
    r'Proton $\phi$',
    r'Proton $\theta$',
    'Opening Angle',
    r'$\theta_p + \theta_e$',
    r'|$\phi_p - \phi_e$|',
    'Proton Deposited Energy',
    r'$p_z - E_\nu$',
    'Vertex X',
    'Vertex Y',
    'Vertex Z',
    r'Shower Charge in Image / Shower Charge in e$^-$ Cluster',
    'Length of Longest Track',
    'Muon MPID Score',
    'Proton MPID Score',
    'Electron MPID Score']

shortname = ['alphaT',
             'pT',
             'pToverp',
             'leptondqdx',
             'protondqdx',
             'bjorkenx',
             'bjorkeny',
             'twobodyconsistency',
             'q0',
             'q3',
             'vertexq',
             'protonshowerfrac',
             'electronshowerfrac',
             'electronphi',
             'protonphi',
             'protontheta',
             'openingangle',
             'sumtheta',
             'phidiff',
             'protonedep',
             'pzminusenu',
             'vertexx',
             'vertexy',
             'vertexz',
             'showerqratio',
             'longesttracklength',
             'mpidmuon',
             'mpidproton',
             'mpidelectron']
             

ranges = [
    (0,np.pi),
    (0,800),
    (0,1),
    (20,70),
    (30,120),
    (0,3),
    (0,1),
    (0,5000),
    (100,700),
    (0,1400),
    (0,800),
    (0,1),
    (0,1),
    (-np.pi,np.pi),
    (-np.pi,np.pi),
    (0,np.pi),
    (0,np.pi),
    (0,2*np.pi),
    (0,2*np.pi),
    (60,500),
    (-1500,300),
    (0,256),
    (-117,117),
    (0,1036),
    (0,2),
    (0,150),
    (0,0.2),
    (0,1),
    (0,1)]

np.random.shuffle(Variables)

NSELECT = min(len(Variables),KEEP_N)
Variables = Variables[0:NSELECT]

Nbins = 10

output = []
outroot = TFile("blindplothistograms.root","recreate")

for i,j in enumerate(names):

    
    # THIS WOULD REQUIRE MATPLOTLIB, ACTUALLY MAKES PLOTS
    #plt.clf()
    #plt.figure(figsize=(8,5))
    #plt.hist([x[i] for x in Variables],Nbins,ranges[i],color='blue',weights=[1.0/len(Variables)]*len(Variables))
    #plt.xlabel(names[i],fontsize=15)
    #plt.ylabel('Unit Normalized')
    #plt.grid(b=True, which='major', color='#666666', linestyle='-',alpha=0.17)
    #plt.minorticks_on()
    #plt.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.07)
    #plt.show()

    # THIS ONLY REQUIRES NUMPY AND DUMPS A HISTOGRAM TUPLE
    hist = TH1F("h{}".format(shortname[i]),j,10,ranges[i][0],ranges[i][1])
    for ev in Variables:
        hist.Fill( ev[i] )
    norm = 1.0/hist.Integral()            
    for i in xrange(10):
        binerr = max( GetErrors(hist.GetBinContent(i+1)) )
        binerr *= norm
        hist.SetBinError(i+1,binerr)
    hist.Scale(norm)

    
    hraw  = np.histogram([x[i] for x in Variables],bins=Nbins,range=ranges[i])
    errs  = np.asarray([GetErrors(x) for x in hraw[0]])
    norm  = 1.0/len(Variables)
    errs  = errs*norm
    
    thisHist = np.histogram([x[i] for x in Variables],bins=Nbins,range=ranges[i],weights=[1.0/len(Variables)]*len(Variables))
    outDict = {'name':'%s'%names[i],'bins':thisHist[1],'unitNormHeight':thisHist[0],'1sigConfBand':errs}

    output.append(outDict)
    hist.Write()

with open("BlindPlotHistogramData.pickle","wb") as handle: pickle.dump(output,handle)
outroot.Close()
