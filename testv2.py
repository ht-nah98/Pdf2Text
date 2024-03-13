left = [[81, 278, 291, 586], [83, 615, 352, 625], [94, 630, 419, 846], [86, 850, 415, 860]]
mid = [[82, 0, 724, 117], [82, 45, 537, 117], [82, 122, 711, 156], [79, 170, 749, 237], [323, 277, 532, 586]]
right = [[565, 276, 766, 586], [443, 615, 731, 625], [447, 631, 781, 843], [524, 850, 770, 860]]

# Combine all lists
combined_data = left + mid + right

# Sort the combined list based on the y-coordinate (second element)
combined_data.sort(key=lambda x: x[1])

# Group elements with similar y values within a threshold
threshold = 10
groups = []
current_group = [combined_data[0]]
for bbox in combined_data[1:]:
    if abs(bbox[1] - current_group[-1][1]) <= threshold:
        current_group.append(bbox)
    else:
        groups.append(current_group)
        current_group = [bbox]
groups.append(current_group)

# Sort each group based on x-coordinate
sorted_groups = [sorted(group, key=lambda x: x[0]) for group in groups]

# Concatenate all sorted groups to get the final sorted list
final_sorted_list = [bbox for group in sorted_groups for bbox in group]

print(final_sorted_list)