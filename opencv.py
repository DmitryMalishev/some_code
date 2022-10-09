# Python script to demonstrate OpenCV manipulations

# Task: read an image from a file as grayscale. Find the four non-overlapping 5x5 patches
#  with highest average brightness. Take the patch centers as corners of a quadrilateral,
#  calculate its area in pixels, and draw the quadrilateral in red into the image and save
#  it in PNG format

from absl import app
import numpy as np
import unittest
import heapq
import cv2

PATCH_SZ = 5
PATCH_COUNT = 4

def process_image(img_rgb: np.array, save_out_image = True) -> int:
    # Convert image to grayscale
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)

    # Make a template for search (a square with max bright)
    template = np.full((PATCH_SZ, PATCH_SZ), 255, np.uint8)
    w, h = template.shape[::-1]

    # Perform match operations
    method = cv2.TM_CCORR
    res = cv2.matchTemplate(img_gray, template, method)

    # Use Heapq to sort the matching results
    res_array = [(-res[w][h], (h, w)) for w in range(res.shape[0]) for h in range(res.shape[1])]
    max_list = []
    heapq.heapify(res_array)
    while len(max_list) < PATCH_COUNT and len(res_array) > 0:
        candidate = heapq.heappop(res_array)[1]
        if len(max_list) and not all([abs(item[0] - candidate[0]) >= PATCH_SZ or
            abs(item[1] - candidate[1]) >= PATCH_SZ for item in max_list]):
            continue
        max_list.append(candidate)

    if len(max_list) < PATCH_COUNT:
        # Could not find required number of matches
        if save_out_image:
            print(f"ERROR: detected only {len(max_list)} matches")
        return -1

    # Update the coordinates order to avoid line intersections
    max_list_tmp = []
    max_list_tmp.append(min(max_list, key = lambda x: x[0])); max_list.remove(max_list_tmp[-1])
    max_list_tmp.append(min(max_list, key = lambda x: x[1])); max_list.remove(max_list_tmp[-1])
    max_list_tmp.append(max(max_list, key = lambda x: x[0])); max_list.remove(max_list_tmp[-1])
    max_list_tmp.append(max(max_list, key = lambda x: x[1])); max_list.remove(max_list_tmp[-1])
    max_list = max_list_tmp
    centers_list = [(pos[0] + PATCH_SZ//2, pos[1] + PATCH_SZ//2) for pos in max_list]

    # Calculate the area of the polygon
    points = np.array(centers_list)
    polygon_sz = cv2.contourArea(points)

    if save_out_image:
        # Prepare resulting image
        img_out = cv2.cvtColor(img_gray, cv2.COLOR_GRAY2BGR)
        for i, pos_loc in enumerate(max_list):
            if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
                top_left = pos_loc
            else:
                top_left = pos_loc
            bottom_right = (top_left[0] + w, top_left[1] + h)
            cv2.rectangle(img_out, top_left, bottom_right, (0, 0, 255), 2)
            cv2.line(img_out, centers_list[i], centers_list[i-1], (0, 0, 255), 2)

        cv2.imwrite('detected.png', img_out)

    return int(polygon_sz)

def main(argv):
    print("USAGE: Provide input file name OR auto unit tests when no arguments")
    if len(argv) == 2:
        # Read the image from argv
        img_rgb = cv2.imread(argv[1])
        process_image(img_rgb)
    else:
        # Unit tests when no arguments provided
        tc = unittest.TestCase()
        img_test = np.full((PATCH_SZ*5, PATCH_SZ*5, 3), 0, np.uint8)
        img_test[0][0] = img_test[15][0] = img_test[0][15] = img_test[15][15] = 128
        tc.assertIn(process_image(img_test, False), range(150, 200))
        tc.assertEqual(process_image(np.full((10, 10, 3), 128, np.uint8), False), 25)
        tc.assertEqual(process_image(np.full((9, 9, 3), 128, np.uint8), False), -1)
        tc.assertEqual(process_image(np.full((5, 20, 3), 128, np.uint8), False), -1)
        print('Tests PASSED!')

if __name__ == '__main__':
    app.run(main)
