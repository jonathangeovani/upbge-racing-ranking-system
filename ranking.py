import bge


def updateCarCheckpoint(object):
    # Exit from function if the collided object is not a car
    if 'car' not in object:
        return
    
    next = object['curr_checkpoint'] + 1 if object['curr_checkpoint'] != len(checkpoints) - 1 else 0
    for idx, checkpoint in enumerate(checkpoints):
        if object.collide(checkpoint)[0] and idx == next:
            object['curr_checkpoint'] = next
            object['passed_checkpoints'] += 1
            if next == 0:
                object['curr_lap'] += 1


def main():
    ranking = []
    for car in cars:
        lap = car['curr_lap']
        next_checkpoint_id = (car['curr_checkpoint'] + 1) % len(checkpoints)
        next_checkpoint = checkpoints[next_checkpoint_id]
        passed_checkpoints = car['passed_checkpoints']
        ranking.append((car, lap, passed_checkpoints, car.getDistanceTo(next_checkpoint)))
        
    ranking.sort(key=lambda x: (-x[1], -x[2], x[3]))
    
    for (car, lap, next, distance) in ranking:
        car['rank'] = ranking.index((car, lap, next, distance)) + 1
        print(car, car['rank'])
                

# Initialization
scene = bge.logic.getCurrentScene()

cars = [obj for obj in scene.objects if 'car' in obj]
for car in cars: 
    car['curr_checkpoint'] = 0
    car['passed_checkpoints'] = 0
    car['curr_lap'] = 0
    car['rank'] = 0

checkpoints = [obj for obj in scene.objects if 'checkpoint' in obj]
checkpoints.sort(key=lambda ckp: ckp.name)

# Add the checkpoint collision verification to each checkpoint in the track
for checkpoint in checkpoints:
    checkpoint.collisionCallbacks.append(updateCarCheckpoint)