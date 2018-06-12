import urllib2
import HTMLParser
import codecs
import json


class HTMLtoJSONParser(HTMLParser.HTMLParser):
    def __init__(self, raise_exception=True):
        HTMLParser.HTMLParser.__init__(self)
        self.doc = {}
        self.path = []
        self.cur = self.doc
        self.line = 0
        self.raise_exception = raise_exception

    @property
    def json(self):
        return self.doc

    @staticmethod
    def to_json(content, raise_exception=True):
        parser = HTMLtoJSONParser(raise_exception=raise_exception)
        parser.feed(content)
        return parser.json

    def handle_starttag(self, tag, attrs):
        self.path.append(tag)
        attrs = {k: v for k, v in attrs}
        if tag in self.cur:
            if isinstance(self.cur[tag], list):
                self.cur[tag].append({"__parent__": self.cur})
                self.cur = self.cur[tag][-1]
            else:
                self.cur[tag] = [self.cur[tag]]
                self.cur[tag].append({"__parent__": self.cur})
                self.cur = self.cur[tag][-1]
        else:
            self.cur[tag] = {"__parent__": self.cur}
            self.cur = self.cur[tag]

        for a, v in attrs.items():
            self.cur["#" + a] = v
        self.cur[""] = ""

    def handle_endtag(self, tag):
        if tag != self.path[-1] and self.raise_exception:
            raise Exception("html is malformed around line: {0} (it might be because of a tag <br>, <hr>, <img .. > not closed)".format(self.line))
        del self.path[-1]
        memo = self.cur
        self.cur = self.cur["__parent__"]
        self.clean(memo)

    def handle_data(self, data):
        self.line += data.count("\n")
        if "" in self.cur:
            self.cur[""] += data

    def clean(self, values):
        keys = list(values.keys())
        for k in keys:
            v = values[k]
            if isinstance(v, str):
                # print ("clean", k,[v])
                c = v.strip(" \n\r\t")
                if c != v:
                    if len(c) > 0:
                        values[k] = c
                    else:
                        del values[k]
        del values["__parent__"]


def text2json():
    import random
    out = open('eval_results/caption_zh_en.txt', 'r')
    lines = out.readlines()
    out = []
    explanation = {}
    for i in range(len(lines) / 5):
        tmp = [int(lines[i * 5].replace('\n','').split('/')[-1].split('_')[-1].replace('.jpg', '')), 0]
        explanation[str(int(lines[i * 5].replace('\n','').split('/')[-1].split('_')[-1].replace('.jpg', '')))] = lines[i * 5 + 4].replace('\n','')
        out.append(tmp)
    list_of_random_items = random.sample(range(1572), 327)
    for i in list_of_random_items:
        out.append(out[i])
    directory = 'main/users'
    for i in range(len(out)/100):
        with open(directory + '/u' + str(i) + '/im_c_list.json', 'w') as outfile:
            json.dump(out[i*100:i*100+100], outfile)
    with open('coco_caption_human_eval.json', 'w') as outfile:
        json.dump(explanation, outfile)

def gt2json():
    import random
    imgs = json.load(open('mscoco/dataset_coco.json', 'r'))
    imgs = imgs['images']
    out = {}
    for i, img in enumerate(imgs):
        out[str(img['cocoid'])] = img['sentences'][random.randint(0,4) ]['raw']

    json.dump(out, open('coco_caption_human_eval_gt.json', 'w'))

def analsys():
    import os
    from statistics import mean
    import shutil
    fluent_score = []
    correct_score = []
    fluent_score_u = []
    correct_score_u = []
    fluent_score_g = []
    correct_score_g = []
    directory = 'users'
    outdirs = [dI for dI in os.listdir(directory) if os.path.isdir(os.path.join(directory, dI))]
    for dir in outdirs:
        for file in os.listdir(directory + '/' + dir + '/result/'):
            if file.endswith(".json"):
                tmp = json.load(open(directory + '/' + dir + '/result/' + file, 'r'))
                fluent_score.append(tmp['fluent_score'])
                correct_score.append(tmp['correct_score'])
                fluent_score_u.append(tmp['fluent_score_u'])
                correct_score_u.append(tmp['correct_score_u'])
                fluent_score_g.append(tmp['fluent_score_g'])
                correct_score_g.append(tmp['correct_score_g'])

    max_len = len(fluent_score)
    print('Max length = {}'.format(max_len))
    avg_fluent_score = mean(fluent_score)
    avg_correct_score = mean(correct_score)
    avg_fluent_score_u = mean(fluent_score_u)
    avg_correct_score_u = mean(correct_score_u)
    avg_fluent_score_g = mean(fluent_score_g)
    avg_correct_score_g = mean(correct_score_g)
    print('User: Relevant {} Resemble {}'.format(avg_fluent_score, avg_correct_score))
    print('Upper: Relevant {} Resemble {}'.format(avg_fluent_score_u, avg_correct_score_u))
    print('GT: Relevant {} Resemble {}'.format(avg_fluent_score_g, avg_correct_score_g))

def avg_len():
    from statistics import mean
    out = open('tmp/coco_test_5k_en.txt', 'r')
    lines = out.readlines()
    len = []
    for line in lines:
        words = line.split()
        len.append(words.__len__())
    avg_len = mean(len)
    print('Average len {}'.format(avg_len))
analsys()
#avg_len()
