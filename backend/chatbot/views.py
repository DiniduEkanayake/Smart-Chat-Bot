from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import random
import nltk
from newspaper import Article
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import warnings

# Download necessary NLTK data
nltk.download('punkt', quiet=True)
warnings.filterwarnings('ignore')

# Function to get the article content
def get_article():
    url = 'https://www.mayoclinic.org/diseases-conditions/chronic-kidney-disease/symptoms-causes/syc-20354521'
    article = Article(url)
    try:
        article.download()
        article.parse()
        article.nlp()
        corpus = article.text
        sentence_list = nltk.sent_tokenize(corpus)
    except Exception as e:
        corpus = ""
        sentence_list = []
        print(f"Error loading article: {e}")
    return corpus, sentence_list

# Chatbot logic: Greeting response
def greeting_response(text):
    text = text.lower()
    bot_greetings = ['howdy', 'hi', 'hey', 'hello', 'hola']
    user_greetings = ['hi', 'hey', 'hello', 'hola', 'greetings', 'wassup']

    for word in text.split():
        if word in user_greetings:
            return random.choice(bot_greetings)
    return None
def farewell_response(text):
    text = text.lower()
    bot_farewell = ['Bye! Have a great day.', 'Goodbye! Take care.', 'Farewell!']
    user_farewell = ['bye', 'goodbye', 'farewell', 'see you later', 'cya']

    for word in text.split():
        if word in user_farewell:
            return random.choice(bot_farewell)
    return None

# Chatbot logic: Generate response based on similarity
def get_response(user_input, sentence_list, corpus):
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
        bot_response = "I apologize, I don't understand."

    sentence_list.remove(user_input)
    return bot_response

# Helper function to sort similarity indices
def index_sort(list_var):
    length = len(list_var)
    list_index = list(range(0, length))
    
    x = list_var
    for i in range(length):
        for j in range(length):
            if x[list_index[i]] > x[list_index[j]]:
                temp = list_index[i]
                list_index[i] = list_index[j]
                list_index[j] = temp
                
    return list_index

class ChatbotAPIView(APIView):
    def post(self, request):
        user_input = request.data.get('message')
        if not user_input:
            return JsonResponse({'error': 'Message not provided'}, status=status.HTTP_400_BAD_REQUEST)

        # Load the article content
        corpus, sentence_list = get_article()

        # Check for greetings
        greeting = greeting_response(user_input)
        if greeting:
            return JsonResponse({'response': greeting})
        
        #check for farewell
        farewell = farewell_response(user_input)
        if farewell:
            return JsonResponse({'response': farewell})

        # Generate a bot response based on the input
        bot_response = get_response(user_input, sentence_list, corpus)

        return JsonResponse({'response': bot_response}, status=status.HTTP_200_OK)
