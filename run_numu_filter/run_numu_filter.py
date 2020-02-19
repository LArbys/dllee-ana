import os,sys,argparse

parser = argparse.ArgumentParser("wrapper to run_filter binary")
parser.add_argument("--input",   "-i", required=True,type=str,help="Input DL merged file")
parser.add_argument("--sample",  "-s", required=True,type=str,help="Sample Type")
parser.add_argument("--datatype","-t", required=True,type=str,help="Data Type")
parser.add_argument("--out-dir", "-od",required=True,type=str,help="Output Directory")

args = parser.parse_args()

basename = os.path.basename(args.input)
run = int(basename.split("-")[-2][len("Run"):])
subrun = int(basename.split("-")[-1].split(".")[0][len("SubRun"):])

outputfile = "numufilterana-%s-Run%06d-SubRun%06d.root"%(args.sample,run,subrun)
larcvout   = "dlreco_filtered_larcv-%s-Run%06d-SubRun%06d.root"%(args.sample,run,subrun)
larliteout = "dlreco_filtered_larlite-%s-Run%06d-SubRun%06d.root"%(args.sample,run,subrun)
merged     = "merged_dlreco_filtered-%s-Run%06d-SubRun%06d.root"%(args.sample,run,subrun)


beamwin_start = { "bnb":190,
                  "ext":215,
                  "overlay":210 }
if args.datatype not in beamwin_start.keys():
    raise ValueError("data type ({}) given not valid. options: {}".format(args.datatype,beamwin_start.keys()))

command = "run_filter %s %s %s %s %d"%(args.input, outputfile, larcvout, larliteout, beamwin_start[args.datatype])
os.system(command)
os.system("/usr/local/root/root-6.16.00/bin/./hadd -f %s/%s %s %s %s"%(args.out_dir,merged,outputfile,larcvout,larliteout))
