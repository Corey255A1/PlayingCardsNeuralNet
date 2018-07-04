import numpy as np
import pandas as pd

trainraw = pd.read_csv('D:\\Documents\\CodeProjects\\PlayingCardsNeuralNet\\Cards.txt')

filenames = trainraw['FILENAME'].values
ids = trainraw['ID'].values
cardnames = trainraw['CARD'].values

