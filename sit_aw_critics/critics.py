import json

#build the critics in a way to give newer to oldest argument to the trigger functions 

def critics_trigger_reply1(reply1):
    valid = True
    disagreement = ''

    valid, disagreement = json_format_critic(reply1)
    if valid == False:
        return valid, disagreement
    
    valid, disagreement = gripper_zero_critic(reply1)
    if valid == False:
        return valid, disagreement

    valid, disagreement = task_critic(reply1)
    return valid, disagreement

#critics that check if the 1st response is in  a valid json format
def json_format_critic(reply1):
    valid = True
    disagreement = '' 

    if '```json' in reply1 :
        jsonreply = reply1[reply1.find('```json')+8 :reply1.find('}\n```')+1]
        try : 
            json_response = json.loads(jsonreply)

        except json.decoder.JSONDecodeError as error:
            if (error.lineno,error.colno,error.pos) == (1,1,0):
                valid = False
                disagreement = 'I wanted the analyse in json format, your previous response cannot be parsed to json due to an error, correct it.'
            else : 
                valid = False
                disagreement = 'You made an error in the format : '+str(error)+', correct it.' 
    else : 
        valid = False
        disagreement = 'I wanted the analyse in json format, your previous response cannot be parsed to json due to an error, correct it.'

    return valid, disagreement


def task_critic(reply1):
    valid = True
    disagreement = ''
    known_correlation = ''
    jsonreply = reply1[reply1.find('```json')+8 :reply1.find('}\n```')+1]
    json_response = json.loads(jsonreply)

    if json_response['data']['gripper_jaws_positions']['at_the_beginning']['mean_position'] == 0.165 and json_response['data']['gripper_jaws_positions']['at_the_end']['mean_position']<0.165 :
        known_correlation = 'pick block'

    if json_response['data']['gripper_jaws_positions']['at_the_beginning']['mean_position'] == 0.165 and json_response['data']['gripper_jaws_positions']['at_the_end']['mean_position']==0.165 : 
        known_correlation = 'pick block'

    try :
        if json_response['task']['performed_task'] != known_correlation :
            valid = False
            disagreement = 'You made an error in the performed_task, remember the known correlation "When the gripper jaws position starts at 0.165 and ends at a lower value, you are performing "pick block" task.'
    except : 
        if json_response['data']['task']['performed_task'] != known_correlation :
            valid = False
            disagreement = 'You made an error in the performed_task, remember the known correlation "When the gripper jaws position starts at 0.165 and ends at a lower value, you are performing "pick block" task.'

    return valid, disagreement


def gripper_zero_critic(reply1): 
    valid = True
    disagreement = ''
    jsonreply = reply1[reply1.find('```json')+8 :reply1.find('}\n```')+1]
    json_response = json.loads(jsonreply)

    if json_response['data']['gripper_jaws_positions']['at_the_beginning']['mean_position'] > 0.0 and json_response['data']['gripper_jaws_positions']['at_the_beginning']['is_gripper_zero'] == True:
        valid= False
        disagreement = 'If the value of gripper_jaws_positions is not 0 then the value of is_gripper_zero cannot be "True".'
    
    if json_response['data']['gripper_jaws_positions']['at_the_end']['mean_position'] > 0.0 and json_response['data']['gripper_jaws_positions']['at_the_end']['is_gripper_zero'] == True:
        valid= False
        disagreement = 'If the value of gripper_jaws_positions is not 0 then the value of is_gripper_zero cannot be "True".'

    return valid, disagreement



def critics_trigger_reply2(reply2, reply1):
    valid = True
    disagreement = ''

    valid, disagreement = anomaly_format_critic(reply2)
    if valid == False:
        return valid, disagreement
    
    is_reply1_json, _ = json_format_critic(reply1)
    if is_reply1_json == True :
        valid, disagreement = concistency_critic(reply2, reply1)

    return valid, disagreement


def anomaly_format_critic(reply2):
    valid = True
    disagreement = ''
    situations = ['I picked a block.', 'I picked an object which is not a block.', 'I picked nothing and a human has been detected (one probably intervened in your task).', 'I picked nothing and no human has been detected.']
    situin = False
    for situ in situations:
        if situ in reply2:
            situin = True
    if situin == True:
        valid= True
        disagreement = ''
    else : 
        valid= False
        disagreement = 'The situation description must be ONE OF THE LIST:\n1. I picked a block.\n2. I picked an object which is not a block.\n3. I picked nothing and a human has been detected (one probably intervened in your task).\n4. I picked nothing and no human has been detected.'
    return (valid,disagreement)


def concistency_critic(reply2, reply1) :
    valid = True
    disagreement = ''
    jsonreply = reply1[reply1.find('```json')+8 :reply1.find('}\n```')+1]
    json_response = json.loads(jsonreply)

    if json_response['data']['video']['is_human_detected'] == 'false' and 'a human has been detected' in reply2:
        disagreement = 'Hallucination detected, VLM did not detected any human in the scene description, either the scene description or the situation description contain an hallucination.'

    if json_response['data']['video']['at_the_beginning']['number_of_blocks'] == json_response['data']['video']['at_the_end']['number_of_blocks'] and 'I picked a block' in reply2:
        disagreement = 'Hallucination detected, There is the same amount of blocks at the start and at the end of the scene dscription, either the scene description or the situation description contain an hallucination.'

    return valid, disagreement
