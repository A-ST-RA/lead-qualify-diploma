import numpy as np

y_true_input = input('y_true: ')
y_true = np.array(y_true_input.replace(' ', '').replace('[', '').replace(']', '').split(',')).astype(int)

y_prob_input = input('y_prob: ')
y_prob = np.array(y_prob_input.replace(' ', '').replace('[', '').replace(']', '').split(',')).astype(float)

threshold = float(input('threshold: '))
y_pred = (y_prob >= threshold).astype(int)

print(y_pred)

TN = np.sum((y_pred == 0) & (y_true == 0))
TP = np.sum((y_pred == 1) & (y_true == 1))
FP = np.sum((y_pred == 1) & (y_true == 0))
FN = np.sum((y_pred == 0) & (y_true == 1))

accuracy = (TP + TN) / (TP + TN + FP + FN)

print(f'TN: {TN}')
print(f'TP: {TP}')
print(f'FP: {FP}')
print(f'FN: {FN}')
print(f'Accuracy: {accuracy}')
