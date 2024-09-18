import cairosvg
import os
import numpy as np
from skimage.io import imsave, imread

COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255)] # red, green, blue
NUM_TREES = 3
MASK_SIZE = 1000
PATH_TO_OPENCCO_EXE = os.path.join(".", "build", "bin", "generateTree2D")

mask = np.ones((MASK_SIZE, MASK_SIZE), dtype=np.uint8)
mask[:, 0:5] = 0
mask[0:5, :] = 0
mask[:, MASK_SIZE-5:MASK_SIZE] = 0
mask[MASK_SIZE-5:MASK_SIZE, :] = 0

imsave("./overlapping-masks/mask0.png", mask*255)

# Gerando sub-arvores
for t in range(NUM_TREES):
    print(f"Gerando arvore n {t+1}")
    os.system(f"{PATH_TO_OPENCCO_EXE} -n 300 -a 2000 -d ./overlapping-masks/mask{t}.png")
    cairosvg.svg2png(url='result.svg', write_to="./overlapping-masks/result.png", output_width=mask.shape[0], output_height=mask.shape[1])

    result = imread("./overlapping-masks/result.png")

    # O fundo cinza tem cor exata=(200, 200, 200)
    mask[result[:, :, 0]!=200] = 0
    mask[result[:, :, 0]==200] = 1

    imsave(f"./overlapping-masks/mask{t+1}.png", (mask*255).astype(np.uint8))

    