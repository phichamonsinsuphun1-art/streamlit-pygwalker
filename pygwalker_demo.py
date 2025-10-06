import streamlit as st
import pandas as pd
import pygwalker as pyg
import numpy as np

st.set_page_config(page_title="PyGwalker Faceted Pattern", page_icon="📊", layout="wide")

def create_sample_data():
    """Create sample dataset matching the exact pattern in the image"""
    
    # Exact categories from the image
    mfgid_list = ['QS0101', 'QSA101', 'QSA201', 'QSA301', 'QSA401', 'QSC201', 'QSC301', 'QSC401']
    suspension_types = ['NHK', 'PJCL', 'PJLE', 'myDa', 'PJLG', 'PJLI']
    dates = ['20231026', '20231106', '20231108', '20231112', '20231124', '20231128']
    testerids = ['RP48', 'RP49', 'RP50', 'RP51', 'RP52', 'RP53']
    
    # Generate scatter points
    data_list = []
    n_points = 1000
    
    for _ in range(n_points):
        date = np.random.choice(dates)
        tester = np.random.choice(testerids)
        
        data_list.append({
            'mfgid': np.random.choice(mfgid_list),
            'suspension_type': np.random.choice(suspension_types),
            'asmdate': date,
            'testerid': tester,
            'asmdate_testerid': f"{date}_{tester}",  # Combined for X-axis
            'value': np.random.uniform(0, 100),
            'count': 1  # Each point counts as 1
        })
    
    df = pd.DataFrame(data_list)
    return df

# Title
st.title("📊 PyGwalker - วิธีสร้าง Pattern ที่ถูกต้อง")

# Critical instructions
st.error("""
### ⚠️ สำคัญ! ใน PyGwalker ต้องทำแบบนี้:

จากรูปที่คุณส่งมา pattern คือ:
- **แนวนอนด้านบน**: mfgid (QS0101, QSA101, ...)
- **แนวตั้งด้านซ้าย**: suspension_type (NHK, PJCL, ...)  
- **แนวล่าง**: asmdate + testerid (hierarchical)
- **จุดสีดำ**: scatter plot
""")

st.success("""
### ✅ วิธีที่ถูกต้องใน PyGwalker:

**หลักการ:**
ใน PyGwalker มี 2 แนวคิดหลัก:
1. **Faceting** (แยก panel) = ใช้ Column/Row encoding
2. **Position** (ตำแหน่งใน chart) = ใช้ X/Y encoding

**สำหรับ Pattern นี้:**

**Step 1: เลือก Chart Type = Circle/Point**
- คลิกที่ Chart Type selector
- เลือก **Circle** หรือ **Point**

**Step 2: Facet Columns (แนวนอน)**
- หา encoding channel ที่ชื่อ **"Column"** (ไม่ใช่ "Columns shelf")
- ลาก `mfgid` ไปวาง
- จะได้ facets แนวนอน 8 ช่อง

**Step 3: X-axis (แกนล่าง)**
- หา encoding ชื่อ **"X"** 
- ลาก `asmdate_testerid` ไปวาง
- หรือลาก `asmdate` แล้วเพิ่ม `testerid` ใน Detail

**Step 4: Y-axis (แกนซ้าย)**
- หา encoding ชื่อ **"Y"**
- ลาก `suspension_type` ไปวาง

**Step 5: ปรับแต่ง**
- Opacity: ลดลงเพื่อดูจุดที่ซ้อนกัน
- Size: ตั้งเป็นค่าคงที่ หรือใช้ `count`
""")

# Sidebar
with st.sidebar:
    st.header("📁 Data Source")
    
    option = st.radio("Choose:", ["Upload File", "Use Sample Data"])
    
    df = None
    
    if option == "Upload File":
        file = st.file_uploader("Upload CSV or Excel", type=['csv', 'xlsx', 'xls'])
        
        if file:
            try:
                if file.name.endswith('.csv'):
                    df = pd.read_csv(file)
                else:
                    df = pd.read_excel(file)
                
                st.success(f"✅ {file.name}")
                st.info(f"📊 {len(df):,} rows × {len(df.columns)} cols")
                
            except Exception as e:
                st.error(f"❌ {e}")
    else:
        df = create_sample_data()
        st.success("✅ Sample data loaded")
        st.info(f"📊 {len(df):,} rows × {len(df.columns)} cols")
    
    if df is not None:
        st.markdown("---")
        st.markdown("### 🎯 Mapping for Pattern:")
        
        st.code("""
Facet Column → mfgid
X-axis → asmdate_testerid  
Y-axis → suspension_type
Chart Type → Circle/Point
        """)
        
        st.markdown("---")
        st.markdown("### 📊 Available Fields:")
        
        for col in df.columns:
            unique = df[col].nunique()
            st.text(f"• {col}: {unique} unique")

# Main area
if df is not None:
    
    with st.expander("🔍 Preview Data"):
        st.dataframe(df.head(100), use_container_width=True)
    
    st.markdown("---")
    
    # Detailed guide
    st.warning("""
    ### 📝 คำแนะนำแบบละเอียด:
    
    **ใน PyGwalker Interface จะมี:**
    
    1. **Chart Type Selector** (มุมบน)
       - เลือก **Circle** หรือ **Point** ก่อนอื่น!
    
    2. **Encoding Channels** (ขวามือ):
       - **Column** = Facet แนวนอน → ลาก `mfgid`
       - **Row** = Facet แนวตั้ง → ไม่ใช้
       - **X** = แกนล่าง → ลาก `asmdate_testerid`
       - **Y** = แกนซ้าย → ลาก `suspension_type`
       - **Color** = สี (optional)
       - **Size** = ขนาด (optional)
       - **Opacity** = ความโปร่งใส (ปรับด้วยมือ)
    
    3. **ไม่ใช้ "Rows" หรือ "Columns" Shelf แบบ Tableau!**
       - PyGwalker ใช้ encoding channels ตรงๆ
       - "Column" = facet horizontal
       - "Row" = facet vertical (ไม่ใช่ hierarchical axis)
    
    **สำหรับ Hierarchical X-axis:**
    - ใน PyGwalker ไม่สามารถทำ nested axis ได้โดยตรง
    - วิธีแก้: รวม fields เป็น `asmdate_testerid` (20231026_RP48)
    - หรือใช้ detail encoding เพื่อ group data
    """)
    
    st.info("""
    ### 💡 Tips สำคัญ:
    
    **ถ้า Pattern ไม่ออก:**
    
    1. **ตรวจสอบ Chart Type**
       - ต้องเป็น Circle/Point ก่อน!
       - ไม่ใช่ Bar หรือ Line
    
    2. **ตรวจสอบ Encoding**
       - Column = mfgid (สำหรับ facet แนวนอน)
       - X = asmdate_testerid (แกนล่าง)
       - Y = suspension_type (แกนซ้าย)
    
    3. **Aggregation**
       - ถ้าเป็น bar chart → มี aggregation (SUM, COUNT)
       - ถ้าเป็น scatter → ไม่ต้อง aggregate, ใช้ raw data
       - ตรวจสอบว่าไม่มี SUM() หรือ COUNT() wrap field
    
    4. **Data Type**
       - suspension_type ควรเป็น categorical (text)
       - asmdate_testerid ควรเป็น categorical
       - ถ้าเป็น continuous จะแสดงแบบ numeric axis
    
    5. **ลองใช้ "Detail" Encoding**
       - ลาก mfgid ไปที่ Column
       - ลาก asmdate ไปที่ X
       - ลาก testerid ไปที่ Detail (จะ group data)
       - ลาก suspension_type ไปที่ Y
    """)
    
    # Visualization
    st.markdown("---")
    st.subheader("🎨 PyGwalker Interface")
    
    st.warning("👇 ลากวางตามคำแนะนำด้านบน ใน interface ด้านล่างนี้")
    
    try:
        pyg_html = pyg.to_html(df)
        st.components.v1.html(pyg_html, height=1200, scrolling=True)
        
    except Exception as e:
        st.error(f"Error: {e}")

else:
    st.info("👈 Upload file or use sample data!")
    
    st.markdown("""
    ### 🎓 ความแตกต่างระหว่าง PyGwalker กับ Tableau:
    
    **Tableau:**
    - มี Columns Shelf และ Rows Shelf
    - สามารถซ้อน fields ใน shelf เดียวได้ → hierarchical axis
    - ลากหลาย fields เข้า Rows = nested axis
    
    **PyGwalker:**
    - ใช้ Encoding Channels (Column, Row, X, Y, Color, Size, ...)
    - Column/Row = สำหรับ faceting (แยก panel)
    - X/Y = สำหรับตำแหน่งภายใน panel
    - ไม่รองรับ hierarchical axis โดยตรง
    
    **วิธีแก้:**
    - รวม fields ก่อน: date_tester = "20231026_RP48"
    - ใช้ Detail encoding เพื่อ group
    - ใช้ faceting แทน hierarchical axis
    """)

st.markdown("---")
st.caption("PyGwalker uses Grammar of Graphics encoding | Different from Tableau's shelf system")