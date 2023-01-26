from backend.nlu.preprocesing import pretokenize
from backend.nlu.joint_bert import JointBERT
from transformers import BertConfig, BertTokenizerFast
import torch
import numpy as np
import torch.nn.functional as F
from backend.nlu.utils import load_pickle_file

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


def resource_path(relative_path):
    # abs_path = r'C:/Users/darteaga/PycharmProjects/chatbot_cursos_inictel/'
    abs_path = r'C:/Users/user/PycharmProjects/chatbot_cursos_inictel/'
    # abs_path = r'/var/www/html/chatbot_cursos_inictel/'
    return abs_path + relative_path


MODEL_PATH = resource_path("backend/nlu/model_checkpoint/joint_bert")


def nlu_pipeline(text, model_path = MODEL_PATH):
    ## Load Model
    label2int = load_pickle_file(f"{model_path}/label2int.pkl")
    label2ent = load_pickle_file(f"{model_path}/label2ent.pkl")

    bert_config = BertConfig.from_pretrained(model_path)

    model = JointBERT.from_pretrained(
        model_path,
        config=bert_config,
        num_intent_labels=len(label2int),
        num_slot_labels=len(label2ent),
    ).to(device)

    tokenizer = BertTokenizerFast.from_pretrained(model_path)
    ## Preprocesing

    ## Pretokenizacion
    tokens = pretokenize(text)
    ## Tokenization Model
    tokenized_inputs = tokenizer(tokens, truncation=True, padding=True, is_split_into_words=True, return_tensors="pt")
    inputs = {k: v.to(device) for k, v in tokenized_inputs.items()}
    ## Inference Model
    with torch.no_grad():
        outputs = model(**inputs)
        intent_logits = outputs['intent_logits']
        slot_logits = outputs['slot_logits']
        intent_logits = intent_logits.detach().cpu()
        intent_probs = F.softmax(intent_logits[0], dim=0)
        intent_label = np.argmax(intent_logits.numpy(), axis=1)
        intent_score = intent_probs[intent_label[0].item()].item()
        intent_name = label2int[intent_label[0]]
        entities_labels = np.argmax(slot_logits.detach().cpu().numpy(), axis=2)
        entities_names = [label2ent[id] for id in entities_labels[0]]

        output_nlu = {"intent": {"intent": intent_name, "intent_score": intent_score}, "entities": []}

        entity_words = []
        current_entity = None

        word_ids = tokenized_inputs.word_ids()
        pre_word_id = None
        for idx, word_idx in enumerate(word_ids):
            if word_idx is None or pre_word_id == word_idx:
                continue
            entity_label = entities_names[idx]
            if current_entity != None:
                if entity_label == 'O' or current_entity != entity_label[2:]:
                    output_nlu['entities'].append({"value": " ".join(entity_words),
                                                   "entity": current_entity})
                    current_entity = None
                    entity_words = []

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
        return output_nlu
        # for ent_name in entities_names:
