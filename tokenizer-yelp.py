from __future__ import print_function
import argparse
import json
import random
from util import Dictionary
import spacy


# 划分训练集和验证集
def split_train_val():
    tf_lines = []
    vf_lines = []
    tf = open("data/train_json_data", 'w')
    vf = open("data/val_json_data", 'w')
    with open("data/train_text", 'r', encoding='utf-8') as f:
        for line in f.readlines():
            if random.randint(1, 8) == 3:
                vf_lines.append(line)
            else:
                tf_lines.append(line)
    for line in tf_lines:
        tf.write(line)
    for line in vf_lines:
        vf.write(line)
    tf.close()
    vf.close()


# 将文本转化为json表示
def trans_text_to_json():
    of = open("data/test_json_data", 'w', )
    with open("data/test_data", 'r', encoding='utf-8') as f:
        for line in f.readlines():
            if " 1\n" in line:
                json_line = {
                    'text': line.replace(" 1\n", "").split(),
                    'label': '1'
                }
            elif " 0\n" in line:
                json_line = {
                    'text': line.replace(" 0\n", "").split(),
                    'label': '0'
                }
            of.write(json.dumps(json_line) + "\n")
    of.close()
    print("Finish.")


if __name__ == '__main__':
    parser = argparse.ArgumentParser('Tokenizer')
    parser.add_argument('--input', type=str, default='', help='input file')
    parser.add_argument('--output', type=str, default='', help='output file')
    parser.add_argument('--dict', type=str, default='', help='dictionary file')
    args = parser.parse_args()
    args.input = "data/test_json_data"
    args.output = "data/test_json"
    args.dict = "data/dict_data"
    dictionary = Dictionary()
    dictionary.add_word('<pad>')  # add padding word
    with open(args.output, 'w') as fout:
        lines = open(args.input).readlines()
        random.shuffle(lines)
        for i, line in enumerate(lines):
            item = json.loads(line)
            words = item['text']
            data = {
                'label': item['label'],
                'text': words
            }
            fout.write(json.dumps(data) + '\n')
            for item in data['text']:
                dictionary.add_word(item)
            if i % 100 == 99:
                print('%d/%d files done, dictionary size: %d' %
                      (i + 1, len(lines), len(dictionary)))
        fout.close()
    '''
    with open(args.dict, 'w') as fout:  # save dictionary for fast next process
        fout.write(json.dumps(dictionary.idx2word) + '\n')
        fout.close()
    '''
