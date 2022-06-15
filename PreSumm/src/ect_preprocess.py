import stanza
import os, json
from tqdm import tqdm
from stanza.pipeline.processor import Processor, register_processor, register_processor_variant

@register_processor("lowercase")
class LowercaseProcessor(Processor):
    ''' Processor that lowercases all text '''
    _requires = set(['tokenize'])
    _provides = set(['lowercase'])

    def __init__(self, config, pipeline, use_gpu):
        pass

    def _set_up_model(self, *args):
        pass

    def process(self, doc):
        doc.text = doc.text.lower()
        for sent in doc.sentences:
            for tok in sent.tokens:
                tok.text = tok.text.lower()

            for word in sent.words:
                word.text = word.text.lower()

        return doc


def preproces(s_):
    s = []
    for line in s_:    
      line = line.replace('\n',"").replace("  "," ")
      tokens=[]
      doc = nlp(line)
      for i, sentence in enumerate(doc.sentences):
          tokens.extend([token.text for token in sentence.tokens])
      s.append(tokens)
    return s

def create_dataset(splits):    
    nlp = stanza.Pipeline(lang='en', processors='tokenize,lowercase')
    for split in splits:
        base_path = "/content/Long-Text-Summarization/data/final/exp1"
        path_articles = f"{base_path}/{split}/ects"
        path_summaries = f"{base_path}/{split}/gt_summaries"
        
        if split=="val":
            split="valid"

        outfile = f"/content/Long-Text-Summarization/PreSumm/json_data/ect.{split}.json"
        articles = os.listdir(path_articles)
        summaries = os.listdir(path_summaries)
        assert (len(articles)==len(summaries))

        data = []
        for article in tqdm(articles):
            data_point = {}
            a_ = open(os.path.join(path_articles, article), 'r').readlines()
            a = preproces(a_)
            s_ = open(os.path.join(path_summaries, article), 'r').readlines()
            s = preproces(s_)
            
            #skip empty files
            if len(a_)==0 or len(s_)==0:
              os.remove(os.path.join(path_articles, article))
              os.remove(os.path.join(path_summaries, article))
              print(f"Deleting {article} as it is empty")

            data_point["src"] = a
            data_point["tgt"] = s
            data_point["article_id"] = article
            data.append(data_point)

        with open(outfile, "w") as myfile:
            json.dump(data, myfile)
            print(f"{split} has {len(data)} instances")
        myfile.close()
        

def merge_JsonFiles(filename):
    result = list()
    for f1 in filename:
        with open(f1, 'r') as infile:
            result.extend(json.load(infile))

    with open("/content/Long-Text-Summarization/PreSumm/json_data/ect.all.json", 'w') as output_file:
        json.dump(result, output_file)


if __name__ == "__main__":
    splits = ["train", "test", "val"] 
    files= ["/content/Long-Text-Summarization/PreSumm/json_data/ect.train.json",
            "/content/Long-Text-Summarization/PreSumm/json_data/ect.valid.json",
            "/content/Long-Text-Summarization/PreSumm/json_data/ect.text.json"]

    create_dataset(splits)
    merge_JsonFiles(files)