"""
Synthesize 1000 images of same structure
Name: AnDN
Email: andn@fpt.com
License: MIT License
"""
import os
import random
import json
from typing import Any, List, Dict, Tuple
from .TableGeneration.GenerateTable import GenerateTable
from bs4 import BeautifulSoup
from tqdm import tqdm
import codecs

def fill_id_and_border(html: str) -> str:
    # Fill id to each html data tag
    soup = BeautifulSoup(html, 'html.parser')
    soup.find('table')['border'] = '1'
    for i, td in enumerate(soup.find_all(['td', 'th'])):
        td['id'] = str(i)
    return str(soup)

def get_id_counts(gt_lines: List[Dict]) -> List[int]:
    # Count how many data cells in the html structure
    id_counts = [len([i for i in line['html']['structure']['tokens']
                      if i == '</td>'])
                      for line in gt_lines]
    return id_counts

def read_label_file(label_path: str):
    # Usually gt.txt
    gt_lines = []
    with open(label_path, 'r') as f:
        while True:
            line = f.readline()
            if not line.strip():
                break
            gt_lines.append(line)
    gt_lines = [json.loads(line) for line in gt_lines]
    return gt_lines

def get_english_dict(vocab_file: str):
    # Get English dictionary using a vocabulary file
    with open(vocab_file) as f:
        word_list = f.read().splitlines()
    return word_list

def random_number(number_range: Tuple[float] = (-10., 10.)) -> str:
    # Generate a random number in a range
    assert number_range[0] < number_range[1], "number_range must be in format (min, max)"
    number = str("{:.3f}".format(random.uniform(number_range[0],
                                                number_range[1])))
    number = random.choices(['$',''])[0] + number
    if number[:2] == "$-":
        number = "-$" + number[2:]
    return number

def random_word_float(word_list: List[str],
                      id_count: int,
                      word_prob: float = 0.6,
                      number_range: Tuple[float] = (-10., 10.),
                      ) -> List[str]:
    """
    Generate k random entities (word or number).
    Args:
        word_list (List[str]): list of English words.
        id_count (int): number of entities to generate.
        word_prob (float, optional): probability of return a word. Defaults to 0.6.
        number_range (Tuple[float], optional): Range of numbers to generate.
        Defaults to [-10., 10.].
    Returns:
        str: A list of k strings of either word or number.
    """
    if id_count < 1:
        raise ValueError("k must be greater than 0")
    if word_prob < 0. or word_prob > 1.:
        raise ValueError("word_prob must be in range [0, 1]")
    
    return [random.choices([random.choice(word_list), random_number(number_range)],
                              weights=[word_prob, 1.0-word_prob],
                              k=1)[0]
                              for _ in range(id_count)]


class SynthesizeTable:
    def __init__(self, input_path: str,
                 out_path: str,
                 en_dict: str = os.path.join(os.path.dirname(__file__),
                                             'corpus', 'google-10000-english.txt'),
                brower: str = 'chrome'):
        # only input the folder path, e.g. 'outputs/html' or 'outputs/img'
        if input_path == out_path:
            raise ValueError("input_path and out_path must be different")
        self.html_path = input_path + "\\html"
        self.img_path = input_path + "\\img"
        # usually gt.txt
        self.label_path = input_path + "\\gt.txt"
        self.out_path = out_path

        # read label file and add the content to gt_lines
        self.gt_lines = read_label_file(self.label_path)
        print(f"Read {len(self.gt_lines)} lines from {self.label_path}")

        # Get id counts for each line
        self.id_count = get_id_counts(self.gt_lines)
        print(f"Get id counts successfully")

        # Get english dictionary    
        self.en_dict = get_english_dict(en_dict)
        print(f"Read {len(self.en_dict)} words from corpus")

        # Create output folder
        os.makedirs(os.path.join(self.out_path, 'html'), exist_ok=True)
        os.makedirs(os.path.join(self.out_path, 'img'), exist_ok=True)

        self.generator = GenerateTable(output='path',
                        ch_dict_path = "dict/ch_news.txt",
                        en_dict_path = "dict/en_corpus.txt",
                        brower=brower)

    def __call__(self, num_synth: int = 10) -> None:
        self.synthesize(self.generator, num_synth)

    def synthesize(self,
                   generator: GenerateTable,
                   num_synth: int = 10):
        # Synthesize num_synth images of same structure
        with open(
            os.path.join(self.out_path, 'gt.txt'),
                         encoding='utf-8', mode='w') as f_gt:
            for i in range(len(self.gt_lines)):
                print("Synthesizing image", i+1)
                gt_line = self.gt_lines[i].copy()
                filename = os.path.splitext(gt_line['filename'])[0]
                id_count = self.id_count[i]
                # html_raw is html without ids and color, html_file does
                html_raw = gt_line['gt']
                soup_raw = BeautifulSoup(html_raw, 'html.parser')
                # Make sure html file exists, otherwise skip it
                html_file_present = False
                try:
                    html_path = os.path.join(self.html_path, filename + ".html")
                    with codecs.open(html_path, 'r') as f:
                        html_file = f.read()
                except FileNotFoundError:
                    print(f"File {html_path} not found. Using raw html file instead.")
                else:
                    soup_file = BeautifulSoup(html_file, 'html.parser')
                    html_file_present = True
                # Generate new words
                for k in tqdm(range(num_synth), desc="Synthesizing"):
                    new_texts = random_word_float(self.en_dict, id_count)
                    # print(len(new_texts), len(gt_line['html']['cells']))
                    for j, cell in enumerate(gt_line['html']['cells']):
                        cell['tokens'] = [*new_texts[j]]
                        if len(cell['bbox'][0]) == 4:
                            cell['bbox'] = [[cell['bbox'][0][0], cell['bbox'][0][2]]]
                    if html_file_present:
                        for j, td in enumerate(soup_file.find_all(['td', 'th'])):
                            # change content of that html tag
                            td.string = new_texts[j]
                        html_file = str(soup_file)
                    for j, td in enumerate(soup_raw.find_all(['td', 'th'])):
                        # change content of that html tag
                        td.string = new_texts[j]
                    html_raw = str(soup_raw)
                    gt_line['gt'] = html_raw
                    gt_line['filename'] = filename + f"_{k}.jpg"
                    if html_file_present:
                        img, contents = generator.html_to_img(html_file, id_count)
                    else:
                        html_raw = fill_id_and_border(html_raw)
                        img, contents = generator.html_to_img(html_raw, id_count)
                    img, contents = generator.clip_white(img, contents)
                    img.save(self.out_path + "\\img\\" + filename+ f"_{k}.jpg",
                            dpi=(600, 600))
                    # Output html, if it exists
                    if html_file_present:
                        with open(self.out_path + "\\html\\" + filename+f"_{k}.html",
                                encoding='utf-8', mode='w') as f:
                            f.write(html_file)
                    # Output new gt.txt
                    f_gt.write('{}\n'.format(
                    json.dumps(
                        gt_line, ensure_ascii=False)))
        

if __name__ == '__main__':
    syn = SynthesizeTable(input_path='test',
                          out_path='test_out')
    generator = GenerateTable(output='outputs',
                           ch_dict_path = "dict/ch_news.txt",
                           en_dict_path = "dict/en_corpus.txt",
                           brower='chrome')
    syn(generator,
        num_synth=1)
    generator.close()