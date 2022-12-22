import torch
import torch.nn as nn
from transformers import BertConfig
from transformers.models.bert.modeling_bert import BertModel
from transformers.models.bert.modeling_bert import BertPreTrainedModel

class JointBERT(BertPreTrainedModel):
    config_class = BertConfig

    def __init__(self, config, num_intent_labels, num_slot_labels, dropout_rate=0.1):
        super(JointBERT, self).__init__(config)
        self.num_intent_labels = num_intent_labels
        self.num_slot_labels = num_slot_labels
        self.bert = BertModel(config=config)  # Load pretrained bert

        encoder_layer = nn.TransformerEncoderLayer(d_model=768, nhead=8, batch_first=True)

        self.transformer_encoder = nn.TransformerEncoder(encoder_layer, num_layers=4)
        ## Freeze parameters
        # for param in self.bert.parameters():
        # param.requires_grad = False

        self.dropout = nn.Dropout(dropout_rate)
        self.intent_classifier = nn.Linear(config.hidden_size, num_intent_labels)

        self.slot_classifier = nn.Linear(config.hidden_size, num_slot_labels)

        self.init_weights()

    def forward(self, input_ids=None, attention_mask=None, token_type_ids=None, intent_label_ids=None,
                slot_labels_ids=None, **kwargs):
        outputs = self.bert(input_ids, attention_mask=attention_mask,
                            token_type_ids=token_type_ids,
                            **kwargs)  # sequence_output, pooled_output, (hidden_states), (attentions)
        sequence_output = outputs[0]
        pooled_output = outputs[1]

        # sequence_output = self.transformer_encoder(sequence_output)
        # pooled_output = sequence_output[:,0,:]
        sequence_output = self.dropout(sequence_output)

        # outputs[1]  # [CLS]

        # sequence_output will be used for slot_filling / classification

        pooled_output = self.dropout(pooled_output)

        intent_logits = self.intent_classifier(pooled_output)
        slot_logits = self.slot_classifier(sequence_output)

        total_loss = 0
        # 1. Intent Softmax
        if intent_label_ids is not None:
            if self.num_intent_labels == 1:
                intent_loss_fct = nn.MSELoss()
                intent_loss = intent_loss_fct(intent_logits.view(-1), intent_label_ids.view(-1))
            else:
                intent_loss_fct = nn.CrossEntropyLoss()
                intent_loss = intent_loss_fct(intent_logits.view(-1, self.num_intent_labels), intent_label_ids.view(-1))
            total_loss += intent_loss

        # 2. Slot Softmax
        if slot_labels_ids is not None:
            slot_loss_fct = nn.CrossEntropyLoss()  ## Ignore padding
            # Only keep active parts of the loss
            if attention_mask is not None:
                active_loss = attention_mask.view(-1) == 1
                active_logits = slot_logits.view(-1, self.num_slot_labels)[active_loss]
                active_labels = slot_labels_ids.view(-1)[active_loss]
                slot_loss = slot_loss_fct(active_logits, active_labels)
            else:
                slot_loss = slot_loss_fct(slot_logits.view(-1, self.num_slot_labels), slot_labels_ids.view(-1))

            total_loss += 0.8 * slot_loss

        outputs = ((intent_logits, slot_logits),) + outputs[2:]  # add hidden states and attention if they are here

        outputs = (total_loss,) + outputs

        outputs = {"loss": total_loss, "intent_logits": intent_logits, "slot_logits": slot_logits}
        return outputs