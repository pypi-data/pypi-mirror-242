import os
import traceback
import sys
import numpy as np

import matplotlib.pyplot as plt

import skimage.measure

from cellacdc import core, myutils, widgets, load, html_utils

from qtpy.QtWidgets import QApplication, QStyleFactory

try:
    import pytest
    pytest.skip('skipping this test since it is gui based', allow_module_level=True)
except Exception as e:
    pass

from cellacdc._run import _setup_app

# Ask which model to use --> Test if new model is visible
app, splashScreen = _setup_app(splashscreen=True)  
splashScreen.close()

gdrive_path = myutils.get_gdrive_path()

test_img_path = (
    # os.path.join(gdrive_path, *(r'01_Postdoc_HMGU\Python_MyScripts\MIA\Git\DeepSea\data\test_images\A11_z007_c001.png').split('\\')"
    # os.path.join(gdrive_path, *(r'01_Postdoc_HMGU\Python_MyScripts\MIA\Git\DeepSea\data\test_images\train_A11_z001_c001.png').split('\\')"
    # os.path.join(gdrive_path, *(r'01_Postdoc_HMGU\Python_MyScripts\MIA\Git\Cell_ACDC\data\test_images\test_cellpose.tif').split('\\')"
    # os.path.join(gdrive_path, *(r'01_Postdoc_HMGU\Python_MyScripts\MIA\Git\Cell_ACDC\data\test_images\test_YeaZ.tif').split('\\')"
    os.path.join(
        gdrive_path, 
        *(r'01_Postdoc_HMGU\Python_MyScripts\MIA\Git\Cell_ACDC\data\test_timelapse\Yagya_Kurt_presentation\Position_6\Images\SCGE_5strains_23092021_Dia_Ph3.tif').split('\\'))
    # os.path.join(gdrive_path, *(r'01_Postdoc_HMGU\Python_MyScripts\MIA\Git\DeepSea\data\test_tracking\Position_1\Images\A3_03_1_1_Phase Contrast.tif').split('\\')"
)

channel_name = 'Phase Contrast'
end_filename_segm = 'segm'# 'segm_test'
START_FRAME = 0 
STOP_FRAME = 20
PLOT_FRAME = 10
SAVE = False
SCRUMBLE_IDs = False

posData = load.loadData(
    test_img_path, channel_name
)
posData.loadImgData()
posData.loadOtherFiles(
    load_segm_data=True, 
    load_metadata=True,
    end_filename_segm=end_filename_segm
)

trackers = myutils.get_list_of_trackers()
txt = html_utils.paragraph('''
    <b>Select the tracker</b> to use<br><br>
''')
win = widgets.QDialogListbox(
    'Select tracker', txt, trackers, multiSelection=False, parent=None
)
win.exec_()

if win.cancel:
    sys.exit('Execution aborted')

trackerName = win.selectedItemsText[0]

# Load tracker
tracker, track_params = myutils.init_tracker(
    posData, trackerName, qparent=None
)
if track_params is None:
    exit('Execution aborted')    

lab_stack = posData.segm_data[START_FRAME:STOP_FRAME+1]

if SCRUMBLE_IDs:
    # Scrumble IDs last frame
    
    last_lab = lab_stack[-1]
    last_rp = skimage.measure.regionprops(lab_stack[-1])
    IDs = [obj.label for obj in last_rp]
    randomIDs = np.random.choice(IDs, size=len(last_rp), replace=False)
    for obj, randomID in zip(last_rp, randomIDs):
        last_lab[obj.slice][obj.image] = randomID

    # Randomly delete some objects last frame
    num_obj_to_del = 4
    idxs = np.arange(len(last_rp))
    random_idxs = np.random.choice(idxs, size=num_obj_to_del, replace=False)
    for random_idx in random_idxs:
        obj_to_del = last_rp[random_idx]
        last_lab[obj_to_del.slice][obj_to_del.image] = 0

print(f'Tracking data with shape {lab_stack.shape}')

trackerInputImage = None
if 'image' in track_params:
    trackerInputImage = track_params.pop('image')[START_FRAME:STOP_FRAME+1]

if 'image_channel_name' in track_params:
    # Store the channel name for the tracker for loading it 
    # in case of multiple pos
    track_params.pop('image_channel_name')

tracked_stack = core.tracker_track(
    lab_stack, tracker, track_params, 
    intensity_img=trackerInputImage,
    logger_func=print
)

if SAVE:
    try:
        np.savez_compressed(
            posData.segm_npz_path.replace('segm', 'segm_tracked'), 
            tracked_stack
        )
    except Exception as e:
        import pdb; pdb.set_trace()

from cellacdc.plot import imshow

images = [
    lab_stack[PLOT_FRAME-START_FRAME-1], 
    lab_stack[PLOT_FRAME-START_FRAME],
    tracked_stack[PLOT_FRAME-START_FRAME-1], 
    tracked_stack[PLOT_FRAME-START_FRAME]
]
titles = [
    f'Untracked labels at frame {PLOT_FRAME}',
    f'Untracked labels at frame {PLOT_FRAME+1}',
    f'TRACKED labels at frame {PLOT_FRAME}',
    f'TRACKED labels at frame {PLOT_FRAME+1}',
]
imshow(
    *images, axis_titles=titles,
    max_ncols=2
)
