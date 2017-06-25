class PyramidGenerator:
    def __init__(self,
                 session,
                 log2_input_size,
                 log2_output_size,
                 num_features,
                 convs_per_cell,
                 filter_size,
                 conv_activation,
                 num_attributes,
                 name = 'pyrgen'):

        self.session = session
        self.log2_input_size = log2_input_size
        self.log2_output_size = log2_output_size
        self.num_attributes = num_attributes

        if not hasattr(num_features, '__iter__'):
            num_features = [num_features] * (log2_output_size - log2_input_size)
        if not hasattr(convs_per_cell, '__iter__'):
            convs_per_cell = [convs_per_cell] * (log2_output_size - log2_input_size)
        if not hasattr(filter_size, '__iter__'):
            filter_size = [filter_size] * (log2_output_size - log2_input_size)

        with tf.variable_scope(name) as scope:
            self.training_images = tf.placeholder(tf.float32, (None, 2 ** log2_output_size, 2 ** log2_output_size, 3), 'training_images')
            if num_attributes:
                self.image_attributes = tf.placeholder(tf.float32, (None, num_attributes))
            self.seed_images = tf.placeholder(tf.float32, (None, 2 ** log2_input_size, 2 ** log2_input_size, 3), 'seed_images')
            self.learning_rate = tf.placeholder(tf.float32, (), 'learning_rate')

            self.scope_name = scope.name
            self.cost = 0

            def _augment(img):
                img = tf.image.random_flip_left_right(img)
                return img

            augmented = tf.map_fn(_augment, self.training_images)
            training_scales = {s:tf.image.resize_area(augmented, (2 ** s, 2 ** s)) for s in range(log2_input_size, log2_output_size + 1)}
            x_gen = self.seed_images
            x_train = None
            if num_attributes:
                h_gen = h_train = tf.tile(tf.reshape(self.image_attributes, (-1, 1, 1, num_attributes)), (1, 2 ** log2_input_size, 2 ** log2_input_size, 1))
            else:
                h_gen = h_train = None

            self.generator_outputs = []

            for n_features, conv_size, n_convs, log2_size in zip(num_features, filter_size, convs_per_cell, range(log2_input_size, log2_output_size)):
                size = 2 ** log2_size
                with tf.variable_scope('level_%d' % size) as level_scope:
                    y_train = training_scales[log2_size + 1]
                    x_train = training_scales[log2_size]

                    x_train, h_train = ops.sharpen_cell(x_train, h_train, 2, n_features, conv_size, n_convs, conv_activation, 'upsampler')
                    self.cost += tf.reduce_mean((x_train - y_train) ** 2)

                    level_scope.reuse_variables()

                    x_gen, h_gen = ops.sharpen_cell(x_gen, h_gen, 2, n_features, conv_size, n_convs, conv_activation, 'upsampler')
                    self.generator_outputs.append(tf.clip_by_value(x_gen, -1, 1))

            with tf.variable_scope('training'):
                opt = tf.train.AdamOptimizer(self.learning_rate)
                grads = opt.compute_gradients(self.cost)
                grads = [(tf.clip_by_value(g, -1.0, 1.0), v) for g, v in grads]
                self.train_step = opt.apply_gradients(grads)

            self.variables = tf.get_collection(tf.GraphKeys.VARIABLES, self.scope_name)
            self.init_vars = tf.initialize_variables(self.variables)
            self.saver = tf.train.Saver(self.variables)

    def save(self, fn):
        self.saver.save(self.session, fn)

    def restore(self, fn):
        self.saver.restore(self.session, fn)

    def initialize(self):
        self.session.run(self.init_vars)

    def train(self, training_images, validation_images = [], learning_rate = 1e-3, batch_size = 32):
        with ThreadPoolExecutor(max(os.cpu_count(), batch_size)) as exc:
            def _loadImage(fn):
                img = cv2.imread(fn, cv2.IMREAD_COLOR)
                img = cv2.resize(img, (2 ** self.log2_output_size, 2 ** self.log2_output_size))
                return np.float32(img / 128.0 - 1.0)

            def _loadBatch(b):
                if self.num_attributes:
                    imgs, attrs = zip(*b)
                else:
                    imgs = b
                    attrs = None
                imgs = list(exc.map(_loadImage, imgs))
                return imgs, attrs

            total_cost = 0
            batches = list(_batch(training_images, batch_size, False))
            loader = exc.submit(_loadBatch, batches[0])
            for i in range(len(batches)):
                imgs, attrs = loader.result()
                if i < len(batches) - 1:
                    loader = exc.submit(_loadBatch, batches[i + 1])
                feed_dict = {self.training_images: imgs, self.learning_rate: learning_rate}
                if self.num_attributes:
                    feed_dict.update({self.image_attributes: attrs})
                total_cost += self.session.run((self.cost, self.train_step), feed_dict)[0]
                print('Training Batch(%d/%d) Cost(%e)' % (i + 1, len(batches), total_cost / (i + 1)), end = '\r')
            print()
            return total_cost / (i + 1)

    def generate_random(self):
        img = np.clip(np.random.randn(1, 2 ** self.log2_input_size, 2 ** self.log2_input_size, 3), -1, 1)
        if self.num_attributes:
            attrs = np.random.choice((1.0, -1.0), size = (1, self.num_attributes))
            feed = {self.seed_images: img, self.image_attributes: attrs}
        else:
            feed = {self.seed_images: img}
        y = self.session.run(self.generator_outputs, feed)
        return [img] + y

    def generate_from(self, seed_image):
        if self.num_attributes:
            img, attrs = seed_image
        else:
            img = seed_image
        img = cv2.imread(img, cv2.IMREAD_COLOR)
        img = cv2.resize(img, (2 ** self.log2_input_size, 2 ** self.log2_input_size))
        img = np.expand_dims(np.float32(img / 128.0 - 1.0), 0)
        if self.num_attributes:
            feed = {self.seed_images: img, self.image_attributes: [attrs]}
        else:
            feed = {self.seed_images: img}
        y = self.session.run(self.generator_outputs, feed)
        return [img] + y