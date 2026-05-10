SUPPORTED_LANGUAGES = {
    "English": "en",
    "Hindi": "hi",
    "Bengali": "bn",
    "Gujarati": "gu",
    "Kannada": "kn",
    "Malayalam": "ml",
    "Marathi": "mr",
    "Odia": "or",
    "Punjabi": "pa",
    "Tamil": "ta",
    "Telugu": "te",
    "Urdu": "ur",
}

DEFAULT_LANGUAGE = "English"

INDIAN_STATES = [
    "All India",
    "Andhra Pradesh",
    "Arunachal Pradesh",
    "Assam",
    "Bihar",
    "Chhattisgarh",
    "Goa",
    "Gujarat",
    "Haryana",
    "Himachal Pradesh",
    "Jharkhand",
    "Karnataka",
    "Kerala",
    "Madhya Pradesh",
    "Maharashtra",
    "Manipur",
    "Meghalaya",
    "Mizoram",
    "Nagaland",
    "Odisha",
    "Punjab",
    "Rajasthan",
    "Sikkim",
    "Tamil Nadu",
    "Telangana",
    "Tripura",
    "Uttar Pradesh",
    "Uttarakhand",
    "West Bengal",
    "Delhi",
    "Jammu and Kashmir",
]

CATEGORIES = ["General", "OBC", "SC", "ST", "EWS", "Minority", "All"]
EDUCATION_LEVELS = [
    "School",
    "Class 10",
    "Class 12",
    "Diploma",
    "Undergraduate",
    "Postgraduate",
    "PhD",
    "Any",
]

RANKING_WEIGHTS = {
    "eligibility": 0.38,
    "state": 0.18,
    "income": 0.18,
    "education": 0.14,
    "retrieval": 0.12,
}
