import os
import argparse

# Examples:
# python merge_ntuple.py DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/crab_testElectronMVA2018/181009_085005/0000 ~/data/Egamma/testElectronMVA2018.root
# python merge_ntuple.py DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/crab_testElectronMVA2017/181009_085327/0000 ~/data/Egamma/testElectronMVA2017.root
# python merge_ntuple.py DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/crab_testElectronMVA2016/181009_085138/0000 ~/data/Egamma/testElectronMVA2016.root

parser = argparse.ArgumentParser(description='Submit crab jobs.')
parser.add_argument('crab_out_dir', metavar='crab_out_dir', type=str,
                    help='crab output directory')
parser.add_argument('target_file', metavar='target_file', type=str,
                    help='target directory')
parser.add_argument('--crab_base_dir',
                    default="/dpm/in2p3.fr/home/cms/trivcat/store/user/rembserj",
                    help='base directory for crab output')
parser.add_argument('--host', default="polgrid4.in2p3.fr", help='xroot host')

args = parser.parse_args()

target_dir = "/".join(args.target_file.split("/")[:-1])
if target_dir == "":
    target_dir = "."

if not os.path.exists(target_dir):
    os.makedirs(target_dir)

# Reconstruct the directory where crab stored the ntuples
crab_dir = args.crab_base_dir + "/" + args.crab_out_dir

print("xrdfs polgrid4.in2p3.fr ls -u {}".format(crab_dir))
file_list = os.popen("xrdfs polgrid4.in2p3.fr ls -u {}".format(crab_dir)).read().split("\n")
file_list = [x for x in file_list if '.root' in x]

os.system("source root-v6-06-00-el6-gcc48-thisroot.sh && hadd -f " + args.target_file + " " + " ".join(file_list))
