import streamlit as st
import string
import warnings
warnings.filterwarnings("ignore")


def text_to_clean(text):
    text = text.upper().replace(" ", "")
    return ''.join([c for c in text if c.isalpha()])


def vigenere_encrypt(plaintext, keyword):
    clean_text = text_to_clean(plaintext)
    keyword = text_to_clean(keyword)
    
    if not keyword:
        return clean_text, []
    
    cipher_text = []
    steps = []
    
    for i, char in enumerate(clean_text):
        key_char = keyword[i % len(keyword)]
        shift = ord(key_char) - ord('A')
        plain_num = ord(char) - ord('A')
        cipher_num = (plain_num + shift) % 26
        cipher_char = chr(cipher_num + ord('A'))
        cipher_text.append(cipher_char)
        
        steps.append({
            'position': i + 1,
            'plain': char,
            'plain_num': plain_num,
            'key': key_char,
            'key_num': shift,
            'formula': f"({ord(char)-ord('A')} + {shift}) mod 26 = {cipher_num}",
            'cipher': cipher_char,
            'cipher_num': cipher_num
        })
    
    return ''.join(cipher_text), steps


def vigenere_decrypt(ciphertext, keyword):
    clean_text = text_to_clean(ciphertext)
    keyword = text_to_clean(keyword)
    
    if not keyword:
        return clean_text, []
    
    plain_text = []
    steps = []
    
    for i, char in enumerate(clean_text):
        key_char = keyword[i % len(keyword)]
        shift = ord(key_char) - ord('A')
        cipher_num = ord(char) - ord('A')
        plain_num = (cipher_num - shift) % 26
        plain_char = chr(plain_num + ord('A'))
        plain_text.append(plain_char)
        
        steps.append({
            'position': i + 1,
            'cipher': char,
            'cipher_num': cipher_num,
            'key': key_char,
            'key_num': shift,
            'formula': f"({cipher_num} - {shift}) mod 26 = {plain_num}",
            'plain': plain_char,
            'plain_num': plain_num
        })
    
    return ''.join(plain_text), steps


st.set_page_config(page_title="维吉尼亚密码演示", layout="wide")
st.title("🔐 维吉尼亚密码可视化演示系统")
st.markdown("使用关键字生成的重复密钥流进行加密，支持可视化每一步计算过程")


with st.sidebar:
    st.header("密钥设置")
    st.markdown("""
    **维吉尼亚密码原理：**
    - 使用关键字作为密钥
    - 密钥字母决定每个明文字母的移位量
    - 重复使用密钥直到覆盖所有明文
    
    **示例：**
    - 关键字 "KEY" 
    - K=10, E=4, Y=24
    - 移位量依次为 10, 4, 24, 10, 4, 24...
    """)
    
    keyword = st.text_input("输入关键字", "KEY")
    clean_keyword = text_to_clean(keyword)
    st.write(f"**清理后关键字：** {clean_keyword}")
    st.write(f"**关键字长度：** {len(clean_keyword)}")


tab1, tab2 = st.tabs(["加密", "解密"])

with tab1:
    st.subheader("明文加密")
    plaintext = st.text_input("输入明文", "HELLOWORLD")
    
    if st.button("开始加密", key="enc_vig"):
        cipher_text, steps = vigenere_encrypt(plaintext, keyword)
        
        st.success("加密成功！")
        st.write(f"**原始明文：** {plaintext}")
        st.write(f"**清理后明文：** {text_to_clean(plaintext)}")
        st.write(f"**密钥流：** {' '.join([keyword[i % len(keyword)] for i in range(len(text_to_clean(plaintext)))]) if keyword else ''}")
        st.write(f"**最终密文：** {cipher_text}")
        
        st.subheader("详细加密过程")
        if steps:
            step_data = {
                '位置': [s['position'] for s in steps],
                '明文': [s['plain'] for s in steps],
                '明文数值': [s['plain_num'] for s in steps],
                '密钥字母': [s['key'] for s in steps],
                '移位量': [s['key_num'] for s in steps],
                '计算公式': [s['formula'] for s in steps],
                '密文': [s['cipher'] for s in steps],
                '密文数值': [s['cipher_num'] for s in steps]
            }
            st.table(step_data)

with tab2:
    st.subheader("密文解密")
    ciphertext = st.text_input("输入密文", "KIFSMICOG")
    
    if st.button("开始解密", key="dec_vig"):
        plain_text, steps = vigenere_decrypt(ciphertext, keyword)
        
        st.success("解密成功！")
        st.write(f"**原始密文：** {ciphertext}")
        st.write(f"**清理后密文：** {text_to_clean(ciphertext)}")
        st.write(f"**密钥流：** {' '.join([keyword[i % len(keyword)] for i in range(len(text_to_clean(ciphertext)))]) if keyword else ''}")
        st.write(f"**最终明文：** {plain_text}")
        
        st.subheader("详细解密过程")
        if steps:
            step_data = {
                '位置': [s['position'] for s in steps],
                '密文': [s['cipher'] for s in steps],
                '密文数值': [s['cipher_num'] for s in steps],
                '密钥字母': [s['key'] for s in steps],
                '移位量': [s['key_num'] for s in steps],
                '计算公式': [s['formula'] for s in steps],
                '明文': [s['plain'] for s in steps],
                '明文数值': [s['plain_num'] for s in steps]
            }
            st.table(step_data)
