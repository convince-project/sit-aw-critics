Generic Principles
==================

Critics principle is to use expert algorithms to detect the VLM hallucinations, and then do a new call to the VLM API with an updated prompt to correct the previously detected hallucination.
Each critics target a specific hallucination that was observed empirically.


we designed 5 critics : 
* json_format_critic : verify if the model output is in a valid json format 
* task_critic : verify the consistency between the value of the anounced performed task and the rest of the scene description following rules given in the prompt
* gripper_zero_critic :  verify the consistency between the value of is_gripper_zero and the value of gripper_mean_position
* anomaly_format_critic : verify if the output is in a format we expect, the format was precised in the prompt
* consistency_critic : verify the consistency between the scene description and the anomaly classification, if they are contradictory, that means that one of the two ishallucinatory