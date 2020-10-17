from . import Trigers
from data_contracts.analysis_result import AnalysisResult
from googletrans import Translator
trigers = Trigers.trigers

def analyze_user(fb_user):
    posts = fb_user.posts
    postsNum = len(posts) # get total posts num
   
    # check what is the rate of posts of each triger
    # create dict of results: <triger, trigerPostsRate>
    trigersPostsCount = dict()
    
    # count how may posts are there for each triger
    for post in posts:
        postTrigers = detect_post_trigers_V2(post, trigersPostsCount)
        increase_count(trigersPostsCount, postTrigers)

    # calculate trigers rates
    trigersPostsRates = dict()
    for triger in trigersPostsCount:
        trigersPostsRates[triger] = trigersPostsCount[triger] / postsNum  # calculate rate of posts in this triger
    
    #convert to analysis result
    percentResult = "See percent of triger in text result."
    textResult = convert_trigers_rates_to_text(trigersPostsRates)

    return AnalysisResult(percentResult, textResult)

# calculate post's trigers and add to counter dictionary
# improve - currently returns only one triger per post
def detect_post_trigers(post, counterDictionary):
    trigers_word_count = {}    # holds word count per triger
    postWords = post.split()
    postWordsNum = len(postWords)

    threshold = 0.05*postWordsNum   # threshold!

    for word in postWords:
        wordSubjcets = find_word_in_trigers(word)
        increase_count(trigers_word_count, wordSubjcets)
    
    # increase post triger in counter dict
    for triger in trigers_word_count:
        if trigers_word_count[triger] >= threshold:
            increase_count(counterDictionary, trigers)
            
    return counterDictionary

def detect_post_trigers_V2(post, counterDictionary):
    post_trigers = set()
    postSentences = post.split(".")
    
    for sentence in postSentences:
        sentenceWords = post.split()
        for word in sentenceWords:
            wordSubjcets = detect_word_trigers(word)
            if wordSubjcets!=None:
                for wordTriger in wordSubjcets:    
                    post_trigers.add(wordTriger)
            
    return post_trigers

def increase_count(dictionary, trigers):
    for triger in trigers:
        if triger in dictionary.keys():
            dictionary[triger] += 1
        else:
            dictionary.update({triger : 1})
    return

# check if word exist in each triger
# improve - currently returns only one triger per word
def detect_word_trigers(word):
    wordTrigers = set()
    for triger in trigers:
        for triger_word in trigers[triger]:
            if word==triger_word or word=="ה"+triger_word:       # check if current word is substring of the triger word 
                wordTrigers.add(triger)
    return wordTrigers

def convert_trigers_rates_to_text(trigersPostsRates):
    textResult = "Posts of user according to trigers: "

    for triger in trigersPostsRates.keys():
        if triger != None:
            textResult += triger + ": " + str(trigersPostsRates[triger]) + ","
    
    return textResult[:-1]  # trim the last ","