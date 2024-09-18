import cairosvg
import os
import numpy as np
from skimage.io import imsave, imread

NUM_TREES = 3
MASK_SIZE = 1000
MASK_COEFICIENT = MASK_SIZE // NUM_TREES
PATH_TO_OPENCCO_EXE = os.path.join(".", "build", "bin", "generateTree2D")

mask = np.zeros((MASK_SIZE, MASK_SIZE), dtype=np.uint8)

# Gerando sub-arvores
for i in range(NUM_TREES):
    sub_mask = mask.copy()
    sub_mask[:, MASK_COEFICIENT*i : MASK_COEFICIENT*(i+1)] = 255
    imsave(f"./masks/mask{i}.png", sub_mask)
    os.system(f"{PATH_TO_OPENCCO_EXE} -n 300 -a 2000 -d ./masks/mask{i}.png")
    cairosvg.svg2png(url='result.svg', write_to=f"./subtrees/subtree{i}.png", output_width=sub_mask.shape[0], output_height=sub_mask.shape[1])

# Juntando as sub-arvores
output = np.ones((MASK_SIZE, MASK_SIZE), dtype=np.uint8)*255
for i in range(NUM_TREES):
    output[:, MASK_COEFICIENT*i : MASK_COEFICIENT*(i+1)] = imread(f"./subtrees/subtree{i}.png", as_gray=True)[:, MASK_COEFICIENT*i : MASK_COEFICIENT*(i+1)]*255

imsave(f"florest.png", output)
