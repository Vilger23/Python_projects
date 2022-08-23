import numpy as np
from PIL import Image

im = Image.open('day.png')
# Convert image to numpy array
im_arr = np.array(im)

def create_mask(im : np.ndarray):
    margin = 255
    target_rgb = np.array([115,80,54])
    low_bound = np.minimum(target_rgb - margin, 0)
    high_bound = np.maximum(target_rgb + margin, 255)
    target_ranges = [range(low, high) for low, high in zip(low_bound, high_bound)]
    print(target_ranges)
    # Filter im so that only colors that are within margin of target_rgb are kept
    im_mask =  low_bound[0] < im[:,:,0] < high_bound[0] and low_bound[1] < im[:,:,1] < high_bound[1] and low_bound[2] < im[:,:,2] < high_bound[2]

    # Convert mask to image
    im_mask = Image.fromarray(im_mask.astype(np.uint8)*255)
    return im_mask

create_mask(im_arr).save('filter.png')

#fishing rod rgb = (115,80,54)
