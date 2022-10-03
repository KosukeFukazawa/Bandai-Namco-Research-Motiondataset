import numpy as np
import os
from os.path import join as pjoin
import bvh, quat
BASEPATH = os.path.normpath(pjoin(os.path.dirname(os.path.abspath(__file__)), ".."))

datapaths = [
    pjoin(BASEPATH, "dataset/Bandai-Namco-Research-Motiondataset-1/data"),
    pjoin(BASEPATH, "dataset/Bandai-Namco-Research-Motiondataset-2/data")]


def animation_mirror(lrot, lpos, names, parents):

    joints_mirror = np.array([(
        names.index('Left'+n[5:]) if n.startswith('Right') else (
        names.index('Right'+n[4:]) if n.startswith('Left') else 
        names.index(n))) for n in names])

    mirror_pos = np.array([-1, 1, 1])
    mirror_rot = np.array([[-1, -1, 1], [1, 1, -1], [1, 1, -1]])

    grot, gpos = quat.fk(lrot, lpos, parents)

    gpos_mirror = mirror_pos * gpos[:,joints_mirror]
    grot_mirror = quat.from_xform(mirror_rot * quat.to_xform(grot[:,joints_mirror]))
    
    return quat.ik(grot_mirror, gpos_mirror, parents)


for datapath in datapaths:
    # List all of the bvh files in datapath.
    bvh_files = [pjoin(datapath, f) for f in os.listdir(datapath) 
                if f.endswith(".bvh")]
    
    # Create output dir.
    savepath = pjoin(datapath, "../cleaned")
    if not os.path.exists(savepath):
        os.makedirs(savepath, exist_ok=True)
    
    for i, bvh_file in enumerate(bvh_files):
        print("Processing Capture {}/{} ".format(i+1, len(bvh_files)))
        filename = bvh_file.split("/")[-1]
        
        motion = bvh.load(bvh_file)
        
        # Remove "joint_Root" bone and set ROOT to "Hips"
        rotations = motion["rotations"][:,1:]
        positions = motion["positions"][:,1:]
        offsets = motion["offsets"][1:]
        # Root to 0 on Rest pose.
        offsets[0] = np.zeros(3)
        parents = motion["parents"][1:] - 1
        names = motion["names"][1:]
        order = motion["order"]
        frametime = motion["frametime"]
        
        # Rename *_L(*_R) to Left*(Right*)
        new_names = []
        for name in names:
            if name.endswith("L"):
                new_names.append("Left" + name[:-2])
            elif name.endswith("R"):
                new_names.append("Right" + name[:-2])
            else:
                new_names.append(name)
        
        cleaned = {
            'rotations': rotations,
            'positions': positions,
            'offsets': offsets,
            'parents': parents,
            'names': new_names,
            'order': order,
            'frametime': frametime,
        }
        
        bvh.save(pjoin(savepath, filename), cleaned)
        
        # Mirroring motion and save as *_mirror.bvh.
        rot = quat.from_euler(np.radians(rotations), order)
        rot, positions = animation_mirror(rot, positions, new_names, parents)
        
        cleaned["positions"] = positions
        cleaned["rotations"] = np.degrees(quat.to_euler(rot, order))
        
        bvh.save(pjoin(savepath, filename.split(".")[0]+"_mirror.bvh"), cleaned)
    
    print("finished : {}".format(datapath))