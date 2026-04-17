Generic Principles
==================

Critics principle is to use expert algorithms to detect the hallucinations in the VLM response, and then do a new call to the VLM API with an updated prompt to correct the previously detected hallucination.
Each critics target a specific hallucination that was observed empirically.

In this particular application with 2 successive VLM calls, we have to do 2 sets of critics that verify different type of hallucinations.


.. image:: VLM-criticized-scheme.png
    :width: 600
    :align: center
    :alt: Visual language model identification procedure.

we designed 5 critics : 
* json_format_critic : applied on the first vlm call, verify if the model output is in a valid json format 
* task_critic : applied on the first vlm call, verify the consistency between the value of the anounced performed task and the rest of the scene description following rules given in the prompt
* gripper_zero_critic :  applied on the first vlm call, verify the consistency between the value of is_gripper_zero and the value of gripper_mean_position
* anomaly_format_critic : applied on the second vlm call, verify if the output is in a format we expect, the format was precised in the prompt
* consistency_critic : applied on the second vlm call, verify the consistency between the scene description and the anomaly classification, if they are contradictory, that means that one of the two contain an hallucination


It can happen that the model generates the same hallucination again even after being told not to, but having the information that there is an error in the model output can still be a valuable information.
