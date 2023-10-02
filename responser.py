from datetime import datetime
import openai

def query(role, content):
    return {"role": role, "content": content}

def generate_resp(history, sender_email, owner_email, free_time):
    # Initialize the conversation with the assistant's role and a prompt
    today = datetime.now()
    formatted_date = today.strftime("%Y-%m-%d")
    print("CONTENT: {}".format(history))

    # Set the context for the assistant
    body_context = ('''You are a virtual assistant, named Zen, acting as a bridge between two individuals for scheduling meetings.
               Your primary goal is to facilitate efficient communication, aiming to achieve the desired outcome
               in as few emails as possible. Avoid asking followup questions like meeting agenda and preferences
               Just use the free time of owner provided to you to make decisions. Always provide clear, concise, and actionable responses
               Today is {}, and Your owner, {}, is available during following free time: {}.
               Use this information to schedule a meeting with the sender, {}. 
               Do not keep them waiting, neither should you send email regarding "I'll get back to you soon"
               Try to reply with a single email containing some approapriate free time. If not mentioned explicitly,
               assume day time is most appropriate any day of them week. If not mentioned 
               explicitly, try to arrange 2-3 suitable hours from the available time.'''.format(str(today), owner_email, free_time, sender_email))

    # Create the prompt
    body_prompt = (f'''Have a look at given conversation and give the best response.(the mails are in order as Message 1, Message 2 etc).
                If there are multiple messages then most probably First message was sent by you denoting the free time available by owner, and second message was sent by sender choosing some right time.
                Select Appropriate time based on the messages. If there is only one message, decide whether to ask the sender for his free time, or schedule a time immediately if sender has provided details already about their free time.
                '{history}'. I suppose you
              have the calendar and availability of your owner, Use that to generate CONCISE responses fo
              the sender avoid asking any follow-up questions.''')

    messages_list = [
        query("system", body_context),
        query("user", body_prompt)
    ]

    # Generate a response using GPT-3.5-turbo
    print("GENERATING RESPONSE")
    body_response = openai.ChatCompletion.create(
        # model="gpt-3.5-turbo",
        model="gpt-4",
        messages=messages_list
    )
    print("GOT IT")

    # Extract the assistant's reply from the response
    body_reply = body_response['choices'][0]['message']['content']

    subject_context = ('''I will give you en email, and generate just a single proper subject for the email. Return the subject and nothing else''')

    # Create the prompt
    subject_prompt = ('''Content of the email: "{}"'''.format(body_reply))

    messages_list = [
        query("system", subject_context),
        query("user", subject_prompt)
    ]

    # Generate a response using GPT-3.5-turbo
    print("GENERATING RESPONSE")
    subject_response = openai.ChatCompletion.create(
        # model="gpt-3.5-turbo",
        model="gpt-4",
        messages=messages_list
    )
    print("GOT IT")

    # Extract the assistant's reply from the response
    subject_reply = subject_response['choices'][0]['message']['content']

    return body_reply, subject_reply


