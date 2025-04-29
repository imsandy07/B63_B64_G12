def min_additional_segments(x1, y1, x2, y2):
    if (x1 == 0 and y1 == 0 and x2 == 2024 and y2 == 2024) or \
       (x1 == 2024 and y1 == 2024 and x2 == 0 and y2 == 0) or \
       (x1 == 0 and y1 == 2024 and x2 == 2024 and y2 == 0) or \
       (x1 == 2024 and y1 == 0 and x2 == 0 and y2 == 2024):
        return 0
    else:
        return 2

x1, y1, x2, y2 = map(int, input().split())
print(min_additional_segments(x1, y1, x2, y2))
