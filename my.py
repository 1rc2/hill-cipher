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

col1, col2, col3 = st.columns(3)

cipher_buttons = [
    ("1_希尔密码", "📊", "希尔密码（Hill Cipher）使用矩阵乘法进行加密"),
    ("2_仿射密码", "🔢", "仿射密码（Affine Cipher）使用线性变换公式加密"),
    ("3_代换密码", "🔄", "代换密码（Substitution Cipher）使用字符映射表加密"),
    ("4_维吉尼亚密码", "🔑", "维吉尼亚密码（Vigenère Cipher）使用重复密钥流加密"),
    ("5_置换密码", "📐", "置换密码（Permutation Cipher）通过位置重排加密"),
    ("6_移位密码", "➡️", "移位密码（Shift Cipher）即经典凯撒密码"),
]

for i, (page_name, icon, desc) in enumerate(cipher_buttons):
    if i % 3 == 0:
        col1, col2, col3 = st.columns(3)

    cols = [col1, col2, col3]
    with cols[i % 3]:
        st.markdown(f"#### {icon} {page_name[2:]}")
        st.markdown(desc)
        if st.button(f"打开 {page_name[2:]}", key=f"btn_{page_name}"):
            st.switch_page(f"pages/{page_name}.py")

st.markdown("---")
st.info("💡 **提示：** 点击上方按钮即可跳转到对应的密码演示页面，或使用左侧边栏的页面导航菜单。")

st.markdown("---")

st.markdown("<p style='text-align: right; color: gray; font-size: 14px;'>creator: 芙伊</p>", unsafe_allow_html=True)

st.markdown("""
<style>
footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)
