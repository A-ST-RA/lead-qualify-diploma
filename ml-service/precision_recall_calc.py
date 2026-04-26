TN = int(input('TN: '))
TP = int(input('TP: '))
FP = int(input('FP: '))
FN = int(input('FN: '))

precision = TP / (TP + FP)
recall = TP / (TP + FN)
f1 = 2 * (precision * recall) / (precision + recall)

print(f'Precision: {precision}')
print(f'Recall: {recall}')
print(f'F1: {f1}')
accuracy = (TP + TN) / (TP + TN + FP + FN)
print(f'Accuracy: {accuracy}')