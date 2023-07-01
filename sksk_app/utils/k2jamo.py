# k2jamo
# substitute(text)
import re
 
initial = ["ᄀ", "ᄁ", "ᄂ", "ᄃ", "ᄄ", "ᄅ", "ᄆ", "ᄇ", "ᄈ", "ᄉ", "ᄊ", "ᄋ",
			"ᄌ", "ᄍ", "ᄎ", "ᄏ", "ᄐ", "ᄑ", "ᄒ"]
medial = ["ᅡ", "ᅢ", "ᅣ", "ᅤ", "ᅥ", "ᅦ", "ᅧ", "ᅨ", "ᅩ", "ᅪ", "ᅫ", "ᅬ",
		   "ᅭ", "ᅮ", "ᅯ", "ᅰ", "ᅱ", "ᅲ", "ᅳ", "ᅴ", "ᅵ", ""]
final = ["", "ᆨ", "ᆩ", "ᆪ", "ᆫ", "ᆬ", "ᆭ", "ᆮ", "ᆯ", "ᆰ", "ᆱ", "ᆲ",
		  "ᆳ", "ᆴ", "ᆵ", "ᆶ", "ᆷ", "ᆸ", "ᆹ", "ᆺ", "ᆻ", "ᆼ", "ᆽ", "ᆾ",
		  "ᆿ", "ᇀ", "ᇁ", "ᇂ"]

REGEX = '[가-힣]'
pattern = re.compile(REGEX)
 
 
def convert_main(match):
    '正規表現でマッチした完成形ハングル<match>を字母に分解する'
    # ord...文字をUnicodeにする
    # group(0)...パターンにマッチした文字列全体を返す
    value = ord(match.group(0))
    my_int = value - 44032
    my_int_index = int(my_int / 588)
    my_final_index = my_int % 28
    my_medial_index = \
        int((my_int - (my_int_index * 588) - my_final_index) / 28)
    # Unicodeの番号からハングルを割り出す
    result = initial[my_int_index] + \
        medial[my_medial_index] + \
        final[my_final_index]
    return result
 
 
def substitute(text):
    '正規表現で完成形ハングルにマッチした入力<text>を置換する'
    # convert_main Unicordから割り出されたハングル文字
    result = re.sub(pattern, convert_main, text)
    return result
 
 
if __name__ == '__main__':
    for letters in ['가', '안녕', '한국어 문장입니다.', '영문자 a/b를 포함']:
        output = substitute(letters)
        print(letters, '=>', output)