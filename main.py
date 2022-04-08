import cv2
import numpy as np
import random
import math

def get_first_point():      # Bad realization, better use pixels from image
    return [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]


def get_distance(p1, p2):       # Calculate euclidean distance
    return round(math.sqrt((p2[0]-p1[0])**2 + (p2[1]-p1[1])**2 + (p2[2]-p1[2])**2))


def get_centroid(clusters, im):     
    clusters_new = []
    for i in range(len(clusters)):
        a = []
        if len(clusters[i]) > 1:
            for j in range(1, len(clusters[i])):
                x, y = clusters[i][j][0], clusters[i][j][1]
                zxc = im[x, y].tolist()
                a.append(zxc)
            asd = []
            asd.append(np.mean(a, axis=0).tolist())
            asd[0][0] = round(asd[0][0])
            asd[0][1] = round(asd[0][1])
            asd[0][2] = round(asd[0][2])
            clusters_new.append(asd)
        else:
            clusters_new.append(clusters[i])
    return clusters_new


def get_clusters(count):
    clusters = []
    for i in range(count):
        a = []
        a.append(get_first_point())
        clusters.append(a)
    return clusters


if __name__ == "__main__":
    im = cv2.imread("your_image.jpg")
    height, width = im.shape[0], im.shape[1]
    shodimost = 5
    clusters = get_clusters(5)      # You can change this value for increase/decrease count of colors
    for i in range(height):
        for j in range(width):
            dist_best = 1000000
            for k in (range(len(clusters))):
                dist_hz = get_distance(im[i][j].tolist(), clusters[k][0])
                if dist_hz < dist_best:
                    dist_best = dist_hz
                    a = k
            clusters[a].append([i, j])

    while True:
        old_centroid = clusters[0][0]
        clusters = get_centroid(clusters, im)
        new_centroid = clusters[0][0]
        rez = get_distance(old_centroid, new_centroid)
        for i in range(height):
            for j in range(width):
                dist_best = 1000000
                for k in (range(len(clusters))):
                    dist_hz = get_distance(im[i][j].tolist(), clusters[k][0])
                    if dist_hz < dist_best:
                        dist_best = dist_hz
                        a = k
                clusters[a].append([i, j])
        if shodimost > rez:
            break

    
    for i in range(len(clusters)):
        for j in range(1, len(clusters[i])):
            a, b = clusters[i][j][0], clusters[i][j][1]
            im[a, b] = clusters[i][0]


    vis = im
    for i in range(len(clusters)):      # Add visualization for result of work
        im2 = np.zeros((200, 20, 3), np.uint8)
        start_point = (0, 0)
        end_point = ((i+1)*20, 200)
        color = clusters[i][0]
        thickness = -1
        im2 = cv2.rectangle(im2, start_point, end_point, color, thickness)
        vis = np.concatenate((vis, im2), axis=1)


    cv2.imwrite('your_new_image.jpg', im)       # Saving new image
    cv2.imshow('kek', vis)
    cv2.waitKey(0) 