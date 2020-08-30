import numpy as np

def detect_spaces(image, offset, pixels, min_len_bright, min_len_dark,  axis):
    hist = np.sum(image, axis=axis)
    cut = np.where(hist>pixels*255, hist, 0)
    length = cut.shape[0]
    #looking for frist indicies
    x1 = np.where(cut==0)[0]
    if x1.size == 0:
        return [(0, length - 1)]
    x1_cut = np.where(np.diff(x1)>1)[0]
    first_index = x1[x1_cut]
    #looking for second indicies
    x2 = np.where(cut[::-1]==0)[0]
    x2_cut = np.where(np.diff(x2)>1)[0]
    second_index = (length - 1 -x2[x2_cut])[::-1]
    indicies = [(0, x1[0])]
    indicies.extend(list(zip(first_index, second_index)))
    temp_index = 0
    new_indicies = []
    if len(indicies) == 1:
        new_indicies.append(indicies[0])
    else:
        for i, (_, index2) in enumerate(indicies[:-1]):
            space = indicies[i+1][0] - index2
            if space > min_len_dark:
                new_indicies.append((max(0, indicies[temp_index][0] - offset), min(length - 1, indicies[i][1] + offset)))
                temp_index = i + 1
            elif i == len(indicies) - 2:
                new_indicies.append((max(0, indicies[temp_index][0] - offset), min(length - 1, indicies[i+1][1] + offset)))
    indicies = []
    for item in new_indicies:
        if item[1] - item[0] >= min_len_bright:
            indicies.append(item)

    return indicies
