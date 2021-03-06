from tracker_particle import *

DIR_DATA_MOT = DATASET_FOLDER + "MOT17-11-FRCNN/"
DIR_FRAMES = DIR_DATA_MOT + "img1/"
INIT_FILE = DIR_DATA_MOT + "gt/gt.txt"

with open(INIT_FILE, "r") as file:
    lines = file.read().splitlines()[:900]
gt = np.array([item.split(',')[2:6] for item in lines], dtype=int)
person1_bbox = gt[0]

frame_list = glob.glob(DIR_FRAMES + "*.jpg")[:900]


def track_MOT(scale=0.25, box_size_evolution=1, particle_movement=20, nb_particles=200, histogram=True):
    bbox_list = tracker_particle(frame_list, [person1_bbox], printing=False,
                                 scale=scale, box_size_evolution=box_size_evolution, particle_movement=particle_movement, nb_particles=nb_particles, histogram=histogram)

    accuracy = 0
    for i, bbox in enumerate(bbox_list):
        res = iou(gt[i], bbox)
        if res > 0.5:
            accuracy += 1

    accuracy /= len(bbox_list)
    return accuracy


param_grid = {'scale': np.arange(0.1, 0.5, step=0.05), 'box_size_evolution': range(1, 16, 2),
              'particle_movement': range(1, 53, 3), 'nb_particles': np.append(range(10, 100, 10), range(100, 500, 50))}
histogram = False
for epoch in range(1000):
    print(f"Epoch {epoch}")
    scale = 0.25  # np.random.choice(param_grid["scale"])
    box_size_evolution = np.random.choice(param_grid["box_size_evolution"])
    particle_movement = np.random.choice(param_grid["particle_movement"])
    nb_particles = np.random.choice(param_grid["nb_particles"])
    print(f"Parameters : scale = {scale}, box_size_evolution = {box_size_evolution}, "
          f"particle_movement = {particle_movement}, nb_particles = {nb_particles}")
    score = track_MOT(scale=scale, box_size_evolution=box_size_evolution, particle_movement=particle_movement, nb_particles=nb_particles, histogram=histogram)
    print(f"Score = {score}")
    score_file = "score_orb.txt"
    if histogram:
        score_file = "score_hist.txt"
    with open(score_file, "a") as file:
        file.write(f"{scale};{box_size_evolution};{particle_movement};{nb_particles};{score}\n")


