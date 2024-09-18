import numpy as np
from skimage.io import imread, imsave

COLORS = [(0, 0, 0), (255, 0, 0), (0, 255, 0), (0, 0, 255)] # red, green, blue

n = int(input("Informe o numero de subarvores: "))
flips = list(map(int, (input("Digite a necessidade de flip horizontal para mask 1, ..., n, respectivamente. Ex. Formato: 0, 1, 0, ..., \nEntrada: ").split(','))))

imgs = []

for i, flip in enumerate(flips):
    img = imread(f"./overlapping-masks/mask{i+1}.png", as_gray=True)//255
    if flip:
        img = np.flipud(img)
    imgs.append(img)

final_mask = imgs[0].copy()
tmp_mask = imgs[0].copy()

for i, mask in enumerate(imgs[1:]):
    final_mask[np.logical_not(tmp_mask==mask)] = 2+i # indicando a cor da arvore
    tmp_mask = mask # prosseguindo o crescimento da mascara

final_image = np.ones((imgs[0].shape[0], imgs[0].shape[1], 3)) * 255

for i in range(imgs[0].shape[0]):
    for j in range(imgs[0].shape[1]):
        if final_mask[i, j] != 1: # Nao eh plano de fundo

            if final_mask[i, j] == 0:
                final_image[i, j, 0] = COLORS[0][0]
                final_image[i, j, 1] = COLORS[0][1]
                final_image[i, j, 2] = COLORS[0][2]
            else: 
                final_image[i, j, 0] = COLORS[final_mask[i, j]-1][0]
                final_image[i, j, 1] = COLORS[final_mask[i, j]-1][1]
                final_image[i, j, 2] = COLORS[final_mask[i, j]-1][2]

print(final_image)
print(final_image.shape)

imsave("./colored/colored.png", final_image.astype(np.uint8))









