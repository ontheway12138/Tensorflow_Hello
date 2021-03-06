import tensorflow as tf
from numpy.random import RandomState
batch_size = 8

w1 = tf.Variable(tf.random_normal((2, 3), stddev=1, seed=1))
w2 = tf.Variable(tf.random_normal((3, 1), stddev=1, seed=1))

# None方便使用不同batch大小
x = tf.placeholder(tf.float32, shape=(None, 2), name="x-input")
y_ = tf.placeholder(tf.float32, shape=(None, 1), name="y-input")
a = tf.matmul(x, w1)
y = tf.matmul(a, w2)

# 损失函数和反向传播
# clip_by_value 用来把数限定在某一范围
y = tf.sigmoid(y)
cross_entropy = -tf.reduce_mean(y_ * tf.log(tf.clip_by_value(y, 1e-10, 1.0)) + (
    1 - y_) * tf.log(tf.clip_by_value(1 - y, 1e-10, 1.0)))
train_step = tf.train.AdamOptimizer(0.001).minimize(cross_entropy)

# 通过随机数生成模拟数据集
rdm = RandomState(1)
dataset_size = 128
X = rdm.rand(dataset_size, 2)
# 定义 x1 + x2 < 1 为正样本
Y = [[int(x1 + x2 < 1)] for (x1, x2)in X]

with tf.Session() as sess:
    # 初始化变量
    init_op = tf.global_variables_initializer()
    sess.run(init_op)

    # 打印初始值
    print(sess.run(w1))
    print(sess.run(w2))

    # 训练轮数
    STEPS = 5000
    for i in range(STEPS):
        # 选取batch_size个样本训练
        start = (i * batch_size) % dataset_size
        end = min(start + batch_size, dataset_size)

        # 通过选取样本训练神经网络并更新参数
        sess.run(train_step, feed_dict={x: X[start:end], y_: Y[start:end]})
        if i % 1000 == 0:
            # 每隔一段时间计算在所有数据上的交叉熵并输出
            total_cross_entropy = sess.run(
                cross_entropy, feed_dict={x: X, y_: Y})
            print("After %d training step(s), cross entropy on all data is %g" % (
                i, total_cross_entropy))

    # 训练后的值
    print(sess.run(w1))
    print(sess.run(w2))
