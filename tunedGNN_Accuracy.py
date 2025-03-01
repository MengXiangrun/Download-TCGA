def tunedGNN_Accuracy(y_true, y_pred):
    acc_list = []
    y_true = y_true.detach().cpu().numpy()

    y_pred = F.log_softmax(y_pred, dim=1)
    predicted_classes = torch.argmax(y_pred, dim=1)
    num_classes = y_pred.shape[1]
    y_pred = F.one_hot(predicted_classes, num_classes=num_classes)
    y_pred = y_pred.detach().cpu().numpy()

    for i in range(y_true.shape[1]):
        is_labeled = y_true[:, i] > 0.0
        correct = y_true[is_labeled, i] == y_pred[is_labeled, i]

        acc = float(np.sum(correct)) / len(correct)
        acc_list.append(acc)

    return sum(acc_list) / len(acc_list)
