import os,sys

OUTDIR="/cluster/kappa/90-days-archive/wongjiradlab/twongj01/dllee-ana/skim_mctruth/outdir/"

INPUTLIST="/cluster/kappa/90-days-archive/wongjiradlab/twongj01/dllee-ana/skim_mctruth/inputlists/mcc9tag2_nueintrinsic_corsika_dlcosmictaggood.list"
RUNLIST="/cluster/kappa/90-days-archive/wongjiradlab/twongj01/dllee-ana/skim_mctruth/rerunlists/mcc9tag2_nueintrinsic_corsika_dlcosmictaggood.list"

frun = open(RUNLIST,'r')
fout   = open("tmp.txt",'w')

runfiles = frun.readlines()
print "number of files made: ",len(runfiles)
frun.close()

nleft = 0
for f in runfiles:
    f = f.strip()
    base = os.path.basename(f).replace("reco2d","mcskim")
    outname = OUTDIR + "/" + base
    if os.path.exists(outname):
        print "found ",outname
        continue
    else:
        print "RUN: ",outname
        print >> fout,f
        nleft += 1
fout.close()

print "number of files to run: ",nleft
os.system("mv tmp.txt %s"%(RUNLIST))
