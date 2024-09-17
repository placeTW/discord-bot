PINYIN_INITIALS = {
    "b": "ㄅ",
    "p": "ㄆ",
    "m": "ㄇ",
    "f": "ㄈ",
    "d": "ㄉ",
    "t": "ㄊ",
    "n": "ㄋ",
    "l": "ㄌ",
    "g": "ㄍ",
    "k": "ㄎ",
    "h": "ㄏ",
    "j": "ㄐ",
    "q": "ㄑ",
    "x": "ㄒ",
    "zh": "ㄓ",
    "ch": "ㄔ",
    "sh": "ㄕ",
    "r": "ㄖ",
    "z": "ㄗ",
    "c": "ㄘ",
    "s": "ㄙ",
}

# In Hanyu Pinyin, 「ㄜ」 and 「ㄝ」 share the same character 〔e〕
# because the possible initials are almost different.
# Only 「誒」 (「ㄝˋ」) interferes with 「惡」(「ㄜˋ」),
# in this case 「ㄝ」 is spelt as 〔ê〕
PINYIN_ALONE = {
    "zhi": "ㄓ",
    "chi": "ㄔ",
    "shi": "ㄕ",
    "ri": "ㄖ",
    "zi": "ㄗ",
    "ci": "ㄘ",
    "si": "ㄙ",
    "a": "ㄚ",
    "o": "ㄛ",
    "e": "ㄜ",
    "ê": "ㄝ",
    "ai": "ㄞ",
    "ei": "ㄟ",
    "ao": "ㄠ",
    "ou": "ㄡ",
    "an": "ㄢ",
    "en": "ㄣ",
    "ang": "ㄤ",
    "er": "ㄦ",
    "yi": "ㄧ",
    "wu": "ㄨ",
    "yu": "ㄩ",
    # Combined
    "ya": "ㄧㄚ",
    "yo": "ㄧㄛ",
    "ye": "ㄧㄝ",
    "yai": "ㄧㄞ",
    "yao": "一ㄠ",
    "you": "ㄧㄡ",
    "yan": "ㄧㄢ",
    "yin": "ㄧㄣ",
    "yang": "ㄧㄤ",
    "ying": "ㄧㄥ",
    "wa": "ㄨㄚ",
    "wo": "ㄨㄛ",
    "wai": "ㄨㄞ",
    "wei": "ㄨㄟ",
    "wan": "ㄨㄢ",
    "wen": "ㄨㄣ",
    "wang": "ㄨㄤ",
    "weng": "ㄨㄥ",
    "yue": "ㄩㄝ",
    "yuan": "ㄩㄢ",
    "yun": "ㄩㄣ",
    "yong": "ㄩㄥ",
}

PINYIN_CENTER = {
    "i": "ㄧ",
    "u": "ㄨ",  # also ㄩ
    "ü": "ㄩ",
}

# The designer of Hanyu Pinyin used e to represent both 「ㄜ」 and 「ㄝ」.
# This is because 「ㄝ」 could only be used in  「ㄩㄝ」 and 「ㄧㄝ」
PINYIN_FINALS = {
    "a": "ㄚ",
    "o": "ㄛ",
    "e": "ㄜ",  # also ㄝ
    "ai": "ㄞ",
    "ei": "ㄟ",
    "ao": "ㄠ",
    "ou": "ㄡ",
    "an": "ㄢ",
    "en": "ㄣ",
    "ang": "ㄤ",
    "eng": "ㄥ",
    "er": "ㄦ",
}

PINYIN_COMBINED = {
    "iu": "ㄧㄡ",
    "ian": "ㄧㄢ",
    "in": "ㄧㄣ",
    "iang": "ㄧㄤ",
    "ing": "ㄧㄥ",
    "ui": "ㄨㄟ",
    "uan": "ㄨㄢ",  # also ㄩㄢ
    "un": "ㄨㄣ",  # also ㄨㄣ
    "uang": "ㄨㄤ",
    "ong": "ㄨㄥ",
    "ue": "ㄩㄝ",
    "iong": "ㄩㄥ",
}

# Only 「a﹑o﹑e﹑i﹑u﹑ü」 are added diacritics in Hanyu Pinyin
# Neutral tones are not labeled
DIACRITIC_TO_BASE_AND_TONE = {
    # ā (ɑ̄) ē ī ō ū ǖ
    # á (ɑ́) é í ó ú ǘ
    # ǎ (ɑ̌) ě ǐ ǒ ǔ ǚ
    # à (ɑ̀) è ì ò ù ǜ
    "ā": ("a", "¯"),
    "á": ("a", "ˊ"),
    "ǎ": ("a", "ˇ"),
    "ă": ("a", "ˇ"),
    "à": ("a", "ˋ"),
    "ē": ("e", "¯"),
    "é": ("e", "ˊ"),
    "ě": ("e", "ˇ"),
    "ĕ": ("e", "ˇ"),
    "è": ("e", "ˋ"),
    "ī": ("i", "¯"),
    "í": ("i", "ˊ"),
    "ǐ": ("i", "ˇ"),
    "ĭ": ("i", "ˇ"),
    "ì": ("i", "ˋ"),
    "ō": ("o", "¯"),
    "ó": ("o", "ˊ"),
    "ǒ": ("o", "ˇ"),
    "ŏ": ("o", "ˇ"),
    "ò": ("o", "ˋ"),
    "ū": ("u", "¯"),
    "ú": ("u", "ˊ"),
    "ǔ": ("u", "ˇ"),
    "ŭ": ("u", "ˇ"),
    "ù": ("u", "ˋ"),
    "ǖ": ("ü", "¯"),
    "ǘ": ("ü", "ˊ"),
    "ǚ": ("ü", "ˇ"),
    "ü̆": ("ü", "ˇ"),
    "ǜ": ("ü", "ˋ"),
    "ề": ("ê", "ˋ"),  # 「ㄝ」 could only possibly be the fourth tone
}


# Matches chewing from substrings
def match_chewing(string: str, index: int, target: dict[str, str]):
    global PINYIN_COMBINED, PINYIN_FINALS
    # Substrings only to the maxium possible character amount
    for i in range(max([len(i) for i in target.keys()]), 0, -1):
        target_str = string[index : index + i]
        result = target.get(target_str)
        if result:
            # Resolve duplicates
            if target == PINYIN_COMBINED:
                if target_str == "uan" and string[index - 1] in [
                    "j",
                    "q",
                    "x",
                ]:
                    result = "ㄩㄢ"
                elif target_str == "un" and string[index - 1] in [
                    "j",
                    "q",
                    "x",
                ]:
                    result = "ㄩㄣ"
            elif target == PINYIN_CENTER:
                if target_str == "u" and string[index - 1] in ["j", "q", "x"]:
                    result = "ㄩ"
            elif target == PINYIN_FINALS:
                if target_str == "e" and string[index - 1] in "iü":
                    result = "ㄝ"
                # TODO separate those which can have j, q, x as the initial constant
                # FIXME ugly bad code
                elif target_str == "en" and (
                    string[index - 1] in ["j", "q", "x"] or string[index - 2] in ["j", "q", "x"]
                ):
                    continue

            if target == PINYIN_COMBINED:
                if forms_new_word(string, index + i):
                    return (index + i, result)
            else:
                return (index + i, result)
    return (index + 1, None)


# Ensure there are no trailing characters unable to form word
def forms_new_word(pinyin: str, index: int):
    global PINYIN_INITIALS, PINYIN_ALONE
    return (
        match_chewing(pinyin, index, PINYIN_INITIALS | PINYIN_ALONE)[1]
        or index >= len(pinyin)
        or not pinyin[index].isalpha()
    )


def to_chewing(pinyin: str) -> str:
    # Remove leading and trailing spaces
    pinyin = pinyin.strip()
    # Handle all capital letters and lower-case letters
    pinyin = pinyin.lower()

    # Temporarily store the chewing tones and original index
    tones = []
    for index in range(len(pinyin)):
        value = DIACRITIC_TO_BASE_AND_TONE.get(pinyin[index])
        if not value:
            continue
        pinyin = pinyin[:index] + value[0] + pinyin[index + 1 :]
        tones.append((index, value[1]))

    chewing = ""
    index = 0
    while index < len(pinyin):

        # Ignore special characters
        if not (pinyin[index].isalpha() and pinyin[index].islower()):
            chewing += pinyin[index]
            index += 1
            continue

        # In case of Erhua, 〔r〕 is adeed to the last character instead of 〔er〕
        if index == len(pinyin) - 1 and pinyin[index] == "r":
            chewing += "ㄦ¯"
            break

        # Check matches for independent words
        res = match_chewing(pinyin, index, PINYIN_ALONE)
        if res[1] and forms_new_word(pinyin, res[0]):
            chewing += res[1]  # ㄧㄚ
            index = res[0]

        else:
            initial = match_chewing(pinyin, index, PINYIN_INITIALS)
            assert initial[1], f"Failed to match initial in '{pinyin}' at index {index - 1}"
            index = initial[0]
            chewing += initial[1]  # ㄍ
            combined = match_chewing(pinyin, index, PINYIN_COMBINED)
            if combined[1]:
                index = combined[0]
                chewing += combined[1]  # ㄨㄤ
            else:
                center = match_chewing(pinyin, index, PINYIN_CENTER)
                if center[1]:
                    chewing += center[1]  # ㄍㄨ
                    index = center[0]
                final = match_chewing(pinyin, index, PINYIN_FINALS)
                if final[1]:
                    chewing += final[1]  # ㄍㄨㄛ
                    index = final[0]

        if len(tones) and tones[0][0] < index:
            chewing += tones.pop(0)[1]  # ㄍㄨㄛˊ
        else:
            chewing += "˙"

        chewing += "　"  # Add a fullwidth space between words

    return chewing
