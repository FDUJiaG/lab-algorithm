import numpy as np
import mglearn
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.datasets import make_circles


X, y = make_circles(noise=0.25, factor=0.5, random_state=1)

# 为了便于说明，我们将两个类别重命名为 blue 和 red
y_named = np.array(["blue", "red"])[y]

# 我们可以对任意个数组调用 train_test_split
# 所有的数组的划分方式都是一致的
X_train, X_test, y_train_named, y_test_named, y_train, y_test = \
    train_test_split(X, y_named, y, random_state=0)

# 构建梯度提升模型
gbrt = GradientBoostingClassifier(random_state=0)
gbrt.fit(X_train, y_train_named)

print("X_test.shape:", X_test.shape)
print("Decision function shape:", gbrt.decision_function(X_test).shape)

# 显示 decision_function 的前几个数
print("Decision function:", gbrt.decision_function(X_test)[:6])

print("Thresholded decision function:\n", gbrt.decision_function(X_test) > 0)
print("Predictions:\n", gbrt.predict(X_test))

# 将布尔值 True/False 转换成 0 和 1
greater_zero = (gbrt.decision_function(X_test) > 0).astype(int)
# 利用 0 和 1 作为 classes_ 的索引
pred = gbrt.classes_[greater_zero]
# pred 与 gbrt.predict 的输出完全相同
print("pred is equal to predictions:", np.all(pred == gbrt.predict(X_test)))


fig, axes = plt.subplots(1, 2, figsize=(12, 5))
plt.subplots_adjust(left=0.1, right=0.85, top=0.85, bottom=0.1)
mglearn.tools.plot_2d_separator(gbrt, X, ax=axes[0], alpha=.4, fill=True, cm=mglearn.cm2)
scores_image = mglearn.tools.plot_2d_scores(gbrt, X, ax=axes[1], alpha=.4, cm=mglearn.ReBl)

for ax in axes:
    # 画成训练点和测试点
    mglearn.discrete_scatter(X_test[:, 0], X_test[:, 1], y_test, markers='^', ax=ax)
    mglearn.discrete_scatter(X_train[:, 0], X_train[:, 1], y_train, markers='o', ax=ax)
    ax.set_xlabel("Feature 0")
    ax.set_ylabel("Feature 1")
position = fig.add_axes([0.9, 0.1, 0.02, 0.75])  # 位置 [左, 下, 宽, 高]
cbar = plt.colorbar(scores_image, cax=position, ax=axes.tolist(), orientation="vertical")
cbar.set_alpha(1)
cbar.draw_all()
axes[0].legend(["Test class 0", "Test class 1", "Train class 0",
                "Train class 1"], ncol=4, loc=(.1, 1.1))
plt.show()
