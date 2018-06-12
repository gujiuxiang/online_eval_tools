import json
im_q_list = []
for i in range(20,30):
    for j in range(0,2):
        im_q_list.append([i, j])

with open('im_q_list.json', 'w') as outfile:
    json.dump(im_q_list, outfile)
