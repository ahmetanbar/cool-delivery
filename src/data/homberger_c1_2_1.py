from typing import List, Dict

# x, y, capacity
data: Dict = {
    "vehicle_capacity": 130,
    "coordinates_and_capacity": [[24, 26, 20, ],
                                 [86, 36, 20, ],
                                 [95, 35, 10, ],
                                 [63, 50, 10, ],
                                 [100, 106, 10, ],
                                 [99, 112, 20, ],
                                 [36, 135, 10, ],
                                 [57, 59, 10, ],
                                 [8, 124, 10, ],
                                 [85, 106, 20, ],
                                 [103, 69, 30, ],
                                 [109, 131, 20, ],
                                 [43, 140, 10, ],
                                 [115, 134, 30, ],
                                 [98, 70, 10, ],
                                 [112, 67, 10, ],
                                 [102, 104, 20, ],
                                 [93, 75, 30, ],
                                 [90, 104, 20, ],
                                 [127, 108, 10, ],
                                 [84, 99, 20, ],
                                 [113, 69, 20, ],
                                 [129, 9, 10, ],
                                 [18, 38, 30, ],
                                 [30, 27, 10, ],
                                 [25, 80, 20, ],
                                 [17, 37, 30, ],
                                 [32, 106, 10, ],
                                 [43, 135, 10, ],
                                 [61, 59, 20, ],
                                 [104, 106, 20, ],
                                 [109, 71, 20, ],
                                 [121, 110, 30, ],
                                 [61, 48, 20, ],
                                 [74, 99, 20, ],
                                 [89, 73, 10, ],
                                 [21, 25, 20, ],
                                 [99, 28, 30, ],
                                 [101, 96, 10, ],
                                 [9, 114, 20, ],
                                 [121, 112, 20, ],
                                 [137, 6, 10, ],
                                 [118, 131, 20, ],
                                 [34, 82, 10, ],
                                 [4, 125, 30, ],
                                 [26, 105, 40, ],
                                 [35, 123, 20, ],
                                 [21, 48, 10, ],
                                 [21, 115, 10, ],
                                 [99, 108, 20, ],
                                 [1, 34, 20, ],
                                 [94, 70, 20, ],
                                 [74, 93, 20, ],
                                 [32, 128, 20, ],
                                 [94, 73, 10, ],
                                 [135, 3, 20, ],
                                 [97, 28, 20, ],
                                 [59, 56, 20, ],
                                 [80, 97, 10, ],
                                 [134, 31, 20, ],
                                 [103, 34, 30, ],
                                 [30, 79, 20, ],
                                 [4, 30, 40, ],
                                 [87, 39, 20, ],
                                 [90, 101, 10, ],
                                 [119, 136, 30, ],
                                 [78, 92, 30, ],
                                 [110, 66, 10, ],
                                 [62, 58, 20, ],
                                 [127, 112, 20, ],
                                 [113, 71, 10, ],
                                 [34, 104, 10, ],
                                 [2, 28, 10, ],
                                 [17, 43, 10, ],
                                 [1, 24, 10, ],
                                 [112, 71, 20, ],
                                 [135, 0, 10, ],
                                 [125, 108, 20, ],
                                 [8, 138, 30, ],
                                 [103, 111, 20, ],
                                 [57, 53, 10, ],
                                 [98, 31, 20, ],
                                 [116, 132, 10, ],
                                 [28, 99, 10, ],
                                 [137, 3, 20, ],
                                 [29, 28, 10, ],
                                 [94, 105, 10, ],
                                 [92, 107, 30, ],
                                 [10, 134, 10, ],
                                 [34, 79, 10, ],
                                 [94, 72, 20, ],
                                 [35, 76, 10, ],
                                 [76, 99, 20, ],
                                 [127, 28, 30, ],
                                 [8, 119, 20, ],
                                 [102, 110, 10, ],
                                 [24, 24, 10, ],
                                 [64, 61, 20, ],
                                 [22, 38, 20, ],
                                 [88, 72, 30, ],
                                 [107, 63, 30, ],
                                 [33, 131, 30, ],
                                 [123, 112, 20, ],
                                 [67, 55, 10, ],
                                 [39, 128, 10, ],
                                 [136, 0, 30, ],
                                 [93, 36, 20, ],
                                 [7, 115, 10, ],
                                 [21, 44, 20, ],
                                 [28, 74, 20, ],
                                 [86, 102, 10, ],
                                 [19, 37, 20, ],
                                 [84, 36, 10, ],
                                 [118, 108, 10, ],
                                 [132, 24, 10, ],
                                 [6, 25, 10, ],
                                 [28, 78, 10, ],
                                 [2, 132, 10, ],
                                 [22, 22, 10, ],
                                 [88, 35, 20, ],
                                 [94, 104, 10, ],
                                 [74, 96, 30, ],
                                 [0, 117, 30, ],
                                 [99, 96, 10, ],
                                 [119, 114, 20, ],
                                 [28, 107, 20, ],
                                 [133, 12, 10, ],
                                 [35, 102, 10, ],
                                 [36, 105, 20, ],
                                 [84, 39, 20, ],
                                 [34, 138, 20, ],
                                 [136, 29, 10, ],
                                 [33, 133, 20, ],
                                 [16, 39, 20, ],
                                 [32, 77, 20, ],
                                 [122, 131, 20, ],
                                 [77, 100, 20, ],
                                 [96, 26, 10, ],
                                 [127, 29, 20, ],
                                 [91, 95, 20, ],
                                 [42, 136, 10, ],
                                 [36, 132, 10, ],
                                 [103, 106, 30, ],
                                 [107, 105, 10, ],
                                 [96, 74, 10, ],
                                 [63, 57, 10, ],
                                 [122, 113, 20, ],
                                 [14, 131, 10, ],
                                 [30, 31, 20, ],
                                 [40, 132, 20, ],
                                 [99, 26, 40, ],
                                 [10, 118, 10, ],
                                 [102, 60, 30, ],
                                 [120, 136, 10, ],
                                 [97, 29, 30, ],
                                 [19, 39, 10, ],
                                 [27, 77, 10, ],
                                 [30, 24, 20, ],
                                 [126, 112, 10, ],
                                 [105, 110, 20, ],
                                 [118, 114, 10, ],
                                 [135, 6, 30, ],
                                 [111, 66, 20, ],
                                 [95, 77, 10, ],
                                 [139, 10, 30, ],
                                 [61, 54, 10, ],
                                 [16, 38, 20, ],
                                 [16, 138, 10, ],
                                 [91, 78, 10, ],
                                 [91, 71, 20, ],
                                 [0, 27, 30, ],
                                 [6, 113, 20, ],
                                 [119, 139, 20, ],
                                 [35, 99, 20, ],
                                 [31, 112, 20, ],
                                 [5, 119, 20, ],
                                 [3, 135, 20, ],
                                 [30, 136, 10, ],
                                 [20, 39, 10, ],
                                 [131, 11, 10, ],
                                 [28, 33, 20, ],
                                 [4, 23, 10, ],
                                 [87, 108, 20, ],
                                 [21, 26, 20, ],
                                 [121, 134, 20, ],
                                 [119, 130, 20, ],
                                 [91, 108, 10, ],
                                 [130, 27, 30, ],
                                 [101, 107, 10, ],
                                 [34, 108, 10, ],
                                 [131, 31, 20, ]]}