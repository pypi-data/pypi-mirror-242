import os
import shutil
import sys
from typing import Optional, Iterable, List, Tuple

import datasets
import torch
from datasets import Dataset
from torch import nn

from fmrai import fmrai
from fmrai.agent import run_agent, AgentAPI
from fmrai.agent.agents.transformers import TransformersAgentAPI
from fmrai.agent.api import TokenizedText, AgentDatasetList
from fmrai.analysis.attention import compute_attention_head_divergence_matrix
from fmrai.analysis.common import DatasetInfo
from fmrai.analysis.structure import find_multi_head_attention
from fmrai.fmrai import Fmrai
from fmrai.logging import get_log_dir
from fmrai.tracker import OrdinalTensorId, TensorId


class SimpleModel(nn.Module):
    def __init__(self):
        super().__init__()

        self.linear1 = nn.Linear(512, 64)
        self.linear2 = nn.Linear(64, 1)

    def forward(self, x):
        x = self.linear1(x)
        x = self.linear2(x)
        x = x.sum()
        return x


def pasten():
    from transformers import AutoModel

    shutil.rmtree(get_log_dir(), ignore_errors=True)

    with fmrai() as fmr:
        fmr: Fmrai

        # model = SimpleModel()

        # config = reai.bert.base.BertConfig(
        #     vocab_size=8,
        #     hidden_size=4,
        #     num_heads=1,
        #     num_layers=1,
        #     max_len=16,
        #     attention_type=reai.bert.base.BertAttentionType.STANDARD,
        # )
        # model = reai.bert.base.BertModelForMaskedLM(config)
        model = AutoModel.from_pretrained('bert-base-uncased')

        fmr.add_model(model, log_parameters=True)

        with fmr.track() as tracker:
            # x = torch.randn((1, 512))
            x = torch.randint(0, 8, (1, 16))

            # build initial graph
            y = model(x)
            graph = tracker.build_graph(y.pooler_output).make_nice()
            graph.save_dot(os.path.join(get_log_dir(), 'model.dot'))

            optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)
            tracker.step()

            # train
            for _ in range(0):
                y = model(x)

                y.backward()
                optimizer.step()
                optimizer.zero_grad()

                print('y', y)
                # tracker.log_tensors(parameters=True, activations=False)
                tracker.step()

            # mp = tracker.build_map()
            # print(len(mp.data))


def create_simple_model_api():
    model = SimpleModel()

    class MyAgentAPI(AgentAPI):
        def predict_zero(self):
            return model(torch.zeros((1, 512)))

        def predict_text(
                self,
                texts: List[str],
                *,
                track_tensors: Optional[Iterable[TensorId]] = None
        ) -> TokenizedText:
            x = torch.randn((1, 512))
            model(x)

            raise NotImplementedError()

    return MyAgentAPI()


def create_bert_api():
    from transformers import AutoModel, AutoTokenizer

    model = AutoModel.from_pretrained('bert-base-uncased')
    tokenizer = AutoTokenizer.from_pretrained('bert-base-uncased')

    dataset_infos = [
        DatasetInfo(
            name='glue/sst2',
            text_column='sentence',
        )
    ]

    class BertAgentAPI(TransformersAgentAPI):
        def __init__(self):
            super().__init__('bert-base-uncased')

        def list_datasets(self) -> AgentDatasetList:
            return AgentDatasetList(
                datasets=dataset_infos,
            )

        def load_dataset(self, name: str) -> Optional[Tuple[Dataset, DatasetInfo]]:
            if name == 'glue/sst2':
                return (
                    datasets.load_dataset('glue', 'sst2', split='validation'),
                    dataset_infos[0],
                )

            assert False

    return BertAgentAPI()


def pasten_agent():
    with fmrai():
        # api = create_simple_model_api()
        api = create_bert_api()

        run_agent(api)


def pasten_specific_tracking():
    from transformers import AutoModel

    with fmrai() as fmr:
        fmr: Fmrai

        model = AutoModel.from_pretrained('bert-base-uncased')
        fmr.add_model(model)

        with fmr.track() as tracker:
            y = model(torch.randint(0, 7, (1, 64)))
            g = tracker.build_graph(y.pooler_output).make_nice()

        mha = list(find_multi_head_attention(g))
        print(mha)

        with fmr.track(
                track_tensors=[
                    instance.softmax_value.tensor_id
                    for instance in mha
                ]) as tracker:
            model(torch.randint(0, 7, (1, 64)))
            mp = tracker.build_map()

        print(mp)


def pasten_attention_head_matrix():
    with fmrai() as fmr:
        fmr: Fmrai

        api = create_bert_api()

        attention_tensor_ids = [
            OrdinalTensorId(ordinal=21),
            OrdinalTensorId(ordinal=50),
        ]

        with fmr.track(track_tensors=attention_tensor_ids) as tracker:
            with torch.no_grad():
                api.predict_text_bunch(
                    ['hello world', 'wassup?'],
                )

            batch_cmap = tracker.build_map()

        js_matrix = compute_attention_head_divergence_matrix(batch_cmap, attention_tensor_ids)
        return js_matrix


if __name__ == '__main__':
    if len(sys.argv) >= 2 and sys.argv[1] == '--agent':
        pasten_agent()
    else:
        # pasten()
        # pasten_specific_tracking()
        pasten_attention_head_matrix()
