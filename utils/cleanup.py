import numpy as np
import os
from os.path import join as pjoin
import bvh
BASEPATH = pjoin(os.path.dirname(os.path.abspath(__file__)), "..")

datapaths = [
    pjoin(BASEPATH, "dataset/Bandai-Namco-Research-Motiondataset-1/data"),
    pjoin(BASEPATH, "dataset/Bandai-Namco-Research-Motiondataset-2/data")]



for datapath in datapaths:
    
    bvh_files = [pjoin(datapath, f) for f in os.listdir(datapath) 
                if f.endswith(".bvh")]
    
    savepath = pjoin(datapath, "../cleaned")
    if not os.path.exists(savepath):
        os.makedirs(savepath, exist_ok=True)
    
    for i, bvh_file in enumerate(bvh_files):
        print("Processing Capture {} of {} ".format(i+1, len(bvh_files)))
        filename = bvh_file.split("/")[-1]
        
        motion = bvh.load(bvh_file)
        
        rotations = motion["rotations"][:,1:]
        positions = motion["positions"][:,1:]
        offsets = motion["offsets"][1:]
        offsets[0] = np.zeros(3)
        parents = motion["parents"][1:] - 1
        names = motion["names"][1:]
        order = motion["order"]
        frametime = motion["frametime"]

        cleaned = {
            'rotations': rotations,
            'positions': positions,
            'offsets': offsets,
            'parents': parents,
            'names': names,
            'order': order,
            'frametime': frametime,
        }
        
        bvh.save(pjoin(savepath, filename), cleaned)
    
    print("finished : {}".format(datapath))