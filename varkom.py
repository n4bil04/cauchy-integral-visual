# file: cauchy_integral_teorema.py
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.title("Pembuktian Interaktif Teorema Cauchy")

# --- Sidebar: Parameter Lintasan ---
st.sidebar.header("Parameter Lintasan")
radius = st.sidebar.slider("Radius Lingkaran", 0.1, 5.0, 1.0, 0.1)
center_x = st.sidebar.slider("Re(Center)", -5.0, 5.0, 0.0, 0.1)
center_y = st.sidebar.slider("Im(Center)", -5.0, 5.0, 0.0, 0.1)
n_points = st.sidebar.slider("Jumlah Titik Jalur", 20, 500, 200, 10)

# --- Parametrik Lintasan C ---
t = np.linspace(0, 2 * np.pi, n_points)
z_center = complex(center_x, center_y)
z_path = z_center + radius * np.exp(1j * t)
dz = np.gradient(z_path)

# --- Sidebar: Pilihan Fungsi f(z) ---
st.sidebar.header("Pilih Fungsi f(z)")
func_option = st.sidebar.selectbox("Fungsi:", [
    "f(z) = z**2",
    "f(z) = 1/z",
    "f(z) = exp(z)",
    "f(z) = 1/(z - a)",
    "f(z) = sin(z)"
])

# --- Definisi fungsi f(z) sesuai pilihan ---
def f(z):
    if func_option == "f(z) = z**2":
        return z**2
    elif func_option == "f(z) = 1/z":
        return 1/z
    elif func_option == "f(z) = exp(z)":
        return np.exp(z)
    elif func_option == "f(z) = 1/(z - a)":
        return 1/(z - z_center)
    elif func_option == "f(z) = sin(z)":
        return np.sin(z)

# --- Evaluasi fungsi dan integral ---
fz = f(z_path)
integral_result = np.sum(fz * dz)

# --- Plotting Lintasan ---
fig, ax = plt.subplots()
ax.plot(z_path.real, z_path.imag, label="Lintasan C", color='blue')
ax.scatter(center_x, center_y, color='red', label='Pusat', marker='x')
# Titik tambahan (bukan singularitas) di luar lintasan
extra_points = [complex(2, 1), complex(-1.5, -2)]  # Bisa diganti jadi input nanti

for pt in extra_points:
    ax.scatter(pt.real, pt.imag, color='green', label='Titik Tambahan', marker='o')

# Hindari label ganda di legend
handles, labels = ax.get_legend_handles_labels()
by_label = dict(zip(labels, handles))
ax.legend(by_label.values(), by_label.keys())


ax.set_xlabel("Re(z)")
ax.set_ylabel("Im(z)")
ax.set_title("Lintasan Kompleks (Lingkaran)")
ax.grid(True)
ax.axis("equal")
ax.legend()
# --- Deteksi singularitas ---
def is_singularity_inside():
    if func_option == "f(z) = 1/z":
        distance = abs(0 - z_center)
        return distance < radius
    elif func_option == "f(z) = 1/(z - a)":
        return True  # selalu di pusat lingkaran
    else:
        return False

inside = is_singularity_inside()

# --- Tampilkan informasi deteksi ---
st.markdown("### Deteksi Singularitas")
if inside:
    st.warning("⚠️ Terdapat singularitas di dalam lintasan. Nilai integral mungkin tidak nol (sesuai Teorema Cauchy).")
else:
    st.success("✅ Tidak ada singularitas di dalam lintasan. Jika fungsi analitik, maka integral harus nol.")

# --- Penjelasan otomatis berdasarkan kondisi ---
st.markdown("### Penjelasan Otomatis")

if func_option in ["f(z) = z**2", "f(z) = exp(z)", "f(z) = sin(z)"] and not inside:
    st.info("""
    Fungsi yang dipilih bersifat **analitik** di seluruh domain dan **tidak memiliki singularitas** di dalam lintasan.
    Maka sesuai **Teorema Cauchy**, nilai integral kompleks sepanjang lintasan tertutup adalah **nol**:
    """)
    st.latex(r"\oint_C f(z) \, dz = 0")
elif inside:
    st.info("""
    Fungsi memiliki **singularitas di dalam lintasan**.
    Karena itu, **Teorema Cauchy tidak berlaku**, dan nilai integral dapat **tidak nol**.
    """)
    st.latex(r"\oint_C f(z) \, dz \ne 0")
else:
    st.info("""
    Fungsi yang dipilih **analitik**, namun sistem tidak dapat memastikan secara simbolik seluruh properti fungsi.
    Jika benar tidak ada singularitas dalam lintasan, maka integral seharusnya **nol**.
    """)

st.pyplot(fig)
st.markdown("### Titik Non-Singular di Luar Lintasan")
st.info("""
Titik-titik tambahan (hijau) adalah **nilai dari fungsi f(z)** di luar lintasan tertutup C.
Namun karena **Teorema Cauchy hanya berlaku di dalam dan sepanjang lintasan**, nilai integral:
""")
st.latex(r"\oint_C f(z) \, dz")
st.write("**tidak dipengaruhi** oleh nilai fungsi di luar lintasan tersebut.")

# --- Hasil Integral ---
st.markdown("### Hasil Integral Garis")
st.latex(r"\oint_C f(z) \, dz")
st.write(f"Hasil: {integral_result:.5f}")
if abs(integral_result) < 1e-2:
    st.success("Hasil mendekati nol — sesuai Teorema Cauchy.")
else:
    st.warning("Hasil tidak nol — kemungkinan karena singularitas atau error numerik.")

import plotly.graph_objects as go

st.markdown("### Visualisasi 3D Permukaan $|f(z)|$")

# --- Buat meshgrid pada domain z = x + iy ---
x_vals = np.linspace(center_x - radius * 1.5, center_x + radius * 1.5, 100)
y_vals = np.linspace(center_y - radius * 1.5, center_y + radius * 1.5, 100)
X, Y = np.meshgrid(x_vals, y_vals)
Z = X + 1j * Y

# --- Evaluasi fungsi di domain meshgrid ---
try:
    F = f(Z)
    surface = np.abs(F)

    fig3d = go.Figure(data=[go.Surface(
        x=X, y=Y, z=surface,
        colorscale='Viridis'
    )])

    fig3d.update_layout(
        scene=dict(
            xaxis_title='Re(z)',
            yaxis_title='Im(z)',
            zaxis_title='|f(z)|'
        ),
        margin=dict(l=10, r=10, t=40, b=10),
        height=500
    )

    st.plotly_chart(fig3d, use_container_width=True)
except:
    st.error("Fungsi tidak terdefinisi di beberapa titik pada domain ini.")
