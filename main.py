from office import *
from tags import *
import matplotlib.pyplot as plt
import csv
from nn_keras import *

colors = ["red", "blue", "brown", "black", "purple", "yellow", "pink", "orange"]

def K_Means_Clustering(landmarks, products): #K means clustering w.r.t max rssi values 
    for product in products:
        product.set_max_rssi()
    for landmark in landmarks:
        landmark.set_max_rssi()
    centres  = [[landmark.max_time, landmark.max_rssi] for landmark in landmarks]
    for product in products:
        distances = [math.dist([product.max_time, product.max_rssi], i) for i in centres]
        min_distance = min(distances)
        index_min = distances.index(min_distance)
        product.color = landmarks[index_min].color
        product.predicted_landamrk_id = landmarks[index_min].id
    plot_rssi(products, landmarks)    



def write_data(passive_landmarks, landmarks, products): #writing data for data genertion by NN_training_testing.ipynb
    active_landmark_list = []
    for landmark in landmarks:
        for i in range(0, len(landmark.timestamp)):
            active_landmark_list.append([landmark.id, landmark.rssi[i], landmark.timestamp[i]])
    product_list = []
    for product in products:
        for i  in range(len(product.rssi)):
            product_list.append([product.item_no, product.id, product.rssi[i], product.timestamp[i], product.actual_landmark_id])

    landmark_list = []
    for landmark in passive_landmarks:
        for i in range(0, len(landmark.timestamp)):
            landmark_list.append([landmark.id, landmark.rssi[i], landmark.timestamp[i]])
            
    with open('Products.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(product_list)
    with open('Active_Landmarks.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(active_landmark_list)

    with open('Landmarks.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(landmark_list)


def main():
    result = animation() #draw animation for data generation
    products = result[0]    
    landmarks = result[1]
    passive_landmarks = result[2]
    sections = result[3]

    color_dict = {}
    for landmark in landmarks: #hash map for colours and location
        color_dict[landmark.id] = landmark.color

    #calculatigm the rssi value for all tags to use for prediction
    calculate_rssi(products)
    calculate_rssi(landmarks)
    calculate_rssi(passive_landmarks)

    #writing the data for each landmark and product
    write_data(passive_landmarks, landmarks, products)

    #prediction with the loaded NN generated by NN_training_testing.ipynb
    products = run_model(products, passive_landmarks, landmarks, color_dict)
    #K_Means_Clustering(landmarks, products)
    result_renderer(products, landmarks, sections) #render the results to a new animation window for visualization of the classification results

if __name__ == '__main__':
    main()