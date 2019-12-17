import os,sys

from dlreco_check import get_entries

filelist = sys.argv[1]

f = open(filelist,'r')

ll = f.readlines()

fout = open(filelist.replace(".list","_badlist.list"),'w')
f2out = open(filelist.replace(".list","_goodlist.list"),'w')

for l in ll:
    
    input_file = l.split('\t')[0].strip()
    output_file = l.split('\t')[1].strip()

    ok = True    
    try:
        input_entries  = get_entries(input_file)
        output_entries = get_entries(output_file)

        print "input: ",input_entries
        print "output: ",output_entries

        base_entries = input_entries["image2d_wire_tree"]
        print "base entries: ",base_entries
        for tname in ["image2d_wire_tree","pgraph_test_tree","track_trackReco_tree","shower_showerreco_tree"]:
            if input_entries[tname]!=base_entries or input_entries[tname] != output_entries[tname] or output_entries[tname]!=base_entries:
                ok = False
                print "error in ",tname
    except:
        ok = False

    print ok,output_file
    if not ok:
        print>>fout,output_file
    else:
        print>>f2out,input_file," ",output_file

