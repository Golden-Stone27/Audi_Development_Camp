import numpy as np
from sklearn.linear_model import LinearRegression

def train_and_predict(new_temperature, new_volume):
    temperature = [
        20, 22, 24, 26, 28, 30, 32, 34, 36, 38, 40,
        42, 44, 46, 48, 50, 50, 50, 50, 50, 50,
        52, 55, 57, 59, 60, 60, 63, 65, 67,
        70, 72, 74, 75, 77, 78, 79,
        80, 82, 84, 86, 88, 90, 90, 93, 95, 97, 100
    ]

    volume = [
        90, 95, 100, 105, 110, 115, 120, 125, 130, 135, 140,
        200, 220, 240, 260, 200, 220, 240, 260, 280, 300,
        190, 210, 230, 250, 200, 240, 180, 270, 300,
        200, 230, 250, 275, 290, 260, 280,
        210, 240, 265, 285, 290, 200, 240, 270, 280, 300, 300
    ]

    water = [
        180, 190, 200, 215, 230, 245, 260, 275, 290, 305, 320,
        380, 400, 420, 440, 390, 410, 430, 450, 470, 490,
        410, 430, 450, 470, 495, 510, 480, 520, 540,
        560, 585, 600, 630, 650, 615, 640,
        670, 700, 720, 740, 760, 780, 800, 820, 840, 860, 880
    ]

    X = np.column_stack((temperature, volume))
    model = LinearRegression()
    model.fit(X, water)
    predicted_water = model.predict([[new_temperature, new_volume]])
    return predicted_water[0]
