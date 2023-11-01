import streamlit as st
import cv2 as cv

import cv2
import matplotlib.pyplot as plt
import matplotlib.patches as patches


thing_classes = [
    "Aortic enlargement",
    "Atelectasis",
    "Calcification",
    "Cardiomegaly",
    "Consolidation",
    "ILD",
    "Infiltration",
    "Lung Opacity",
    "Nodule/Mass",
    "Other lesion",
    "Pleural effusion",
    "Pleural thickening",
    "Pneumothorax",
    "Pulmonary fibrosis"
]

class_colors = {
    "Aortic enlargement": "red",
    "Atelectasis": "green",
    "Calcification": "blue",
    "Cardiomegaly": "yellow",
    "Consolidation": "purple",
    "ILD": "cyan",
    "Infiltration": "magenta",
    "Lung Opacity": "orange",
    "Nodule/Mass": "pink",
    "Other lesion": "brown",
    "Pleural effusion": "lime",
    "Pleural thickening": "indigo",
    "Pneumothorax": "gold",
    "Pulmonary fibrosis": "navy",
}

id2class = {i: c for i, c in enumerate(thing_classes)}
# st.write(id2class)

# Load your model and other necessary setups here

# Sample data
results = {
    'image1.jpg': [
    ],
    # ... other images
}

box = "11 0.5975274443626404 1351 285 1690 360 3 0.5276792049407959 819 1204 1899 1603 0 0.49623745679855347 1156 643 1438 914 11 0.32363370060920715 1367 280 1785 432 11 0.19730019569396973 604 299 945 378 11 0.1882581263780594 491 308 724 443 11 0.15678586065769196 521 282 938 425 11 0.1249791830778122 1515 305 1811 448 11 0.1048220843076706 1460 283 1723 399 11 0.09819411486387253 457 288 828 472 11 0.07879801839590073 574 287 796 405 11 0.07410267740488052 461 330 646 457 11 0.047079551964998245 1468 294 1867 511 11 0.046289194375276566 1312 294 1566 367 11 0.04018415883183479 1620 327 1815 469 11 0.03954971954226494 420 306 696 508 11 0.036270417273044586 688 302 925 354 11 0.022821377962827682 631 290 846 350 11 0.021881036460399628 1331 290 1549 336 11 0.019169870764017105 726 308 986 400 11 0.018906541168689728 594 296 748 373 9 0.012285430915653706 112 1427 921 1793 9 0.012149740941822529 1277 476 1375 658 5 0.012043152004480362 277 835 912 1540 11 0.011809926480054855 399 262 906 532 0 0.011631193570792675 821 1200 1879 1638 11 0.010751578025519848 1697 354 1822 457 11 0.009209363721311092 1313 297 1487 348 11 0.009147604927420616 849 323 983 399 5 0.009034254588186741 500 982 930 1486 11 0.008934409357607365 389 345 598 514 0 0.008909516967833042 1184 664 1408 835 5 0.008082673884928226 161 514 951 1648 11 0.007999802008271217 1674 338 1888 509 9 0.007980262860655785 108 1409 1013 2137 8 0.0077011785469949245 235 1461 342 1562 8 0.007654805202037096 330 1374 371 1409 11 0.0070134918205440044 632 292 1018 468 11 0.006977188400924206 485 360 580 436 5 0.006024951580911875 1396 469 2119 1762 5 0.005871806759387255 361 1081 839 1470 9 0.0057854182086884975 1431 1477 1798 1775 11 0.005438139196485281 1306 306 1454 372 9 0.00541920168325305 1198 713 1507 1633 9 0.005411069840192795 990 712 1400 1859 9 0.005175124388188124 1289 1491 2044 1814 11 0.004987648688256741 1336 248 1887 587 11 0.004901163280010223 453 359 567 465 11 0.0048675439320504665 715 295 896 335 0 0.004454032052308321 1060 632 1448 1030 11 0.004297418519854546 1295 191 1919 456 9 0.0042817238718271255 1105 569 1425 1406 3 0.004180277697741985 823 1056 1978 1803 9 0.00408690981566906 231 1395 673 1740 9 0.0038852414581924677 1428 1534 2058 1731 9 0.0034791664220392704 1313 1501 2276 2444 11 0.003345770062878728 559 324 730 407 9 0.003324696095660329 987 365 1346 1545 13 0.0032530000898987055 450 1169 816 1477 5 0.003113773185759783 1532 1309 2208 1748 12 0.0030969472136348486 1316 275 2047 753 8 0.0030844639986753464 1827 1291 1892 1357 11 0.0030676601454615593 836 308 1006 438 6 0.003027992555871606 510 979 933 1483 11 0.0028694074135273695 325 339 576 605 8 0.0028078071773052216 249 1490 326 1556 11 0.0026938295923173428 823 301 991 372 9 0.002649372210726142 595 1131 1014 1601 2 0.002635503653436899 1548 826 1631 913 13 0.0025721052661538124 515 1013 929 1471 9 0.0025372218806296587 1608 1537 2195 1799 5 0.0025361538864672184 581 1165 890 1471 12 0.0025200892705470324 213 260 963 807 12 0.002501209732145071 136 142 1039 1366 9 0.0024494740646332502 286 1409 855 1629 9 0.002421105047687888 966 300 1186 916 13 0.002387100365012884 1405 854 1672 1149 9 0.0023426006082445383 1540 1337 2200 1752 5 0.002334652002900839 406 1244 843 1493 9 0.0023242884781211615 1391 260 1841 451 11 0.0022957390174269676 1355 313 1634 399 8 0.0022665965370833874 1430 1477 1786 1772 6 0.0022501922212541103 537 1153 858 1473 8 0.0022137293126434088 336 1373 390 1415 11 0.0021498047281056643 416 396 524 502 11 0.002038411796092987 118 1071 267 1684 7 0.00202185264788568 595 1178 885 1475 10 0.0019834761042147875 87 1716 159 1853 9 0.0019562658853828907 335 1285 959 1653 9 0.001886312966234982 100 998 964 1775 8 0.0018249363638460636 330 1362 383 1398 12 0.0017258343286812305 1338 108 1961 603 13 0.0016794308321550488 398 1299 825 1513 13 0.001676063402555883 545 1214 881 1446 9 0.0016732983058318496 1328 192 1955 579 12 0.001670140540227294 0 61 1147 2154 10 0.0016613375628367066 108 1730 165 1823 12 0.001643961644731462 1317 300 1882 540 9 0.0016197746153920889 1232 294 1405 685 7 0.0016031115083023906 521 999 930 1484"
box = box.split()

def convert_to_dict(box):
    class_id = int(box[0])
    confidence = float(box[1])
    xmin, ymin, xmax, ymax = map(int, box[2:])
    return {'class_id': class_id, 'confidence': confidence, 'bbox': [xmin, ymin, xmax, ymax]}

for i in range(0, len(box), 6):
    row = convert_to_dict(box[i:i+6])
    if row['confidence'] > 0.4:
        row['class_id'] = id2class[row['class_id']]
        results['image1.jpg'].append(row)


# Streamlit UI
st.title('X-ray Image Segmentation Visualization')

# Image selection
image_id = st.selectbox('Select an image', list(results.keys()))

# Load image
image = cv2.imread(f'{image_id}')
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# Create a matplotlib figure and axis
fig, ax = plt.subplots()

# Display image
ax.imshow(image)

# Get predictions for the selected image
predictions = results.get(image_id, [])

for pred in predictions:
    class_id, confidence, (xmin, ymin, xmax, ymax) = pred.values()
    color = class_colors.get(str(class_id), 'white')  # Default to white if class_id is not in the map
    rect = patches.Rectangle((xmin, ymin), xmax-xmin, ymax-ymin, linewidth=1, edgecolor=color, facecolor='none')
    ax.add_patch(rect)
    ax.text(xmin, ymin, f'{class_id} ({confidence:.2f})', fontsize=8, bbox=dict(boxstyle='round,pad=0.2', edgecolor=color,linewidth=0.5, facecolor='none'), color=color)
# Show the plot
st.pyplot(fig)
