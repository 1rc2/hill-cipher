import streamlit as st
import string
import warnings
warnings.filterwarnings("ignore")


def create_substitution_map(keyword):
    keyword = keyword.upper().replace(" ", "")
    keyword = ''.join([c for c in keyword if c.isalpha()])
    keyword = ''.join(dict.fromkeys(keyword))
    alphabet = string.ascii_uppercase
    remaining = ''.join([c for c in alphabet if c not in keyword])
    substitution = keyword + remaining
    forward_map = dict(zip(alphabet, substitution))
    backward_map = dict(zip(substitution, alphabet))
    return forward_map, backward_map


def text_to_clean(text):
    text = text.upper().replace(" ", "")
    return ''.join([c for c in text if c.isalpha()])


def encrypt_substitution(plaintext, keyword):
    forward_map, _ = create_substitution_map(keyword)
    clean_text = text_to_clean(plaintext)
    cipher_text = ''.join([forward_map.get(c, c) for c in clean_text])
    
    steps = []
    for i, (orig, mapped) in enumerate(zip(clean_text, cipher_text)):
        steps.append({
            'position': i + 1,
            'plain': orig,
            'cipher': mapped,
            'formula': f"{orig} → {mapped}"
        })
    
    return cipher_text, steps


def decrypt_substitution(ciphertext, keyword):
    _, backward_map = create_substitution_map(keyword)
    clean_text = text_to_clean(ciphertext)
    plain_text = ''.join([backward_map.get(c, c) for c in clean_text])
    
    steps = []
    for i, (orig, mapped) in enumerate(zip(clean_text, plain_text)):
        steps.append({
            'position': i + 1,
            'cipher': orig,
            'plain': mapped,
            'formula': f"{orig} → {mapped}"
        })
    
    return plain_text, steps


st.set_page_config(page_title="代换密码演示", layout="wide")
st.title("🔐 代换密码可视化演示系统")
st.markdown("使用关键字生成代换表，实现字符的一对一映射加解密")


with st.sidebar:
    st.header("密钥设置")
    st.markdown("""
    **代换密码原理：**
    - 使用关键字生成代换表
    - 明文字母按代换表映射为密文字母
    - 每个字母有唯一的固定替代
    """)
    
    keyword = st.text_input("输入关键字（用于生成代换表）", "CIPHER")
    
    forward_map, backward_map = create_substitution_map(keyword)
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("正向代换表")
        for i in range(0, 26, 2):
            st.write(f"{string.ascii_uppercase[i]}→{forward_map[string.ascii_uppercase[i]]}  "
                    f"{string.ascii_uppercase[i+1]}→{forward_map[string.ascii_uppercase[i+1]]}")
    with col2:
        st.subheader("反向代换表")
        for i in range(0, 26, 2):
            original1 = list(forward_map.keys())[list(forward_map.values()).index(string.ascii_uppercase[i])]
            original2 = list(forward_map.keys())[list(forward_map.values()).index(string.ascii_uppercase[i+1])]
            st.write(f"{string.ascii_uppercase[i]}→{original1}  "
                    f"{string.ascii_uppercase[i+1]}→{original2}")


tab1, tab2 = st.tabs(["加密", "解密"])

with tab1:
    st.subheader("明文加密")
    plaintext = st.text_input("输入明文", "HELLOWORLD")
    
    if st.button("开始加密", key="enc_sub"):
        cipher_text, steps = encrypt_substitution(plaintext, keyword)
        
        st.success("加密成功！")
        st.write(f"**原始明文：** {plaintext}")
        st.write(f"**清理后明文：** {text_to_clean(plaintext)}")
        st.write(f"**最终密文：** {cipher_text}")
        
        st.subheader("详细加密过程")
        step_data = {
            '位置': [s['position'] for s in steps],
            '明文字母': [s['plain'] for s in steps],
            '密文字母': [s['cipher'] for s in steps],
            '映射关系': [s['formula'] for s in steps]
        }
        st.table(step_data)

with tab2:
    st.subheader("密文解密")
    ciphertext = st.text_input("输入密文", "KHOORZRUOG")
    
    if st.button("开始解密", key="dec_sub"):
        plain_text, steps = decrypt_substitution(ciphertext, keyword)
        
        st.success("解密成功！")
        st.write(f"**原始密文：** {ciphertext}")
        st.write(f"**最终明文：** {plain_text}")
        
        st.subheader("详细解密过程")
        step_data = {
            '位置': [s['position'] for s in steps],
            '密文字母': [s['cipher'] for s in steps],
            '明文字母': [s['plain'] for s in steps],
            '映射关系': [s['formula'] for s in steps]
        }
        st.table(step_data)
