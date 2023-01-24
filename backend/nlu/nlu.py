from backend.nlu.preprocesing import pretokenize
from backend.nlu.joint_bert import JointBERT
from transformers import BertConfig, BertTokenizerFast
import torch
import numpy as np
import torch.nn.functional as F
from backend.nlu.utils import load_pickle_file, resource_path
import os
from dotenv import load_dotenv

load_dotenv()

CHATBOT_HOME = os.getenv('CHATBOT_HOME')
MODEL_PATH = os.getenv('CHATBOT_HOME') + "backend/nlu/model_checkpoint/joint_bert"

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

class NLU:
    def __init__(self, model_path = MODEL_PATH ):
        self.label2int = load_pickle_file(f"{model_path}/label2int.pkl")
        self.label2ent = load_pickle_file(f"{model_path}/label2ent.pkl")

        bert_config = BertConfig.from_pretrained(model_path)

        self.model = JointBERT.from_pretrained(
            model_path,
            config=bert_config,
            num_intent_labels=len(self.label2int),
            num_slot_labels=len(self.label2ent),
        ).to(device)

        self.tokenizer = BertTokenizerFast.from_pretrained(model_path)

    def inference(self, text):
        ## Pretokenizacion
        tokens = pretokenize(text)
        ## Tokenization Model
        tokenized_inputs = self.tokenizer(tokens, truncation=True, padding=True, is_split_into_words=True,
                                     return_tensors="pt")
        inputs = {k: v.to(device) for k, v in tokenized_inputs.items()}
        ## Inference Model
        with torch.no_grad():
            outputs = self.model(**inputs)
            intent_logits = outputs['intent_logits']
            slot_logits = outputs['slot_logits']
            intent_logits = intent_logits.detach().cpu()
            intent_probs = F.softmax(intent_logits[0], dim=0)
            intent_label = np.argmax(intent_logits.numpy(), axis=1)
            intent_score = intent_probs[intent_label[0].item()].item()
            intent_name = self.label2int[intent_label[0]]
            entities_labels = np.argmax(slot_logits.detach().cpu().numpy(), axis=2)
            entities_labels = entities_labels[0]
            entities_names = [self.label2ent[id] for id in entities_labels]

            output_nlu = {"intent": {"intent": intent_name, "intent_score": intent_score}, "entities": []}

            entity_words = []
            current_entity = None
            ner_labels_pred = []
            word_ids = tokenized_inputs.word_ids()
            pre_word_id = None
            for idx, word_idx in enumerate(word_ids):
                if word_idx is None or pre_word_id == word_idx:
                    continue
                entity_label = entities_names[idx]
                ner_labels_pred.append(entities_labels[idx])
                if current_entity != None:
                    if current_entity == entity_label.replace('B-', ''):
                        output_nlu['entities'].append({"value": " ".join(entity_words),
                                                       "entity": current_entity})
                        ## reset entity named
                        # current_entity = entity_label.replace('B-','')
                        entity_words = [tokens[word_idx]]

                    if entity_label == 'O' or current_entity != entity_label[2:]:
                        output_nlu['entities'].append({"value": " ".join(entity_words),
                                                       "entity": current_entity})
                        ## reset entity named
                        current_entity = None
                        entity_words = []

                        if entity_label.startswith('B-'):
                            current_entity = entity_label.replace('B-', '')
                            entity_words.append(tokens[word_idx])

                    if current_entity == entity_label.replace('I-', ''):
                        entity_words.append(tokens[word_idx])



                elif current_entity == None and entity_label.startswith('B-'):
                    current_entity = entity_label.replace('B-', '')
                    entity_words.append(tokens[word_idx])

                pre_word_id = word_idx

            if current_entity != None:
                output_nlu['entities'].append({"value": " ".join(entity_words),
                                               "entity": current_entity
                                               })
            output_nlu['ner_labels_pred'] = ner_labels_pred
            return output_nlu

