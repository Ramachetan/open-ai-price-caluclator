import streamlit as st
from tiktoken import encoding_for_model

# Set page config for layout and title
st.set_page_config(page_title='Azure OpenAI Service Cost and Token Counter', layout='wide')

# Title and Description
st.title('Azure OpenAI Service Cost and Token Counter')
st.markdown("Calculate your Azure OpenAI service costs and count tokens for different models easily.")

# Function to color tokens
def color_tokens(tokens):
    colors = ['#FFDDC1', '#C1FFD7', '#D1C1FF', '#FFC1C1', '#C1D7FF']  # Add more colors if needed
    return ''.join(
        f"<span style='background-color: {colors[i%len(colors)]};'>{t}</span>" 
        for i, t in enumerate(tokens)
    )

# Function to calculate total cost
def calculate_cost(model, prompt_tokens, completion_tokens, messages, conversations, users):
    pricing = {
        'GPT-3.5-Turbo 4K': {'prompt': 0.0015, 'completion': 0.002},
        'GPT-3.5-Turbo 16K': {'prompt': 0.003, 'completion': 0.004},
        'GPT-4 8K': {'prompt': 0.03, 'completion': 0.06},
        'GPT-4 32K': {'prompt': 0.06, 'completion': 0.12},
    }
    prompt_cost = pricing[model]['prompt'] * prompt_tokens / 1000
    completion_cost = pricing[model]['completion'] * completion_tokens / 1000
    cost_per_message = prompt_cost + completion_cost
    cost_per_conversation = cost_per_message * messages
    cost_per_user = cost_per_conversation * conversations
    total_cost = cost_per_user * users
    return {
        "prompt_cost": prompt_cost,
        "completion_cost": completion_cost,
        "cost_per_message": cost_per_message,
        "cost_per_conversation": cost_per_conversation,
        "cost_per_user": cost_per_user,
        "total_cost": total_cost
    }

# Using columns to organize the layout
col1, col2 = st.columns(2)

# Token Counter Section
with col1:
    st.subheader('Token Counter')
    model_tokenizer = st.selectbox('Select the Model for Tokenization', ['gpt-3.5-turbo', 'gpt-4'], key='model_tokenizer')
    tokenizer = encoding_for_model(model_tokenizer)
    user_text = st.text_area("Enter text to count tokens:", height=150, key='user_text')

    if st.button('Count Tokens', key='count_tokens'):
        tokens = tokenizer.encode(user_text)
        tokens_colored = color_tokens([tokenizer.decode([t]) for t in tokens])
        st.markdown(tokens_colored, unsafe_allow_html=True)
        st.success(f"Token count: {len(tokens)}")

    # Show example button
    example_text = """Many words map to one token, but some don't: indivisible.

Unicode characters like emojis may be split into many tokens containing the underlying bytes: 🤚🏾

Sequences of characters commonly found next to each other may be grouped together: 1234567890"""
    
    if st.button('Show Example', key='show_example'):
        example_tokens = tokenizer.encode(example_text)
        tokens_colored = color_tokens([tokenizer.decode([t]) for t in example_tokens])
        st.markdown(tokens_colored, unsafe_allow_html=True)
        st.success(f"Number of tokens in example text: {len(example_tokens)}")

# Cost Estimator Section
with col2:
    st.subheader('Cost Estimator')
    model = st.selectbox('Select the Model for Cost Estimation', ['GPT-3.5-Turbo 4K', 'GPT-3.5-Turbo 16K', 'GPT-4 8K', 'GPT-4 32K'], key='model_cost')

    # Inputs for cost calculation
    avg_prompt_tokens = st.number_input("Average Prompt Tokens per Query (INPUT)", min_value=0, key='avg_prompt')
    avg_completion_tokens = st.number_input("Average Completion Tokens per Query (OUTPUT)", min_value=0, key='avg_completion')
    messages_per_conversation = st.number_input("Messages Per Conversation", min_value=0, key='messages_convo')
    avg_conversations = st.number_input("Average Number of Conversations per User", min_value=0, key='avg_convo')
    no_of_users = st.number_input("Number of Users", min_value=0, key='no_users')

    if st.button('Calculate Total Cost', key='calculate_cost'):
        cost_breakdown = calculate_cost(model, avg_prompt_tokens, avg_completion_tokens, messages_per_conversation, avg_conversations, no_of_users)
        st.subheader("Cost Breakdown (USD):")
        st.write(f"Prompt Cost: ${cost_breakdown['prompt_cost']:.4f}")
        st.write(f"Completion Cost: ${cost_breakdown['completion_cost']:.4f}")
        st.write(f"Cost Per Message: ${cost_breakdown['cost_per_message']:.4f}")
        st.write(f"Cost Per Conversation: ${cost_breakdown['cost_per_conversation']:.4f}")
        st.write(f"Cost Per User: ${cost_breakdown['cost_per_user']:.4f}")
        st.subheader(f"Total Cost (USD): ${cost_breakdown['total_cost']:.2f}")
# Footer and credits
st.markdown("---")
st.caption("Developed by [Rama Chetan Atmudi](https://www.linkedin.com/in/rama-chetan/)")
