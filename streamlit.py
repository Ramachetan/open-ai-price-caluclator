import streamlit as st
from tiktoken import encoding_for_model

# Set page config for layout and title
st.set_page_config(page_title='Azure OpenAI Service Cost and Token Counter', layout='wide')

# Title and Description
st.title('Azure OpenAI Service Cost and Token Counter')
st.markdown("Easily calculate your Azure OpenAI service costs and count tokens for different models.")

# Model selection for token counting
st.subheader('Token Counter')
model_tokenizer = st.selectbox('Select the Model for Tokenization', ['gpt-3.5-turbo', 'gpt-4'])
tokenizer = encoding_for_model(model_tokenizer)

# Text area for input text
user_text = st.text_area("Enter your text to count tokens:", height=150)
if st.button('Count Tokens'):
    tokens = tokenizer.encode(user_text)
    st.success(f"Number of tokens in input text: {len(tokens)}")

# Divider
st.markdown("---")

# Cost estimation section
st.subheader('Cost Estimator')
model = st.selectbox('Select the Model for Cost Estimation', ['GPT-3.5-Turbo 4K', 'GPT-3.5-Turbo 16K', 'GPT-4 8K', 'GPT-4 32K'])

# Pricing dictionary
pricing = {
    'GPT-3.5-Turbo 4K': {'prompt': 0.0015, 'completion': 0.002},
    'GPT-3.5-Turbo 16K': {'prompt': 0.003, 'completion': 0.004},
    'GPT-4 8K': {'prompt': 0.03, 'completion': 0.06},
    'GPT-4 32K': {'prompt': 0.06, 'completion': 0.12},
}

# Inputs for cost calculation
avg_prompt_tokens_per_query = st.number_input("Average Prompt Tokens per Query (INPUT)", min_value=0)
avg_completion_tokens_per_query = st.number_input("Average Completion Tokens per Query (OUTPUT)", min_value=0)
messages_per_conversation = st.number_input("Messages Per Conversation", min_value=0)
avg_no_of_conversations = st.number_input("Average Number of Conversations per User", min_value=0)
no_of_users = st.number_input("Number of Users", min_value=0)

# Calculate total cost button
if st.button('Calculate Total Cost'):
    prompt_cost = pricing[model]['prompt'] * avg_prompt_tokens_per_query / 1000
    completion_cost = pricing[model]['completion'] * avg_completion_tokens_per_query / 1000
    cost_per_message = prompt_cost + completion_cost
    cost_per_conversation = cost_per_message * messages_per_conversation
    cost_per_user = cost_per_conversation * avg_no_of_conversations
    total_cost = cost_per_user * no_of_users

    st.subheader("Itemized Costs:")
    st.write(f"1. Cost per message: ${cost_per_message:.5f}")
    st.write(f"2. Cost per conversation: ${cost_per_conversation:.5f}")
    st.write(f"3. Cost per user: ${cost_per_user:.5f}")
    st.subheader(f"Total Cost (In USD): ${total_cost:.2f}")

# Footer
st.markdown("---")
st.caption("Created with Streamlit")

# Run this with `streamlit run your_script.py` in your terminal
