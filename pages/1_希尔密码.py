import streamlit as st
import numpy as np
from sympy import Matrix
import warnings
warnings.filterwarnings("ignore")

# 希尔密码核心函数
def prepare_text(text, n):
    text = text.upper().replace(" ", "")
    text = ''.join([c for c in text if c.isalpha()])
    while len(text) % n != 0:
        text += 'X'
    return text

def text_to_matrix(text, n):
    nums = [ord(c) - ord('A') for c in text]
    return np.array(nums).reshape(-1, n).T

def matrix_to_text(matrix):
    nums = matrix.T.flatten()
    text = ''.join([chr(num % 26 + ord('A')) for num in nums])
    return text

def encrypt(plaintext, key_matrix, n):
    plain_matrix = text_to_matrix(plaintext, n)
    cipher_matrix = np.dot(key_matrix, plain_matrix) % 26
    return matrix_to_text(cipher_matrix), plain_matrix, cipher_matrix

def mod_inverse_matrix(matrix, mod=26):
    mat = Matrix(matrix)
    det = int(mat.det()) % mod
    try:
        det_inv = pow(det, -1, mod)
    except ValueError:
        return None
    adj = np.array(mat.adjugate() % mod)
    inv_matrix = (det_inv * adj) % mod
    return inv_matrix

def decrypt(ciphertext, key_matrix, n):
    inv_key = mod_inverse_matrix(key_matrix)
    if inv_key is None:
        return None, None, None
    cipher_matrix = text_to_matrix(ciphertext, n)
    plain_matrix = np.dot(inv_key, cipher_matrix) % 26
    return matrix_to_text(plain_matrix), cipher_matrix, plain_matrix

# 网页界面
st.set_page_config(page_title="希尔密码演示", layout="wide")
st.title("🔐 希尔密码可视化演示系统")
st.markdown("支持设置密钥、明文、密文，完整展示加解密过程")

with st.sidebar:
    st.header("参数设置")
    n = st.selectbox("密钥矩阵阶数 n", [2, 3], index=0)
    st.subheader("输入密钥矩阵")
    key_matrix = []
    for i in range(n):
        default_val = "1 2" if n == 2 else "1 2 3"
        row = st.text_input(f"第{i+1}行", value=default_val)
        row_nums = list(map(int, row.split()))
        key_matrix.append(row_nums)
    key_matrix = np.array(key_matrix)
    st.write("密钥矩阵：")
    st.write(key_matrix)

tab1, tab2 = st.tabs(["加密", "解密"])

with tab1:
    st.subheader("明文加密")
    plaintext = st.text_input("输入明文", "HELLO")
    if st.button("开始加密"):
        plain_fixed = prepare_text(plaintext, n)
        cipher, plain_mat, cipher_mat = encrypt(plain_fixed, key_matrix, n)
        st.success("加密成功！")
        st.write("原始明文：", plaintext)
        st.write("处理后：", plain_fixed)
        st.write("明文矩阵：")
        st.write(plain_mat)
        st.write("密文矩阵：")
        st.write(cipher_mat)
        st.write("最终密文：", cipher)

with tab2:
    st.subheader("密文解密")
    ciphertext = st.text_input("输入密文")
    if st.button("开始解密"):
        cipher_fixed = prepare_text(ciphertext, n)
        plain_res, cipher_mat, plain_mat = decrypt(cipher_fixed, key_matrix, n)
        if plain_res is None:
            st.error("密钥不可逆，无法解密")
        else:
            st.success("解密成功！")
            st.write("密文矩阵：")
            st.write(cipher_mat)
            st.write("明文矩阵：")
            st.write(plain_mat)
            st.write("最终明文：", plain_res)