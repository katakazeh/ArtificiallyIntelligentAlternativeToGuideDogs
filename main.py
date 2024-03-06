import cv2
import numpy as np

# read image
#cap = cv2.VideoCapture(0)
cap = cv2.VideoCapture(0, cv2.CAP_ANY)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)  # Adjust the width as needed
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)  # Adjust the height as needed
cv2.waitKey(1000)
if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()


ret, img = cap.read()
while True:
        if not ret:
                print("Error: Could not read frame.")
                break

# threshold on white/gray sidewalk stripes
lower = (100,130,130)
upper = (180,200,200)
thresh = cv2.inRange(img, lower, upper)


# apply morphology close to fill interior regions in mask
kernel = np.ones((3,3), np.uint8)
morph = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
kernel = np.ones((5,5), np.uint8)
morph = cv2.morphologyEx(morph, cv2.MORPH_CLOSE, kernel)

# get contours
cntrs = cv2.findContours(morph, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
# bounding_boxes = [cv2.boundingRect(contour) for contour in cntrs]
cntrs = cntrs[0] if len(cntrs) == 2 else cntrs[1]

# filter on area
contours = img.copy()
good_contours = []
for c in cntrs:
    area = cv2.contourArea(c)
    if area > 200:
        cv2.drawContours(contours, [c], -1, (0,0,255), 1)
        good_contours.append(c)

# combine good contours
contours_combined = np.vstack(good_contours)
bounding_boxes = [cv2.boundingRect(contour) for contour in contours_combined]
print(bounding_boxes)
# get convex hull
result = img.copy()
hull = cv2.convexHull(contours_combined)
cv2.polylines(result, [hull], True, (0,0,255), 2)

# write result to disk
#cv2.imwrite("walkway_thresh.jpg", thresh)
#cv2.imwrite("walkway_morph.jpg", morph)
#cv2.imwrite("walkway_contours.jpg", contours)
cv2.imwrite("walkway_result.jpg", result)

# display it
#cv2.imshow("THRESH", thresh)
#cv2.imshow("MORPH", morph)
#cv2.imshow("CONTOURS", contours)
cv2.imshow("RESULT", result)
cv2.waitKey(0)
# get convex hull
result = img.copy()
hull = cv2.convexHull(contours_combined)
cv2.polylines(result, [hull], True, (0,0,255), 2)

# write result to disk
#cv2.imwrite("walkway_thresh.jpg", thresh)
#cv2.imwrite("walkway_morph.jpg", morph)
#cv2.imwrite("walkway_contours.jpg", contours)
cv2.imwrite("walkway_result.jpg", result)

# display it
#cv2.imshow("THRESH", thresh)
#cv2.imshow("MORPH", morph)
#cv2.imshow("CONTOURS", contours)
cv2.imshow("RESULT", result)
cv2.waitKey(0)

# get convex hull
result = img.copy()
hull = cv2.convexHull(contours_combined)

# Approximate a polygon around the convex hull
epsilon = 0.02 * cv2.arcLength(hull, True)
approx = cv2.approxPolyDP(hull, epsilon, True)

# Draw the approximate polygon on the result image
cv2.polylines(result, [approx], True, (0, 0, 255), 2)

# Get the vertices of the approximate polygon
approx_vertices = approx.reshape(-1, 2)

# Take only the first 4 vertices
quadrilateral_vertices = approx_vertices[:4]

# Print the vertices in unit coordinates
for vertex in quadrilateral_vertices:
    print("Vertex:", vertex)

# Display and save the updated result
cv2.imshow("UPDATED RESULT", result)
cv2.imwrite("walkway_updated_result.jpg", result)
cv2.waitKey(0)

# Get the vertices of the approximate polygon
approx_vertices = approx.reshape(-1, 2)

# Take only the first 4 vertices
quadrilateral_vertices = approx_vertices[:4]

# Assuming quadrilateral_vertices are ordered as [top-left, top-right, bottom-right, bottom-left]
# Calculate the slope of the long sides
slope_top = (quadrilateral_vertices[1][1] - quadrilateral_vertices[0][1]) / (quadrilateral_vertices[1][0] - quadrilateral_vertices[0][0])
slope_bottom = (quadrilateral_vertices[2][1] - quadrilateral_vertices[3][1]) / (quadrilateral_vertices[2][0] - quadrilateral_vertices[3][0])

# Calculate the intersection point of the extended lines
intersection_x = (slope_top * quadrilateral_vertices[0][0] - quadrilateral_vertices[0][1] - slope_bottom * quadrilateral_vertices[3][0] + quadrilateral_vertices[3][1]) / (slope_top - slope_bottom)
intersection_y = slope_top * (intersection_x - quadrilateral_vertices[0][0]) + quadrilateral_vertices[0][1]

# Set the middle of the picture as x=0
intersection_x -= result.shape[1] // 2
# Mark the x=0 point at the bottom of the picture
zero_point = (result.shape[1] // 2, result.shape[0])
cv2.circle(result, zero_point, 5, (0, 255, 0), -1)

# Print the intersection point
print("Intersection Point:", (intersection_x, intersection_y))

# Draw a circle at the intersection point on the result image
cv2.circle(result, (int(intersection_x + result.shape[1] // 2), int(intersection_y)), 5, (255, 0, 0), -1)

# Determine the movement direction
if abs(intersection_x) < 8:
    print("Move straight")
elif intersection_x < 0:
    print("Move left")
else:
    print("Move right")

# Display and save the updated result
cv2.imshow("UPDATED RESULT", result)
cv2.imwrite("walkway_updated_result.jpg", result)
cv2.waitKey(0)
