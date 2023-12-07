

SIGNATURE_REGEXES = [
    r"(\b.?sign\b)",
    r"(\bplease consider the environment\b)"
]

GREETING_REGEXES = [
    r"(\bhi.*?\b)",
    r"(\bthanks+\b)",
    r"(\bbest regards\b)"
]

NORMALIZATION_REGEXES = {
    r"(\bcod\b)": "code",
    r"(\bnr\b)": "number",
    r"(\bnum\b)": "number",
    r"(\binfo\b)": "information"
}

WEB_TOKENS = ["![]", "cid:image", "@", "javascript", "cid:", "www"]
