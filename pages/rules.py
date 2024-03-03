import streamlit as st
import st_pages

st.set_page_config(
    page_title='Situation Puzzle', 
    page_icon='🧩'
)

# main page
st.header('🧩 Game Rules', divider='rainbow')
st.markdown("""
Situation puzzles are intriguing brain teasers where players are given a mysterious situation, and they have to figure out what's happening by asking yes-or-no questions. Follow these rules to enjoy the game:

### 📜 The Setup

- **The Puzzle Presentation:** One player, known as the *puzzle master*, presents a brief scenario to the other players. This scenario is usually a strange or unusual situation that requires an explanation.
- **The Goal:** The other players must uncover the truth behind the scenario by asking questions that can be answered with "yes," "no," or "irrelevant."

### 🤔 Asking Questions

- **Type of Questions:** Players can only ask questions that receive "yes," "no," or "irrelevant" as answers. No open-ended questions are allowed.
- **Unlimited Questions:** There is no limit to the number of questions players can ask. The game continues until the puzzle is solved.
- **Turn-Based or Free-For-All:** Depending on the group's preference, questions can be asked in a turn-based fashion or by anyone at any time.

### 🔍 Solving the Puzzle

- **The Eureka Moment:** The game ends when a player figures out the situation completely. They must explain the scenario in detail, based on the answers received.
- **Confirmation by the Puzzle Master:** The puzzle master confirms if the explanation is correct. If it's not, the game continues.

### 💡Tips for Players

- **Think Laterally:** Look for solutions outside the box. The answer often requires a leap of imagination.
- **Listen Carefully:** Pay attention to the answers given to others' questions. They can provide crucial clues.
- **Ask Strategic Questions:** Focus on questions that help narrow down the possibilities.

**Enjoy the challenge and happy puzzle-solving!**
""")

# sidebar   
st_pages.show_pages([
    st_pages.Page('webui.py', 'About', '🏠'),
    st_pages.Page('pages/rules.py', 'Game Rules', '📜'), 

    st_pages.Section(name='Play!', icon='🔽'), 
    st_pages.Page('pages/bot_to_player.py', 'AI vs. Player', '🕹️'),
    st_pages.Page('pages/bot_to_bot.py', 'AI vs. AI', '🤖')
])

st.sidebar.markdown('**This demo presented by:**')
st.sidebar.markdown('*University of Washington - Foster School of Business*')
st.sidebar.markdown('*:violet[Class of 2024 - MSIS Purple Team 9]*')

