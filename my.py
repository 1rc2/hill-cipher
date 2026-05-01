import streamlit as st
import os

st.set_page_config(
    page_title="密码学演示平台",
    page_icon="🔐",
    layout="wide"
)

st.title("🔐 密码学演示平台")
st.markdown("### 探索经典密码学的奥秘")

st.markdown("---")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    ### 📚 密码学演示
    
    本平台提供六种经典密码算法的可视化演示：
    
    - **希尔密码** - 矩阵乘法加密
    - **仿射密码** - 线性变换加密
    - **代换密码** - 字符映射加密
    - **维吉尼亚密码** - 多表移位
    - **置换密码** - 位置重排
    - **移位密码** - 凯撒密码
    """)

with col2:
    st.markdown("""
    ### 🎯 功能特点
    
    - ✅ 可视化加解密过程
    - ✅ 实时设置密钥
    - ✅ 详细计算步骤展示
    - ✅ 交互式操作界面
    - ✅ 完全免费使用
    """)

with col3:
    st.markdown("""
    ### 🚀 使用方法
    
    1. 在左侧选择 **页面导航**
    2. 点击您想学习的密码类型
    3. 输入明文/密文
    4. 设置密钥参数
    5. 点击按钮查看详细过程
    """)

st.markdown("---")

st.markdown("### 📂 选择密码演示")

ciphers = [
    ("1_希尔密码", "希尔密码（Hill Cipher）使用矩阵乘法进行加密，是第一个实用的多字母代替密码。", "📊"),
    ("2_仿射密码", "仿射密码（Affine Cipher）使用公式 C=(a×M+b) mod 26 进行线性变换加密。", "🔢"),
    ("3_代换密码", "代换密码（Substitution Cipher）使用关键字生成字符映射表进行一一替换。", "🔄"),
    ("4_维吉尼亚密码", "维吉尼亚密码（Vigenère Cipher）使用关键字生成的重复密钥流进行加密。", "🔑"),
    ("5_置换密码", "置换密码（Permutation Cipher）通过矩阵列重排改变字符位置实现加密。", "📐"),
    ("6_移位密码", "移位密码（Shift Cipher）即凯撒密码，每个字母循环移动固定位数。", "➡️"),
]

for i, (page_name, description, icon) in enumerate(ciphers):
    if i % 3 == 0:
        cols = st.columns(3)
    
    with cols[i % 3]:
        st.markdown(f"#### {icon} {page_name[2:]}")
        st.markdown(description)

st.markdown("---")

st.markdown("<p style='text-align: right; color: gray; font-size: 14px;'>creator: 芙伊</p>", unsafe_allow_html=True)

st.markdown("""
<style>
footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)
