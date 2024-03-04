import json
from difflib import get_close_matches


def load_bot(file_path: str)->dict:
    with open(file_path,'r') as file:
        data:dict=json.load(file)
    return data

#save bot
def save_bot(file_path: str,data: dict):
    with open(file_path,'w')as file:
        json.dump(data,file,indent=2)

#find best match
def find_best_match(user_question: str,questions: list[str])->str |None:
    matches: list=get_close_matches(user_question,questions,n=1,cutoff=0.6)
    return matches[0] if matches else None

def get_answer_for_question(question:str,bot:dict)->str|None:
    for q in bot['questions']:
        if q['question']==question:
            return q['answer']

def chat_bot():
    bot:dict=load_bot('bot.json')

    while True:
        user_input:str=input('You:  ')
        if user_input.lower()=='quit':
            break

        best_match:str |None= find_best_match(user_input,[q["question"] for q in bot["questions"]])

        if best_match:
            answer:str=get_answer_for_question(best_match,bot)
            print(f'Bot:  {answer}')
        else:
            print('Bot: I dont know the answer, Can you teach me?')
            new_answer:str=input('Type the answer or "skip" to skip: ')

            if new_answer.lower() !='skip':
                bot['questions'].append({"question": user_input,"answer":new_answer})
                save_bot('bot.json',bot)
                print('Bot: Thank You! , I learned a new response!')



if __name__=='__main__':
    chat_bot()
