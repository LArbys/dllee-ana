import os,sys

# we make a list of run,subruns that we are trying to run from the input list
# we then make a list of run,subruns of successfully generated check files
# then we dump out a new input list of the remaining runs

dataset="mcc9jan_bnb5e19"

fin = open("inputlists/supera_list_%s_good_ssnetserver_files.txt"%(dataset),'r')
readin = fin.readlines()

rse_input = []
rse_filemap = {}
for l in readin:
    run = int(l.split()[0])
    subrun = int(l.split()[1])
    
    rse_input.append( (run,subrun) )
    rse_filemap[(run,subrun)] = l.split()[2].strip()

resultfiles = os.listdir("resultfiles")

rse_input.sort()
foundlist = []
notfound  = []
for (run,subrun) in rse_input:
    rfile = "run%d_subrun%d.out"%(run,subrun)
    if rfile in resultfiles:
        foundlist.append( (run,subrun) )
    else:
        notfound.append( (run,subrun) )

print "Number remaining: ",len(notfound)
frerun = open("rerunlists/rerun_supera_list_%s_good_ssnetserver_files.txt"%(dataset), 'w')
for (run,subrun) in notfound:
    print>>frerun,"%d %d %s"%(run,subrun,rse_filemap[(run,subrun)])
frerun.close()
