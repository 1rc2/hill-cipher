import streamlit as st
import numpy as np
import warnings
warnings.filterwarnings("ignore")


def text_to_numbers(text):
    text = text.upper().replace(" ", "")
    text = ''.join([c for c in text if c.isalpha()])
    return [ord(c) - ord('A') for c in text]


def numbers_to_text(numbers):
    return ''.join([chr(num % 26 + ord('A')) for num in numbers])


def mod_inverse(a, m):
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None


def is_coprime(a):
    return np.gcd(a, 26) == 1


def encrypt(plaintext, a, b):
    plain_numbers = text_to_numbers(plaintext)
    cipher_numbers = []
    steps = []
    
    for num in plain_numbers:
        result = (a * num + b) % 26
        cipher_numbers.append(result)
        steps.append({
            'plain': numbers_to_text([num]),
            'plain_num': num,
            'formula': f"({a} × {num} + {b}) mod 26 = {result}",
            'cipher_num': result,
            'cipher': numbers_to_text([result])
        })
    
    return numbers_to_text(cipher_numbers), steps


def decrypt(ciphertext, a, b):
    a_inv = mod_inverse(a, 26)
    if a_inv is None:
        return None, None
    
    cipher_numbers = text_to_numbers(ciphertext)
    plain_numbers = []
    steps = []
    
    for num in cipher_numbers:
        result = (a_inv * (num - b)) % 26
        plain_numbers.append(result)
        steps.append({
            'cipher': numbers_to_text([num]),
            'cipher_num': num,
            'formula': f"({a_inv} × ({num} - {b})) mod 26 = {result}",
            'plain_num': result,
            'plain': numbers_to_text([result])
        })
    
    return numbers_to_text(plain_numbers), steps


st.set_page_config(page_title="仿射密码演示", layout="wide")
st.title("🔐 仿射密码可视化演示系统")
st.markdown("支持设置密钥、明文、密文，完整展示加解密过程")


with st.sidebar:
    st.header("密钥设置")
    st.markdown("""
    **仿射密码密钥 (a, b):**
    - a 必须与 26 互质（可选值：1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25）
    - b 任意 0-25 的整数
    """)
    
    a = st.selectbox("选择 a（必须与26互质）", 
                     [1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25], 
                     index=1)
    b = st.slider("选择 b（0-25）", 0, 25, 5)
    
    st.write(f"**当前密钥：** (a={a}, b={b})")
    a_inv = mod_inverse(a, 26)
    st.write(f"**a 的模逆：** a⁻¹ = {a_inv}")
    st.write(f"**加密公式：** C = ({a} × M + {b}) mod 26")
    st.write(f"**解密公式：** M = ({a_inv} × (C - {b})) mod 26")


tab1, tab2 = st.tabs(["加密", "解密"])

with tab1:
    st.subheader("明文加密")
    plaintext = st.text_input("输入明文", "HELLOWORLD")
    
    if st.button("开始加密"):
        ciphertext, steps = encrypt(plaintext, a, b)
        
        st.success("加密成功！")
        st.write(f"**原始明文：** {plaintext}")
        st.write(f"**处理后明文：** {''.join([c for c in plaintext.upper() if c.isalpha()])}")
        st.write(f"**最终密文：** {ciphertext}")
        
        st.subheader("详细加密过程")
        for i, step in enumerate(steps):
            with st.expander(f"第 {i+1} 步：{step['plain']} → {step['cipher']}"):
                st.write(f"明文字母：{step['plain']} (数值：{step['plain_num']})")
                st.write(f"计算公式：{step['formula']}")
                st.write(f"密文字母：{step['cipher']} (数值：{step['cipher_num']})")

with tab2:
    st.subheader("密文解密")
    ciphertext = st.text_input("输入密文", "KHOORZRUOG")
    
    if st.button("开始解密"):
        plaintext, steps = decrypt(ciphertext, a, b)
        
        if plaintext is None:
            st.error("密钥 a 不可逆，无法解密！")
        else:
            st.success("解密成功！")
            st.write(f"**原始密文：** {ciphertext}")
            st.write(f"**最终明文：** {plaintext}")
            
            st.subheader("详细解密过程")
            for i, step in enumerate(steps):
                with st.expander(f"第 {i+1} 步：{step['cipher']} → {step['plain']}"):
                    st.write(f"密文字母：{step['cipher']} (数值：{step['cipher_num']})")
                    st.write(f"计算公式：{step['formula']}")
                    st.write(f"明文字母：{step['plain']} (数值：{step['plain_num']})")
