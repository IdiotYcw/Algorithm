# coding: utf-8
import os
import tensorflow as tf
from algorithm import settings

tf.app.flags.DEFINE_integer('model_version', 1, 'version number of the model.')
tf.app.flags.DEFINE_string('work_dir', settings.NER_ROOT, 'Working directory.')
tf.app.flags.DEFINE_string('model_dir', '/tmp/ner', 'saved model directory')
FLAGS = tf.app.flags.FLAGS


def export_saved_model(path=FLAGS.work_dir):
    with tf.Session() as sess:
        saver = tf.train.import_meta_graph(os.path.join(path, 'ner.ckpt.meta'))
        saver.restore(sess, tf.train.latest_checkpoint(path))

        export_path = os.path.join(
            tf.compat.as_bytes(FLAGS.model_dir),
            tf.compat.as_bytes(str(FLAGS.model_version)))
        builder = tf.saved_model.builder.SavedModelBuilder(export_path)

        pos = tf.placeholder(
            dtype=tf.int32,
            shape=[None, 300],
            name="pos"
        )
        ner = tf.placeholder(
            dtype=tf.int32,
            shape=[None, 300],
            name="ner"
        )

        tensor_info_x = tf.saved_model.utils.build_tensor_info(pos)
        tensor_info_y = tf.saved_model.utils.build_tensor_info(ner)

        prediction_signature = (
            tf.saved_model.signature_def_utils.build_signature_def(
                inputs={'pos': tensor_info_x},
                outputs={'ner': tensor_info_y},
                method_name=tf.saved_model.signature_constants.PREDICT_METHOD_NAME))

        legacy_init_op = tf.group(tf.tables_initializer(), name='legacy_init_op')  # ???
        builder.add_meta_graph_and_variables(
            sess, [tf.saved_model.tag_constants.SERVING],
            signature_def_map={
                tf.saved_model.signature_constants.DEFAULT_SERVING_SIGNATURE_DEF_KEY:
                    prediction_signature
            },
            legacy_init_op=legacy_init_op
        )

        builder.save()

if __name__ == '__main__':
    export_saved_model()
