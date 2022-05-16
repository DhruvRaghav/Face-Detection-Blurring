
# boxes = [[320, 141, 320+12, 141+15], [423, 138, 423+26, 138+36]]
import cv2
import os
import numpy as np

def blur(img, boxes):

    # os.remove('output/image.jpg')

    if len(boxes) > 0:

        tempimg = img.copy()
        # print('entered 1')
        maskShape = (img.shape[0], img.shape[1], 1)
        # print("entered 2")
        mask = np.full(maskShape, 0, dtype=np.uint8)
        # print(boxes) # print(result_list) fd

        for row in boxes:
            # print('row', row)
            # print(row
            # row=row[0]
            # print(row[0][1:-1])
            # row1 = [int(j) for j in row[0][1:-1].split(',')]
            row2 = [int(j) for j in row]
            row1 = [row2[0], row2[1], row2[0]+row2[2], row2[1]+row2[3]]
            # print('row1', row1)
            box = [0, 0, 0, 0]
            box[0] = row1[0]
            box[1] = row1[1]
            box[2] = row1[2]
            box[3] = row1[3]
            tempimg[box[1]:(box[1] + (box[3] - box[1]) + 20),
            box[0]:(box[0] + (box[2] - box[0]) + 20)] = cv2.GaussianBlur(cv2.blur(
                tempimg[box[1]:(box[1] + (box[3] - box[1]) + 20), box[0]:(box[0] + (box[2] - box[0]) + 20)],
                (5, 5)), (23, 23), 5)

            m = (box[2] + box[0]) / 2

            n = (box[3] + box[1]) / 2
            center = (int(m), int(n))

            o = (box[3] - box[1]) / 2
            radius = int(o)

            cv2.circle(mask, center, radius, (255), -1)

            mask_inv = cv2.bitwise_not(mask)
            img1_bg = cv2.bitwise_and(img, img, mask=mask_inv)
            img2_fg = cv2.bitwise_and(tempimg, tempimg, mask=mask)
            img = cv2.add(img1_bg, img2_fg)
            cv2.imwrite('output/image.jpg', img)
            # status = cv2.imwrite("output/" + filename + ".jpg", img)
            # print("Image written to file-system : ", status)

    return img





def draw(img, boxes):
    # os.remove('output/image.jpg')

    if len(boxes) > 0:

        # tempimg = img.copy()
        # print('entered 1')
        # maskShape = (img.shape[0], img.shape[1], 1)
        # print("entered 2")
        # mask = np.full(maskShape, 0, dtype=np.uint8)
        # print(boxes) # print(result_list) fd

        for row in boxes:
            # print('row', row)
            # print(row
            # row=row[0]
            # print(row[0][1:-1])
            # row1 = [int(j) for j in row[0][1:-1].split(',')]
            row2 = [int(j) for j in row]
            row1 = [row2[0], row2[1], row2[0] + row2[2], row2[1] + row2[3]]
            # print('row1', row1)
            # box = [0, 0, 0, 0]
            # box[0] = row1[0]
            # box[1] = row1[1]
            # box[2] = row1[2]
            # box[3] = row1[3]

            start_point = (row1[0], row1[1])
            end_point = (row1[2], row1[3])

            # tempimg[box[1]:(box[1] + (box[3] - box[1]) + 20),
            # box[0]:(box[0] + (box[2] - box[0]) + 20)] = cv2.GaussianBlur(cv2.blur(
            #     tempimg[box[1]:(box[1] + (box[3] - box[1]) + 20), box[0]:(box[0] + (box[2] - box[0]) + 20)],
            #     (5, 5)), (23, 23), 5)
            #
            # m = (box[2] + box[0]) / 2
            #
            # n = (box[3] + box[1]) / 2
            # center = (int(m), int(n))
            #
            # o = (box[3] - box[1]) / 2
            # radius = int(o)
            #
            # cv2.circle(mask, center, radius, (255), -1)
            #
            # mask_inv = cv2.bitwise_not(mask)
            # img1_bg = cv2.bitwise_and(img, img, mask=mask_inv)
            # img2_fg = cv2.bitwise_and(tempimg, tempimg, mask=mask)
            # img = cv2.add(img1_bg, img2_fg)
            img = cv2.rectangle(img, start_point, end_point, (255, 255, 255), 2)
            cv2.imwrite('output_draw/image.jpg', img)
    return img







# blur()