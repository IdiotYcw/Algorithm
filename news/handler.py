import re
import csv
import json
import math
from news.preprocess import re_cut_sentences


class NewsHandler(object):
    def __init__(self,):
        self._freq_dict = {}
        self._dis_dict = {}

    def check_trigger(self, text):
        raise NotImplementedError

    def check_argument(self, text):
        raise NotImplementedError

    def check_entity(self, text):
        raise NotImplementedError

    def pair_prop(self):
        raise NotImplementedError

    def _dis_2_score(self, dis):
        return 1 / pow(math.e, dis / 3)

    def _freq_2_score(self, freq):
        return freq

    def _cal_freq_score(self, entity_list):
        for item in entity_list:
            entity = item.get('entity')
            if self._freq_dict.get(entity):
                self._freq_dict[entity] += 1
            else:
                self._freq_dict[entity] = 1


class StockNewsHandler(NewsHandler):
    def __init__(self):
        super(StockNewsHandler, self).__init__()
        self.keys = []
        with open('./stock.json', 'r') as f:
            self.map = json.load(f)
        if self.map:
            self.keys = list(self.map.keys())

        self.entity = set()
        self.trigger = []
        self.event_pair = {}

    def check_trigger(self, sentence):
        pass

    def check_argument(self, sentence):
        pass

    def _search_entity(self, text):
        entity_dict = {}
        for idx, sentence in enumerate(re_cut_sentences(text)):
            for k in self.keys:
                if k in sentence:
                    if not entity_dict.get(k):
                        entity_dict[k] = [idx]
                    else:
                        entity_dict[k].append(idx)
        return entity_dict

    def padding_entity(self, entity, entity_dict):
        if entity not in entity_dict.keys():
            return [0, 0]
        else:
            locations = entity_dict.get(entity)
            loca_scores = sum([self._dis_2_score(d) for d in locations])
            return [len(locations), loca_scores]


    def _check_entity(self, text):
        entity_list = []
        for idx, sentence in enumerate(re_cut_sentences(text)):
            entity_list.extend([k for k in self.keys if k in sentence])
        return set(entity_list)

    def check_entity(self, text):
        return self._search_entity(text)

    def pair_prop(self):
        pass


if __name__ == '__main__':
    snh = StockNewsHandler()
    # print(snh.keys)
    for i in range(6, 7):
        res_list = []
        count = 0
        with open('../materials/stock_news__00%d.csv' % i, 'r') as f:
            reader = csv.reader(f, dialect='excel', delimiter=',')
            for line in reader:
                title_entities = snh._search_entity(line[1])
                summary_entities = snh._search_entity(line[2])
                content_entities = snh._search_entity(line[3])
                entity_list = eval(line[4])
                el = len(entity_list)
                print('\n\n')
                print(line[1])
                print(line[2])
                print(line[3])
                for entity in entity_list:
                    item = [line[0]]
                    item.extend(snh.padding_entity(entity, title_entities))
                    item.extend(snh.padding_entity(entity, summary_entities))
                    item.extend(snh.padding_entity(entity, content_entities))
                    item.append(el)
                    print(item)
                    conf = input('%s is Topic?[y/N]:' % entity)
                    if conf == 'y':
                        item.append(1)
                    else:
                        item.append(0)
                    res_list.append(item)

        # with open('stock_news__00%d.csv' % i, 'w') as f:
        #     writer = csv.writer(f, dialect='excel', delimiter=',')
        #     writer.writerows(res_list)
