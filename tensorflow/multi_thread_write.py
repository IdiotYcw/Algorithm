import os
os.environ['DJANGO_SETTINGS_MODULE'] = \
    'algorithm.settings'
import sys
import django
import matplotlib.image as mpimg
import numpy as np
import tensorflow as tf
import pandas as pd
import threading
import time
import multiprocessing
import gevent
from material.models import Material
from estimation.preprocess import TagIndex
import gc


# sys.path.append('/home/ycw/PycharmProjects/algorithm/algorithm')
# os.environ['DJANGO_SETTINGS_MODULE'] = \
#     'algorithm.settings'
# django.setup()


# get the amount of files in folder
def sizeOfFolder(folder_path):
    fileNameList = os.listdir(path=folder_path)
    size = 0
    for fileName in fileNameList:
        if os.path.isfile(path=os.path.join(folder_path, fileName)):
            size += 1
    return size


def process_img(size, folder_path, th_num, th_ind, isTrain=False, labels=None):
    name = 'train' if isTrain else 'test'

    batch = int(size / th_num)
    outfile = './utility/TFRecords/multi_%s-%.5d.tfrecords' % (name, th_ind)
    writer = tf.python_io.TFRecordWriter(outfile)
    start = batch * (th_ind - 1) + 1
    end = start + batch if th_ind != th_num else size + 1
    # print('start from %s to the end %s' % (start, end-1))

    for f in range(start, end):
        if (f - start + 1) % 50000 == 0:
            print('[thread %d]: Processed %s\'th images in thread batch.' % (th_ind, f))
        filename = folder_path + str(f) + ".png"
        try:
            img = mpimg.imread(fname=filename)
        except FileNotFoundError:
            continue
        width = img.shape[0]
        # print(width)
        # trans to string
        img_raw = img.tostring()

        if isTrain:
            example = tf.train.Example(
                features=tf.train.Features(
                    feature={
                        "img_raw": tf.train.Feature(bytes_list=tf.train.BytesList(value=[img_raw])),
                        "label": tf.train.Feature(int64_list=tf.train.Int64List(value=[labels[f - 1]])),
                        "width": tf.train.Feature(int64_list=tf.train.Int64List(value=[width]))
                    }
                )

            )
            writer.write(record=example.SerializeToString())
        else:
            example = tf.train.Example(
                features=tf.train.Features(
                    feature={
                        "img_raw": tf.train.Feature(bytes_list=tf.train.BytesList(value=[img_raw])),
                        "width": tf.train.Feature(int64_list=tf.train.Int64List(value=[width]))
                    }
                )

            )
            writer.write(record=example.SerializeToString())
    writer.close()

# path(path of folder)
# if isTrain=True,labels can't be None
def pics_to_TFRecord(folder_path, labels=None, isTrain=False, isMultiThread=False):
    size = sizeOfFolder(folder_path=folder_path)
    print('\nThe num of files in %s is %s\n' % (folder_path, size))
    th_num = int(input('threads number?')) if isMultiThread else 1

    # train set
    if isTrain:
        if labels is None:
            print("labels can't be None!!!")
            return None
        if labels.shape[0] != size:
            print("something wrong with shape!!!")
            return None

        if isMultiThread:
            print("Begin write --Train-- TFRecords with --multi(%s)-- threads" % th_num)
            start = time.time()

            # use gevent
            # threads = [gevent.spawn(
            #     process_img, size, folder_path, th_num, i, True, labels) for i in range(1, th_num + 1)]
            # gevent.joinall(threads)

            # use muliti process
            # process = [multiprocessing.Process(
            #     target=process_img, args=(size, folder_path, th_num, i, True, labels)) for i in range(1, th_num + 1)]
            # for p in process:
            #     p.start()

            # use multi threads
            # coord = tf.train.Coordinator()
            # threads = [threading.Thread(
            #     target=process_img, args=(size, folder_path, th_num, i, True, labels)) for i in range(1, th_num + 1)]
            # for t in threads:
            #     t.start()
            # coord.join(threads)

            # use process pool
            pool = multiprocessing.Pool(4)
            for i in range(1, 5):
                pool.apply_async(process_img, args=(size, folder_path, th_num, i, True, labels))
            pool.close()
            pool.join()

            print("Write --Multi Train-- TFRecords Time taken: %f\n" % (time.time() - start))
        else:
            writer = tf.python_io.TFRecordWriter("./utility/TFRecords/single_train.tfrecords")
            print("Begin write --Train-- TFRecords with --single-- thread")
            start = time.time()
            for i in range(1, size + 1):
                print("----------processing the ", i, "\'th image----------") if i % 10000 == 0 else None
                filename = folder_path + str(i) + ".png"
                img = mpimg.imread(fname=filename)
                width = img.shape[0]
                # print(width)
                # trans to string
                img_raw = img.tostring()

                example = tf.train.Example(
                    features=tf.train.Features(
                        feature={
                            "img_raw": tf.train.Feature(bytes_list=tf.train.BytesList(value=[img_raw])),
                            "label": tf.train.Feature(int64_list=tf.train.Int64List(value=[labels[i - 1]])),
                            "width": tf.train.Feature(int64_list=tf.train.Int64List(value=[width]))
                        }
                    )

                )
                writer.write(record=example.SerializeToString())
            writer.close()
            print("Write --Single Train-- TFRecords Time taken: %f\n" % (time.time() - start))

    # test set
    else:
        if isMultiThread:
            print("Begin write --Test-- TFRecords with --multi(%s)-- threads" % th_num)
            start = time.time()

            # use multi threads
            # coord = tf.train.Coordinator()
            # threads = [threading.Thread(
            #     target=process_img, args=(size, folder_path, labels, th_num, i)) for i in range(1, th_num+1)]
            # for t in threads:
            #     t.start()
            # coord.join(threads)

            # use process pool
            pool = multiprocessing.Pool(4)
            for i in range(1, 5):
                pool.apply_async(process_img, args=(size, folder_path, th_num, i))
            pool.close()
            pool.join()

            print("Write --Multi Test-- TFRecords Time taken: %f\n" % (time.time() - start))
        else:
            writer = tf.python_io.TFRecordWriter("./utility/TFRecords/single_test.tfrecords")
            print("Begin write --Test-- TFRecords with --single-- thread")
            start = time.time()
            for i in range(1, size + 1):
                print("----------processing the ", i, "\'th image----------") if i % 100000 == 0 else None
                filename = folder_path + str(i) + ".png"
                img = mpimg.imread(fname=filename)
                width = img.shape[0]
                # print(width)
                # trans to string
                img_raw = img.tostring()

                example = tf.train.Example(
                    features=tf.train.Features(
                        feature={
                            "img_raw": tf.train.Feature(bytes_list=tf.train.BytesList(value=[img_raw])),
                            "width": tf.train.Feature(int64_list=tf.train.Int64List(value=[width]))
                        }
                    )

                )
                writer.write(record=example.SerializeToString())
            writer.close()
            print("Write --Single Test-- TFRecords Time taken: %f\n" % (time.time() - start))


train_labels_frame = pd.read_csv("/home/ycw/multi_thread_test/trainLabels.csv")
train_labels_frame_dummy = pd.get_dummies(data=train_labels_frame)
# print(train_labels_frame_dummy)
train_labels_frame_dummy.pop(item="id")
# print(train_labels_frame_dummy)
train_labels_values_dummy = train_labels_frame_dummy.values
# print(train_labels_values_dummy)
train_labels_values = np.argmax(train_labels_values_dummy, axis=1)
# print(train_labels_values)


def queryset_iterator(queryset, count, chunksize=100):
    """
    Iterate over a Django Queryset ordered by the primary key

    This method loads a maximum of chunksize rows in it's
    memory at the same time while django normally would load all rows in it's
    memory. Using the iterator() method only causes it to not preload all the
    classes.

    Note that the implementation of the iterator does not support ordered
    query sets.
    """
    pk = 0
    last_pk = queryset.order_by('-pk')[0].pk
    print(last_pk, queryset.count())
    queryset = queryset.order_by('pk')
    while pk < last_pk:
        for row in queryset.filter(pk__gt=pk)[:chunksize]:
            pk = row.pk
            yield row
        gc.collect()


def process_material_batch(words, pos, ner, mul_ind):
    # start = batch * (mul_ind - 1)
    # end = batch * mul_ind if mul_ind != mul else count
    # batch_queryset = querset[start: end]
    # ti = TagIndex()
    writer = tf.python_io.TFRecordWriter('./utility/TFRecords/material_%.5d.tfrecords' % mul_ind)

    print("[Process %s]: Begin write material TFRecords" % mul_ind)
    # for q in queryset_iterator(batch_queryset, batch_queryset.count()):
    #     word_index, pos_index, ner_index = [], [], []
    #     if q.words:
    #         for wl in q.words:
    #             word_index.extend(ti.tags_to_indexes(wl, 'word'))
    #     if q.pos:
    #         for pl in q.pos:
    #             for p in pl:
    #                 pos_index.extend(ti.tags_to_indexes(p, 'pos'))
    #     if q.ner:
    #         for nl in q.ner:
    #             for n in nl:
    #                 ner_index.extend(ti.tags_to_indexes(n, 'ner'))
    assert len(words) == len(pos) == len(ner)
    start = time.time()
    for i in range(len(words)):

        example = tf.train.Example(
            features=tf.train.Features(
                feature={
                    'words': tf.train.Feature(int64_list=tf.train.Int64List(value=words[i])),
                    'pos': tf.train.Feature(int64_list=tf.train.Int64List(value=pos[i])),
                    'ner': tf.train.Feature(int64_list=tf.train.Int64List(value=ner[i]))
                }
            )
        )
        writer.write(record=example.SerializeToString())

    writer.close()
    # gc.collect()
    use = time.time() - start
    print("[Process %s]:Write TFRecords Time taken: %f\n" % (mul_ind, use))
    # return use


def test(x, y, z, i):
    print(x, y, z, x+y+z)
    time.sleep(2)
    print('end')


def material_to_tfrecord(isMulti=False):
    mul = multiprocessing.cpu_count()
    materials = Material.objects.filter(source='people-daily').order_by('pk')
    origin = materials[0].pk
    count = materials.count()
    batch_size = int(count / mul)
    print(mul, count, batch_size)

    if isMulti:
        print("Begin write material TFRecords with %s process" % mul)
        # start = time.time()
        process, threads = [], []
        for i in range(1, mul+1):
            start = batch_size * (i - 1)
            end = batch_size * i if i != mul else count
            batch_queryset = Material.objects.filter(
                source='people-daily', pk__gte=origin+start, pk__lt=origin+end)

            ti = TagIndex()
            words, pos, ner = [], [], []
            for q in queryset_iterator(batch_queryset, batch_queryset.count()):
                # print('now process the %s material' % q.pk)
                word_index, pos_index, ner_index = [], [], []
                if q.words:
                    for wl in q.words:
                        word_index.extend(ti.tags_to_indexes(wl, 'word'))
                if q.pos:
                    for pl in q.pos:
                        for p in pl:
                            pos_index.extend(ti.tags_to_indexes(p, 'pos'))
                if q.ner:
                    for nl in q.ner:
                        for n in nl:
                            ner_index.extend(ti.tags_to_indexes(n, 'ner'))

                words.append(word_index)
                pos.append(pos_index)
                ner.append(ner_index)

            # process.append(multiprocessing.Process(
            #     target=process_material_batch, args=(words, pos, ner, i)))
            threads.append(threading.Thread(
                target=process_material_batch, args=(words, pos, ner, i)))

        start = time.time()

        coord = tf.train.Coordinator()
        for t in threads:
            t.start()
        coord.join(threads)

        # for p in process:
        #     p.start()
        # for p in process:
        #     p.join()

        # use process pool
        # pool = multiprocessing.Pool(mul)
        # for i in range(1, mul+1):
        #     # pool.apply_async(process_material_batch, args=(materials, batch_size, i, mul, count))
        #     pool.apply_async(test, args=(mul, count, batch_size, i))
        # pool.close()
        # pool.join()
        print("Write --Multi-- TFRecords Time taken: %f\n" % (time.time() - start))
    else:
        ti = TagIndex()
        writer = tf.python_io.TFRecordWriter('./utility/TFRecords/material_single.tfrecords')
        print("Begin write material TFRecords")
        start = time.time()
        for q in queryset_iterator(materials, count):
            word_index = ti.tags_to_indexes(q.word, 'word') if q.word else []
            pos_index = ti.tags_to_indexes(q.pos, 'pos') if q.pos else []
            ner_index = ti.tags_to_indexes(q.ner, 'ner') if q.ner else []

            example = tf.train.Example(
                features=tf.train.Feature(
                    feature={
                        'word': tf.train.Feature(int64_list=tf.train.Int64List(value=word_index)),
                        'pos': tf.train.Feature(int64_list=tf.train.Int64List(value=pos_index)),
                        'ner': tf.train.Feature(int64_list=tf.train.Int64List(value=ner_index))
                    }
                )
            )
            writer.write(record=example.SerializeToString())

        writer.close()
        print("Write --Single-- TFRecords Time taken: %f\n" % (time.time() - start))

# write record single
if input('single process?') == 'y':
    material_to_tfrecord()

# write record multi
if input('multi process?') == 'y':
    material_to_tfrecord(isMulti=True)

# write train record
if input('train single thread?') == 'y':
    pics_to_TFRecord(folder_path="/home/ycw/multi_thread_test/train/", labels=train_labels_values, isTrain=True)

# write test record
if input('test single thread?') == 'y':
    pics_to_TFRecord(folder_path="/home/ycw/multi_thread_test/test/")

# write train record with multi threads
if input('train multi threads?') == 'y':
    pics_to_TFRecord(folder_path="/home/ycw/multi_thread_test/train/", labels=train_labels_values, isTrain=True, isMultiThread=True)

# write test record with multi threads
if input('test multi threads?') == 'y':
    pics_to_TFRecord(folder_path="/home/ycw/multi_thread_test/test/", isMultiThread=True)
