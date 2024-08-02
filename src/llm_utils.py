from llama_index.core.base.llms.types import LLMMetadata
from llama_index.llms.mistralai import MistralAI
from llama_index.llms.mistralai.utils import is_mistralai_function_calling_model

# Prompt for combining node-level titles to obtain document title.
"""\
{context_str}. Based on the above candidate titles and content, \
what is the comprehensive title for this document? Title: """  # Original

TITLE_CMB_PROMPT = """\
{context_str}. Based on the above candidate titles and content, \
provide a comprehensive title for this document. The title must be:\
1. A single sentence
2. Not enclosed in quotes, asterisks, or any other formatting
3. Directly written without any prefixes like 'Title:'\

Write only the title as your response:"""


class CustomMistralAI(MistralAI):
    """
    Custom class for MistralAI models.
    """

    def mistralai_modelname_to_contextsize(modelname: str) -> int:
        # handling finetuned models
        if modelname.startswith("ft:"):
            modelname = modelname.split(":")[1]

        mistralai_models: dict[str, int] = {
            "mistral-small-latest": 32000,
            "mistral-large-latest": 32000,
            "open-mistral-nemo": 128000,
        }

        if modelname not in mistralai_models:
            raise ValueError(
                f"Unknown model: {modelname}. Please provide a valid MistralAI model name."
                "Known models are: " + ", ".join(mistralai_models.keys())
            )

        return mistralai_models[modelname]

    @property
    def metadata(self) -> LLMMetadata:
        return LLMMetadata(
            context_window=CustomMistralAI.mistralai_modelname_to_contextsize(
                self.model
            ),
            num_output=self.max_tokens,
            is_chat_model=True,
            model_name=self.model,
            safe_mode=self.safe_mode,
            random_seed=self.random_seed,
            is_function_calling_model=is_mistralai_function_calling_model(self.model),
        )
