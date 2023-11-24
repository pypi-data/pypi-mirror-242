# Derived from yule-BUAA/MergeLM/merging_methods.py
import re
from typing import Dict
import torch
import torch.nn as nn
from transformers import AutoModelForCausalLM, PreTrainedModel, PreTrainedTokenizer


def is_exclude_param_name(param_name: str, exclude_param_names_regex: list):
    """
    Check whether the param_name is in the exclude_param_names_regex
    """
    if exclude_param_names_regex:
        exclude = any(
            [
                re.match(exclude_pattern, param_name)
                for exclude_pattern in exclude_param_names_regex
            ]
        )
    else:
        exclude = False
    return exclude


def get_model_params(model: nn.Module):
    """
    Get model parameters
    """
    params_dict = {
        param_name: param_value for param_name, param_value in model.named_parameters()
    }
    return params_dict


def copy_params_to_model(params_dict: dict, model: nn.Module):
    """
    Copy params to model
    """
    for param_name, param_value in model.named_parameters():
        if param_name in params_dict:
            param_value.data.copy_(params_dict[param_name])


def smart_tokenizer_and_embedding_resize(
    special_tokens_dict: Dict,
    tokenizer: PreTrainedTokenizer,
    model: PreTrainedModel,
):
    """Resize tokenizer and embedding.

    Note: This is the unoptimized version that may make your embedding size not be divisible by 64.
    """
    assert tokenizer.vocab_size == 32000
    num_new_tokens = tokenizer.add_special_tokens(special_tokens_dict)
    if num_new_tokens > 0:
        model.resize_token_embeddings(tokenizer.vocab_size + num_new_tokens)

        input_embeddings = model.get_input_embeddings().weight.data
        output_embeddings = model.get_output_embeddings().weight.data

        input_embeddings_avg = input_embeddings[:-num_new_tokens].mean(
            dim=0, keepdim=True
        )
        output_embeddings_avg = output_embeddings[:-num_new_tokens].mean(
            dim=0, keepdim=True
        )

        input_embeddings[-num_new_tokens:] = input_embeddings_avg
        output_embeddings[-num_new_tokens:] = output_embeddings_avg


class DeltaWeights:
    """
    Functions to compute the delta weights between two models 
    """
    def __init__(
        self,
        base_model: nn.Module = None,
        tuned_model: nn.Module = None,
        params_dict: dict = None,
        exclude_param_names_regex: list = None,
    ):
        """
        Task vector. Initialize the task vector from a pretrained model and a tuned model, or
        directly passing the task_vector_param_dict dictionary.
        :param base_model: nn.Module, base model
        :param tuned_model: nn.Module, tuned model
        :param exclude_param_names_regex: list, regular expression of names of parameters that need to be excluded
        :param params_dict: dict, prams dict to initialize self.params_dict
        """
        self.params_dict = {}

        if params_dict is not None:
            self.params_dict = params_dict
        else:
            base_params_dict = get_model_params(base_model)
            tuned_params_dict = get_model_params(tuned_model)
            for param_name in base_params_dict:
                if not is_exclude_param_name(param_name, exclude_param_names_regex):
                    self.params_dict[param_name] = (
                        tuned_params_dict[param_name] - base_params_dict[param_name]
                    )

    def __add__(self, other):
        """
        add task vector
        :param other: DeltaWeights to add, at right side
        :return:
        """
        assert isinstance(
            other, DeltaWeights
        ), "addition of DeltaWeights can only be done with another DeltaWeights!"
        new_params_dict = {}
        for param_name in self.params_dict:
            assert (
                param_name in other.params_dict.keys()
            ), f"param_name {param_name} is not contained in both params!"
            new_params_dict[param_name] = (
                self.params_dict[param_name] + other.param_dict[param_name]
            )
        return DeltaWeights(params_dict=new_params_dict)

    def __radd__(self, other):
        """
        other + self = self + other
        :param other: DeltaWeights to add, at left side
        :return:
        """
        return self.__add__(other)

    def combine_with_pretrained_model(
        self, base_model: nn.Module, scaling_coefficient: float = 1.0
    ):
        """
        combine the delta weights with pretrained model
        :param base_model: nn.Module, base model
        :param scaling_coefficient: float, scaling coefficient to merge the delta weights
        :return:
        """
        base_params_dict = get_model_params(base_model)

        with torch.no_grad():
            merged_params = {}
            for param_name in self.params_dict:
                merged_params[param_name] = (
                    base_params_dict[param_name]
                    + scaling_coefficient * self.params_dict[param_name]
                )

        return merged_params


def do_delta_weights(args):
    """
    Compute the delta weights between two models and save the delta weights to a file
    """
    print(f"Loading base model from {args.base_model_name_or_path} ...")
    base_model = AutoModelForCausalLM.from_pretrained(
        args.base_model_name_or_path, device_map=args.device_map, trust_remote_code=True
    ).half()
    print(f"Loading tuned model from {args.tuned_model_name_or_path} ...")
    tuned_model = AutoModelForCausalLM.from_pretrained(
        args.tuned_model_name_or_path,
        device_map=args.device_map,
        trust_remote_code=True,
    ).half()

    delta_weights = DeltaWeights(base_model=base_model, tuned_model=tuned_model)
    print(f"Saving delta weights to {args.save_path} ...")
    torch.save(delta_weights.params_dict, args.save_path)

    print(f"Succesfully saved delta weights to {args.save_path}")
