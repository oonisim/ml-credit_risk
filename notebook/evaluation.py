from sklearn.metrics import (
    accuracy_score,
    recall_score,
    roc_auc_score,
    precision_score,
    f1_score,
    classification_report,
    confusion_matrix,
    roc_curve
)
import matplotlib.pyplot as plt


def evaluate_roc(model, X_test, y_test, model_name):
    # Predicting proba
    y_pred_prob = model.predict_proba(X_test)[:,1]

    # Generate ROC curve values: fpr, tpr, thresholds
    fpr_xb, tpr_xb, thresholds = roc_curve(y_test, y_pred_prob)

    # Plot ROC curve
    plt.plot([0, 1], [0, 1], 'k--')
    plt.plot(fpr_xb, tpr_xb)
    plt.xlabel(f'{model_name} False Positive Rate')
    plt.ylabel(f'{model_name} True Positive Rate')
    plt.grid()
    plt.title(f'{model_name}  ROC Curve')
    plt.show()


def evaluate_model(model, X_test, y_test, model_name):
    y_pred = model.predict(X_test)
    y_pred_prob = model.predict_proba(X_test)[:, 1]

    results = {
        'Model': model_name,
        'Accuracy': accuracy_score(y_test, y_pred),
        'Recall': recall_score(y_test, y_pred),
        'Precision': precision_score(y_test, y_pred),
        'F1': f1_score(y_test, y_pred),
        'AUC': roc_auc_score(y_test, y_pred_prob)
    }

    print(f"\n{model_name} Results:")
    print(f"Confusion Matrix\n{confusion_matrix(y_test, y_pred)}")

    for metric, value in results.items():
        if metric != 'Model':
            print(f"{metric}: {value:.4f}")

    print(f"classification report\n{classification_report(y_test, y_pred)}")

    evaluate_roc(model, X_test, y_test, model_name)
    return results
