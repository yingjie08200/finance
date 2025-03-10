import dash
from dash import html, dcc, Input, Output, State, callback
from dash.long_callback import DiskcacheLongCallbackManager
import diskcache
from dash.exceptions import PreventUpdate
from openai import OpenAI
import json
from datetime import datetime
import os
from dotenv import load_dotenv
import asyncio
from dash import callback_context
from concurrent.futures import ThreadPoolExecutor

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key="sk-eedeec16dfd44f2d8f0b3c0007187b04", base_url="https://api.deepseek.com")

# Initialize cache and long callback manager
cache = diskcache.Cache("./cache")
long_callback_manager = DiskcacheLongCallbackManager(cache)

# Initialize Dash app with async support
app = dash.Dash(__name__, suppress_callback_exceptions=True, long_callback_manager=long_callback_manager)

# Styling
CHAT_STYLE = {
    'width': '80%',
    'margin': '20px auto',
    'padding': '20px',
    'boxShadow': '0 0 10px rgba(0,0,0,0.1)',
    'borderRadius': '10px',
    'backgroundColor': 'white',
    'minHeight': '500px',
    'display': 'flex',
    'flexDirection': 'column'
}

MESSAGE_STYLE = {
    'margin': '10px',
    'padding': '10px',
    'borderRadius': '10px',
    'maxWidth': '70%',
    'position': 'relative',  # For timestamp positioning
}

TIMESTAMP_STYLE = {
    'fontSize': '10px',
    'color': '#666',
    'marginTop': '5px',
    'textAlign': 'right',
}

USER_MESSAGE_STYLE = {
    **MESSAGE_STYLE,
    'backgroundColor': '#e3f2fd',
    'marginLeft': 'auto',
}

BOT_MESSAGE_STYLE = {
    **MESSAGE_STYLE,
    'backgroundColor': '#f5f5f5',
    'marginRight': 'auto',
}

MESSAGE_CONTAINER_STYLE = {
    'margin': '10px',
    'display': 'flex',
    'flexDirection': 'column',
}

INPUT_STYLE = {
    'width': '100%',
    'padding': '10px',
    'borderRadius': '5px',
    'border': '1px solid #ddd',
    'marginTop': '10px',
}

BUTTON_STYLE = {
    'backgroundColor': '#2196F3',
    'color': 'white',
    'padding': '10px 20px',
    'border': 'none',
    'borderRadius': '5px',
    'marginLeft': '10px',
    'cursor': 'pointer',
}

def get_bot_response(message, conversation_history):
    """Get response from OpenAI API"""
    try:
        # Prepare the messages including conversation history
        messages = [
            {"role": "system", "content": "You are a helpful assistant."}
        ]
        
        # Add conversation history
        for msg in conversation_history:
            role = "assistant" if msg['type'] == "bot" else "user"
            content = msg['content']
            messages.append({"role": role, "content": content})
        
        # Add the current message
        messages.append({"role": "user", "content": message})
        
        # Get completion from OpenAI
        completion = client.chat.completions.create(
            model="deepseek-chat",
            messages=messages,
            temperature=0.7,
            max_tokens=1000
        )
        
        return completion.choices[0].message.content
        
    except Exception as e:
        return f"Error: {str(e)}"

def create_message_components(conversation_history):
    """Create message components from conversation history"""
    messages = []
    for message in conversation_history:
        message_container = html.Div(style=MESSAGE_CONTAINER_STYLE)
        
        if message['type'] == "user":
            style = USER_MESSAGE_STYLE
        else:
            style = BOT_MESSAGE_STYLE
            
        # Message content
        message_container.children = [
            html.Div(message['content'], style=style),
            html.Div(message['timestamp'], style=TIMESTAMP_STYLE)
        ]
        
        messages.append(message_container)
    return messages

# App layout
app.layout = html.Div([
    html.H1("AI Chatbot", 
            style={'textAlign': 'center', 'color': '#2196F3', 'marginTop': '20px'}),
    
    # Chat container
    html.Div([
        # Messages area
        html.Div(id='chat-messages', style={
            'overflowY': 'auto',
            'height': '400px',
            'padding': '10px',
            'border': '1px solid #ddd',
            'borderRadius': '5px',
            'marginBottom': '20px'
        }),
        
        # Input area
        html.Div([
            dcc.Input(
                id='user-input',
                type='text',
                placeholder='Type your message here...',
                style=INPUT_STYLE
            ),
            html.Button('Send', id='send-button', style=BUTTON_STYLE),
        ], style={'display': 'flex', 'alignItems': 'center'}),
        
        # Store conversation history
        dcc.Store(id='conversation-history', data=[]),
        
        # Store for triggering bot response
        dcc.Store(id='trigger-bot-response', data=None),
        
        # Interval component for auto-scrolling
        dcc.Interval(id='interval-component', interval=500, n_intervals=0)
    ], style=CHAT_STYLE)
])

# First callback: Handle user input and update immediately
@callback(
    [Output('conversation-history', 'data'),
     Output('user-input', 'value'),
     Output('trigger-bot-response', 'data')],
    [Input('send-button', 'n_clicks'),
     Input('user-input', 'n_submit')],
    [State('user-input', 'value'),
     State('conversation-history', 'data')],
    prevent_initial_call=True
)
def handle_user_input(n_clicks, n_submit, user_input, conversation_history):
    if not user_input:
        raise PreventUpdate
    
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Add user message to conversation
    user_message = {
        "type": "user",
        "content": user_input,
        "timestamp": current_time
    }
    conversation_history.append(user_message)
    
    # Return updated conversation history and trigger bot response
    return conversation_history, '', user_input

async def get_bot_response_async(message, conversation_history):
    """Get response from OpenAI API asynchronously"""
    try:
        # Prepare the messages including conversation history
        messages = [
            {"role": "system", "content": "You are a helpful assistant."}
        ]
        
        # Add conversation history
        for msg in conversation_history:
            role = "assistant" if msg['type'] == "bot" else "user"
            content = msg['content']
            messages.append({"role": role, "content": content})
        
        # Add the current message
        messages.append({"role": "user", "content": message})
        
        # Get completion from OpenAI
        # Use asyncio.to_thread to run the synchronous API call in a separate thread
        completion = await asyncio.to_thread(
            client.chat.completions.create,
            model="deepseek-chat",
            messages=messages,
            temperature=0.7,
            max_tokens=1000
        )
        
        return completion.choices[0].message.content
        
    except Exception as e:
        return f"Error: {str(e)}"

def get_bot_response_sync(message, conversation_history):
    """Get response from OpenAI API synchronously"""
    try:
        # Prepare the messages including conversation history
        messages = [
            {"role": "system", "content": "You are a helpful assistant."}
        ]
        
        # Add conversation history
        for msg in conversation_history:
            role = "assistant" if msg['type'] == "bot" else "user"
            content = msg['content']
            messages.append({"role": role, "content": content})
        
        # Add the current message
        messages.append({"role": "user", "content": message})
        
        # Get completion from OpenAI
        completion = client.chat.completions.create(
            model="deepseek-chat",
            messages=messages,
            temperature=0.7,
            max_tokens=1000
        )
        
        return completion.choices[0].message.content
        
    except Exception as e:
        return f"Error: {str(e)}"

@dash.callback(
    Output('chat-messages', 'children'),
    [Input('conversation-history', 'data'),
     Input('trigger-bot-response', 'data')],
    prevent_initial_call=True,
    manager=long_callback_manager,
    running=[
        (Output('send-button', 'disabled'), True, False),
        (Output('user-input', 'disabled'), True, False),
    ],
)
def update_chat_messages(conversation_history, trigger):
    ctx = callback_context
    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    if triggered_id == 'trigger-bot-response' and trigger is not None:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Add a "typing" indicator
        typing_message = {
            "type": "bot",
            "content": "Typing...",
            "timestamp": current_time
        }
        conversation_history.append(typing_message)
        
        # Create and return temporary message components with typing indicator
        temp_messages = create_message_components(conversation_history)
        
        # Get bot response
        bot_response = get_bot_response(trigger, conversation_history[:-1])  # Exclude typing message
        
        # Remove typing message and add actual response
        conversation_history.pop()  # Remove typing indicator
        bot_message = {
            "type": "bot",
            "content": bot_response,
            "timestamp": current_time
        }
        conversation_history.append(bot_message)
    
    # Create message components
    return create_message_components(conversation_history)

@callback(
    Output('chat-messages', 'children', allow_duplicate=True),
    Input('interval-component', 'n_intervals'),
    State('chat-messages', 'children'),
    prevent_initial_call=True
)
def scroll_to_bottom(n_intervals, children):
    if not children:
        raise PreventUpdate
    
    # Add a dummy div at the bottom to scroll to
    children.append(html.Div(id='scroll-bottom'))
    
    return children

if __name__ == '__main__':
    app.run(debug=True, port=8050) 