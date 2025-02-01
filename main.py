# Install required libraries
import nltk
from newspaper import Article
import random
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import warnings

# Suppress warnings
warnings.filterwarnings('ignore')

# Download NLTK data
nltk.download('punkt', quiet=True)

# URL of the article
url = 'https://www.mayoclinic.org/diseases-conditions/chronic-kidney-disease/symptoms-causes/syc-20354521'

# Initialize the Article object
article = Article(url)

try:
    # Download, parse, and perform NLP on the article
    article.download()
    article.parse()
    article.nlp()

    # Extract the text (corpus)
    corpus = article.text

    # Tokenize the corpus into sentences
    sentence_list = nltk.sent_tokenize(corpus)

except Exception as e:
    print(f"An error occurred: {e}")

# Function to return a random greeting response to a user's greeting
def greeting_response(text):
    text = text.lower()

    # Bot's response to a user's greeting
    bot_greetings = ['howdy', 'hi', 'hey', 'hello', 'hola']
    # User's greeting
    user_greetings = ['hi', 'hey', 'hello', 'hola', 'greetings', 'wassup']

    for word in text.split():
        if word in user_greetings:
            return random.choice(bot_greetings)
    return None

# Function to sort indices based on similarity scores
def index_sort(list_var):
    length = len(list_var)
    list_index = list(range(0, length))

    x = list_var
    for i in range(length):
        for j in range(length):
            if x[list_index[i]] > x[list_index[j]]:
                # Swap
                temp = list_index[i]
                list_index[i] = list_index[j]
                list_index[j] = temp

    return list_index

# Function to create the bot's response
def bot_response(user_input):
    user_input = user_input.lower()
    sentence_list.append(user_input)
    bot_response = ''
    cm = CountVectorizer().fit_transform(sentence_list)
    similarity_scores = cosine_similarity(cm[-1], cm)
    similarity_scores_list = similarity_scores.flatten()
    index = index_sort(similarity_scores_list)

    index = index[1:]
    response_flag = 0

    j = 0
    for i in range(len(index)):
        if similarity_scores_list[index[i]] > 0.0:
            bot_response = bot_response + ' ' + sentence_list[index[i]]
            response_flag = 1
            j = j + 1
        if j > 2:
            break

    if response_flag == 0:
        bot_response = bot_response + ' ' + "I apologize, I don't understand."

    sentence_list.remove(user_input)
    return bot_response

# Start the chat
print('Doc Bot: I am Doctor Bot or Doc Bot for short. I will answer your queries about Chronic Kidney Disease. If you want to exit, type bye.')

exit_list = ['exit', 'see you later', 'bye', 'quit', 'break']

while True:
    user_input = input("You: ")
    if user_input.lower() in exit_list:
        print('Doc Bot: Chat with you later!')
        break
    else:
        response = greeting_response(user_input)
        if response is not None:
            print('Doc Bot: ' + response)
        else:
            print('Doc Bot: ' + bot_response(user_input))