from typing import List

from PIL import Image
import torch

from open_flamingo.eval.eval_model import BaseEvalModel
from open_flamingo.src.factory import create_model_and_transforms
from .modeling_otter import OtterForConditionalGeneration

class EvalModel(BaseEvalModel):
    """OpenFlamingo model evaluation.

    Attributes:
      model (nn.Module): Underlying Torch model.
      tokenizer (transformers.PreTrainedTokenizer): Tokenizer for model.
      device: Index of GPU to use, or the string "CPU"
    """

    def __init__(self, model_args):
        model_args["device"] = int(model_args["device"])
        self.device = model_args["device"] if model_args["device"] >= 0 else "cpu"
        self.model_path = model_args.model_path
        self.model = OtterForConditionalGeneration.from_pretrained(self.model_path)
        self.tokenizer = self.model.text_tokenizer
        self.tokenizer.padding_side = 'left'

    def _prepare_images(self, batch: List[List[torch.Tensor]]) -> torch.Tensor:
        """Preprocess images and stack them.

        Args:
            batch: A list of lists of images.

        Returns:
            A Tensor of shape
            (batch_size, images_per_example, frames, channels, height, width).
        """
        images_per_example = max(len(x) for x in batch)
        batch_images = None
        for iexample, example in enumerate(batch):
            for iimage, image in enumerate(example):
                preprocessed = self.image_processor(image)

                if batch_images is None:
                    batch_images = torch.zeros(
                        (len(batch), images_per_example, 1) + preprocessed.shape,
                        dtype=preprocessed.dtype,
                    )
                batch_images[iexample, iimage, 0] = preprocessed
        return batch_images

    def get_outputs(
        self,
        batch_text: List[str],
        batch_images: List[List[Image.Image]],
        max_generation_length: int,
        num_beams: int,
        length_penalty: float,
    ) -> List[str]:
        encodings = self.tokenizer(
            batch_text,
            padding="longest",
            truncation=True,
            return_tensors="pt",
            max_length=2000,
        )
        input_ids = encodings["input_ids"]
        attention_mask = encodings["attention_mask"]
        
        vision_x = self._prepare_images(batch_images).to(self.device),
        with torch.inference_mode():
            outputs = self.model.generate(
                vision_x=vision_x,
                lang_x=input_ids.to(self.device),
                attention_mask=attention_mask.to(self.device),
                max_new_tokens=max_generation_length,
                num_beams=num_beams,
                length_penalty=length_penalty,
            )
        outputs = outputs[:, len(input_ids[0]) :]
        return self.tokenizer.batch_decode(outputs, skip_special_tokens=True)

    def get_vqa_prompt(self, question, answer=None) -> str:
        return f"<image>User: Question:{question} Short answer:{answer if answer is not None else ''} GPT:<answer>{'<|endofchunk|>' if answer is not None else ''}"

    def get_caption_prompt(self, caption=None) -> str:
        return f"<image>User: Output:{caption if caption is not None else ''} GPT:<answer>{'<|endofchunk|>' if caption is not None else ''}"

    def get_classification_prompt(self, class_str=None) -> str:
        return f"<image>User: A photo of a {class_str if class_str is not None else ''} GPT:<answer>{'<|endofchunk|>' if class_str is not None else ''}"
