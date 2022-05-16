import cv2
import os
import numpy as np
#
# import base64
#
#
# with open("bluroutput/image.jpg", "rb") as image2string:
#     converted_string = base64.b64encode(image2string.read())
# print(converted_string)
# decodeit = open('pano/lolol.jpeg', 'wb')
# decodeit.write(base64.b64decode(converted_string))
# decodeit.close()



def testrectblur(img, boxes):

    if len(boxes) > 0:


        img = (img.copy())
        width, height=img.shape[0], img.shape[1]
        print(img.shape)

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
            if row1[0]>0 and row1[1]>0 and row1[2] < width and row1[3] < height:

                cv2.rectangle(img, (box[0], box[1]), (box[2], box[3]),(255,255,255),4)

                ROI=img[box[1]:box[3], box[0]:box[2]]

                blur=cv2.GaussianBlur(ROI, (23,23),30)
                # print(type(blur))
                # blur=np.array(blur)

                img[box[1]:box[1]+blur.shape[0],box[0]:box[0]+blur.shape[1]]=blur
                # img1_bg = cv2.bitwise_and(img, img, mask=blur)
                # img=cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                # print("save")
                cv2.imwrite('bluroutput/image.jpg', img)
            else:
                return 'Invalid parameter'
            # Image.fromarray(img).save('bluroutput/image.jpg')
    # return img