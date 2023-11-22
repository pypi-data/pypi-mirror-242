QUERY_KW: str = "vector_search"
VECTOR_SEARCH_MODIFIER: str = "vector_search_modifier"

EMBEDDING_COLUMN_VECTORS: str = "EMBEDDING_COLUMN_VECTORS"

SCORE_DISTANCE_COLUMN_NAME: str = "vector_distance"
LABEL_SCORE_COLUMN_NAME: str = "label_score"
KEYWORDS_SCORE_COLUMN_NAME: str = "keywords_score"

ACCEPTED_LANGUAGES: list = ["eng", "jp"]

APPRECIATION_DEFINITIONS: dict = {
    "eng": {
        "positive": ["positive", "positively", "positiveness", "positivenesses", "positivity", "positivities", "positivistic", "positivistically"],
        "negative": ["negative", "negatively", "negativeness", "negativenesses", "negativity", "negativities", "negativistic", "negativistically"],
    },
    "jp": {
        "positive": ["ポジティブ", "ポジティブに", "ポジティブさ", "ポジティブさ", "ポジティブさ", "ポジティブさ", "ポジティブ主義的", "ポジティブ主義的"],
        "negative": ["ネガティブ", "ネガティブに", "ネガティブさ", "ネガティブさ", "ネガティブさ", "ネガティブさ", "ネガティブ主義的", "ネガティブ主義的"]
    }
}


SENTIMENTS_DEFINITIONS: dict = {
    "eng": {
        "joy": ["joy", "joyful", "joyous", "joyed", "joying", "joyousness", "joyfulness", "joylessness", "joylessly", "joyousnesses", "joyfulnesses", "joylessnesses", "joylessly", "joyousness", "joyfulness", "joylessness", "joylessly", "joyousnesses", "joyfulnesses", "joylessnesses", "joylessly", "joyousness", "joyfulness", "joylessness", "joylessly", "joyousnesses", "joyfulnesses", "joylessnesses", "joylessly", "joyousness", "joyfulness", "joylessness", "joylessly", "joyousnesses", "joyfulnesses", "joylessnesses", "joylessly", "joyousness", "joyfulness", "joylessness", "joylessly", "joyousnesses", "joyfulnesses", "joylessnesses", "joylessly"],
        "jealousy": ["jealousy", "jealous"],
        "surprise": ["surprise", "surprised", "surprises", "surprising"],
        "sadness": ["sadness", "sad", "sads", "sadded"],
        "anger": ["anger", "angry", "angers", "angered"],
        "fear": ["fear", "fearful", "fears", "feared"],
        "disgust": ["disgust", "disgusted", "disgusting", "disgusts", "disgustingly"],
        "trust": ["trust", "trusted", "trusting", "trusts", "trustingly"],
        "love": ["love", "loved", "loves", "loving", "lovingly"],
        "disappointment": ["disappointment", "disappoint", "disappointed", "disappoints", "disappointing"],
        "like": ["like", "liked", "likes", "liking", "likings"],
        "hate": ["hate", "hated", "hates", "hating", "hatred"],
        "confusion": ["confusion", "confused", "confuses", "confusing", "confusingly"],
        "hope": ["hope", "hoped", "hopes", "hoping", "hopeful", "hopefulness", "hopeless", "hopelessly", "hopelessness", "hopefulnesses", "hopelessnesses", "hopelessly", "hopefulness", "hopelessness", "hopelessly", "hopefulnesses", "hopelessnesses", "hopelessly", "hopefulness", "hopelessness", "hopelessly", "hopefulnesses", "hopelessnesses", "hopelessly", "hopefulness", "hopelessness", "hopelessly", "hopefulnesses", "hopelessnesses", "hopelessly", "hopefulness", "hopelessness", "hopelessly", "hopefulnesses", "hopelessnesses", "hopelessly", "hopefulness", "hopelessness", "hopelessly", "hopefulnesses", "hopelessnesses", "hopelessly"],
    },
    "jp": {
        "joy": ["喜び", "うれしい", "喜ばしい", "喜ぶ", "喜んでいる", "喜び", "喜び", "無喜", "喜ばずに", "無喜", "喜び", "無喜", "喜ばずに", "無喜", "喜び", "喜び", "無喜", "喜ばずに", "無喜", "喜び", "無喜", "喜ばずに", "無喜", "喜び", "無喜", "喜ばずに", "無喜", "喜び", "無喜", "喜ばずに", "無喜", "喜び", "無喜", "喜ばずに", "無喜", "喜び", "無喜", "喜ばずに", "無喜", "喜び", "無喜", "喜ばずに", "無喜", "喜び", "無喜", "喜ばずに", "無喜", "喜び", "無喜", "喜ばずに", "無喜", "喜び", "無喜", "喜ばずに", "無喜", "喜び", "無喜", "喜ばずに", "無喜", "喜び", "無喜", "喜ばずに", "無喜", "喜び", "無喜", "喜ばずに", "無喜", "喜び", "無喜", "喜ばずに", "無喜", "喜び", "無喜", "喜ばずに", "無喜", "喜び", "無喜", "喜ばずに", "無喜", "喜び", "無喜", "喜ばずに", "無喜", "喜び", "無喜", "喜ばずに", "無喜", "喜び", "無喜", "喜ばずに", "無喜", "喜び", "無喜", "喜ばずに", "無喜", "喜び", "無喜", "喜ばずに", "無喜", "喜び", "無喜", "喜ばずに", "無喜", "喜び", "無喜", "喜ばずに", "無喜", "喜び", "無喜", "喜ばずに", "無喜", "喜び", "無喜", "喜ばずに", "無喜", "喜び", "無喜", "喜ばずに", "無喜", "喜び", "無喜", "喜ばずに", "無喜", "喜び", "無喜", "喜ばずに", "無喜", "喜び", "無喜", "喜ばずに", "無喜", "喜び", "無喜", "喜ばずに", "無喜", "喜び", "無喜", "喜ばずに", "無喜", "喜び", "無喜", "喜ばずに", "無喜", "喜び", "無喜", "喜ばずに", "無喜", "喜び", "無喜", "喜ばずに", "無喜", "喜び", "無喜", "喜ばずに", "無喜", "喜び", "無喜", "喜ばずに", "無喜", "喜び", "無喜", "喜ばずに", "無喜", "喜び", "無喜", "喜ばずに", "無喜", "喜び", "無喜", "喜ばずに", "無喜", "喜び", "無喜", "喜ばずに", "無喜", "喜び", "無喜", "喜ばずに", "無喜", "喜び", "無喜", "喜ばずに", "無喜"],
        "jealousy": ["嫉妬", "嫉妬心"],
        "surprise": ["驚き", "驚いた", "驚き", "驚く"],
        "sadness": ["悲しみ", "悲しい", "悲しい", "悲しんだ"],
        "anger": ["怒り", "怒っている", "怒り", "怒った"],
        "fear": ["恐れ", "恐れている", "恐れ", "恐れた"],
        "disgust": ["嫌悪", "嫌悪した", "嫌悪的な", "嫌悪", "嫌悪的に"],
        "trust": ["信頼", "信頼された", "信頼している", "信頼する", "信頼的に"],
        "love": ["愛", "愛された", "愛する", "愛する", "愛情をもって"],
        "disappointment": ["失望", "失望する", "失望した", "失望させる", "失望的"],
        "like": ["好き", "好きだった", "好き", "好きな", "好み"],
        "hate": ["憎しみ", "憎む", "憎む", "憎む", "憎しみ"],
        "confusion": ["混乱", "混乱した", "混乱させる", "混乱している", "混乱している"],
        "hope": ["希望", "希望した", "希望する", "希望している", "希望的", "希望的な"],
    },
}
