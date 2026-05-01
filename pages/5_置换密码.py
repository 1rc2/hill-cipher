import streamlit as st
import numpy as np
import warnings
warnings.filterwarnings("ignore")


def text_to_clean(text):
    text = text.upper().replace(" ", "")
    return ''.join([c for c in text if c.isalpha()])


def get_column_order(keyword):
    keyword = text_to_clean(keyword)
    sorted_chars = sorted(list(keyword))
    order = []
    for char in keyword:
        order.append(sorted_chars.index(char) + 1)
        sorted_chars[sorted_chars.index(char)] = None
    return order


def encrypt_permutation(plaintext, keyword):
    clean_text = text_to_clean(plaintext)
    keyword = text_to_clean(keyword)
    
    if not keyword:
        return clean_text, []
    
    rows = len(clean_text) // len(keyword) + (1 if len(clean_text) % len(keyword) != 0 else 0)
    padding = rows * len(keyword) - len(clean_text)
    clean_text += 'X' * padding
    
    matrix = []
    for i in range(rows):
        row = list(clean_text[i*len(keyword):(i+1)*len(keyword)])
        matrix.append(row)
    
    order = get_column_order(keyword)
    cipher_chars = []
    steps = []
    
    for col_idx in np.argsort(order):
        col_chars = [matrix[row][col_idx] for row in range(rows)]
        for i, char in enumerate(col_chars):
            cipher_chars.append(char)
            steps.append({
                'row': i + 1,
                'column': col_idx + 1,
                'char': char,
                'from': f"位置({i+1},{col_idx+1})"
            })
    
    cipher_text = ''.join(cipher_chars)
    return cipher_text, steps, matrix, order


def decrypt_permutation(ciphertext, keyword):
    clean_text = text_to_clean(ciphertext)
    keyword = text_to_clean(keyword)
    
    if not keyword:
        return clean_text, [], [], []
    
    rows = len(clean_text) // len(keyword) + (1 if len(clean_text) % len(keyword) != 0 else 0)
    order = get_column_order(keyword)
    sorted_order = np.argsort(order)
    
    col_lengths = [rows] * len(keyword)
    
    matrix = [[None] * len(keyword) for _ in range(rows)]
    char_idx = 0
    
    for col_idx in sorted_order:
        for row in range(col_lengths[col_idx]):
            matrix[row][col_idx] = clean_text[char_idx]
            char_idx += 1
    
    plain_chars = []
    for i in range(rows):
        for j in range(len(keyword)):
            plain_chars.append(matrix[i][j])
    
    plain_text = ''.join(plain_chars).rstrip('X')
    return plain_text, [], matrix, order


st.set_page_config(page_title="置换密码演示", layout="wide")
st.title("🔐 置换密码可视化演示系统")
st.markdown("通过列移位实现字符位置的重新排列，支持可视化矩阵变换过程")


with st.sidebar:
    st.header("密钥设置")
    st.markdown("""
    **置换密码原理：**
    - 将明文按行填入矩阵
    - 使用关键字确定列读取顺序
    - 按列顺序读取生成密文
    
    **示例：**
    - 关键字 "CIPHER" → 列顺序 [2, 4, 5, 3, 1, 6]
    - 按第2列、第4列、第5列...的顺序读取
    """)
    
    keyword = st.text_input("输入关键字", "CIPHER")
    clean_keyword = text_to_clean(keyword)
    order = get_column_order(clean_keyword)
    
    st.write(f"**清理后关键字：** {clean_keyword}")
    st.write(f"**列顺序：** {order}")
    
    if clean_keyword:
        st.subheader("列顺序映射")
        col1, col2 = st.columns(2)
        with col1:
            st.write("列号：", " ".join([str(i+1) for i in range(len(clean_keyword))]))
        with col2:
            st.write("顺序：", " ".join([str(o) for o in order]))


tab1, tab2 = st.tabs(["加密", "解密"])

with tab1:
    st.subheader("明文加密")
    plaintext = st.text_input("输入明文", "HELLOWORLD")
    
    if st.button("开始加密", key="enc_perm"):
        cipher_text, steps, matrix, order = encrypt_permutation(plaintext, keyword)
        clean_text = text_to_clean(plaintext)
        
        st.success("加密成功！")
        st.write(f"**原始明文：** {plaintext}")
        st.write(f"**清理后明文：** {clean_text}")
        st.write(f"**最终密文：** {cipher_text}")
        
        if matrix and clean_keyword:
            st.subheader("矩阵填充过程（按行）")
            import pandas as pd
            df = pd.DataFrame(matrix, columns=[f'C{i+1}' for i in range(len(clean_keyword))])
            st.table(df)
            
            st.subheader("列读取顺序")
            sorted_order = np.argsort(order)
            st.write("读取顺序：", " → ".join([f"C{i+1}" for i in sorted_order]))
            
            st.subheader("详细加密过程")
            step_data = {
                '读取顺序': [f"C{sorted_order[i]+1}" for i in range(len(steps))],
                '行号': [s['row'] for s in steps],
                '列号': [s['column'] for s in steps],
                '字符': [s['char'] for s in steps],
                '来源': [s['from'] for s in steps]
            }
            st.table(step_data)

with tab2:
    st.subheader("密文解密")
    ciphertext = st.text_input("输入密文")
    
    if st.button("开始解密", key="dec_perm"):
        plain_text, steps, matrix, order = decrypt_permutation(ciphertext, keyword)
        
        if matrix and clean_keyword:
            st.success("解密成功！")
            st.write(f"**原始密文：** {ciphertext}")
            st.write(f"**最终明文：** {plain_text}")
            
            st.subheader("矩阵恢复过程")
            import pandas as pd
            df = pd.DataFrame(matrix, columns=[f'C{i+1}' for i in range(len(clean_keyword))])
            st.table(df)
            
            st.subheader("按行读取")
            st.write("从矩阵按行读取并移除填充字符 'X'")
