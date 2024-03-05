import streamlit as st
import st_pages

st.set_page_config(
    page_title='Situation Puzzle', 
    page_icon='🧩'
)

# main page
st.header('🧩 Situation Puzzle', divider='rainbow')
st.subheader('💭 About the Game')
st.markdown("**Welcome to Situation Puzzle Game**, a realm where mystery and intellect intertwine, challenging your perception and wit at every turn. In this digital escapade, you'll encounter situation puzzles – a unique blend of riddles and storytelling that has captivated minds for centuries.")

st.subheader('📜 A Brief History')
st.markdown("The art of situation puzzles dates back to when storytellers would weave complex narratives, leaving listeners to deduce outcomes or unravel mysteries using only sparse details. Over time, these puzzles transitioned from oral traditions to become a beloved challenge in salons, classrooms, and publications, encouraging collaborative problem-solving and critical thinking across cultures and generations.")

st.header("🎮 Ready to Start?", divider='rainbow')
st.page_link("pages/bot_to_player.py", label="Click Me to Start a Game", icon="🕹️")

st.header("👋 New to this game? We've got you!", divider='rainbow')
st.subheader('📜 Check Out Our Game Rules Page')
st.page_link("pages/rules.py", label="Click Me to Game Rules", icon="📜")
st.subheader("🛠️ Hands-Off Learner? For Sure!")
st.page_link("pages/bot_to_bot.py", label="Click Me to Spectate a AI vs. AI Game", icon="🤖")

# sidebar   
st_pages.show_pages([
    st_pages.Page('webui.py', 'About', '🏠'),
    st_pages.Page('pages/rules.py', 'Game Rules', '📜'), 

    st_pages.Section(name='Play!', icon='🔽'), 
    st_pages.Page('pages/bot_to_player.py', 'AI vs. Player', '🕹️'),
    st_pages.Page('pages/bot_to_bot.py', 'AI vs. AI', '🤖'), 
    st_pages.Page('pages/bot_to_player_AI_Questions.py', 'AI Generated Puzzles (BETA)', '🤖')
])

st.sidebar.markdown('**This demo presented by:**')
st.sidebar.markdown('*University of Washington - Foster School of Business*')
st.sidebar.markdown('*:violet[Class of 2024 - MSIS Purple Team 9]*')

