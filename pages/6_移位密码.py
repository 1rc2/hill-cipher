import streamlit as st
import string
import warnings
warnings.filterwarnings("ignore")


def text_to_clean(text):
    text = text.upper().replace(" ", "")
    return ''.join([c for c in text if c.isalpha()])


def shift_encrypt(plaintext, shift):
    clean_text = text_to_clean(plaintext)
    cipher_text = []
    steps = []
    
    for i, char in enumerate(clean_text):
        plain_num = ord(char) - ord('A')
        cipher_num = (plain_num + shift) % 26
        cipher_char = chr(cipher_num + ord('A'))
        cipher_text.append(cipher_char)
        
        steps.append({
            'position': i + 1,
            'plain': char,
            'plain_num': plain_num,
            'formula': f"({plain_num} + {shift}) mod 26 = {cipher_num}",
            'cipher': cipher_char,
            'alphabet_shift': f"{string.ascii_uppercase[plain_num]} → {string.ascii_uppercase[cipher_num]}"
        })
    
    return ''.join(cipher_text), steps


def shift_decrypt(ciphertext, shift):
    clean_text = text_to_clean(ciphertext)
    plain_text = []
    steps = []
    
    for i, char in enumerate(clean_text):
        cipher_num = ord(char) - ord('A')
        plain_num = (cipher_num - shift) % 26
        plain_char = chr(plain_num + ord('A'))
        plain_text.append(plain_char)
        
        steps.append({
            'position': i + 1,
            'cipher': char,
            'cipher_num': cipher_num,
            'formula': f"({cipher_num} - {shift}) mod 26 = {plain_num}",
            'plain': plain_char,
            'alphabet_shift': f"{string.ascii_uppercase[cipher_num]} → {string.ascii_uppercase[plain_num]}"
        })
    
    return ''.join(plain_text), steps


def show_shift_alphabet(shift):
    shifted = string.ascii_uppercase[shift:] + string.ascii_uppercase[:shift]
    return shifted


st.set_page_config(page_title="移位密码演示", layout="wide")
st.title("🔐 移位密码可视化演示系统")
st.markdown("最经典的凯撒密码，简单的字母循环移位，支持可视化每个字母的转换过程")


with st.sidebar:
    st.header("密钥设置")
    st.markdown("""
    **移位密码原理：**
    - 又称凯撒密码（Caesar Cipher）
    - 每个字母向后移动固定的位数
    - 超过 'Z' 时循环回到 'A'
    
    **加密公式：** C = (M + K) mod 26
    **解密公式：** M = (C - K) mod 26
    """)
    
    shift = st.slider("选择移位量 K（0-25）", 0, 25, 3)
    st.write(f"**当前移位量：** {shift}")
    st.write(f"**加密公式：** C = (M + {shift}) mod 26")
    st.write(f"**解密公式：** M = (C - {shift}) mod 26")
    
    st.subheader("字母映射表")
    normal = string.ascii_uppercase
    shifted = show_shift_alphabet(shift)
    col1, col2 = st.columns(2)
    with col1:
        st.write("原文：", normal)
    with col2:
        st.write("密文：", shifted)


tab1, tab2 = st.tabs(["加密", "解密"])

with tab1:
    st.subheader("明文加密")
    plaintext = st.text_input("输入明文", "HELLOWORLD")
    
    if st.button("开始加密", key="enc_shift"):
        cipher_text, steps = shift_encrypt(plaintext, shift)
        
        st.success("加密成功！")
        st.write(f"**原始明文：** {plaintext}")
        st.write(f"**清理后明文：** {text_to_clean(plaintext)}")
        st.write(f"**最终密文：** {cipher_text}")
        
        st.subheader("详细加密过程")
        step_data = {
            '位置': [s['position'] for s in steps],
            '明文字母': [s['plain'] for s in steps],
            '明文数值': [s['plain_num'] for s in steps],
            '计算公式': [s['formula'] for s in steps],
            '密文字母': [s['cipher'] for s in steps],
            '字母映射': [s['alphabet_shift'] for s in steps]
        }
        st.table(step_data)
        
        st.subheader("字母映射图示")
        normal = string.ascii_uppercase
        shifted = show_shift_alphabet(shift)
        for i in range(0, 26, 2):
            st.write(f"{normal[i]}→{shifted[i]}  {normal[i+1]}→{shifted[i+1]}")

with tab2:
    st.subheader("密文解密")
    ciphertext = st.text_input("输入密文", "KHOORZRUOG")
    
    if st.button("开始解密", key="dec_shift"):
        plain_text, steps = shift_decrypt(ciphertext, shift)
        
        st.success("解密成功！")
        st.write(f"**原始密文：** {ciphertext}")
        st.write(f"**清理后密文：** {text_to_clean(ciphertext)}")
        st.write(f"**最终明文：** {plain_text}")
        
        st.subheader("详细解密过程")
        step_data = {
            '位置': [s['position'] for s in steps],
            '密文字母': [s['cipher'] for s in steps],
            '密文数值': [s['cipher_num'] for s in steps],
            '计算公式': [s['formula'] for s in steps],
            '明文字母': [s['plain'] for s in steps],
            '字母映射': [s['alphabet_shift'] for s in steps]
        }
        st.table(step_data)
        
        st.subheader("字母映射图示")
        normal = string.ascii_uppercase
        shifted = show_shift_alphabet(shift)
        for i in range(0, 26, 2):
            st.write(f"{shifted[i]}→{normal[i]}  {shifted[i+1]}→{normal[i+1]}")
