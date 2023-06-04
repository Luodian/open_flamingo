cd /home/v-boli7/projects/open_flamingo

python -m open_flamingo.eval.evaluate \ 
--lm_path "luodian/llama-7b-hf" \ 
--lm_tokenizer_path "luodian/llama-7b-hf" \ 
--vision_encoder_path "ViT-L-14" \ 
--vision_encoder_pretrained "openai" \ 
--checkpoint_path "/home/v-boli7/azure_storage/models/openflamingo/checkpoint.pt" \ 
--cross_attn_every_n_layers 4 \ 
--device 0 \ 
--coco_image_dir_path "/home/v-boli7/azure_storage/data/lavis/coco2017/train2017" \ 
--coco_annotations_json_path "/home/v-boli7/azure_storage/data/lavis/coco2017/annotations/captions_train2017.json" \ 
--vqav2_train_image_dir_path "/home/v-boli7/azure_storage/data/lavis/coco/images/train2014" \ 
--vqav2_train_annotations_json_path "/home/v-boli7/azure_storage/data/lavis/vqav2/annotations/v2_mscoco_train2014_annotations.json" \ 
--vqav2_train_questions_json_path "/home/v-boli7/azure_storage/data/lavis/vqav2/annotations/v2_OpenEnded_mscoco_train2014_questions.json" \ 
--vqav2_test_image_dir_path "/home/v-boli7/azure_storage/data/lavis/coco/images/val2014" \ 
--vqav2_test_annotations_json_path "/home/v-boli7/azure_storage/data/lavis/vqav2/annotations/v2_mscoco_val2014_annotations.json" \ 
--vqav2_test_questions_json_path "/home/v-boli7/azure_storage/data/lavis/vqav2/annotations/v2_OpenEnded_mscoco_val2014_questions.json" \ 
--results_file "results_flamingo.json" \ 
--eval_vqav2 \ 
--num_samples 5000 \ 
--shots 0 4 8 \ 
--num_trials 1 \ 
--batch_size 1

echo "evaluation complete! results written to ${RESULTS_FILE}"
