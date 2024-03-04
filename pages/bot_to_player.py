import streamlit as st
import streamlit_chatbox as stc
import time
import api_request
import streamlit_scrollable_textbox as stx
import pandas as pd
import random
import os

st.set_page_config(
    page_title='Situation Puzzle', 
    page_icon='🧩'
)

chat_box = stc.ChatBox()

# config sidebar
if st.sidebar.button('🔄 New Game'): 
    if os.path.isfile('question.tmp'): 
        os.remove('question.tmp')
    chat_box.reset_history()
    st.rerun()

bot_llm = st.sidebar.radio('Bot LLM: ', ['OpenAI-GPT-4.0', 'OpenAI-GPT-3.5', 'Gemini Pro'])
image_gen_model = st.sidebar.radio('Image GenAI: ', ['DALL·E 3'])
image_style = st.sidebar.radio('Image Style: ', ['Comic', 'Realistic'])
st.sidebar.divider()
show_quick_question = st.sidebar.button('Question Suggestion')
# guess_mode = st.sidebar.checkbox('Ready to Guess')
st.sidebar.divider()

st.sidebar.markdown('**This demo presented by:**')
st.sidebar.markdown('*University of Washington - Foster School of Business*')
st.sidebar.markdown('*:violet[Class of 2024 - MSIS Purple Team 9]*')


# set up question and answer of situation puzzle
if os.path.isfile('question.tmp'): 
    temp_file = pd.read_csv('question.tmp')
    QUESTION = temp_file['question'][0]
    ANSWER = temp_file['answer'][0]
    
else: 
    questions  = pd.read_json('questions.json')
    choice = random.randint(0, questions.shape[0] - 1)

    QUESTION = questions['Question'][choice]
    ANSWER = questions['Answer'][choice]

    pd.DataFrame({'question': [QUESTION], 'answer': [ANSWER]}).to_csv('question.tmp')


INIT_PROMPT = f"I want you to pretend to be a professional game host of Situation Puzzle. The game rule is as follows: You are hosting the puzzle and the user asking questions which can only be answered with a 'yes' or 'no' answer. Depending upon the settings and level of difficulty, other answers, hints or simple explanations of why the answer is yes or no, may be considered acceptable. The puzzle is solved when one of the players is able to recite most of the narrative the host had in mind, in particular explaining whatever aspect of the initial scenario was puzzling. When the player recite most of situation correctly, you tell the user what exact happen. If the user are heading to a topic completely unrelated to this situation puzzle, please stop the user. Now, here is the puzzle: {QUESTION}, the answer to this puzzle is {ANSWER} Now, user is going to ask you question. The followings are the player question: \n"

# header
st.header('AI🤖 vs. Human Player🧩', divider='rainbow')
st.subheader('Here is a Situation Puzzle for you...')
stx.scrollableTextbox(QUESTION, height=150)

chat_box.output_messages()

# initialize llm
if bot_llm == 'OpenAI-GPT-4.0': 
    llm = api_request.GPT(INIT_PROMPT)
elif bot_llm == 'OpenAI-GPT-3.5': 
    llm = api_request.GPT(INIT_PROMPT, is_4=False)
elif bot_llm == 'Gemini Pro':
    llm = api_request.GeminiText(INIT_PROMPT)


guess_mode = st.toggle('Ready to Guess')

if show_quick_question:  
    with st.spinner('Wait for Quick Questions...'): 
        questions = llm.generate_questions(chat_box.history, QUESTION)

    st.write('Here are Question Suggestions for you...')
    stx.scrollableTextbox('\n'.join(questions))


if user_query := st.chat_input('Input your question here. If you are ready to guess, press on guess on the sidebar, then input'):
    chat_box.user_say(user_query)

    if guess_mode: 
        st.text('Player starts to guess...')
        if llm.check_answer(chat_box.history): 
            st.subheader('', divider='rainbow')
            st.success('You are Correct!', icon="✅")
            st.subheader('Here is the correct answer...')
            stx.scrollableTextbox(ANSWER, height=150)
            st.subheader('Here is the feedback generated to you...')
            with st.spinner('AI Generating...'):
                stx.scrollableTextbox(llm.feedback(chat_box.history), height=300)

            os.remove('question.tmp')

            # generate image
            with st.spinner('Wait for Image...'):
                if image_gen_model == 'DALL·E 3': 
                    image_gen = api_request.Dalle(style=image_style)
                image_url = image_gen.gen_image(ANSWER)
                st.image(image_url)

        else:
            st.error('Sorry, You are wrong. Please continue...', icon="❌")

    else: 
        generator = llm.answer(chat_box.history)
        elements = chat_box.ai_say(
            [
                stc.Markdown("thinking", in_expander=False,
                            expanded=False, title="answer"),
                stc.Markdown("", in_expander=False, title="references"),
            ]
        )
        time.sleep(0.3)
        text = ""
        for chunk in generator:
            if 'OpenAI' in bot_llm:
                buffer = chunk.choices[0].delta.content
            else:
                buffer = chunk.text
            if buffer is not None: 
                text += buffer
            chat_box.update_msg(text, element_index=0, streaming=True)
        chat_box.update_msg(text, element_index=0, streaming=False, state="complete")
